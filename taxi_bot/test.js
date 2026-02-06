
gulp.task("html:dev", function () {
   return (
      gulp
         .src([
            "./src/html/pages/**/*.html",
            "!./**/blocks/**/*.*",
            "!./**/sections/**/*.*",
            "!./**/docs/**/*.*",
         ])
         .pipe(changed("./build/", { hasChanged: changed.compareContents }))
         .pipe(plumber(plumberNotify("HTML")))
         .pipe(fileInclude(fileIncludeSetting))
// Добавлена замена скрытых символов на обычный пробел
         .pipe(
            replace(/[\u00A0\u1680\u180E\u2000-\u200B\u202F\u205F\u3000\uFEFF]/g, ' ')
         )

         .pipe(
            replace(/<img(?:.|\n|\r)*?>/g, function (match) {
               return match
                  .replace(/\r?\n|\r/g, "")
                  .replace(/\s{2,}/g, " ");
            })
         ) // удаляет лишние пробелы и переводы строк внутри тега <img>
         .pipe(
            replace(
               /(?<=src=|href=|srcset=)(['"])(\.(\.)?\/)*(img|images|fonts|css|scss|sass|js|files|audio|video)(\/[^\/'"]+(\/))?([^'"]*)\1/gi,
               "$1./$4$5$7$1"
            )
         )
         // Корректируем пути в src/href (не трогаем srcset)
         .pipe(
            replace(
               /(?<=src=|href=)(['"])(\.(\.)?\/)*(img|images|fonts|css|scss|sass|js|files|audio|video)(\/[^\/'"]+(\/))?([^'"]*)\1/gi,
               "$1./$4$5$7$1"
            )
         )
         // Обрабатываем srcset (сохраняем дескрипторы)
         .pipe(
            replace(
               /(?<=srcset=)(['"])(\.(\.)?\/)*(img|images)(\/[^\/'"]+\.(?:jpg|jpeg|png|gif|webp))(\s+\d+w)(['"])/gi,
               "$1./$4$5$6$7"
            )
         )
         // Преобразуем <img> в <picture> с динамическим определением mobile/desktop по sizes
         .pipe(
            replace(
               /<img\s+([^>]*?)src=["']([^"']+)["'][^>]*srcset=["']([^"']+)["'][^>]*sizes=["']([^"']+)["']([^>]*)>/gi,
               function (match, preAttrs, src, srcset, sizes, postAttrs) {
                  // 1. Извлекаем максимальную ширину для mobile из sizes
                  // Ищем шаблон (max-width: XXXpx)
                  const mobileMaxWidthMatch = sizes.match(
                     /\(max-width:\s*(\d+)px\)/i
                  );
                  const mobileMaxWidth = mobileMaxWidthMatch
                     ? parseInt(mobileMaxWidthMatch[1])
                     : 820; // fallback, если не найдено

                  // 2. Разбираем srcset на {url, descriptor}
                  const srcsetParts = srcset
                     .trim()
                     .split(/\s*,\s*/)
                     .map((part) => {
                        const [url, descriptor] = part
                           .trim()
                           .split(/\s+/);
                        return {
                           url,
                           descriptor: parseInt(descriptor),
                        };
                     });

                  // 3. Находим mobileSrc (макс. ширина ≤ mobileMaxWidth) и desktopSrc (макс. ширина > mobileMaxWidth)
                  const mobileCandidates = srcsetParts.filter(
                     (part) => part.descriptor <= mobileMaxWidth
                  );
                  const desktopCandidates = srcsetParts.filter(
                     (part) => part.descriptor > mobileMaxWidth
                  );

                  const mobileSrc =
                     mobileCandidates.length > 0
                        ? mobileCandidates[mobileCandidates.length - 1]
                           .url // самый большой среди подходящих
                        : src; // fallback

                  const desktopSrc =
                     desktopCandidates.length > 0
                        ? desktopCandidates[
                           desktopCandidates.length - 1
                        ].url // самый большой среди десктопных
                        : src; // fallback

                  // 4. Генерируем @1x и @2x для mobile и desktop
                  const mobile1x = mobileSrc.replace(
                     /\.(jpe?g|png|gif|webp)$/i,
                     ".$1"
                  );
                  const mobile2x = mobileSrc.replace(
                     /\.(jpe?g|png|gif|webp)$/i,
                     "@2x.$1"
                  );

                  const desktop1x = desktopSrc.replace(
                     /\.(jpe?g|png|gif|webp)$/i,
                     ".$1"
                  );
                  const desktop2x = desktopSrc.replace(
                     /\.(jpe?g|png|gif|webp)$/i,
                     "@2x.$1"
                  );
