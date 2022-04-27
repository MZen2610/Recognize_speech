from dotenv import load_dotenv

import json
import os


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    from google.cloud import dialogflow

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[
            message]
    )

    intents_client.create_intent(
        request={'parent': parent, 'intent': intent}
    )


def main():
    load_dotenv()

    project_id = os.environ['PROJECT_ID']

    with open('questions.json', 'r', encoding='utf-8') as file:
        topics = json.load(file)

    for topic, item in topics.items():
        create_intent(project_id, topic, item['questions'], [(item['answer'])])


if __name__ == '__main__':
    main()
