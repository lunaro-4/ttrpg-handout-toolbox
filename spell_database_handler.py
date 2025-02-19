from typing import Annotated, Literal
from html2image.html2image import os
from PIL import Image
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
        self.map_names_to_spells(parse_english_names=True)
        self.populate_classes_maps()
        self.populate_levels_maps()
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

    def map_names_to_spells(self, parse_english_names: bool = True) -> None:
        spell_dict: dict[str, Spell] = {}
        for spell in self.spells:
            if parse_english_names:
                spell_name = spell.get_name()
            else:
                spell_name = spell.get_name_ru()
            spell_dict[spell_name] = spell
        if parse_english_names:
            self.name_to_spell: dict[str, Spell] = spell_dict
        else:
            ic('fire!')
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


    @staticmethod
    def render_spells_to_folder(folder: str, /, *spells: Spell,
                                classes_to_specify: list[str] | None = None,
                                size: tuple[int, int] | None = None,
                                restrict_to: int | None = None,
                                custom_css: str | None = None
                                ) -> None:

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

        if restrict_to:
            spells = spells[:restrict_to]

        for spell in spells:
            print(f'Rendering spell {spell.get_name()}')
            th = TemplateHandler()
            soup = th.soup
            th.set_element_text(th.CONSTANT_BOX_NAMES.spell_name, spell.get_name_ru())
            description_to_set: str = spell.get_description()
            material_component = spell.get_material_component()

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


            is_ritual: bool = spell.get_is_ritual()
            if is_ritual:
                th.append_picture(th.CONSTANT_BOX_NAMES.spell_info, 'src/ritual.png')
                
            requires_concentration: bool = spell.get_requires_concentration()
            if requires_concentration:
                th.append_picture(th.CONSTANT_BOX_NAMES.spell_info, 'src/concentration.png')
                



            th.append_tag_to_element(th.CONSTANT_BOX_NAMES.components, components_element)
            th.append_tag_to_element(th.CONSTANT_BOX_NAMES.duration, duration_element)
            th.append_tag_to_element(th.CONSTANT_BOX_NAMES.spell_range, distance_element)
            # th.append_tag_to_element(th.CONSTANT_BOX_NAMES.description , description_element)

            file_name: str = folder + '/' + spell.get_file_name() + '.png'
            th.render(file_path=file_name, custom_css=custom_css,size=size)

        
    @staticmethod
    def combine_images_to_printable(input_directory: str, output_directory: str,
                                    /,
                                    resolution: Literal[150, 300],
                                    paper_format: Literal['A4'] = 'A4',
                                    margins_pix: tuple[int, int, int, int] | None = None,
                                    margins_inch: tuple[float, float, float, float] | None = None,
                                    gap: tuple[int, int] | None = None,
                                    
                                    ) -> None:
        """
DPI:            DPI of sheet to print on
paper_format:   choose between 'A4' formats
margin_*:       space to cut from rendered sheet. Specify according to printer settings to avoid wrong scaling of picture during printing
    margins_pix:    tuple of margin in pixels: (top, right, left, bottom)
    margins_inch:   tuple of margin in inches: (top, right, left, bottom)
gap:            (horisontal, vertical) gaps between images in pixels



        """

        # CONSTANTS
        SIZE_STANDARTS: dict[str, dict[int, dict[str, int | tuple[int,int]]]] = {
                'A4': {
                    150: {
                        'size': (1240, 1754),
                        'inch_in_pixels': 48
                        },
                    300: {
                        'size': (2480, 3508),
                        'inch_in_pixels': 96
                        }
                    }

                }

        # PREPARATION
        paper_format_values = SIZE_STANDARTS[paper_format][resolution]
        final_margins: tuple[int, int, int, int]
        if not margins_pix:
            final_margins = (0,0,0,0)
            if margins_inch:
                temp_margins_pix: list[int] = []
                for i, inch in enumerate(margins_inch):
                    inch_in_pixel = paper_format_values['inch_in_pixels']
                    if not isinstance(inch_in_pixel, tuple):
                        raise ValueError
                    temp_margins_pix.append(int(inch * inch_in_pixel[i]))
                final_margins = (temp_margins_pix[0], temp_margins_pix[1], temp_margins_pix[2], temp_margins_pix[3])
        else:
            final_margins = margins_pix

        resolution_tuple = paper_format_values['size']
        if not isinstance(resolution_tuple, tuple):
            raise ValueError

        if gap:
            gap_h = gap[0]
            gap_v = gap[1]
        else:
            gap_h = gap_v = 0

        sheet_size = (resolution_tuple[0]-final_margins[0]-final_margins[3], resolution_tuple[1]-final_margins[1]-final_margins[2])


        # Main Logic

        images: list[str] = os.listdir(input_directory)
        for image_filename in images.copy():
            if image_filename[-3:] != 'png':
                print(f'{image_filename} is not a png, skpping')
                images.remove(image_filename)


        all_pictures_printed: bool = False

        sheet_id: int = -1

        while not all_pictures_printed:
            sheet_id += 1
            space_left_on_sheet: bool = True
            sheet = Image.new('RGB', sheet_size, color='white')
            last_height = 0
            last_width = 0
            while space_left_on_sheet:
                if not images:
                    all_pictures_printed = True
                    break
                image_filename = input_directory + '/' + images[0]
                image: Image.Image = Image.open(image_filename)
                if image.width + last_width + gap_h > sheet_size[0]:
                    last_height += image.height + gap_v
                    last_width = 0
                    continue
                if image.height + last_height + gap_v > sheet_size[1]:
                    space_left_on_sheet = False
                    break
                sheet.paste(image, (last_width, last_height))
                last_width += image.width + gap_h
                images = images[1:]
            sheet.save(f'{output_directory}/outp{sheet_id}.png')
            





