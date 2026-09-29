import os, urllib.request, json, re, random, sys
from datetime import datetime

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

def is_valid_image(url):
    """Проверяем, что ссылка ведет на изображение"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            content_type = r.headers.get('Content-Type', '')
            return 'image' in content_type
    except:
        return False

def get_meme():
    """Берем мем только из API"""
    subs = SUBREDDITS.copy()
    random.shuffle(subs)
    
    for sub in subs:
        try:
            url = f"https://meme-api.com/gimme/{sub}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode())
                meme_url = data.get('url', '')
                title = data.get('title', 'Programming meme')
                
                if meme_url and meme_url.startswith('http') and is_valid_image(meme_url):
                    print(f"✅ Нашел мем из r/{sub}: {title}")
                    return meme_url, title
        except Exception as e:
            print(f" r/{sub} не сработал: {e}")
            continue
    
    # Если ни один сабреддит не сработал — завершаем с ошибкой
    print("❌ Не удалось получить мем из API. Коммит не будет создан.")
    sys.exit(1)

now = datetime.now().strftime("%d.%m.%Y %H:%M")
url, title = get_meme()

# Считаем количество мемов
count = 1
old_memes = ""
if os.path.exists(README):
    with open(README, 'r', encoding='utf-8') as f:
        old_content = f.read()
    old_count = len(re.findall(r'### ', old_content))
    count = old_count + 1
    
    if "## 🎲 Свежие мемы" in old_content:
        idx = old_content.index("## 🎲 Свежие мемы") + len("## 🎲 Свежие мемы")
        old_memes = old_content[idx:].strip() + "\n\n"

# Создаем шапку со статистикой
header = f"""#  Коллекция программистских мемов

> Автопополняемая коллекция мемов про код, баги и учебу! 💻

---

##  Статистика

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
