from TTRPG_HTB.translations import Translations
from TTRPG_HTB import Spell, template_handler
from global_constants import RussianTranslations
from typing import Literal, Type
from PIL import Image
import os

TemplateHandler = template_handler.TemplateHandler

def render_spells_to_folder(folder: str,
                            template_path: str,
                            imported_translations: Type[Translations],
                            /,
                            *spells: Spell,
                            classes_to_specify: list[str] | None = None,
                            size: tuple[int, int],
                            restrict_to: int | None = None,
                            custom_css: str | None = None,
                            loglevel: Literal[0, 10, 20, 30, 40, 50] | None = None,
                            add_pictures: bool | None = True,
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
        th = TemplateHandler(template_path, imported_translations, loglevel)
        soup = th.soup
        th.set_element_text(th.CONSTANT_BOX_NAMES.spell_name, spell.get_name_translated())
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
        if add_pictures:
            casting_time_set_picture(th, casting_time_value)
        else:
            casting_time_tag = soup.new_tag('p')
            casting_time_tag.string = th.translate_duration(casting_time_value, is_action=True)
            
            th.append_tag_to_element(th.CONSTANT_BOX_NAMES.casting_time, casting_time_tag)



        is_ritual: bool = spell.get_is_ritual()
        if is_ritual:
            if add_pictures:
                th.append_picture(th.CONSTANT_BOX_NAMES.spell_info, 'src/ritual.png')
            else:
                text_to_add = soup.new_tag('p')
                text_to_add.string = ', Ритуал'
                th.append_tag_to_element(th.CONSTANT_BOX_NAMES.spell_info, text_to_add)


        requires_concentration: bool = spell.get_requires_concentration()
        if requires_concentration:
            if add_pictures:
                th.append_picture(th.CONSTANT_BOX_NAMES.spell_info, 'src/concentration.png')
            else:
                text_to_add = soup.new_tag('p')
                text_to_add.string = ', Концентрация'
                th.append_tag_to_element(th.CONSTANT_BOX_NAMES.spell_info, text_to_add)




        th.append_tag_to_element(th.CONSTANT_BOX_NAMES.components, components_element)
        th.append_tag_to_element(th.CONSTANT_BOX_NAMES.duration, duration_element)
        th.append_tag_to_element(th.CONSTANT_BOX_NAMES.spell_range, distance_element)
        # th.append_tag_to_element(th.CONSTANT_BOX_NAMES.description , description_element)

        file_name: str = folder + '/' + spell.get_file_name() + '.png'
        th.render(size, file_name, custom_css=custom_css)


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
