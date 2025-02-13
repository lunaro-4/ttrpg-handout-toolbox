
from html2image.html2image import os
from icecream import ic
from spell_handler import Spell
from template_handler import TemplateHandler
from global_constants import CLASS_SUBCLASS_MAP


class SpellDatabase:
    """ order of spell processing:
    """
    def __init__(self, directory: str | None = None) -> None:
        self.spells: list[Spell] = []
        if directory:
            self.load_spells_form_directory(directory)

    def process_spells(self) -> None:
        if not self.spells:
            print('No spells loaded, aborting!')
        self.map_names_to_spells()
        self.populate_classes_maps()
        pass

    def load_spell_from_json(self, path_to_file: str) -> None:
        new_spell = Spell.load_from_json(path_to_file)
        self.spells.append(new_spell)

    def load_spells_form_directory(self, path_to_directory: str) -> None:
        files: list[str] = os.listdir(path_to_directory)
        for file in files:
            if not file[-4:] == "json":
                print(f'{file} is not a json, skipping')
                continue
            self.load_spell_from_json(path_to_directory + '/' + file)

    def map_names_to_spells(self) -> None:
        self.name_to_spell: dict[str, Spell] = {}
        for spell in self.spells:
            self.name_to_spell[spell.get_name()] = spell


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
    def render_spells_to_folder(folder: str, classes_to_specify: list[str] | None = None, *spells: Spell) -> None:
        def convert_components_to_string(component_dict: dict[str, bool]) -> str:
            return_list: list[str] = []
            if component_dict.get('verbal'):
                return_list.append('В')
            if component_dict.get('somatic'):
                return_list.append('С')
            if component_dict.get('material'):
                return_list.append('М')
            return ','.join(return_list)


        def casting_time_set_picture(th: TemplateHandler, casting_time_value: int) -> None:
            soup = th.soup
            if casting_time_value == 4:
                th.append_picture(th.CONSTANT_BOX_NAMES.casting_time, 'src/action.png')
            elif casting_time_value == 2:
                th.append_picture(th.CONSTANT_BOX_NAMES.casting_time, 'src/bonus-action.png')
            elif casting_time_value == 6:
                th.append_picture(th.CONSTANT_BOX_NAMES.casting_time, 'src/bonus-action.png')
                th.append_picture(th.CONSTANT_BOX_NAMES.casting_time, 'src/action.png')
            else:
                casting_time_element = soup.new_tag("p")
                casting_time_element.string = th.translate_duration(casting_time_value, is_action=True)
                th.append_tag_to_element(th.CONSTANT_BOX_NAMES.casting_time, casting_time_element)

        for spell in spells:
            print(f'Processing spell {spell.get_name()}')
            th = TemplateHandler()
            soup = th.soup
            th.set_element_text(th.CONSTANT_BOX_NAMES.spell_name, spell.get_name_ru())
            description_to_set: str = spell.get_description()
            material_component = spell.get_material_component()
            ic(spell.get_components())
            ic(spell.get_components()['material'])
            ic(material_component)

            if spell.get_components()['material'] and material_component:
                description_to_set = th.decorate_material_component(material_component) + description_to_set

            th.set_element_text(th.CONSTANT_BOX_NAMES.description, description_to_set)
            
            components_element = soup.new_tag("p")
            components_element.string = convert_components_to_string(spell.get_components())
            duration_element = soup.new_tag("p")
            duration_element.string = th.translate_duration(spell.get_duration())
            distance_element = soup.new_tag("p")
            distance_element.string = th.translate_distance(spell.get_distance())
            level_element = th.get_level_tag(spell.get_level())
            th.append_tag_to_element(th.CONSTANT_BOX_NAMES.spell_info, level_element)

            casting_time_value = spell.get_casting_time()
            casting_time_set_picture(th, casting_time_value)



            if spell.get_is_ritual():
                th.append_picture(th.CONSTANT_BOX_NAMES.spell_info, 'src/ritual.png')
                
                



            th.append_tag_to_element(th.CONSTANT_BOX_NAMES.components, components_element)
            th.append_tag_to_element(th.CONSTANT_BOX_NAMES.duration, duration_element)
            th.append_tag_to_element(th.CONSTANT_BOX_NAMES.spell_range, distance_element)
            # th.append_tag_to_element(th.CONSTANT_BOX_NAMES.description , description_element)

            file_name: str = folder + '/' + spell.get_file_name() + '.png'
            th.render(file_path=file_name)

        




