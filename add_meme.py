import os, urllib.request, json, re, random, sys
from datetime import datetime
from urllib.parse import urlparse

README = "README.md"

# Программистские сабреддиты
SUBREDDITS = [
    "ProgrammerHumor",
    "programming",
    "learnprogramming",
    "coding",
    "webdev",
    "python",
    "javascript",
    "cscareerquestions",
]

# Только надёжные хостинги изображений
ALLOWED_DOMAINS = [
    "i.redd.it",
    "i.imgur.com",
    "media.tenor.com",
    "i.giphy.com",
    "preview.redd.it",
    "external-preview.redd.it",
]

# Допустимые расширения файлов
ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".webp"]

def is_valid_image_url(url):
    """Проверяем, что URL ведёт на прямую картинку с надёжного хостинга"""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        
        # Проверяем домен
        if not any(domain == d or domain.endswith("." + d) for d in ALLOWED_DOMAINS):
            return False
        
        # Проверяем расширение
        path = parsed.path.lower()
        if not any(path.endswith(ext) for ext in ALLOWED_EXTENSIONS):
            return False
        
        return True
    except:
        return False

def get_meme():
    """Берём мем только из API с жёсткой проверкой"""
    # Делаем до 3 попыток на каждый сабреддит
    max_attempts = len(SUBREDDITS) * 3
    
    for attempt in range(max_attempts):
        sub = random.choice(SUBREDDITS)
        try:
            url = f"https://meme-api.com/gimme/{sub}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode())
                meme_url = data.get('url', '')
                title = data.get('title', 'Programming meme')
                
                # Жёсткая проверка URL
                if meme_url and is_valid_image_url(meme_url):
                    print(f"✅ Нашёл мем из r/{sub}: {title}")
                    return meme_url, title
                else:
                    print(f"⚠️ Пропустил битый URL из r/{sub}: {meme_url[:50]}")
        except Exception as e:
            print(f"❌ r/{sub} ошибка: {e}")
            continue
    
    # Если ничего не подошло — ошибка
    print("❌ Не удалось получить валидный мем из API")
    sys.exit(1)

now = datetime.now().strftime("%d.%m.%Y %H:%M")
url, title = get_meme()

# Считаем количество мемов
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
