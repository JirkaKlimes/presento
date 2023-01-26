# this needs to get replaced by official api (doesn't exist yet)

from pyChatGPT import ChatGPT as unofficialChatGPT
import json


class ChatGPT:
    def __init__(self, session_token, debug=False):
        self.debug = debug
        self.api = unofficialChatGPT(session_token)

        self.conversation = []

    def send_message(self, msg):
        resp = self.api.send_message(msg)

        dialogue = {"request": msg, "response": resp['message']}
        self.conversation.append(dialogue)

        if self.debug:
            with open("./debug/conversation.json", "w", encoding="utf-8") as f:
                json.dump(self.conversation, f, ensure_ascii=False, sort_keys=False, indent=4)

        return resp['message']

    def reset_conversation(self):
        self.api.reset_conv()
        self.conversation = []
