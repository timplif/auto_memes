import os, urllib.request, json, re, random, sys
from datetime import datetime
from urllib.parse import urlparse

README = "README.md"

# Сначала русские сабреддиты, потом английские программистские
SUBREDDITS = [
    "russianmemes",
    "memes_ru", 
    "RussianHumor",
    "pikabu",
    "ProgrammerHumor",
    "programming",
    "learnprogramming",
    "coding",
    "webdev",
    "python",
    "javascript",
]

ALLOWED_DOMAINS = [
    "i.redd.it",
    "i.imgur.com",
    "media.tenor.com",
    "i.giphy.com",
    "preview.redd.it",
    "external-preview.redd.it",
]

ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".webp"]

IMAGE_MAGIC_BYTES = [
    b'\xff\xd8\xff',
    b'\x89PNG',
    b'GIF87a', b'GIF89a',
    b'RIFF',
]

def is_valid_image_url(url):
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        if not any(domain == d or domain.endswith("." + d) for d in ALLOWED_DOMAINS):
            return False
        path = parsed.path.lower()
        if not any(path.endswith(ext) for ext in ALLOWED_EXTENSIONS):
            return False
        return True
    except:
        return False

def is_real_image(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            header = r.read(32)
            if len(header) < 10:
                return False
            for magic in IMAGE_MAGIC_BYTES:
                if header[:len(magic)] == magic:
                    return True
            if header[:5] in (b'<!DOC', b'<html', b'<HTML'):
                return False
            return False
    except:
        return False

def has_cyrillic(text):
    """Проверяет наличие кириллицы в тексте"""
    return bool(re.search('[а-яА-ЯёЁ]', text))

def get_meme():
    """Берём мем с приоритетом на русский язык"""
    max_attempts = 30
    
    for attempt in range(max_attempts):
        sub = random.choice(SUBREDDITS)
        try:
            url = f"https://meme-api.com/gimme/{sub}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode())
                meme_url = data.get('url', '')
                title = data.get('title', '')
                
                # Проверка URL
                if not meme_url or not is_valid_image_url(meme_url):
                    continue
                
                # Проверка содержимого
                if not is_real_image(meme_url):
                    continue
                
                # Проверка на русский язык (кириллица в title)
                if has_cyrillic(title):
                    print(f"✅ Нашёл русский мем из r/{sub}: {title}")
                    return meme_url, title
                else:
                    print(f"️ [{attempt+1}] Английский мем из r/{sub}, ищем русский...")
                    continue
                    
        except Exception as e:
            continue
    
    # Если не нашли русский — берём любой валидный мем
    print("⚠️ Не нашли русский мем, берём любой программистский")
    for attempt in range(10):
        sub = random.choice(SUBREDDITS)
        try:
            url = f"https://meme-api.com/gimme/{sub}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode())
                meme_url = data.get('url', '')
                title = data.get('title', 'Programming meme')
                
                if meme_url and is_valid_image_url(meme_url) and is_real_image(meme_url):
                    print(f"✅ Взял мем из r/{sub}: {title}")
                    return meme_url, title
        except:
            continue
    
    print("❌ Не удалось получить мем")
    sys.exit(1)

now = datetime.now().strftime("%d.%m.%Y %H:%M")
url, title = get_meme()

count = 1
old_memes = ""
if os.path.exists(README):
    with open(README, 'r', encoding='utf-8') as f:
        old_content = f.read()
    old_count = len(re.findall(r'### 🗓', old_content))
    count = old_count + 1
    
    if "## 🎲 Свежие мемы" in old_content:
        idx = old_content.index("## 🎲 Свежие мемы") + len("## 🎲 Свежие мемы")
        old_memes = old_content[idx:].strip() + "\n\n"

header = f"""# 😂 Коллекция программистских мемов

> Автопополняемая коллекция мемов про код, баги и учебу! 💻

---

## 📊 Статистика

- 🎲 Всего мемов: **{count}**
- 📅 Последний мем: _{now}_
- 🔄 Обновляется: 3 раза в день
- 📚 Темы: Программирование, учеба, баги, дедлайны

---

## 🎲 Свежие мемы

"""

new_meme = f"""### 🗓 {now} — {title}

![]({url})

<sub>Источник: Reddit</sub>

---

"""

content = header + new_meme + old_memes

with open(README, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Мем #{count} добавлен: {title}")
