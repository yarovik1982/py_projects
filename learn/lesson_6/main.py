import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def process_files():
    src_dir = entry_src.get()
    dst_dir = entry_dst.get()
    ext = entry_ext.get().strip()
    copy_mode = var_copy.get()  # 1 если чекбокс выбран, иначе 0

    if not src_dir or not dst_dir or not ext:
        messagebox.showerror("Ошибка", "Заполните все поля!")
        return

    if not os.path.exists(src_dir):
        messagebox.showerror("Ошибка", f"Исходная директория не найдена: {src_dir}")
        return

    os.makedirs(dst_dir, exist_ok=True)

    processed = 0
    for root_dir, dirs, files in os.walk(src_dir):  # рекурсивный обход
        for file in files:
            if file.endswith(ext):
                src_path = os.path.join(root_dir, file)
                dst_path = os.path.join(dst_dir, file)
                try:
                    if copy_mode:
                        shutil.copy2(src_path, dst_path)  # копирование с метаданными
                    else:
                        shutil.move(src_path, dst_path)   # перенос
                    processed += 1
                except Exception as e:
                    print(f"Ошибка при обработке {file}: {e}")

    mode = "скопировано" if copy_mode else "перенесено"
    messagebox.showinfo("Готово", f"{mode} файлов: {processed}")

def choose_src():
    folder = filedialog.askdirectory()
    if folder:
        entry_src.delete(0, tk.END)
        entry_src.insert(0, folder)

def choose_dst():
    folder = filedialog.askdirectory()
    if folder:
        entry_dst.delete(0, tk.END)
        entry_dst.insert(0, folder)

root = tk.Tk()
root.title("Файловый перенос/копирование")
root.geometry("450x450")
root.configure(bg="#444")

pad = 5
fontsize = 14
tk.Label(root, text="Исходная директория:", bg="#444", fg="#fff",font=fontsize).pack(pady=pad)
entry_src = tk.Entry(root, width=50)
entry_src.pack(pady=pad)
tk.Button(root, text="Выбрать...", command=choose_src).pack(pady=pad)

tk.Label(root, text="Целевая директория:", bg="#444", fg="#fff",font=fontsize).pack(pady=pad)
entry_dst = tk.Entry(root, width=50)
entry_dst.pack(pady=pad)
tk.Button(root, text="Выбрать...", command=choose_dst).pack(pady=pad)

tk.Label(root, text="Расширение (например .txt):", bg="#444", fg="#fff",font=fontsize).pack(pady=pad)
entry_ext = tk.Entry(root, width=10)
entry_ext.pack(pady=pad)

var_copy = tk.IntVar()
tk.Checkbutton(root, text="Копировать вместо переноса", variable=var_copy, bg="#444", fg="#fff", selectcolor="#222",font=fontsize).pack(pady=pad)

tk.Button(root, text="Запустить", command=process_files).pack(pady=10)

root.mainloop()
