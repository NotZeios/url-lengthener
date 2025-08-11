import random
import string
import urllib.parse
import tkinter as tk
from tkinter import messagebox

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def url_lengthener(original_url, extra_length=100):
    if not original_url:
        raise ValueError("No URL provided")
    parsed = urllib.parse.urlparse(original_url)
    if not parsed.scheme:
        original_url = "http://" + original_url
        parsed = urllib.parse.urlparse(original_url)
    query_params = urllib.parse.parse_qs(parsed.query)
    base_query = urllib.parse.urlencode(query_params, doseq=True)
    target_len = len(base_query) + max(0, int(extra_length))
    while len(urllib.parse.urlencode(query_params, doseq=True)) < target_len:
        key = generate_random_string(6)
        value = generate_random_string(12)
        query_params[key] = [value]
    new_query = urllib.parse.urlencode(query_params, doseq=True)
    return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))

def generate_url():
    base_url = url_entry.get().strip()
    try:
        extra_chars = int(extra_entry.get().strip()) if extra_entry.get().strip() else 200
        if extra_chars > 1000:
            messagebox.showerror("Error", "Maximum allowed extra characters is 1000.")
            return
    except ValueError:
        messagebox.showerror("Error", "Extra characters must be a number.")
        return
    try:
        result = url_lengthener(base_url, extra_chars)
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)
        output_text.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", str(e))

ui_font = ("Segoe UI", 11)
ui_font_bold = ("Segoe UI", 18, "bold")
ui_font_small = ("Segoe UI", 10)
ui_font_button = ("Segoe UI", 11, "bold")

root = tk.Tk()
root.title("URL Lengthener")
root.geometry("650x370")
root.resizable(False, False)
root.configure(bg="#f4f6fb")

title_label = tk.Label(
    root,
    text="URL Lengthener",
    font=ui_font_bold,
    fg="#2d3a4a",
    bg="#f4f6fb"
)
title_label.pack(pady=(18, 5))

description_label = tk.Label(
    root,
    text="A URL shortener’s evil twin.",
    font=ui_font_small,
    wraplength=600,
    justify="center",
    fg="#4a5a6a",
    bg="#f4f6fb"
)
description_label.pack(pady=(0, 15))

input_frame = tk.Frame(root, bg="#f4f6fb")
input_frame.pack(pady=0)

url_label = tk.Label(input_frame, text="Enter URL:", font=ui_font, bg="#f4f6fb", fg="#2d3a4a")
url_label.grid(row=0, column=0, sticky="e", padx=(0, 5))
url_entry = tk.Entry(input_frame, width=48, font=ui_font, relief="solid", borderwidth=1)
url_entry.grid(row=0, column=1, padx=(0, 10))

extra_label = tk.Label(input_frame, text="Extra Characters:", font=ui_font, bg="#f4f6fb", fg="#2d3a4a")
extra_label.grid(row=1, column=0, sticky="e", padx=(0, 5), pady=(8,0))
extra_entry = tk.Entry(input_frame, width=8, font=ui_font, relief="solid", borderwidth=1)
extra_entry.grid(row=1, column=1, sticky="w", pady=(8,0))
extra_entry.insert(0, "200")

button_frame = tk.Frame(root, bg="#f4f6fb")
button_frame.pack(pady=12)

generate_btn = tk.Button(
    button_frame,
    text="Generate",
    command=generate_url,
    font=ui_font_button,
    bg="#4a90e2",
    fg="white",
    activebackground="#357abd",
    activeforeground="white",
    relief="flat",
    padx=16,
    pady=4,
    cursor="hand2"
)
generate_btn.pack(side=tk.LEFT, padx=8)

def copy_to_clipboard():
    result = output_text.get("1.0", tk.END).strip()
    if result:
        root.clipboard_clear()
        root.clipboard_append(result)
        messagebox.showinfo("Copied", "URL copied to clipboard!")

copy_btn = tk.Button(
    button_frame,
    text="Copy",
    command=copy_to_clipboard,
    font=ui_font_button,
    bg="#7ed957",
    fg="white",
    activebackground="#5ea23c",
    activeforeground="white",
    relief="flat",
    padx=16,
    pady=4,
    cursor="hand2"
)
copy_btn.pack(side=tk.LEFT, padx=8)

def clear_output():
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)

clear_btn = tk.Button(
    button_frame,
    text="Clear",
    command=clear_output,
    font=ui_font_button,
    bg="#f45b69",
    fg="white",
    activebackground="#c0392b",
    activeforeground="white",
    relief="flat",
    padx=16,
    pady=4,
    cursor="hand2"
)
clear_btn.pack(side=tk.LEFT, padx=8)

output_frame = tk.Frame(root, bg="#f4f6fb")
output_frame.pack(pady=(0, 10), fill=tk.BOTH, expand=True)

output_text = tk.Text(
    output_frame,
    height=6,
    width=70,
    wrap="word",
    font=ui_font,
    relief="solid",
    borderwidth=1,
    bg="#ffffff",
    fg="#2d3a4a",
    state=tk.DISABLED
)
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,0))

scrollbar = tk.Scrollbar(output_frame, command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,10))

output_text.config(yscrollcommand=scrollbar.set)

root.mainloop()
