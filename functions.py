import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import zipfile
import os

class ZipEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Zip File Editor")
        self.geometry("700x500")
        self.create_widgets()
        self.zip_path = None
        self.zip_file = None
        self.file_list = []
        self.current_file = None

    def create_widgets(self):
        frm = ttk.Frame(self)
        frm.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.open_btn = ttk.Button(frm, text="Open Zip", command=self.open_zip)
        self.open_btn.grid(row=0, column=0, sticky="ew")

        self.save_btn = ttk.Button(frm, text="Save Zip", command=self.save_zip, state=tk.DISABLED)
        self.save_btn.grid(row=0, column=1, sticky="ew")

        self.filebox = tk.Listbox(frm, height=15)
        self.filebox.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.filebox.bind("<<ListboxSelect>>", self.load_file_content)

        frm.rowconfigure(1, weight=1)
        frm.columnconfigure(1, weight=1)

        self.text = tk.Text(frm, wrap=tk.NONE)
        self.text.grid(row=1, column=2, sticky="nsew")
        frm.columnconfigure(2, weight=3)

        self.save_file_btn = ttk.Button(frm, text="Save File", command=self.save_file_content, state=tk.DISABLED)
        self.save_file_btn.grid(row=2, column=2, sticky="ew")

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
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, content)
            self.current_file = filename
            self.save_file_btn.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot read file: {e}")

    def save_file_content(self):
        if not self.current_file:
            return
        content = self.text.get("1.0", tk.END)
        # Save to a temp dict
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
    app = ZipEditorApp()
    app.mainloop()