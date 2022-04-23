from telegram import Update, ForceReply, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
# from google.cloud import dialogflow
from tg_log_handler import TelegramLogsHandler
from handle_intent import detect_intent_texts

import os
import logging

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


# def detect_intent_text(project_id, session_id, text, language_code):
#     session_client = dialogflow.SessionsClient()
#     session = session_client.session_path(project_id, session_id)
#
#     text_input = dialogflow.TextInput(text=text, language_code=language_code)
#
#     query_input = dialogflow.QueryInput(text=text_input)
#
#     response = session_client.detect_intent(
#         request={"session": session, "query_input": query_input}
#     )
#     return response


def forward_message(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    intent_text = detect_intent_texts(
        project_id=context.bot_data['project_id'],
        session_id=update.message.chat_id,
        text=update.message.text,
        language_code='ru-RU'
    )
    print(intent_text.query_result.fulfillment_text)
    update.message.reply_text(intent_text.query_result.fulfillment_text)


def main() -> None:
    load_dotenv()

    tgm_token = os.environ["TGM_TOKEN"]
    session_id = os.environ["SESSION_ID"]
    project_id = os.environ["PROJECT_ID"]

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(Bot(token=tgm_token), session_id))
    logger.info('TG bot running...')

    updater = Updater(tgm_token)

    dispatcher = updater.dispatcher
    dispatcher.bot_data = {'project_id': project_id}
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_message))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
