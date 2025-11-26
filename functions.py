import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import os
import ttkbootstrap as ttk
import ttkbootstrap.constants as tb

class McEditorApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.title("Zip File Editor")
        self.geometry("700x500")
        self.create_widgets()
        self.zip_path = None
        self.zip_file = None
        self.file_list = []
        self.current_file = None
        self.display_mode = "plain"  # domyślny tryb wyświetlania

    def create_widgets(self):
        frm = ttk.Frame(self)
        frm.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Buttons Frame
        self.open_btn = ttk.Button(frm, text="Open MCWORLD", command=self.open_zip, bootstyle=(tb.SUCCESS, tb.OUTLINE))
        self.open_btn.grid(row=0, column=0, sticky="ew")

        self.save_btn = ttk.Button(frm, text="Save MCWORLD", command=self.save_zip, state=tk.DISABLED, bootstyle=(tb.PRIMARY, tb.OUTLINE))
        self.save_btn.grid(row=0, column=1, sticky="ew")

        # Menubutton z trzema opcjami wyświetlania
        self.change_text_area_btn = ttk.Menubutton(frm, text="Display type", bootstyle=(tb.INFO, tb.OUTLINE))
        self.change_text_area_btn.grid(row=0, column=2, sticky="ew")

        menu = tk.Menu(self.change_text_area_btn, tearoff=0)
        menu.add_command(label="Plain", command=lambda: self.set_display_mode("plain"))
        menu.add_command(label="Wrapped", command=lambda: self.set_display_mode("wrapped"))
        menu.add_command(label="Hex view", command=lambda: self.set_display_mode("hex"))
        self.change_text_area_btn["menu"] = menu

        # File Listbox
        self.filebox = tk.Listbox(frm, height=15)
        self.filebox.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.filebox.bind("<<ListboxSelect>>", self.load_file_content)

        frm.rowconfigure(1, weight=1)
        frm.columnconfigure(1, weight=1)

        # Text Area for file content
        self.text = tk.Text(frm, wrap=tk.NONE, bg="light yellow")
        self.text.grid(row=1, column=2, sticky="nsew")
        frm.columnconfigure(2, weight=3)

        # Save File Button
        self.save_file_btn = ttk.Button(frm, text="Save the File", command=self.save_file_content, state=tk.DISABLED, bootstyle=(tb.INFO, tb.OUTLINE))
        self.save_file_btn.grid(row=2, column=2, sticky="ew")

    def set_display_mode(self, mode):
        # Przełącz tryb wyświetlania zawartości pola tekstowego
        if mode == getattr(self, "display_mode", "plain"):
            return

        # Jeśli wychodzimy z trybu hex, przywróć oryginalną zawartość (jeśli była zapisana)
        if getattr(self, "display_mode", None) == "hex" and hasattr(self, "hex_original_content"):
            self.text.config(state=tk.NORMAL)
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, self.hex_original_content)
            del self.hex_original_content

        if mode == "plain":
            self.text.config(wrap=tk.NONE)
            self.text.config(state=tk.NORMAL)
        elif mode == "wrapped":
            self.text.config(wrap=tk.WORD)
            self.text.config(state=tk.NORMAL)
        elif mode == "hex":
            # Zachowaj oryginalny tekst, zamień na widok hex i ustaw read-only
            self.hex_original_content = self.text.get("1.0", tk.END)
            data = self.hex_original_content.encode("utf-8", errors="replace")
            hex_lines = []
            for i in range(0, len(data), 16):
                chunk = data[i:i+16]
                hex_bytes = " ".join(f"{b:02x}" for b in chunk)
                ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
                hex_lines.append(f"{i:08x}  {hex_bytes:<47}  {ascii_part}")
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, "\n".join(hex_lines))
            self.text.config(wrap=tk.NONE)
            self.text.config(state=tk.DISABLED)
            self.text.config(font=("consolas", 10))

        self.display_mode = mode

    def open_zip(self):
        path = filedialog.askopenfilename(filetypes=[("MC world", "*.mcworld"), ("All Files", "*.*")])
        if not path:
            return
        self.zip_path = path
        self.zip_file = zipfile.ZipFile(path, "r")
        self.file_list = self.zip_file.namelist()
        self.filebox.delete(0, tk.END)
        for f in self.file_list:
            self.filebox.insert(tk.END, f)
        self.save_btn.config(state=tk.NORMAL)
        self.save_file_btn.config(state=tk.DISABLED)
        self.text.delete("1.0", tk.END)
        self.current_file = None

    def load_file_content(self, event):
        selection = self.filebox.curselection()
        if not selection:
            return
        filename = self.file_list[selection[0]]
        try:
            with self.zip_file.open(filename) as f:
                content = f.read().decode("utf-8", errors="replace")
            self.text.config(state=tk.NORMAL)
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, content)
            self.current_file = filename
            self.save_file_btn.config(state=tk.NORMAL)
            # Zastosuj aktualny tryb wyświetlania po wczytaniu pliku
            if getattr(self, "display_mode", "plain") == "hex":
                self.set_display_mode("hex")
            elif self.display_mode == "wrapped":
                self.text.config(wrap=tk.WORD)
            else:
                self.text.config(wrap=tk.NONE)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot read file: {e}")

    def save_file_content(self):
        if not self.current_file:
            return
        # Jeśli obecny widok to hex, użyj zapisanej oryginalnej zawartości
        if getattr(self, "display_mode", "plain") == "hex" and hasattr(self, "hex_original_content"):
            content = self.hex_original_content
        else:
            content = self.text.get("1.0", tk.END)
        if not hasattr(self, "modified_files"):
            self.modified_files = {}
        self.modified_files[self.current_file] = content
        messagebox.showinfo("Saved", f"Changes to '{self.current_file}' are staged. Click 'Save Zip' to write changes.")

    def save_zip(self):
        if not hasattr(self, "modified_files") or not self.modified_files:
            messagebox.showinfo("No Changes", "No files have been modified.")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".mcworld", filetypes=[("Zip Files", "*.mcworld")])
        if not save_path:
            return
        with zipfile.ZipFile(self.zip_path, "r") as zin, zipfile.ZipFile(save_path, "w") as zout:
            for item in zin.infolist():
                if item.filename in getattr(self, "modified_files", {}):
                    zout.writestr(item.filename, self.modified_files[item.filename])
                else:
                    zout.writestr(item, zin.read(item.filename))
        messagebox.showinfo("MC world Saved", f"Modified world saved to {save_path}")

if __name__ == "__main__":
    app = McEditorApp()
    app.mainloop()