from bs4 import BeautifulSoup
import requests
import asyncio
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop
from config import bot_token
from config import data_source


def make_link(text):
    text = text.lower()
    text = text.replace(" ", "-")
    hero_url = data_source
    hero_url = hero_url.replace("paste", text, 1)
    return hero_url


async def find_heroes(text):
    hero_url = make_link(text)
    try:
        page = requests.get(hero_url, headers={'User-agent': 'your bot 0.1'})
    except:
        return "Упс, героя не нашел, попробуй поссмотреть запрос на опечатки, и на правильность названия. Например: не 'Травоман', а 'Techies'"
    soup = BeautifulSoup(page.text, 'html.parser')
    words = soup.text.split()
    if words[2] == "Not" and words[3] == "Found":
        return "Упс, героя не нашел, попробуй поссмотреть запрос на опечатки, и на правильность названия. Например: не 'Травоман', а 'Techies'"
    hero_name = ""
    for tag in soup.find_all("h1"):
        i = 0
        while 'a' <= tag.text[i] <= 'z' or 'A' <= tag.text[i] <= 'Z' or tag.text[i] == ' ':
            hero_name += tag.text[i]
            i += 1
    ans = []
    flag = False
    cnt = 5
    for tag in soup.find_all("tr"):
        a = tag.text.split()
        if cnt == 0:
            break
        if a[0] == "ГеройНевыгодное":
            flag = True
        elif flag:
            i = 0
            hero = ""
            while not '0' <= tag.text[i] <= '9':
                hero += tag.text[i]
                i += 1
            ans.append(hero)
            cnt -= 1
    str_ans = "Контрпики " + hero_name + ":\n"
    for hero in ans:
        str_ans += hero
        str_ans += '\n'
    return str_ans

async def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        if msg['text'] != '/start':
            text = msg['text']
            text = text.strip()
            print(text)
            ans = await find_heroes(text)
            await bot.sendMessage(chat_id, ans)
        else:
            text = "Привет! Напиши название героя (на английском!), и узнай его контрпики)"
            await bot.sendMessage(chat_id, text)


bot = telepot.aio.Bot(bot_token)
loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot, handle).run_forever())

loop.run_forever()
