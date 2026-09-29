import os, urllib.request, json, re, random
from datetime import datetime

README = "README.md"

FALLBACK = [
    ("https://i.imgflip.com/1g8my4.jpg", "Two Buttons"),
    ("https://i.imgflip.com/30b1gx.jpg", "Drake Hotline Bling"),
    ("https://i.imgflip.com/261o3j.jpg", "But Thats None Of My Business"),
    ("https://i.imgflip.com/46e43q.jpg", "Always Has Been"),
    ("https://i.imgflip.com/3lmzyx.jpg", "Stonks"),
    ("https://i.imgflip.com/1ur9b0.jpg", "Distracted Boyfriend"),
    ("https://i.imgflip.com/24y43o.jpg", "Change My Mind"),
    ("https://i.imgflip.com/1bij.jpg", "One Does Not Simply"),
    ("https://i.imgflip.com/9ehk.jpg", "Success Kid"),
    ("https://i.imgflip.com/1otk96.jpg", "Batman Slapping Robin"),
]

def get_meme():
    try:
        req = urllib.request.Request(
            "https://meme-api.com/gimme",
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
            url = data.get('url', '')
            title = data.get('title', 'Meme')
            if url and url.startswith('http'):
                return url, title
    except Exception as e:
        print(f"API error: {e}")
    m = random.choice(FALLBACK)
    return m[0], m[1]

now = datetime.now().strftime("%d.%m.%Y %H:%M")
url, title = get_meme()

if os.path.exists(README):
    with open(README, 'r', encoding='utf-8') as f:
        content = f.read()
    count = len(re.findall(r'### 🗓', content)) + 1
    content = re.sub(r'Всего мемов: \*\*\d+\*\*', f'Всего мемов: **{count}**', content)
    content = re.sub(r'Последний мем: _.*_', f'Последний мем: _{now}_', content)
    marker = "##  Свежие мемы\n\n"
    if marker in content:
        idx = content.index(marker) + len(marker)
        new_block = f"### 🗓 {now} — {title}\n\n![]({url})\n\n<sub>Источник: Reddit</sub>\n\n---\n\n"
        content = content[:idx] + new_block + content[idx:]
    else:
        content += f"\n### 🗓 {now} — {title}\n\n![]({url})\n\n<sub>Источник: Reddit</sub>\n\n---\n\n"
else:
    count = 1
    content = f"""# 😂 Коллекция мемов

> Автопополняемая коллекция популярных мемов! 🌍

---

##  Статистика

- 🎲 Всего мемов: **{count}**
- 📅 Последний мем: _{now}_
- 🔄 Обновляется: 3 раза в день

---

##  Свежие мемы

### 🗓 {now} — {title}

![]({url})

<sub>Источник: Reddit</sub>

---

"""

with open(README, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Мем #{count} добавлен: {title}")
