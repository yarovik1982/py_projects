# -*- coding: utf-8 -*-
from PIL import Image
import os


def _normalize_format(fmt):
    if not fmt:
        return ""
    return fmt.lower().lstrip(".")


def _save_format(fmt):
    if fmt in ("jpg", "jpeg"):
        return "JPEG"
    if fmt == "png":
        return "PNG"
    if fmt == "webp":
        return "WEBP"
    return fmt.upper()


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
    log_callback,
    progress_callback=None
):
    def log(msg):
        if log_callback:
            log_callback(msg)

    def progress(processed, total, filename=""):
        if progress_callback:
            progress_callback(processed, total, filename)

    if (not src_dir and not src_files) or not dst_dir:
        log("✖ Не выбран источник или назначение")
        return 0

    os.makedirs(dst_dir, exist_ok=True)

    processed = 0
    files_to_process = []
    known_exts = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif", ".gif"}
    effective_convert = do_convert or (not do_resize and not do_compress)

    # Если пользователь выбрал конкретные файлы
    if src_files:
        files_to_process = src_files
        log(f"Обработка {len(src_files)} выбранных файлов")
    else:
        # Иначе собираем все файлы из папки (по известным расширениям)
        for root, _, files in os.walk(src_dir):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in known_exts:
                    files_to_process.append(os.path.join(root, file))

    if not files_to_process:
        log("✖ Файлы для обработки не найдены")
        return 0

    total = len(files_to_process)
    progress(0, total, "")

    # Основной цикл обработки
    for path in files_to_process:
        file = os.path.basename(path)
        try:
            with Image.open(path) as img:
                detected_format = _normalize_format(img.format)
                ext = os.path.splitext(file)[1].lstrip('.').lower()

                # resize
                if do_resize and scale != 1.0:
                    w, h = img.size
                    img = img.resize(
                        (int(w * scale), int(h * scale)),
                        Image.Resampling.LANCZOS
                    )
                    log(f"  Изменен размер: {w}x{h} → {int(w * scale)}x{int(h * scale)}")

                if effective_convert:
                    out_format = _normalize_format(dst_format) or detected_format or ext or _normalize_format(src_format)
                else:
                    out_format = detected_format or ext or _normalize_format(src_format)

                if not out_format:
                    raise ValueError("Не удалось определить формат изображения")

                name = os.path.splitext(file)[0]
                out_ext = out_format if effective_convert else (ext or out_format)
                out_path = os.path.join(dst_dir, f"{name}.{out_ext}")

                # JPG требует RGB
                if out_format in ("jpg", "jpeg") and img.mode != "RGB":
                    img = img.convert("RGB")
                    log("  Конвертация в RGB")

                save_params = {}

                # compress
                if do_compress and out_format in ("jpg", "jpeg", "webp"):
                    save_params["quality"] = quality
                    save_params["optimize"] = True
                    log(f"  Сжатие с качеством {quality}%")

                save_format = _save_format(out_format)
                img.save(out_path, save_format, **save_params)

            processed += 1
            log(f"✔ {file} → {os.path.basename(out_path)}")

        except Exception as e:
            log(f"✖ {file}: {e}")
        finally:
            progress(processed, total, file)

    log(f"\nГотово. Обработано файлов: {processed}")
    return processed
