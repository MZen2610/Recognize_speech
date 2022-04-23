from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from dotenv import load_dotenv
from handle_intent import detect_intent_texts

import os
import vk_api as vk


def process_vk_message(event, vk_bot, project_id):
    answer = detect_intent_texts(
        project_id=project_id,
        session_id=event.user_id,
        text=event.text,
        language_code='ru-RU'
    )
    if not answer.query_result.intent.is_fallback:
        vk_bot.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message=answer.query_result.fulfillment_text
        )


def main():
    load_dotenv()
    vk_token = os.environ["VK_TOKEN"]
    project_id = os.environ["PROJECT_ID"]

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            process_vk_message(event, vk_api, project_id)


if __name__ == "__main__":
    main()
