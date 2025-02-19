from typing import Annotated, Callable, Literal
from html2image.html2image import os
from PIL import Image
from .spell_handler import Spell
from .template_handler import TemplateHandler
import logging

logger = logging.getLogger("TTRPG_CTB_logger")


class SpellDatabase:
    """ A class, responsible for holding and mass processing spell data.
    """
    def __init__(self, directory: str | None = None) -> None:
        """
        directory(optional):    specify directory to automatically parse all spell json from
        """
        self.spells: list[Spell] = []
        if directory:
            self.load_spells_form_directory(directory)

    def process_spells(self) -> None:
        if not self.spells:
            logging.error('No spells loaded, aborting!')
        self.map_names_to_spells(parse_english_names=True)
        self.populate_classes_maps()
        self.populate_levels_maps()
        pass

    def load_spell_from_json(self, path_to_file: str) -> None:
        new_spell = Spell.load_from_json(path_to_file)
        self.spells.append(new_spell)

    def load_spells_form_directory(self, path_to_directory: str) -> None:
        files: list[str] = os.listdir(path_to_directory)
        logging.info(f'found {len(files)} files in {path_to_directory}')
        for file in files:
            if not file[-4:] == "json":
                logging.warning(f'{file} is not a json, skipping')
                continue
            self.load_spell_from_json(path_to_directory + '/' + file)

    def map_names_to_spells(self, parse_english_names: bool = True) -> None:
        spell_dict: dict[str, Spell] = {}
        for spell in self.spells:
            if parse_english_names:
                spell_name = spell.get_name()
            else:
                spell_name = spell.get_name_translated()
            spell_dict[spell_name] = spell
        if parse_english_names:
            self.name_to_spell: dict[str, Spell] = spell_dict
        else:
            self.translated_name_to_spell: dict[str, Spell] = spell_dict

    def populate_levels_maps(self) -> None:
        def add_to_map(map: dict[int, list[Spell]], key: int, value: str | None) -> None:
            if key not in map.keys():
                map[key] = []
            if value:
                map[key].append(self.name_to_spell[value])

        self.level_to_spells: dict[int, list[Spell]] = {}

        for spell in self.spells:
            spell_name: str = spell.get_name()
            spell_level: int = spell.get_level()
            add_to_map(self.level_to_spells, spell_level, spell_name)

    def __get_single_spell_by_name(self, names_to_spells: dict[str, Spell], spell_name: str, presise: bool) -> Spell | None:
        for name, spell in names_to_spells.items():
            if presise:
                is_same_spell: bool = spell_name.casefold() == name.casefold()
            else:
                is_same_spell: bool = spell_name.casefold() in name.casefold()
            if is_same_spell:
                return spell
        return None

    def get_spells_by_names(self, /, *spell_names: str,
                            parse_english_names: bool = True,
                            presise: bool = False,
                            ) -> list[Spell]:
        if parse_english_names:
            names_to_spells = self.name_to_spell
        else:
            self.map_names_to_spells(parse_english_names=False)
            names_to_spells = self.translated_name_to_spell
        return_list: list[Spell] = []
        for spell_name in spell_names:
            found_spell = self.__get_single_spell_by_name(names_to_spells, spell_name, presise)
            if found_spell:
                return_list.append(found_spell)
        return return_list
    


    def populate_classes_maps(self):

        def add_to_map(map: dict[str, list[Spell]], key: str, value: str | None) -> None:
            if key not in map.keys():
                map[key] = []
            if value:
                map[key].append(self.name_to_spell[value])

        self.class_to_spells: dict[str, list[Spell]] = {}

        for spell in self.spells:
            total_classes: list[str] = []
            total_classes.extend(spell.get_classes())
            total_classes.extend(spell.get_classes_tce())
            total_classes.extend(spell.get_archetypes())
            spell_name: str = spell.get_name()
            for class_name in total_classes:
                add_to_map(self.class_to_spells, class_name, spell_name)
    @staticmethod
    def find_intersections(list1: list[Spell], list2: list[Spell]) -> list[Spell]:
        return list(set(list1).intersection(list2))


            





