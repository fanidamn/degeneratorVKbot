# -*- coding: utf-8 -*-
# degenerator vk spammer project
import vk_api, vk, random
from vk_api.keyboard        import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll    import VkBotLongPoll, VkBotEventType
from vk_api.longpoll        import VkLongPoll, VkEventType
from vk_api.utils           import get_random_id

vk_session = vk_api.VkApi(token='ea14ac9d61295a047204c4e1146c7e1bfbcbd762dd62587a78da880ecef0e505ed29e1b34f8c2a727e837')
vk = vk_session.get_api()

longpoll = VkBotLongPoll(vk_session, 208985944)

count = 0

def send(message: str, chat_id: str):
    vk.messages.send(
        random_id = get_random_id(),
        message = message,
        chat_id = chat_id
    )

def get_wib():
    wib_count = 0
    with open("slova.txt", "r") as w:
            foo = w.read()
            for x in foo.split():
                wib_count += 1
            w.close()
    return wib_count + 1

def word_method(word: list, method: str, chat_id: str):
    _words_cache = []
    _word_returns = ""
    wib = get_wib()
    if method == "add_word":
        with open("slova.txt", "a+") as w:
            for n in word:
                try:
                    w.write(f" {n}")
                except Exception:
                    return
            w.flush(); w.close()
        return print(word, "was added in database, current count of words:", wib)
    if method == "random_word":
        if wib > 75:
            with open("slova.txt", "r") as w:
                f = w.read()
                for k in f.split():
                    _words_cache.append(k)
                r = random.randint(1, 5)
                g = random.randint(1, wib - 1)
                for i in range(r):
                    g = g + 1
                    _word_returns = str(_word_returns) + str(_words_cache[g]) + " "
                w.close()
        else:
            send(f"count of words in database can't be < 75\ncurrent words in base: {wib}", chat_id)
        return _word_returns

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if get_wib() > 75:
            count += 1
        u_id = event.object['message']['from_id']
        u_text = event.object['message']['text']
        u_peer_id = event.object['message']['peer_id']
        u_chat_id = event.chat_id
        if (u_text != (None or "")) and (not ("https" or "http" or ".com" or ".ru") in u_text):
            if ("база" or "base") in u_text:
                send(f"в базе {get_wib()} words)", u_chat_id)
            else:
                word_method(u_text.split(), "add_word", u_chat_id)
        if count > 0:
            count = 0
            _word = word_method("", "random_word", u_chat_id)
            send(_word.lower(), u_chat_id)