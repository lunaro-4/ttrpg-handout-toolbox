import re
import sys
from icecream import ic
from typing import Any
from html2image.html2image import os
import requests
from abc import ABC, abstractmethod
from TTRPG_CTB import Spell
import ast
from bs4 import BeautifulSoup
from global_constants import CLASS_SUBCLASS_MAP


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
    def save_spells(self, directory: str,  spell: Spell | None = None) -> str | None:
        if spell:
            save_path = directory+"/"+spell.get_file_name()
            spell.save_to_json(save_path)
            return save_path
        else:
            for spell in self.spells:
                spell.save_to_json(directory+"/"+spell.get_file_name()+ '.json')

    def render_spell(self,spell_info: dict) -> Spell:
        """ Place to do convertions, in case 'Spell' vaules will change """
        spell_data = spell_info
        return Spell(**spell_data)

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
        DAYS_1 = "ден".casefold()
        DAYS_2 = "дне".casefold()
        DAYS_3 = "дня".casefold()
        WEEK = "недел".casefold()
        ACTION = "действ".casefold()
        BONUS_ACTION = "бонусн".casefold()
        REACTION = "реакц".casefold()

    CLASS_ARCHETYPE_CODE_TRANSLATION: dict = {
            23: CLASS_SUBCLASS_MAP.artificer_class_name,
            22: CLASS_SUBCLASS_MAP.druid_class_name,
            21: CLASS_SUBCLASS_MAP.wizard_class_name,
            20: CLASS_SUBCLASS_MAP.warlock_class_name,
            19: CLASS_SUBCLASS_MAP.sorcerer_class_name,
            18: 'Unknown',
            17: CLASS_SUBCLASS_MAP.ranger_class_name,
            16: CLASS_SUBCLASS_MAP.paladin_class_name,
            15: 'Unknown',
            13: CLASS_SUBCLASS_MAP.cleric_class_name,
            12: CLASS_SUBCLASS_MAP.bard_class_name,
            11: 'Unknown',


            '291': CLASS_SUBCLASS_MAP.barbarian_archetype_names['path_of_the_giant'],

            '286': CLASS_SUBCLASS_MAP.sorcerer_archetype_names['lunar_sorcery'],
            '215': CLASS_SUBCLASS_MAP.sorcerer_archetype_names['clockwork_soul'],
            '214': CLASS_SUBCLASS_MAP.sorcerer_archetype_names['abbrant_mind'],
            '212': CLASS_SUBCLASS_MAP.sorcerer_archetype_names['shadow_magic'],
            '211': CLASS_SUBCLASS_MAP.sorcerer_archetype_names['divine_soul'],

            '208': CLASS_SUBCLASS_MAP.ranger_archetype_names['drakewarden'],
            '207': CLASS_SUBCLASS_MAP.ranger_archetype_names['swarmkeeper'],
            '206': CLASS_SUBCLASS_MAP.ranger_archetype_names['fey_wanderer'],
            '205': CLASS_SUBCLASS_MAP.ranger_archetype_names['monster_slayer'],
            '204': CLASS_SUBCLASS_MAP.ranger_archetype_names['gloom_stalker'],
            '203': CLASS_SUBCLASS_MAP.ranger_archetype_names['horrizon_walker'],

            '194': CLASS_SUBCLASS_MAP.rogue_archetype_names['arcane_trickster'],
            '191': CLASS_SUBCLASS_MAP.paladin_archetype_names['oath_of_the_watchers'],
            '190': CLASS_SUBCLASS_MAP.paladin_archetype_names['oath_of_glory'],
            '189': CLASS_SUBCLASS_MAP.paladin_archetype_names['oath_of_conquest'],
            '188': CLASS_SUBCLASS_MAP.paladin_archetype_names['oath_of_redemption'],
            '187': CLASS_SUBCLASS_MAP.paladin_archetype_names['oath_of_the_crown'],
            '186': CLASS_SUBCLASS_MAP.paladin_archetype_names['oathbreaker'],
            '185': CLASS_SUBCLASS_MAP.paladin_archetype_names['oath_of_vengeance'],
            '184': CLASS_SUBCLASS_MAP.paladin_archetype_names['oath_of_the_ancients'],
            '183': CLASS_SUBCLASS_MAP.paladin_archetype_names['oath_of_devotion'],

            '179': CLASS_SUBCLASS_MAP.monk_archetype_names['way_of_sun_soul'],

            '175': CLASS_SUBCLASS_MAP.monk_archetype_names['way_of_four_elements'],
            '174': CLASS_SUBCLASS_MAP.monk_archetype_names['way_of_shadow'],

            '172': CLASS_SUBCLASS_MAP.warlock_archetype_names['undead'],
            '171': CLASS_SUBCLASS_MAP.warlock_archetype_names['genie'],
            '170': CLASS_SUBCLASS_MAP.warlock_archetype_names['fathomless'],
            '169': CLASS_SUBCLASS_MAP.warlock_archetype_names['celestial'],
            '168': CLASS_SUBCLASS_MAP.warlock_archetype_names['hexblade'],
            '167': CLASS_SUBCLASS_MAP.warlock_archetype_names['undying'],
            '166': CLASS_SUBCLASS_MAP.warlock_archetype_names['great_old_one'],
            '165': CLASS_SUBCLASS_MAP.warlock_archetype_names['fiend'],
            '164': CLASS_SUBCLASS_MAP.warlock_archetype_names['archfey'],
            '163': CLASS_SUBCLASS_MAP.artificer_archetype_names['armorer'],
            '162': CLASS_SUBCLASS_MAP.artificer_archetype_names['battle_smith'],
            '161': CLASS_SUBCLASS_MAP.artificer_archetype_names['artillerist'],
            '160': CLASS_SUBCLASS_MAP.artificer_archetype_names['alchemist'],
            '159': CLASS_SUBCLASS_MAP.cleric_archetype_names['twilight_domain'],
            '158': CLASS_SUBCLASS_MAP.cleric_archetype_names['order_domain'],
            '157': CLASS_SUBCLASS_MAP.cleric_archetype_names['peace_domain'],
            '156': CLASS_SUBCLASS_MAP.cleric_archetype_names['grave_domain'],
            '155': CLASS_SUBCLASS_MAP.cleric_archetype_names['forge_domain'],
            '154': CLASS_SUBCLASS_MAP.cleric_archetype_names['arcana_domain'],
            '153': CLASS_SUBCLASS_MAP.cleric_archetype_names['death_domain'],
            '152': CLASS_SUBCLASS_MAP.cleric_archetype_names['light_domain'],
            '151': CLASS_SUBCLASS_MAP.cleric_archetype_names['nature_domain'],
            '150': CLASS_SUBCLASS_MAP.cleric_archetype_names['trickery'],
            '149': CLASS_SUBCLASS_MAP.cleric_archetype_names['knowlege_domain'],
            '148': CLASS_SUBCLASS_MAP.cleric_archetype_names['life_domain'],
            '147': CLASS_SUBCLASS_MAP.cleric_archetype_names['war_domain'],
            '146': CLASS_SUBCLASS_MAP.cleric_archetype_names['tempest_domain'],
            '145': CLASS_SUBCLASS_MAP.druid_archetype_names['circle_of_spores'],
            '144': CLASS_SUBCLASS_MAP.druid_archetype_names['circle_of_stars'],
            '143': CLASS_SUBCLASS_MAP.druid_archetype_names['circle_of_wildfire'],

            '139': CLASS_SUBCLASS_MAP.druid_archetype_names['circle_of_the_land'],

            '136': CLASS_SUBCLASS_MAP.wizard_archetype_names['graviturgy'],
            '135': CLASS_SUBCLASS_MAP.wizard_archetype_names['chronurgy'],

            '124': CLASS_SUBCLASS_MAP.fighter_archetype_names['psi_warrior'],

            '121': CLASS_SUBCLASS_MAP.fighter_archetype_names['arcane_archer'],

            '107': CLASS_SUBCLASS_MAP.bard_archetype_names['college_of_spirits'],

            }


    class ParsedRawSpell:
        def __init__(self) -> None:
            self.__raw_dict: dict= {
                    "description": "",
                    "material_component": "",
                    "distance": -1,
                    "duration": -1,
                    "has_concentration": False,
                    "casting_time": -1
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

    def __parse_duaration_multiplyer(self, raw_duration: str) -> int:
        st = DndSuParser.StaticTranslations()
        if raw_duration.find(st.HOURS) != -1:
            return 3600
        elif raw_duration.find(st.MINUTES) != -1:
            return 60
        elif raw_duration.find(st.SECONDS) != -1:
            return 1
        elif raw_duration.find(st.INSTANT) != -1:
            return 0
        elif raw_duration.find(st.DAYS_1) + raw_duration.find(st.DAYS_2) + raw_duration.find(st.DAYS_3) != -3:
            return 3600*24
        elif raw_duration.find(st.WEEK) != -1:
            return 3600 * 24 * 7
        return -1

    def __clean_duration(self, raw_duration: str) -> int:
        raw_duration =  re.sub(r'(.+?)(\d+ )', r"\2", raw_duration)

        duration_multiplier: int = self.__parse_duaration_multiplyer(raw_duration)
        if duration_multiplier == -1:
            return -1

        duration_value: str = re.sub(r'\D', "" , raw_duration)
        if duration_value.isnumeric():
            return int(duration_value)*duration_multiplier
        return -1

    def __get_spell_list_from_html(self, raw_html: str) -> list[dict]:
        soup = BeautifulSoup(raw_html, features="html.parser")
        spells_raw_encoded: str = soup.find_all(name="script")[-3].text
        spells_raw = spells_raw_encoded.replace('\\/', '/').encode().decode("unicode-escape")
        spells_raw_refined = spells_raw[spells_raw.find('{'):-1]
        spells_dict = ast.literal_eval(spells_raw_refined)
        print(f'Found {len(spells_dict)} spells ')
        return spells_dict['cards']


        
    def populate_spells_list_from_file(self, file_path: str, restrict_length: int = 0) -> None:
        print('Parsing spell list from ', file_path)
        with open(file_path, "r") as file:
            spells_html: str = file.read()
        if restrict_length:
            self.spells_raw = self.__get_spell_list_from_html(spells_html)[:restrict_length]
        else:
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
            print(f'Linking {spell_name} to {file_name}')
            if not os.path.isfile(file_name):
                print(f"ERROR: file {file_name} not found!", file=sys.stderr) 
                exit()
            self.names_to_files[spell_name] = file_name

    def populate_soups_from_files(self) -> None:
        names_to_soups: dict[str, BeautifulSoup] = {}
        for spell, file in self.names_to_files.items():
            print(f'Getting soup for {spell}')
            names_to_soups[spell] = self._ParsingBoss__get_soup_from_file(file)
        self.names_to_soups = names_to_soups


    def __clean_distance(self, raw_distance: str) -> int:
        raw_distance = raw_distance.casefold().strip()
        st = DndSuParser.StaticTranslations()
        if raw_distance.find(st.ON_SELF) != -1:
            return 0
        if raw_distance.find(st.ON_TOUCH) != -1:
            return 5
        processed_distance: str = re.sub(r'\D', "" ,raw_distance) 
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
                        return child.text[child.text.find('(')+1:child.text.find(')')].strip()
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

        duration_value = self.__clean_duration(raw_duration)
        return(duration_value, has_concentration)



    def __get_casting_time_from_soup(self, soup: BeautifulSoup) -> int:
        lists = soup.find_all(name="li")
        raw_casting_time: str = ""
        for li in lists:
            if li.children:
                for i, child in enumerate(li.children):
                    if i == 0 and child.text == "Время накладывания:":
                        continue
                    elif i == 1:
                        raw_casting_time = child.text
                    break
        if not raw_casting_time:
            return -1

        st = DndSuParser.StaticTranslations()

        raw_casting_time =raw_casting_time.casefold()

        if raw_casting_time.find(st.BONUS_ACTION) != -1:
            return Spell.DURATION_CONSTATNS.BONUS_ACTION
        if raw_casting_time.find(st.ACTION) != -1:
            return Spell.DURATION_CONSTATNS.ACTION
        if raw_casting_time.find(st.REACTION) != -1:
            return Spell.DURATION_CONSTATNS.REACTION

        return self.__clean_duration(raw_casting_time)

    def __get_classes_from_query(self, classes_list: list[str | int]) -> list[str]:
        refined_classes: list[str] = []
        for class_id in classes_list:
            refined_classes.append(self.CLASS_ARCHETYPE_CODE_TRANSLATION[class_id])
        return refined_classes

    def __get_level_from_query(self, level: str) -> int:
        if level.casefold() == 'Заговор'.casefold():
            return 0
        return int(level)

    def __get_data_from_soups(self) -> None:
        if not self.names_to_soups: 
            print("ERROR: soups dictionaty is not populated! Run 'update_links' first!", file=sys.stderr)
            exit()
        print('==============================')
        print("Getting data from soups")
        print('==============================')
        for name, soup in self.names_to_soups.items():
            # print(f'Processing {name}, ', end='\t')
            print(f'Processing {name}')

            prs = DndSuParser.ParsedRawSpell()
            desc = self.__get_description_from_soup(soup)
            mater_component = self.__get_material_component_from_soup(soup)
            distance = self.__get_distance_from_soup(soup)
            (duration, has_concentration) = self.__get_duration_and_concentration_from_soup(soup)
            casting_time = self.__get_casting_time_from_soup(soup)
            prs['description'] = desc
            prs['material_component'] = mater_component
            prs['distance'] = distance
            prs['duration'] = duration
            prs['has_concentration'] = has_concentration
            prs['casting_time'] = casting_time
            self.names_to_values[name] = prs


    def __refactor_parsed(self, spell_info: dict) -> Spell:
        spell_name: str = self.__get_spell_name(spell_info)
        components_raw: str = spell_info['filter_components']
        has_verbal: bool = int(components_raw[0]) == 1
        has_somatic: bool = int(components_raw[2]) == 1
        has_material: bool = int(components_raw[4]) == 1
        prs = self.names_to_values[spell_name]
        classes: list[str] = self.__get_classes_from_query(spell_info['filter_class'])
        classes_tce: list[str] = self.__get_classes_from_query(spell_info['filter_class_tce'])
        archetypes: list[str] = self.__get_classes_from_query(spell_info['filter_archetype'])

        components_to_bool: dict[str, bool] = {
                "verbal": has_verbal,
                "somatic": has_somatic,
                "material": has_material
                }

        is_ritual = spell_info['filter_ritual'][0]
        is_ritual = int(is_ritual)
        is_ritual = bool(is_ritual-1)
        # is_ritual = bool(int(spell_info['filter_ritual'][0])-1)
        
        new_spell_dict: dict = {
                "name_translated": spell_name,
                "name": spell_info['title_en'],
                "components": components_to_bool,
                "material_component": prs['material_component'],
                "casting_time": prs['casting_time'],
                "description": prs['description'].replace('"', '\\"'),
                "distance":prs['distance'],
                "duration":prs['duration'],
                "level": self.__get_level_from_query(spell_info['level']),
                "is_ritual": is_ritual,
                "requires_concentration":prs['has_concentration'],
                "classes": classes,
                "classes_tce": classes_tce,
                "archetypes": archetypes
                }
        return Spell(**new_spell_dict)


        
    def translate_spells(self):
        for spell in self.spells_raw:
            self.spells.append(self.__refactor_parsed(spell))

    def process_spells(self) -> None:
        self.__get_data_from_soups()
        self.translate_spells()
        
        pass


def get_archetype(spells:list) -> None:
    delimiter = '\n====================\n'
    print_string: str = ''
    for spell in spells:
        archetype: list | None = spell.get('filter_archetype')
        is_uncatalogued: bool = False
        if archetype and str(archetype) != '[]':
            for key in archetype:
                if key not in DndSuParser.CLASS_ARCHETYPE_CODE_TRANSLATION.keys():
                    if not is_uncatalogued:
                        print_string += spell.get('title')
                        is_uncatalogued = True
                    print_string += '\t' + str(key)
        if is_uncatalogued:
            print_string += delimiter
    print(print_string)

def print_spells(spells: list) -> None:
    delimiter = '\n====================\n'
    print_string: str = ''
    for spell in spells:
        ic(spell)
        # ic(spell.get('title'))
        # ic(spell.get('filter_class'))
        # ic(spell.get('filter_class_tce'))
    print(print_string)
