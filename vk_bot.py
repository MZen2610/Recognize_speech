from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv

import vk_api
import os

load_dotenv()

vk_token = os.environ["VK_TOKEN"]

vk_session = vk_api.VkApi(token=vk_token)
vk_bot = vk_session.get_api()

longpoll = VkLongPoll(vk_session)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        print('Новое сообщение:')
        if event.to_me:
            print('Для меня от: ', event.user_id)
        else:
            print('От меня для: ', event.user_id)
        print('Текст:', event.text)
