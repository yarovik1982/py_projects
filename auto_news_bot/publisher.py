# publisher.py
import aiohttp
import asyncio
from config import BOT_TOKEN, CHANNEL_ID

def split_message(message, max_length=1024):
    """Разделяет длинное сообщение на части не более max_length символов"""
    words = message.split()
    parts = []
    current_part = []
    current_length = 0
    
    for word in words:
        word_length = len(word) + 1  # +1 для пробела
        
        if current_length + word_length <= max_length:
            current_part.append(word)
            current_length += word_length
        else:
            if current_part:
                parts.append(' '.join(current_part))
            current_part = [word]
            current_length = word_length
    
    if current_part:
        parts.append(' '.join(current_part))
    
    return parts

async def publish_article_async(article):
    """Публикует статью в Telegram канал с изображением и текстом"""
    
    async with aiohttp.ClientSession() as session:
        # 1. Сначала отправляем изображение с короткой подписью
        if article.get('image_url'):
            try:
                print(f"🖼️  Отправляем изображение...")
                
                # Короткая подпись для изображения (не более 1024 символов)
                short_caption = f"📢 <b>{article['title']}</b>\n\n{article['content'][:500]}"
                if len(short_caption) > 1024:
                    short_caption = short_caption[:1021] + "..."
                
                # Отправляем фото
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
                data = {
                    "chat_id": CHANNEL_ID,
                    "photo": article['image_url'],
                    "caption": short_caption,
                    "parse_mode": "HTML"
                }
                
                async with session.post(url, json=data) as response:
                    response_data = await response.json()
                    if not response_data.get("ok"):
                        error_msg = response_data.get("description", "Неизвестная ошибка")
                        print(f"⚠️  Не удалось отправить фото: {error_msg}")
                
                # Пауза между сообщениями
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"⚠️  Ошибка при отправке изображения: {e}")
        
        # 2. Отправляем полный текст статьи частями
        print(f"📝 Отправляем текст статьи...")
        
        # Формируем полное сообщение
        full_message = f"📢 <b>{article['title']}</b>\n\n{article['content']}"
        
        # Разделяем на части
        message_parts = split_message(full_message, max_length=4096)  # 4096 - максимум для текстовых сообщений
        
        for i, part in enumerate(message_parts, 1):
            try:
                # Для первой части после изображения можно опустить заголовок
                if i > 1 and article.get('image_url'):
                    part_to_send = part
                else:
                    part_to_send = part
                
                await send_text_message(session, part_to_send)
                print(f"✅ Часть {i}/{len(message_parts)} отправлена")
                
                if i < len(message_parts):
                    await asyncio.sleep(0.5)  # Пауза между частями
                    
            except Exception as e:
                print(f"❌ Ошибка при отправке части {i}: {e}")

async def send_text_message(session, message):
    """Отправляет текстовое сообщение"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    
    async with session.post(url, json=data) as response:
        response_data = await response.json()
        if not response_data.get("ok"):
            error_msg = response_data.get("description", "Неизвестная ошибка")
            raise Exception(f"Ошибка Telegram API: {error_msg}")