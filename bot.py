import dialogflow
import string
import random


def generate_random_string():
    string_len = random.randint(1, 10)
    string_list = [random.choice(string.ascii_lowercase) for i in range(0, string_len)]
    random_session_id = ''.join(string_list)
    return random_session_id


class DialogflowBot:
    def __init__(self, a_project_id, a_session_id=None, language="EN-US"):
        self.session_id = generate_random_string() if a_session_id is None else a_session_id
        self.project_id = a_project_id
        self.language_code = language

    def chat_response(self, text):
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(self.project_id, self.session_id)
        text_input = dialogflow.types.TextInput(text=text, language_code=self.language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(session=session, query_input=query_input)
        response_text = response.query_result.fulfillment_text
        return response_text