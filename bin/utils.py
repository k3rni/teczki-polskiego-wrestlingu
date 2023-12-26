import tomllib
from json import JSONEncoder
from collections import Counter
import yaml
from io import StringIO

def extract_front_matter(text):
    matter = []
    lines = iter(text.split("\n"))
    while True:
        line = next(lines)
        if line == "+++": break

    while True:
        line = next(lines)
        if line == "+++": break
        matter.append(line)

    return "\n".join(matter)

def parse_front_matter(text):
    return tomllib.loads(extract_front_matter(text))

class RichEncoder(JSONEncoder):
    def default(self, obj):
        match obj:
            case set():
                return list(obj)
            case Counter():
                return dict(obj)
            case _:
                return super().default(obj)


def extract_card_block(text):
    card = []
    lines = iter(text.split("\n"))
    for line in lines:
        if line == "{% card() %}": break
    else:
        # Start code not found
        return None

    for line in lines:
        if line == "{% end %}": break
        card.append(line)
    else:
        # End block code not found
        return None

    return "\n".join(card)

def parse_card_block(card):
    text = extract_card_block(card)
    data = yaml.safe_load(StringIO(text))
    return data
