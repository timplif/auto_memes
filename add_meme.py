import os, urllib.request, json, re, random, sys
from datetime import datetime
from urllib.parse import urlparse

README = "README.md"

# ТОЛЬКО программистские сабреддиты (без pikabu и russianmemes!)
SUBREDDITS = [
    "ProgrammerHumor",
    "programming",
    "learnprogramming",
    "coding",
    "webdev",
    "python",
    "javascript",
    "cscareerquestions",
    "softwareengineering",
    "ExperiencedDevs",
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

# Ключевые слова, связанные с программированием и учёбой
# Мем должен содержать хотя бы одно из них в title
KEYWORDS = [
    # Английские
    "code", "coding", "program", "developer", "bug", "debug", "software",
    "algorithm", "python", "java", "javascript", "html", "css", "git",
    "github", "stackoverflow", "compiler", "function", "variable", "loop",
    "api", "database", "sql", "linux", "terminal", "deploy", "production",
    "frontend", "backend", "fullstack", "devops", "server", "client",
    "error", "exception", "syntax", "runtime", "compile", "build",
    "student", "homework", "exam", "deadline", "university", "college",
    "cs ", "it ", "tech", "nerd", "geek", "hacker",
    "when you", "when the", "me when", "my code", "the code",
    "developer", "engineer", "programmer", "coder",
    # Русские
    "код", "программ", "разработ", "баг", "отладк", "софт", "алгоритм",
    "питон", "джава", "функци", "перемен", "цикл", "база данных",
    "деплой", "продакшн", "учёб", "универ", "сессия", "дедлайн",
    "экзамен", "лаб", "курсов", "диплом", "препод", "пара", "лекц",
    "итишник", "программист", "кодер", "айтишник",
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

def is_relevant_meme(title):
    """Проверяем, что мем про программирование или учёбу"""
    title_lower = title.lower()
    for keyword in KEYWORDS:
        if keyword in title_lower:
            return True
    return False

def get_meme():
    """Берём мем с тройной проверкой"""
    max_attempts = 50
    
    for attempt in range(max_attempts):
        sub = random.choice(SUBREDDITS)
        try:
            url = f"https://meme-api.com/gimme/{sub}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode())
                meme_url = data.get('url', '')
                title = data.get('title', '')
                
                # Проверка 1: URL
                if not meme_url or not is_valid_image_url(meme_url):
                    continue
                
                # Проверка 2: реальное изображение
                if not is_real_image(meme_url):
                    continue
                
                # Проверка 3: тематика (программирование/учёба)
                if not is_relevant_meme(title):
                    print(f"⚠️ [{attempt+1}] Не по теме из r/{sub}: {title[:50]}")
                    continue
                
                print(f"✅ Нашёл мем из r/{sub}: {title}")
                return meme_url, title
        except Exception as e:
            continue
    
    print("❌ Не удалось найти подходящий мем после 50 попыток")
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
-  Последний мем: _{now}_
-  Обновляется: 3 раза в день
-  Темы: Программирование, учеба, баги, дедлайны

---

##  Свежие мемы

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
