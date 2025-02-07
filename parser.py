import re
import sys
from typing import Any
from html2image.html2image import os
import requests
from abc import ABC, abstractmethod
from spell_data_handler import Spell
import ast
from bs4 import BeautifulSoup


DNDSU_URL = "https://dnd.su"

class ParsingBoss(ABC):
    """ This is a ParsingBoss class, responseble for parsing spells from files and sites
    and saving them.
    To start you need to create the instance of a class and run 'populate_spells_list_from_*' function.
    Then 
    """
    def __init__(self) -> None:
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

    def get_spells(self) -> list[Spell]:
        return self.spells
    def save_spells(self, spell: Spell | None = None):
        spells_to_save: list[Spell] = []
        if spell:
            spells_to_save.append(spell)
        else:
            spells_to_save = self.spells

        for spell in self.spells:
            spell.save_to_json("spell-data"+"/"+spell.get_name())

    @abstractmethod
    def process_spells(self) -> None:
        pass

class DndSuParser(ParsingBoss):
    DNDSU_URL = "https://dnd.su"
    class StaticTranslations:
        ON_TOUCH = "касание".casefold()
        ON_SELF = "На себя".casefold()
        ON_SPECIAL = "особая".casefold()
        CONCENTRATION = "концентрация".casefold()
        INSTANT= "мгновенная".casefold()
        MINUTES = "мин".casefold()
        HOURS = "час".casefold()
        SECONDS = "сек".casefold()

    class ParsedRawSpell:
        def __init__(self) -> None:
            self.__raw_dict: dict= {
                    "description": "",
                    "material_component": "",
                    "distance": -1,
                    "duration": -1,
                    "has_concentration": False
                    }
        def __getitem__(self, name: str, /) -> Any:
            return self.__raw_dict[name]

        def __setitem__(self, name: str, value: Any, /) -> None:
            if name not in self.__raw_dict.keys():
                raise Exception
            if type(value) is not type(self.__raw_dict[name]):
                raise Exception
            self.__raw_dict[name] = value

    def __init__(self) -> None:
        super().__init__()
        self.spells_raw: list[dict]
        self.names_to_values: dict[str, DndSuParser.ParsedRawSpell] = {}
        self.names_to_soups: dict[str, BeautifulSoup]

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

    def populate_spells_list_from_url(self, url: str = DNDSU_URL+"/spells") -> None:
        spells_html = requests.get(url).text
        self.spells_raw = self.__get_spell_list_from_html(spells_html)

    def __get_spell_name(self, spell: dict) -> str:
        return spell['title'].replace('/', '_')

    def __get_spell_file_name(self, spell_name: str, save_directory: str) -> str:
        return save_directory+'/'+spell_name +'.html'


    def update_links(self) -> None:
        if not self.spells_raw: 
            print("ERROR: spell list is empty! Run 'populate_spells_list_from_*' first!", file=sys.stderr)
            exit()
        for spell in self.spells_raw:
            spell_name = self.__get_spell_name(spell)
            self.names_to_urls[spell_name] = DNDSU_URL+'/'+spell['link']

    def update_files(self, directory: str) -> None:
        if not self.names_to_urls: 
            print("ERROR: links dictionaty is not populated! Run 'update_links' first!", file=sys.stderr)
            exit()
        for spell in self.spells_raw:
            spell_name = self.__get_spell_name(spell)
            file_name= self.__get_spell_file_name(spell_name, directory)
            with open(file_name, "w") as file:
                file.write(requests.get(self.names_to_urls[spell_name]).text)
            self.names_to_files[spell_name] = file_name

    def update_name_to_file(self, spell_name: str, spell_file_name: str) -> None:
        self.names_to_files[spell_name] = spell_file_name

    def link_names_to_files(self, files_directory: str) -> None:
        for spell in self.spells_raw:
            spell_name: str = self.__get_spell_name(spell)
            file_name = self.__get_spell_file_name(spell_name, files_directory)
            if not os.path.isfile(file_name):
                print(f"ERROR: file {file_name} not found!", file=sys.stderr) 
                exit()
            self.names_to_files[spell_name] = file_name

    def populate_soups_from_files(self) -> None:
        names_to_soups: dict[str, BeautifulSoup] = {}
        for spell, file in self.names_to_files.items():
            names_to_soups[spell] = self._ParsingBoss__get_soup_from_file(file)
        self.names_to_soups = names_to_soups

    def __clean_distance(self, raw_distance: str) -> int:
        raw_distance = raw_distance.casefold().strip()
        st = DndSuParser.StaticTranslations()
        if raw_distance.find(st.ON_SELF) != -1:
            return 0
        if raw_distance.find(st.ON_TOUCH) != -1:
            return 5
        processed_distance: str =re.sub(r'\D', "" ,raw_distance) 
        if processed_distance.isnumeric():
            return int(processed_distance)
        return -1

            

    def __get_description_from_soup(self, soup: BeautifulSoup) -> str:
        subsec= soup.find(name="div", itemprop="description")
        if subsec:
            return subsec.text
        return ""

    def __get_material_component_from_soup(self, soup: BeautifulSoup) -> str:
        lists = soup.find_all(name="li")
        for li in lists:
            if li.children:
                for i, child in enumerate(li.children):
                    if i == 0 and child.text == "Компоненты:":
                        continue
                    elif i == 1:
                        return child.text[child.text.find('(')+1:child.text.find(')')]
                    break
        return ""

    def __get_distance_from_soup(self, soup: BeautifulSoup) -> int:
        lists = soup.find_all(name="li")
        for li in lists:
            if li.children:
                for i, child in enumerate(li.children):
                    if i == 0 and child.text == "Дистанция:":
                        continue
                    elif i == 1:
                        return self.__clean_distance(child.text)
                    break
        return 0

    def __get_duration_and_concentration_from_soup(self, soup: BeautifulSoup) -> tuple[int, bool]:
        """ Returns values in format: 'duration_value, value_name, requires_concentration' """
        lists = soup.find_all(name="li")
        raw_duration: str = ""
        for li in lists:
            if li.children:
                for i, child in enumerate(li.children):
                    if i == 0 and child.text == "Длительность:":
                        continue
                    elif i == 1:
                        raw_duration = child.text
                    break
        if not raw_duration:
            return (-1, False)

        st = DndSuParser.StaticTranslations()
        raw_duration = raw_duration.casefold()
        
        has_concentration: bool = False
        if raw_duration.find(st.CONCENTRATION) != -1:
            has_concentration = True

        raw_duration =  re.sub(r'.+? \d', "", raw_duration)
        duration_value_name: str = 'unknown'
        duration_multiplier: int = 1

        if raw_duration.find(st.HOURS) != -1:
            duration_value_name = 'h'
            duration_multiplier = 3600
        elif raw_duration.find(st.MINUTES) != -1:
            duration_value_name = "m"
            duration_multiplier = 60
        elif raw_duration.find(st.SECONDS) != -1:
            duration_value_name = "s"
        elif raw_duration.find(st.INSTANT) != -1:
            return (0, has_concentration)

        duration_value: str = re.sub(r'\D', "" , raw_duration)
        if duration_value.isnumeric():
            return (int(duration_value)*duration_multiplier, has_concentration)
        return(-1, has_concentration)


        






    def __get_data_from_soups(self) -> None:
        if not self.names_to_soups: 
            print("ERROR: soups dictionaty is not populated! Run 'update_links' first!", file=sys.stderr)
            exit()
        print("Getting data from soups")
        for name, soup in self.names_to_soups.items():
            prs = DndSuParser.ParsedRawSpell()
            desc = self.__get_description_from_soup(soup)
            mater_component = self.__get_material_component_from_soup(soup)
            distance = self.__get_distance_from_soup(soup)
            (duration, has_concentration) = self.__get_duration_and_concentration_from_soup(soup)
            prs['description'] = desc
            prs['material_component'] = mater_component
            prs['distance'] = distance
            prs['duration'] = duration
            prs['has_concentration'] = has_concentration
            self.names_to_values[name] = prs


    def conventialize_spell(self,spell_info: dict) -> Spell:
        spell_name: str = self.__get_spell_name(spell_info)
        components_raw: str = spell_info['filter_components']
        has_verbal: bool = int(components_raw[0]) == 1
        has_somatic: bool = int(components_raw[2]) == 1
        has_material: bool = int(components_raw[4]) == 1
        prs = self.names_to_values[spell_name]

        components_to_bool: dict[str, bool] = {
                "verbal": has_verbal,
                "somatic": has_somatic,
                "material": has_material
                }
        new_spell_dict: dict = {
                "name_ru": spell_name,
                "name": spell_info['title_en'],
                "components": components_to_bool,
                "material_component": prs['material_component'],
                "casting_time": spell_info['filter_casttime'][0],
                "description": prs['description'],
                "distance":prs['distance'],
                "duration":prs['duration'],
                "level":1,
                "is_ritual":False,
                "requires_concentration":prs['has_concentration']
                }

        return Spell(**new_spell_dict)

        
    def translate_spells(self):
        for spell in self.spells_raw:
            self.spells.append(self.conventialize_spell(spell))

    def process_spells(self) -> None:
        self.__get_data_from_soups()
        self.translate_spells()
        
        pass




if __name__ == "__main__":
    dsp = DndSuParser()
    # dsp.update_files("spells_raw_html")
    dsp.populate_spells_list_from_file('spells.html')
    dsp.link_names_to_files("spells_raw_html")
    dsp.populate_soups_from_files()
    # print(dsp.spells_raw[0])
    dsp.process_spells()
    print(dsp.spells[0])
    # dsp.process_spells()
    # print(dsp.get_spells()[0])

    
    pass




