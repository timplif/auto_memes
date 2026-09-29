import os, urllib.request, json, re, random, sys
from datetime import datetime
from urllib.parse import urlparse

README = "README.md"

SUBREDDITS = ["ProgrammerHumor"]

ALLOWED_DOMAINS = [
    "i.redd.it", "i.imgur.com", "media.tenor.com",
    "i.giphy.com", "preview.redd.it", "external-preview.redd.it",
]
ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
IMAGE_MAGIC_BYTES = [
    b'\xff\xd8\xff', b'\x89PNG', b'GIF87a', b'GIF89a', b'RIFF',
]

KEYWORDS = [
    "код", "программ", "разработ", "баг", "отладк", "софт", "алгоритм",
    "питон", "джава", "функци", "перемен", "цикл", "база данных",
    "деплой", "продакшн", "учёб", "универ", "сессия", "дедлайн",
    "экзамен", "лаб", "курсов", "диплом", "препод", "пара", "лекц",
    "итишник", "программист", "кодер", "айтишник", "разработчик",
    "git", "github", "stackoverflow", "html", "css", "js", "python",
    "java", "javascript", "compiler", "debug", "error", "bug",
    "deploy", "production", "frontend", "backend", "devops",
    "student", "homework", "exam", "deadline", "university",
    "code", "coding", "program", "developer", "software",
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
    return bool(re.search('[а-яА-ЯёЁ]', text))

def is_relevant(title):
    lower = title.lower()
    return any(kw in lower for kw in KEYWORDS)

def get_meme(existing_urls, existing_titles, prefer_russian=True):
    max_attempts = 60
    
    for attempt in range(max_attempts):
        try:
            url = "https://meme-api.com/gimme/ProgrammerHumor"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode())
                meme_url = data.get('url', '')
                title = data.get('title', '')
                
                if not meme_url or not is_valid_image_url(meme_url):
                    continue
                if not is_real_image(meme_url):
                    continue
                if meme_url in existing_urls or title in existing_titles:
                    continue
                if not is_relevant(title):
                    continue
                
                if prefer_russian and not has_cyrillic(title):
                    continue
                
                print(f"✅ Нашёл мем: {title}")
                return meme_url, title
        except Exception as e:
            continue
    
    if prefer_russian:
        print("⚠️ Русских не нашёл, беру любой программистский")
        return get_meme(existing_urls, existing_titles, prefer_russian=False)
    
    print("❌ Не удалось получить мем")
    sys.exit(1)

def extract_old_memes(content):
    """Надёжно извлекает все блоки мемов через регулярки"""
    # Ищем все блоки, начинающиеся с "### " и идущие до следующего "### " или конца
    pattern = r'### .*?(?=### 🗓|\Z)'
    memes = re.findall(pattern, content, re.DOTALL)
    
    # Чистим каждый блок: убираем лишние "---" в конце
    cleaned = []
    for meme in memes:
        meme = meme.strip()
        # Убираем trailing "---" если есть
        if meme.endswith("---"):
            meme = meme[:-3].strip()
        if meme:
            cleaned.append(meme)
    
    return cleaned

now = datetime.now().strftime("%d.%m.%Y %H:%M")

if not os.path.exists(README):
    url, title = get_meme([], [], prefer_russian=True)
    content = f"""# 😂 Коллекция программистских мемов

> Автопополняемая коллекция мемов про код, баги и учёбу! 💻

---

## 📊 Статистика

- 🎲 Всего мемов: **1**
- 📅 Последний мем: _{now}_
- 🔄 Обновляется: 3 раза в день
- 📚 Темы: Программирование, учёба, баги, дедлайны

---

## 🎲 Свежие мемы

### 🗓 {now} — {title}

![]({url})

<sub>Источник: Reddit</sub>

---

"""
else:
    with open(README, 'r', encoding='utf-8') as f:
        old_content = f.read()
    
    # Извлекаем старые мемы
    old_memes = extract_old_memes(old_content)
    print(f"📦 Найдено старых мемов: {len(old_memes)}")
    
    # Собираем URL и title для проверки дубликатов
    existing_urls = re.findall(r'!\[\]\((https?://[^)]+)\)', old_content)
    existing_titles = re.findall(r'### 🗓 [^—]*— (.+?)(?:\n|$)', old_content)
    
    # Получаем новый мем
    url, title = get_meme(existing_urls, existing_titles, prefer_russian=True)
    
    count = len(old_memes) + 1
    
    # Создаём шапку
    header = f"""# 😂 Коллекция программистских мемов

> Автопополняемая коллекция мемов про код, баги и учёбу! 💻

---

## 📊 Статистика

- 🎲 Всего мемов: **{count}**
- 📅 Последний мем: _{now}_
- 🔄 Обновляется: 3 раза в день
- 📚 Темы: Программирование, учёба, баги, дедлайны

---

## 🎲 Свежие мемы

"""
    
    # Новый мем
    new_meme = f"""### 🗓 {now} — {title}

![]({url})

<sub>Источник: Reddit</sub>

---

"""
    
    # Собираем старые мемы с разделителями
    old_memes_text = ""
    for meme in old_memes:
        old_memes_text += meme + "\n\n---\n\n"
    
    # Итог: шапка + новый мем + старые мемы
    content = header + new_meme + old_memes_text

with open(README, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Мем #{count if 'count' in dir() else 1} добавлен: {title}")
