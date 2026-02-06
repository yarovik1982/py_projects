from PIL import Image
import os


def process_images(
   src_dir,
   src_files,
   dst_dir,
   src_format,
   dst_format,
   quality,
   scale,
   do_resize,
   do_compress,
   do_convert,
   log_callback
):

   if (not src_dir and not src_files) or not dst_dir:
      log_callback("❗ Не выбран источник или назначение")
      return

   os.makedirs(dst_dir, exist_ok=True)

   processed = 0
   files_to_process = []

   # Если пользователь выбрал конкретные файлы
   if src_files:
      files_to_process = src_files
      log_callback(f"Обработка {len(src_files)} выбранных файлов")
   else:
        # Иначе собираем все файлы из папки
      for root, _, files in os.walk(src_dir):
         for file in files:
               file_lower = file.lower()
               if file_lower.endswith(f".{src_format.lower()}"):
                  files_to_process.append(os.path.join(root, file))

   if not files_to_process:
      log_callback("❗ Файлы для обработки не найдены")
      return

    # Основной цикл обработки
   for path in files_to_process:
      try:
         file = os.path.basename(path)
         img = Image.open(path)

            # resize
         if do_resize and scale != 1.0:
            w, h = img.size
            img = img.resize(
                  (int(w * scale), int(h * scale)),
               Image.Resampling.LANCZOS
            )
            log_callback(f"  Изменен размер: {w}x{h} → {int(w * scale)}x{int(h * scale)}")

            # convert (если формат меняется)
         name = os.path.splitext(file)[0]
         out_path = os.path.join(dst_dir, f"{name}.{dst_format}")

            # JPG требует RGB
         if do_convert and dst_format.lower() in ("jpg", "jpeg") and img.mode != "RGB":
            img = img.convert("RGB")
            log_callback(f"  Конвертация в RGB")

         save_params = {}

            # compress
         if do_compress and dst_format.lower() in ("jpg", "webp"):
            save_params["quality"] = quality
            save_params["optimize"] = True
            log_callback(f"  Сжатие с качеством {quality}%")

         img.save(out_path, dst_format.upper(), **save_params)

         processed += 1
         log_callback(f"✔ {file} → {os.path.basename(out_path)}")

      except Exception as e:
         log_callback(f"✖ {file}: {e}")

   log_callback(f"\nГотово. Обработано файлов: {processed}")