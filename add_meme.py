import os, urllib.request, json, re, random
from datetime import datetime

README = "README.md"

# ТОЛЬКО ПРОВЕРЕННЫЕ МЕМЫ С РАБОЧИМИ КАРТИНКАМИ
MEMES = [
    ("https://i.imgflip.com/1g8my4.jpg", "Две кнопки"),
    ("https://i.imgflip.com/30b1gx.jpg", "Дрейк"),
    ("https://i.imgflip.com/261o3j.jpg", "Это фича"),
    ("https://i.imgflip.com/46e43q.jpg", "Всегда так было"),
    ("https://i.imgflip.com/3lmzyx.jpg", "Stonks"),
    ("https://i.imgflip.com/1ur9b0.jpg", "Отвлечённый парень"),
    ("https://i.imgflip.com/24y43o.jpg", "Change My Mind"),
    ("https://i.imgflip.com/1bij.jpg", "One Does Not Simply"),
    ("https://i.imgflip.com/9ehk.jpg", "Success Kid"),
    ("https://i.imgflip.com/1otk96.jpg", "Бэтмен и Робин"),
]

def get_meme():
    # Берём случайный мем из проверенного списка
    meme = random.choice(MEMES)
    return meme[0], meme[1]

now = datetime.now().strftime("%d.%m.%Y %H:%M")
url, title = get_meme()

# Всегда создаём красивый README с нуля
count = 1
if os.path.exists(README):
    with open(README, 'r', encoding='utf-8') as f:
        old_content = f.read()
    # Считаем старые мемы
    old_count = len(re.findall(r'### ', old_content))
    count = old_count + 1

# Создаём шапку со статистикой
header = f"""# 😂 Коллекция мемов

> Автопополняемая коллекция популярных мемов! 🌍

---

##  Статистика

- 🎲 Всего мемов: **{count}**
- 📅 Последний мем: _{now}_
- 🔄 Обновляется: 3 раза в день

---

##  Свежие мемы

"""

# Формируем блок нового мема
new_meme = f"""### 🗓 {now} — {title}

![]({url})

<sub>Источник: Imgflip</sub>

---

"""

# Если был старый README, добавляем старые мемы после нового
if os.path.exists(README):
    # Извлекаем только мемы из старого контента (после "## 🎲 Свежие мемы")
    old_memes = ""
    if "## 🎲 Свежие мемы" in old_content:
        idx = old_content.index("## 🎲 Свежие мемы") + len("## 🎲 Свежие мемы")
        old_memes = old_content[idx:].strip() + "\n\n"
    
    content = header + new_meme + old_memes
else:
    content = header + new_meme

with open(README, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Мем #{count} добавлен: {title}")
print(f" URL: {url}")
