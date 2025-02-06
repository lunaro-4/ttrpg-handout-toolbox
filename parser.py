import requests
from spell_data_handler import Spell
import ast
from bs4 import BeautifulSoup


DNDSU_URL = "https://dnd.su"

class ParsingBoss:
    def __init__(self) -> None:
        self.names_to_descriptions: dict[str, str] = {}
        self.names_to_files: dict[str, str] = {}
        self.names_to_urls: dict[str, str] = {}
        self.spells: list[Spell] = []

    def __get_soup_from_url(self, url: str) -> BeautifulSoup:
        return BeautifulSoup(requests.get(url).text, features="html.parser")

    def __get_soup_from_file(self, file_path: str) -> BeautifulSoup:
        with open(file_path, "r") as file:
            text = file.read()
        return BeautifulSoup(text, features="html.parser")
        
    def __distill_name_to_object(self,name_to_file: dict[str, str]) -> tuple[str, str]:
            name_to_file_values = name_to_file.items()
            return (list(name_to_file_values)[0][0], list(name_to_file_values)[0][1])
    def save_spells(self, spell: Spell | None = None):
        spells_to_save: list[Spell] = []
        if spell:
            spells_to_save.append(spell)
        else:
            spells_to_save = self.spells

        for spell in self.spells:
            spell.save_to_json("spell-data"+"/"+spell.get_name())

class DndSuParser(ParsingBoss):
    DNDSU_URL = "https://dnd.su"

    def __init__(self) -> None:
        self.spells_raw: list[dict]

    def __get_spell_list_from_html(self, raw_html: str) -> list[dict]:
        soup = BeautifulSoup(raw_html, features="html.parser")
        spells_raw_encoded: str = soup.find_all(name="script")[-3].text
        spells_raw = spells_raw_encoded.replace('\\/', '/').encode().decode("unicode-escape")
        spells_raw_refined = spells_raw[spells_raw.find('{'):-1]
        spells_dict = ast.literal_eval(spells_raw_refined)
        return spells_dict['cards']
        
    def populate_spells_list_from_file(self, file_path: str) -> None:
        with open(file_path, "r") as file:
            spells_html: str = file.read()
        self.spells_raw = self.__get_spell_list_from_html(spells_html)

    def populate_spells_list_from_site(self, url: str = DNDSU_URL+"/spells") -> None:
        spells_html = requests.get(url).text
        self.spells_raw = self.__get_spell_list_from_html(spells_html)

    def update_files(self, directory: str) -> None:
        for spell in self.spells_raw:
            file_name=directory+spell['title'].replace('/', '_')
            with open(file_name, "w") as file:
                file.write(requests.get(DNDSU_URL+'/'+spell['link']).text)


    def populate_descriptions_from_files(self) -> None:
        self.names_to_descriptions = self.get_descriptions(self.names_to_descriptions, is_local_file=True)



    def __get_description_from_soup(self, soup: BeautifulSoup) -> str:
        subsec= soup.find(name="div", itemprop="description")
        if subsec:
            return subsec.text
        return ""

    def get_descriptions(self,*names_to_object: dict[str,str], is_local_file: bool) -> dict[str, str]:
        spell_to_desc: dict[str, str] = {}
        for name_to_object in names_to_object:
            name, object = self.__distill_name_to_object(name_to_object)
            if is_local_file:
                soup = self.__get_soup_from_file(object)
            else:
                soup = self.__get_soup_from_url(object)
            subsec = self.__get_description_from_soup(soup)
            spell_to_desc[name] = subsec
        return spell_to_desc


    def conventialize_spell(self,spell_info: dict) -> Spell:
        components_raw: str = spell_info['filter_components']
        has_verbal: bool = int(components_raw[0]) == 1
        has_somatic: bool = int(components_raw[2]) == 1
        has_material: bool = int(components_raw[4]) == 1
        spell_name: str = spell_info['title']
        components_to_bool: dict[str, bool] = {
                "verbal": has_verbal,
                "somatic": has_somatic,
                "material": has_material
                }
        new_spell_dict: dict = {
                "name_ru": spell_name,
                "name": spell_info['title_en'],
                "components": components_to_bool,
                "material_component": spell_info['material_component'],
                "casting_time": spell_info['filter_casttime'][0],
                "description": self.names_to_descriptions[spell_name],
                }

        return Spell(**new_spell_dict)

        
    def translate_spells(self):
        for spell in self.spells_raw:
            self.spells.append(self.conventialize_spell(spell))




if __name__ == "__main__":
    with open("spells.html", "r") as file:
        spells_list = get_spell_list_from_html(file.read())
    # for spell in spells_list:
    #     with open("spells_raw_html/"+ spell['title'].replace('/', '_') + ".html", "w") as file:
    #         file.write(parse_spell(spell['link']))

    print(get_description_from_files({"hellish_rebuke":"spells_raw_html/Адское возмездие.html"}))
    




