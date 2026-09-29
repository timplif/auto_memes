import os, urllib.request, json, re, random, sys
from datetime import datetime
from urllib.parse import urlparse

README = "README.md"

# ТОЛЬКО мем-сабреддиты (там только мемы, не статьи и не вопросы)
SUBREDDITS = [
    "ProgrammerHumor",
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

def get_meme():
    """Берём мем только из ProgrammerHumor"""
    max_attempts = 20
    
    for attempt in range(max_attempts):
        try:
            url = "https://meme-api.com/gimme/ProgrammerHumor"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode())
                meme_url = data.get('url', '')
                title = data.get('title', 'Programming meme')
                
                if not meme_url or not is_valid_image_url(meme_url):
                    continue
                
                if not is_real_image(meme_url):
                    continue
                
                print(f"✅ Нашёл мем: {title}")
                return meme_url, title
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            continue
    
    print("❌ Не удалось получить мем")
    sys.exit(1)

now = datetime.now().strftime("%d.%m.%Y %H:%M")
url, title = get_meme()

# Простая логика: если README нет — создаём с шапкой и первым мемом
# Если есть — добавляем новый мем сразу после заголовка "## 🎲 Свежие мемы"
if not os.path.exists(README):
    content = f"""# 😂 Коллекция программистских мемов

> Автопополняемая коллекция мемов про код, баги и учебу! 💻

---

## 📊 Статистика

- 🎲 Всего мемов: **1**
- 📅 Последний мем: _{now}_
- 🔄 Обновляется: 3 раза в день
- 📚 Темы: Программирование, учеба, баги, дедлайны

---

## 🎲 Свежие мемы

### 🗓 {now} — {title}

![]({url})

<sub>Источник: Reddit</sub>

---

"""
else:
    with open(README, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Считаем мемы
    count = len(re.findall(r'### 🗓', content)) + 1
    
    # Обновляем статистику
    content = re.sub(r'Всего мемов: \*\*\d+\*\*', f'Всего мемов: **{count}**', content)
    content = re.sub(r'Последний мем: _.*_', f'Последний мем: _{now}_', content)
    
    # Находим позицию после "## 🎲 Свежие мемы\n\n"
    marker = "## 🎲 Свежие мемы\n\n"
    if marker in content:
        idx = content.index(marker) + len(marker)
        new_meme = f"###  {now} — {title}\n\n![]({url})\n\n<sub>Источник: Reddit</sub>\n\n---\n\n"
        content = content[:idx] + new_meme + content[idx:]
    else:
        content += f"\n### 🗓 {now} — {title}\n\n![]({url})\n\n<sub>Источник: Reddit</sub>\n\n---\n\n"

with open(README, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Мем #{count if os.path.exists(README) else 1} добавлен: {title}")
