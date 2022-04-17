from vk_api.longpoll import VkLongPoll, VkEventType

import vk_api

vk_session = vk_api.VkApi(token="eb1786499fe3a3d7da94c811ad29e8a6925708c5003cd43c1d75a30189f1a54fa1addb5d0b8c21d735706")
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
