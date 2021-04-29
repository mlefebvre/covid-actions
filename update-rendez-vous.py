import requests
from bs4 import Tag, NavigableString, BeautifulSoup
from requests.auth import HTTPBasicAuth


def get_text(tag) -> str:
    _inline_elements = {"a", "span", "em", "strong", "u", "i", "font", "mark", "label", "s", "sub", "sup", "tt", "bdo",
                        "button", "cite", "del", "b", "a", "font"}

    def _get_text(tag):

        for child in tag.children:
            if type(child) is Tag:
                is_block_element = child.name not in _inline_elements
                if is_block_element: yield "\n"
                yield from ["\n"] if child.name == "br" else _get_text(child)
                if is_block_element: yield "\n"
            elif type(child) is NavigableString:
                yield child.string

    return "".join(_get_text(tag)).replace("\n\n", "\n").replace("\n\n", "\n").strip()


def main():
    j = requests.get("https://api3.clicsante.ca/v3/establishments/60096/texts",
                     auth=HTTPBasicAuth('public@trimoz.com', '12345678!'),
                     headers={
                         "X-Trimoz-Role": "public",
                         "Product": "clicsante"}).json()

    text = get_text(BeautifulSoup(j[0]["popupText"], features="html.parser"))
    with open("texte-rendez-vous.txt", "w") as f:
        f.write(text)


if __name__ == "__main__":
    main()
