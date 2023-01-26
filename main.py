from src.presento import Presento
from src.chat_gpt import ChatGPT
import secrete

DEBUG = True

gpt_api = ChatGPT(secrete.GPT_SESSION_TOKEN, debug = DEBUG)
presento = Presento(gpt_api, debug = DEBUG)

topic = input("Presentation topic: ")
description = input("Description (can be empty): ")
slide_count = int(input("Enter slide count: "))
language = input("Enter wanted language: ")
omit_contents_slide = input("Should table of contents be omitted? (Y/N): ").lower() == "y"

# topic = ''
# description = ''
# slide_count = 8
# language = 'Czech'
# omit_contents_slide = True

presento.generate(topic, slide_count, language, omit_contents_slide, description)
