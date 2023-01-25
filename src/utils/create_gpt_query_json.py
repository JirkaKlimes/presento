import json


query = \
"""Give me information for creating presentation on topic "_TOPIC_" with _SLIDE_COUNT_ slides.
Write the presentation in _LANGUAGE_.
_OPTIONAL_
Output every slide in one of theses formats:

Slide number: 1
Layout: Title Slide
Heading: x
Subheading: x / null
Images: x / null

Slide number: 2
Layout: Title and Content
Heading: x
Images: x / null
Points: ...

After you are done, write the keyword "complete"."""

optional = {
    "omit_contents_slide": "Omit contents / overview slide."
}

redo = "redo current slide and continue"


gpt_query_json = {
    "query": query,
    "optional": optional,
    "redo": redo
    }

with open("gpt_query.json", "w", encoding="utf-8") as f:
    json.dump(gpt_query_json, f, ensure_ascii=False, sort_keys=False, indent=4)