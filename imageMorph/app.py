import customtkinter as ctk
# print(ctk.__version__)

from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from image_utils import *

# Устанавливаем темную тему
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
# ctk.set_default_font(size=14)


# Кастомные цвета для блоков

# Блоки
MAIN_COLOR = "#1a1a1a"  # Темнее фона
BUTTON_COLOR = "#2b2b2b"  # Светлее кнопок
BLOCK_COLOR = "#2b2b2b"  # Светлее темного фона
TOOLBAR_COLOR = "#2b2b2b"
CONSOLE_COLOR = "#111111"

FONT_SIZE = 16


class ImageMorphApp(ctk.CTk):
   """Основной класс приложения"""

   def __init__(self):
      super().__init__()

      self.title("ImageMorph")
      self.geometry("800x650")

      # Устанавливаем темный фон для главного окна
      self.configure(fg_color=MAIN_COLOR)

      self.src_dir = ""
      self.dst_dir = ""
      self.selected_files = []

      self.grid_columnconfigure(0, weight=1)
      self.grid_rowconfigure(1, weight=1)

      self.build_toolbar()
      self.build_main_area()
      self.build_console()

      # Инициализируем drag&drop после создания окна
      self.init_drag_drop()

    # ---------- Drag & Drop ----------
    
   def init_drag_drop(self):
        """Инициализация drag&drop после создания окна"""
        try:
            # Создаем TkinterDnD окно поверх CTk
            self.dnd_window = TkinterDnD.Tk()
            self.dnd_window.withdraw()  # Скрываем дополнительное окно
            
            # Настройка drag&drop для поля файлов
            self.files_entry.drop_target_register(DND_FILES)
            self.files_entry.dnd_bind('<<Drop>>', self.on_files_drop)
            print("Drag&drop инициализирован")
        except Exception as e:
            print(f"Drag&drop не доступен: {e}")

    # ---------- Toolbar ----------

   def build_toolbar(self):
      self.toolbar = ctk.CTkFrame(self, height=50, fg_color=TOOLBAR_COLOR)
      self.toolbar.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))

      self.toolbar.grid_columnconfigure(10, weight=1)

      ctk.CTkLabel(
         self.toolbar,
         text="ImageMorph",
         font=ctk.CTkFont(size=18, weight="bold")
      ).grid(row=0, column=0, padx=10)

      ctk.CTkButton(
         self.toolbar,
         text="Очистить консоль",
         width=150,
         command=lambda: self.console.delete("1.0", "end")
      ).grid(row=0, column=11, padx=10)

    # ---------- Main Area ----------

   def build_main_area(self):
      self.main_frame = ctk.CTkFrame(self, fg_color=BLOCK_COLOR)
      self.main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

      self.main_frame.grid_columnconfigure((0, 1, 2), weight=1)

      self.build_paths_block()
      self.build_modes_block()
      self.build_settings_block()

    # ----- Paths -----

   def build_paths_block(self):
      frame = ctk.CTkFrame(self.main_frame, fg_color=BLOCK_COLOR)
      frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

      frame.grid_columnconfigure(0, weight=1)

      ctk.CTkLabel(frame, text="Пути", )\
         .grid(row=0, column=0, pady=(5, 10), sticky="ew")

      # Источник
      ctk.CTkLabel(frame, text="Источник:")\
         .grid(row=1, column=0, sticky="w", pady=(5, 0))
      src_button_frame = ctk.CTkFrame(frame, fg_color="transparent")
      src_button_frame.grid(row=2, column=0, sticky="ew", pady=(0, 5))
      src_button_frame.grid_columnconfigure(0, weight=1)
      src_button_frame.grid_columnconfigure(1, weight=4)
      
      ctk.CTkButton(src_button_frame, text="Папка", width=80, command=self.choose_src)\
         .grid(row=0, column=0, padx=(0, 5))
      self.src_entry = ctk.CTkEntry(src_button_frame, placeholder_text="Путь к папке источника")
      self.src_entry.grid(row=0, column=1, sticky="ew")

      # Файлы
      ctk.CTkLabel(frame, text="Файлы:")\
         .grid(row=3, column=0, sticky="w", pady=(10, 0))
      files_button_frame = ctk.CTkFrame(frame, fg_color="transparent")
      files_button_frame.grid(row=4, column=0, sticky="ew", pady=(0, 5))
      files_button_frame.grid_columnconfigure(0, weight=1)
      files_button_frame.grid_columnconfigure(1, weight=4)
      
      ctk.CTkButton(files_button_frame, text="Выбрать", width=80, command=self.choose_files)\
         .grid(row=0, column=0, padx=(0, 5))
      self.files_entry = ctk.CTkEntry(files_button_frame, placeholder_text="Перетащите файлы или выберите")
      self.files_entry.grid(row=0, column=1, sticky="ew")

      # Назначение
      ctk.CTkLabel(frame, text="Назначение:")\
         .grid(row=5, column=0, sticky="w", pady=(10, 0))
      dst_button_frame = ctk.CTkFrame(frame, fg_color="transparent")
      dst_button_frame.grid(row=6, column=0, sticky="ew", pady=(0, 5))
      dst_button_frame.grid_columnconfigure(0, weight=1)
      dst_button_frame.grid_columnconfigure(1, weight=4)
      
      ctk.CTkButton(dst_button_frame, text="Папка", width=80, command=self.choose_dst)\
         .grid(row=0, column=0, padx=(0, 5))
      self.dst_entry = ctk.CTkEntry(dst_button_frame, placeholder_text="Путь к папке назначения")
      self.dst_entry.grid(row=0, column=1, sticky="ew")

    # ----- Modes -----

   def build_modes_block(self):
      frame = ctk.CTkFrame(self.main_frame, fg_color=BLOCK_COLOR)
      frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

      frame.grid_columnconfigure(0, weight=1)

      ctk.CTkLabel(frame, text="Режим обработки")\
         .grid(row=0, column=0, pady=(5, 10), sticky="ew")

      self.do_convert = ctk.BooleanVar(value=False)
      self.do_compress = ctk.BooleanVar(value=False)
      self.do_resize = ctk.BooleanVar(value=False)

      ctk.CTkCheckBox(frame, text="Конвертация", variable=self.do_convert, font=ctk.CTkFont(size=FONT_SIZE))\
         .grid(row=1, column=0, sticky="ew", pady=(30,2))

      ctk.CTkCheckBox(frame, text="Сжатие", variable=self.do_compress, font=ctk.CTkFont(size=FONT_SIZE))\
         .grid(row=2, column=0, sticky="ew", pady=2)

      ctk.CTkCheckBox(frame, text="Ресайз", variable=self.do_resize, font=ctk.CTkFont(size=FONT_SIZE))\
         .grid(row=3, column=0, sticky="ew", pady=2)

    # ----- Settings -----

   def build_settings_block(self):
      frame = ctk.CTkFrame(self.main_frame, fg_color=BLOCK_COLOR)
      frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

      frame.grid_columnconfigure(0, weight=1)

      ctk.CTkLabel(frame, text="Настройки", font=ctk.CTkFont(size=FONT_SIZE))\
         .grid(row=0, column=0, pady=(5, 10), sticky="ew")

      # Исходный формат
      ctk.CTkLabel(frame, text="Исходный формат:", font=ctk.CTkFont(size=FONT_SIZE))\
         .grid(row=1, column=0, pady=(5, 0), sticky="w")
      self.src_format = ctk.CTkOptionMenu(frame, values=["jpg", "png", "webp"])
      self.src_format.set("png")
      self.src_format.grid(row=2, column=0, pady=(0, 10), sticky="ew")

      # Целевой формат
      ctk.CTkLabel(frame, text="Целевой формат:", font=ctk.CTkFont(size=FONT_SIZE))\
         .grid(row=3, column=0, pady=(5, 0), sticky="w")
      self.dst_format = ctk.CTkOptionMenu(frame, values=["jpg", "png", "webp"])
      self.dst_format.set("jpg")
      self.dst_format.grid(row=4, column=0, pady=(0, 10), sticky="ew")

      # Качество
      ctk.CTkLabel(frame, text="Качество:", font=ctk.CTkFont(size=FONT_SIZE))\
         .grid(row=5, column=0, pady=(5, 0), sticky="w")
      quality_frame = ctk.CTkFrame(frame, fg_color="transparent")
      quality_frame.grid(row=6, column=0, sticky="ew", pady=(0, 10))
      quality_frame.grid_columnconfigure(0, weight=4)
      quality_frame.grid_columnconfigure(1, weight=1)
      
      self.quality = ctk.CTkSlider(quality_frame, from_=10, to=100)
      self.quality.set(85)
      self.quality.grid(row=0, column=0, padx=(0, 10), sticky="ew")
      self.quality_label = ctk.CTkLabel(quality_frame, text="85%", width=40)
      self.quality_label.grid(row=0, column=1)
      self.quality.configure(command=self.update_quality_label)

      # Масштаб
      ctk.CTkLabel(frame, text="Масштаб:", font=ctk.CTkFont(size=FONT_SIZE))\
         .grid(row=7, column=0, pady=(5, 0), sticky="w")
      self.scale = ctk.CTkOptionMenu(frame, values=["0.25", "0.5", "0.75", "1.0"])
      self.scale.set("1.0")
      self.scale.grid(row=8, column=0, pady=(0, 10), sticky="ew")

      # Кнопка старт
      ctk.CTkButton(frame, text="Старт", height=50,width=100, command=self.start, font=ctk.CTkFont(size=FONT_SIZE))\
         .grid(row=9, column=0, pady=(10, 0),)

    # ---------- Console ----------

   def build_console(self):
      self.console = ctk.CTkTextbox(self, height=160, fg_color=CONSOLE_COLOR, font=ctk.CTkFont(size=FONT_SIZE))
      self.console.grid(row=2, column=0, sticky="ew", padx=20, pady=(5, 15))

      def log(msg):
         self.console.insert("end", msg + "\n")
         self.console.see("end")

      self.log = log

    # ---------- Actions ----------

   def choose_src(self):
      self.src_dir = filedialog.askdirectory()
      self.src_entry.delete(0, "end")
      self.src_entry.insert(0, self.src_dir)
      self.log(f"Источник: {self.src_dir}")

   def choose_files(self):
      files = filedialog.askopenfilenames(
         title="Выберите изображения",
         filetypes=[
            ("Изображения", "*.jpg *.jpeg *.png *.webp"),
            ("Все файлы", "*.*")
         ]
      )
      if files:
         self.selected_files = list(files)
         self.files_entry.delete(0, "end")
         self.files_entry.insert(0, "; ".join(files))
         self.log(f"Выбрано файлов: {len(self.selected_files)}")

   def on_files_drop(self, event):
      """Обработка перетаскивания файлов в поле"""
      files = event.data
      if files:
         # Преобразуем строку с файлами в список
         file_list = self.parse_dropped_files(files)
         self.selected_files = file_list
         self.files_entry.delete(0, "end")
         self.files_entry.insert(0, "; ".join(file_list))
         self.log(f"Перетащено файлов: {len(file_list)}")

   def parse_dropped_files(self, files_string):
      """Парсинг строки с перетащенными файлами"""
      # Для Windows: файлы разделены пробелами и заключены в фигурные скобки
      if files_string.startswith('{') and files_string.endswith('}'):
         files_string = files_string[1:-1]
         file_list = [f.strip() for f in files_string.split('} {')]
      else:
         # Для других систем или простого формата
         file_list = [f.strip() for f in files_string.split()]
      
      return [f for f in file_list if f]

   def choose_dst(self):
      self.dst_dir = filedialog.askdirectory()
      self.dst_entry.delete(0, "end")
      self.dst_entry.insert(0, self.dst_dir)
      self.log(f"Назначение: {self.dst_dir}")

   def update_quality_label(self, value):
      self.quality_label.configure(text=f"{int(value)}%")

   def start(self):
      self.log("▶ Старт обработки")
      
      # Получаем пути из инпутов
      src_dir = self.src_entry.get().strip()
      dst_dir = self.dst_entry.get().strip()
      
      # Если файлы выбраны через поле или перетаскивание
      files_from_entry = self.files_entry.get().strip()
      if files_from_entry and not self.selected_files:
         # Парсим файлы из поля ввода
         self.selected_files = [f.strip() for f in files_from_entry.split(';')]
      
      process_images(
              src_dir=src_dir if src_dir else None,
            src_files=self.selected_files if self.selected_files else None,
            dst_dir=dst_dir,
            src_format=self.src_format.get(),
            dst_format=self.dst_format.get(),
            quality=int(self.quality.get()),
            scale=float(self.scale.get()),
            do_resize=self.do_resize.get(),
            do_compress=self.do_compress.get(),
            do_convert=self.do_convert.get(),
            log_callback=self.log
      )


if __name__ == "__main__":
   app = ImageMorphApp()
   app.mainloop()