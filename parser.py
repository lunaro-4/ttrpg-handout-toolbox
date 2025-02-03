import requests
import codecs
import json
import ast
from bs4 import BeautifulSoup


DNDSU_URL = "https://dnd.su"


def write_info(*spells_info):
    for spell in spells_info:
        pass

def get_html_file():
    r = requests.get(DNDSU_URL+ "/spells")
    with open("spells.html", "w") as file:
        file.write(r.text)

def parse_dnd_su():
    r = requests.get(DNDSU_URL)
    soup = BeautifulSoup(r.text, features="html.parser")
    print(soup.text)
    
def get_spell_list_from_html(raw_html: str) -> list:
    soup = BeautifulSoup(raw_html, features="html.parser")
    spells_raw_encoded: str = soup.find_all(name="script")[-3].text
    spells_raw = spells_raw_encoded.replace('\\/', '/').encode().decode("unicode-escape")
    spells_raw_refined = spells_raw[spells_raw.find('{'):-1]
    spells_dict = ast.literal_eval(spells_raw_refined)
    return spells_dict['cards']


if __name__ == "__main__":
    # parse_dnd_su()
    # get_html_file()
    with open("spells.html", "r") as file:
        print(get_spell_list_from_html(file.read()))



