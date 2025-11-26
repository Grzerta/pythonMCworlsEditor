

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

    self.display_mode = mode
