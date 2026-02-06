import tkinter as tk
from tkinter import messagebox

def check_age():
   name = entry_name.get()
   age = entry_age.get() 

   try:
      age = int(age)
   except ValueError:
      messagebox.showerror("Ошибка", "Введите возраст в числовом формате")
      return
   if age < 18:
      msg = f"Извините, {name}, но вам нет 18 лет 🤓"
   else:
      msg = f"Привет, {name}! Добро пожаловать в нашу систему! 🎉"

   messagebox.showinfo( msg)

root = tk.Tk()
root.title("Проверка возраста")
root.geometry("300x150")
root.configure(bg='#333')

pad = 10
width = 10
tk.Label(root, 
         text="Имя: Имя Имя Имя",
         bg="#555",
         fg="#ccc",
         ).pack(pady=pad)
entry_name = tk.Entry(root,bg="#555",fg="#ccc")
entry_name.pack()

tk.Label(root, 
         text="Возраст:",
         bg="#555",
         fg="#ccc",
         width=width,
).pack(pady=pad)
entry_age = tk.Entry(root,
                     bg="#555",
                     fg="#ccc")
entry_age.pack()

tk.Button(root, 
         text="Проверить", 
         bg="#555",
         fg="#ccc",
          command=check_age
).pack(pady=pad)

root.mainloop()
