import asyncio
import json
from publisher import publish_article_async

STORAGE_FILE = "storage.json"

# Здесь хранятся статьи для публикации
ARTICLES_FOR_PUBLISHING = [
    {
        "title": "🧠 Новая новость",
        "content":   "Разраб фиксит баг.\nна проде.\n\n", 
        "image_url": "https://raw.githubusercontent.com/yarovik1982/images/refs/heads/main/Screenshot_15.png",
        "link": "post_004"
    }
]

def load_storage():
    """Загружает историю опубликованных статей"""
    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_storage(data):
    """Сохраняет историю опубликованных статей"""
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

async def publish_all_articles():
    """Публикует все неопубликованные статьи один раз"""
    published_links = load_storage()
    print("🚀 Запуск публикации статей...")
    
    published_count = 0
    
    for article in ARTICLES_FOR_PUBLISHING:
        if article["link"] not in published_links:
            try:
                print(f"📌 Публикуем: {article['title']}")
                await publish_article_async(article)
                print(f"✅ Опубликовано: {article['title']}")
                
                published_links.append(article["link"])
                save_storage(published_links)
                published_count += 1
                
                # Задержка между публикациями (2 секунды)
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"❌ Ошибка при публикации: {e}")
                print(f"   Статья: {article['title']}")
        else:
            print(f"⏭️ Уже опубликовано: {article['title']}")
    
    if published_count > 0:
        print(f"\n✅ Готово! Опубликовано {published_count} новых статей.")
    else:
        print("\n📝 Все статьи уже были опубликованы ранее.")
    
    return published_count

if __name__ == "__main__":
    # Запускаем публикацию один раз и завершаем работу
    result = asyncio.run(publish_all_articles())
    
    # Добавляем паузу перед закрытием (чтобы видеть результат)
    input("\nНажмите Enter для выхода...")