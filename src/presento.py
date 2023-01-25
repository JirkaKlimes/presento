import json
from src.gpt_parser import GPTPresentationParser
from src.presentation_generator import PPTXGenerator

class Presento:
    """
    Class for generating original presentation automatically using ChatGPT
    """
    
    def __init__(self, gpt_api, debug = False) -> None:
        self.debug = debug
        self._load_query_data()

        # gpt api must have methond "send_message" and "reset_conversation" 
        self.gpt_api = gpt_api

        self.parser = GPTPresentationParser()
        self.pptx_generator = PPTXGenerator()

    def _load_query_data(self) -> None:
        # loads empty gpt query body
        with open("./data/gpt_query.json") as f:
            self._gpt_query = json.load(f)

    def _create_gpt_query(self, request: dict) -> str:
        # formats presentation request into ChatGPT compatible messsage

        new_query = self._gpt_query["query"]
        new_query = new_query.replace("_TOPIC_", request["topic"])
        new_query = new_query.replace("_SLIDE_COUNT_", str(request["slide_count"]))
        new_query = new_query.replace("_LANGUAGE_", request["language"])

        optional = []

        if request["omit_contents_slide"]:
            optional.append(self._gpt_query["optional"]["omit_contents_slide"])

        if request["description"]:
            optional.append(request["description"])

        new_query = new_query.replace("_OPTIONAL_", "\n".join(optional))

        return new_query
    
    def _repr_request(self, request) -> str:
        # returns request summary as string 
        text = ""

        text += "Presento will generate presentation:\n"
        text += f"\tTopic: {request['topic']}\n"
        text += f"\tSlides: {request['slide_count']}\n"
        text += f"\tLanguage: {request['language']}\n"
        text += f"\tContents slide: {'omitted' if request['omit_contents_slide'] else 'included'}\n"
        text += f"\tDescription: {request['description']}"

        return text

    def _get_gpt_response(self, query: str) -> str:
        generated = ""

        response = self.gpt_api.send_message(query)
        generated += response

        while 'complete' not in generated[-15:].lower():
            response = self.gpt_api.send_message(self._gpt_query['redo'])
            generated += "\n" + response

        return generated


    def generate(self, topic: str, slide_count: int, language: str, omit_contents_slide: bool, description: str) -> None:
        """
        Takes topic, slide count, etc. sens request to ChatGPT, parses it's output and creates simple presentations in .pptx format
        """
        request = {"topic": topic,
                    "slide_count": slide_count,
                    "language": language,
                    "omit_contents_slide": omit_contents_slide,
                    "description": description}

        print(self._repr_request(request))
        print()

        query = self._create_gpt_query(request)

        # print("GPT Query:\n")
        # print("="*20)
        # print(query)
        # print("="*20)
        # print()

        print("Sending request to ChatGPT...")
        generated_text = self._get_gpt_response(query)

        if self.debug:
            with open("./debug/generated_text.txt", "w", encoding='utf-8') as f:
                f.write(generated_text)

        print("Got response from ChatGPT.")        
        print(f"Generated text length: {len(generated_text)}")
        print("Parsing presentation.")        
        parsed = self.parser(generated_text)

        if self.debug:
            with open("./debug/parsed_presentation.json", "w", encoding='utf-8') as f:
                json.dump(parsed, f, ensure_ascii=False, sort_keys=False, indent=4)


        print("Creating simple .pptx file")
        self.pptx_generator.generate(parsed, request['topic'])
        print("Your presentation is ready.")


    
