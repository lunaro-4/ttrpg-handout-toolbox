from typing import Literal, Self, TypedDict, Unpack
import os
import json
import logging

logging.basicConfig(level=logging.ERROR)


class SpellInput(TypedDict):
    name_ru: str | None
    name: str
    components: dict[str, bool]
    material_component: str | None

    casting_time: int
    description: str
    distance: int
    duration: int
    level: int
    is_ritual: bool
    requires_concentration: bool
    classes: list[str]
    classes_tce: list[str]
    archetypes: list[str]



class Spell:

    logger = logging.getLogger("TTRPG_CTB_spell")
    class DURATION_CONSTATNS:
        ACTION = 4
        BONUS_ACTION = 2
        REACTION = 0

    def __init__(self, **kwargs: Unpack[SpellInput]) -> None:
        self.__name_translated: str | None = kwargs.get('name_ru')
        self.__name: str = kwargs['name']
        self.__components: dict[str, bool] = kwargs['components']
        self.__material_component: str | None = kwargs.get('material_component')
        self.__casting_time: int = kwargs['casting_time']
        self.__description: str = kwargs['description']
        self.__distance: int = kwargs['distance'] # 0 == cast on self
        self.__duration: int = kwargs['duration']
        self.__level: int = kwargs['level']
        self.__is_ritual: bool = kwargs['is_ritual']
        self.__requires_concentration: bool = kwargs['requires_concentration']
        self.__classes: list[str] = kwargs['classes']
        self.__classes_tce: list[str] = kwargs['classes_tce']
        self.__archetypes: list[str] = kwargs['archetypes']

        self.__json: dict = dict(kwargs)

    def set_logger_level(self, loglevel: Literal[0, 10, 20, 30, 40, 50]) -> None:
        self.logger.setLevel(loglevel)

    @classmethod
    def load_from_json(cls, spell_path: str ) -> Self:
        """
        example of valid json is provied with static metod 'get_valid_json_example()'
        """
        loaded_data: dict = {}
        if not spell_path[-4:] == "json":
            logging.error(f'{spell_path} is not a json')
            raise Exception
        with open(spell_path, 'r') as f:
            try:
                loaded_data =  json.load(f, strict=False)
            except Exception as e:
                logging.error(spell_path)
                raise e

        for component, value in loaded_data['components'].items():
            loaded_data['components'][component] = bool(value)

        return cls(**loaded_data)

    def __repr__(self) -> str :
        return json.dumps(self.__json, indent=2).replace('\\/', '/').encode().decode("unicode-escape")
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Spell):
            return NotImplemented
        return self.get_name() == other.get_name()
    
    def __hash__(self) -> int:
        return hash(self.get_name())

    @staticmethod
    def get_valid_json_example() -> str:
        json_example: str = """
{
    "name_translated": "Сигнал тревоги",
    "name": "Alarm",
    "components": {
        "verbal": true,
        "somatic": true,
        "material": true
    },
    "material_component": "колокольчик и серебряная проволочка",
    "casting_time": 60,
    "description": "Вы устанавливаете сигнализацию на случай вторжения. Выберите дверь, окно или область в пределах дистанции не больше куба с длиной ребра 20 футов. До окончания действия заклинания тревога уведомляет вас каждый раз, когда охраняемой области касается или входит в неё существо с размером не меньше Крошечного. При накладывании заклинания вы можете указать существ, которые не будут вызывать срабатывание тревоги. Вы также выбираете, мысленной будет тревога или слышимой.
Мысленная тревога предупреждает вас звоном в сознании, если вы находитесь в пределах 1 мили от охраняемой области. Этот звон пробуждает вас, если вы спите.
Слышимая тревога издает звон колокольчика в течение 10 секунд в пределах 60 футов.
",
    "distance": 30,
    "duration": 28800,
    "level": 1,
    "is_ritual": true,
    "requires_concentration": false,
    "classes": [
        "wizard",
        "artificer",
        "ranger"
    ],
    "classes_tce": [],
    "archetypes": [
        "oath_of_the_watchers",
        "clockwork_soul"
    ]
}


        """
        return json_example

    def save_to_json(self, save_path: str) -> None:
        """
        Saves spell to json file, from which it can later be loaded

        `save_path`: path to file. `.json` is not added automatically
        """
        with open(f'{save_path}', "w") as file:
            file.write(json.dumps(self.__json, indent=4).encode().decode("unicode-escape"))


    def get_file_name(self) -> str:
        return self.__name.replace('/', '_').replace('\\', '_').replace(' ', '_')

    def get_name(self) -> str:
        return self.__name

    def get_name_translated(self) -> str:
        if self.__name_translated:
            return self.__name_translated
        return self.__name

    def get_components(self) -> dict[str, bool]:
        """ returns dictionary with keys: 'verbal', 'somatic', 'material'"""
        return self.__components

    def get_casting_time(self) -> int:
        return self.__casting_time

    def get_description(self) -> str:
        return self.__description

    def get_distance(self) -> int:
        return self.__distance
    def get_duration(self) -> int:
        return self.__duration

    def get_level(self) -> int:
        return self.__level

    def get_material_component(self) -> str | None:
        return self.__material_component

    def get_is_ritual(self) -> bool:
        return self.__is_ritual

    def get_requires_concentration(self) -> bool:
        return self.__requires_concentration

    def get_classes(self) -> list[str]:
        return self.__classes

    def get_classes_tce(self) -> list[str]:
        return self.__classes_tce

    def get_archetypes(self) -> list[str]:
        return self.__archetypes

class SpellDatabase:
    """ A class, responsible for holding and mass processing spell data.
    """

    logger = logging.getLogger("TTRPG_CTB_SpellDatabase")
    def __init__(self, directory: str | None = None, loglevel: Literal[0, 10, 20, 30, 40, 50] | None = None) -> None:
        """
        directory(optional):    specify directory to automatically parse all spell json from
        """
        if loglevel:
            self.logger.setLevel(loglevel)
            Spell.logger.setLevel(loglevel)
        self.spells: list[Spell] = []
        """ A list, containing all the spells, loaded into library"""
        if directory:
            self.load_spells_form_directory(directory)

    def process_spells(self) -> None:
        """
        Populate the internal dictionaries by calling methods:
            map_names_to_spells()
            populate_classes_maps()
            populate_levels_maps()
        """
        if not self.spells:
            logging.error('No spells loaded, aborting!')
        self.map_names_to_spells(parse_english_names=True)
        self.populate_classes_maps()
        self.populate_levels_maps()
        pass

    def load_spell_from_json(self, path_to_file: str) -> None:
        new_spell = Spell.load_from_json(path_to_file)
        self.spells.append(new_spell)
        """
        Attempts to load spell, using Spell.load_from_json() method

        On success, adds it to 'spells' dictionary
        """
    def load_spells_form_directory(self, path_to_directory: str) -> None:
        """
        A method, that scans directory for .json files and applies 'load_spell_from_json()' on each.

        It is not recursive, and in complex projects you might want to use 'load_spell_from_json()' directly
        """
        files: list[str] = os.listdir(path_to_directory)
        logging.info(f'found {len(files)} files in {path_to_directory}')
        for file in files:
            if not file[-4:] == "json":
                logging.warning(f'{file} is not a json, skipping')
                continue
            self.load_spell_from_json(path_to_directory + '/' + file)

    def map_names_to_spells(self, parse_english_names: bool = True) -> None:
        """
        Populate internal dictionary self.name_to_spell, which allows other methods to find spell by conventionalized name
        """
        spell_dict: dict[str, Spell] = {}
        for spell in self.spells:
            if parse_english_names:
                spell_name = spell.get_name()
            else:
                spell_name = spell.get_name_translated()
            spell_dict[spell_name] = spell
        if parse_english_names:
            self.name_to_spell: dict[str, Spell] = spell_dict
            """ A dictionary, allowing other methods to find spells, by referring to their 'string name'. Unlike 'translated_' version, keys are in English """
        else:
            self.translated_name_to_spell: dict[str, Spell] = spell_dict
            """ A dictionary, allowing other methods to find spells, by referring to their 'string name'. Unlike 'name_to_spell' version, keys are localized names"""

    def populate_levels_maps(self) -> None:
        """
        Populate internal dictionary self.level_to_spells, containing spells, grouped by their level"""
        def add_to_map(map: dict[int, list[Spell]], key: int, value: str | None) -> None:
            if key not in map.keys():
                map[key] = []
            if value:
                map[key].append(self.name_to_spell[value])

        self.level_to_spells: dict[int, list[Spell]] = {}
        """ A dictionary, with key being spell level, and values being spells with corresponding level"""

        for spell in self.spells:
            spell_name: str = spell.get_name()
            spell_level: int = spell.get_level()
            add_to_map(self.level_to_spells, spell_level, spell_name)


    def __get_single_spell_by_name(self, names_to_spells: dict[str, Spell], spell_name: str, presise: bool) -> Spell | None:
        for name, spell in names_to_spells.items():
            is_same_spell: bool
            if presise:
                is_same_spell = spell_name.casefold() == name.casefold()
            else:
                is_same_spell = spell_name.casefold() in name.casefold()
            if is_same_spell:
                return spell
        return None

    def get_spells_by_names(self, /, *spell_names: str,
                            parse_english_names: bool = True,
                            precise: bool = False,
                            ) -> list[Spell]:
        """ Returns list of spells, found by specified names.
        For each name specified, the method runs through all the spell names, and adds first occurrence to the returning list

        Arguments: 
            `spell_names`: any amount of arguments of type str. Search is case-insensitive, but all punctuation should be considered.
            `parse_english_names`: whether names specified in English or translated. Default is `True`, which means the method is expecting input of English spell names
            `precise`: whether to return spells with exact names (using `==`) or spells, which name contains specified part (using `in` keyword)

        """

        if parse_english_names:
            names_to_spells = self.name_to_spell
        else:
            self.map_names_to_spells(parse_english_names=False)
            names_to_spells = self.translated_name_to_spell
        return_list: list[Spell] = []
        for spell_name in spell_names:
            found_spell = self.__get_single_spell_by_name(names_to_spells, spell_name, precise)
            if found_spell:
                return_list.append(found_spell)
        return return_list
    


    def populate_classes_maps(self) -> None:
        """
        Populate internal dictionary self.class_to_spells, containing spells, grouped by their class
        """
        def add_to_map(map: dict[str, list[Spell]], key: str, value: str | None) -> None:
            if key not in map.keys():
                map[key] = []
            if value:
                map[key].append(self.name_to_spell[value])

        self.class_to_spells: dict[str, list[Spell]] = {}
        """ A dictionary, with key being class or archetype, and values being spells with corresponding level"""

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
        """ Static method, that returns spells found in both lists """
        return list(set(list1).intersection(list2))


