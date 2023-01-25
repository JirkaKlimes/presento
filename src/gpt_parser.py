import re


class GPTPresentationParser:

    SLIDE_SPLIT_PATTERN = "Slide number: "
    SLIDE_LAYOUT_TITLE = "Title Slide"
    SLIDE_LAYOUT_TITLE_AND_CONTENT = "Title and Content"
    FINISH_PATERN = "complete"

    def __call__(self, text) -> dict:
        return self.parse(text)

    def _split_slides(self, text) -> list:
        # removes the keyword "complete" on the end
        text = text[:text.lower().rfind(self.FINISH_PATERN)]

        # splits slides into list
        chunks = text.split(self.SLIDE_SPLIT_PATTERN)[1:]

        slides = []

        pattern = re.compile(r"^(\d+)")

        # removed not finished slides and duplicates and removes whitespace
        for ch in chunks:
            ch = ch.strip()
            slide_number = int(pattern.findall(ch)[0])
            if slide_number <= len(slides):
                slides[slide_number-1] = ch
            else:
                slides.append(ch)

        return slides

    def _parse_slide(self, text) -> dict:

        layout = re.compile(r"Layout: (.+)").findall(text)[0]

        heading = re.compile(r"Heading: (.+)").findall(text)[0]

        subheading = re.compile(r"Subheading: (.+)").findall(text)

        if subheading:
            if 'null' in subheading[0]:
                subheading = None
            else:
                subheading = subheading[0]
        else:
            subheading = None

        images = re.compile(r"Images: (.+)").findall(text)[0]
        images = [] if 'null' in images else images.split(', ')

        if layout == self.SLIDE_LAYOUT_TITLE_AND_CONTENT:
            points = text.split('Points:')[1].strip().split("\n")
            points = list(filter(lambda x: "..." not in x, points))
            points = list(map(lambda x: x.replace("* ", ""), points))
        else:
            points = None

        slide = {"layout": layout,
                 "heading": heading,
                 "subheading": subheading,
                 "images": images,
                 "points": points, }

        return slide

    def parse(self, text) -> list:
        slides = self._split_slides(text)

        slides = [self._parse_slide(slide) for slide in slides]

        return slides


if __name__ == "__main__":
    import json

    parser = GPTPresentationParser()

    with open('./debug/generated_text.txt', encoding='utf-8') as f:
        text = f.read()
        parsed = parser(text)
        with open("./debug/parsed_presentation.json", "w", encoding='utf-8') as f:
            json.dump(parsed, f, sort_keys=False, ensure_ascii=False, indent=4)
