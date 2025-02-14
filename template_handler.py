from typing import Any
from bs4 import BeautifulSoup, Tag
from html2image import Html2Image
import shutil
import os
from global_constants import RussianTranslations


DEFAULT_TEMPLATE = "basic-template"
OUTP_HTML = "build/outp.html"
DEFAULT_OUTP_NAME = "build/outp.png"
DEFAULT_SIZE = (408, 700)

class TemplateHandler:
    screenshot_options: dict = {
            "html_file": 'build/html_outp/outp.html',
            "css_file": 'build/html_outp/outp.css',
            }
    class CONSTANT_BOX_NAMES:
        components: str = "components"
        casting_time: str = "casting-time"
        spell_range: str = "range"
        duration: str = "duration"
        description: str = "description"
        spell_info:str = "spell-info"
        spell_name: str = "spell-name"

    class ParsedStrings:
        def __init__(self) -> None:
            cbn: TemplateHandler.CONSTANT_BOX_NAMES = TemplateHandler.CONSTANT_BOX_NAMES()
            self.__raw_dict: dict= {
                    cbn.components: None,
                    cbn.casting_time: None,
                    cbn.spell_range: None,
                    cbn.duration: None,
                    cbn.description: None,
                    cbn.spell_info: None,
                    cbn.spell_name: None
                    }
        def __getitem__(self, name: str, /) -> Tag | None:
            return self.__raw_dict[name]

        def __setitem__(self, name: str, value: Tag | None, /) -> None:
            if name not in self.__raw_dict.keys():
                raise Exception
            self.__raw_dict[name] = value

        def keys(self) -> list:
            return list(self.__raw_dict.keys())


    def __init__(self, template_name: str | None = None) -> None:
        if not template_name:
            template_name = DEFAULT_TEMPLATE
        self.soup: BeautifulSoup
        self.parsed_strings: TemplateHandler.ParsedStrings =  self.ParsedStrings()
        self.template: str = template_name
        self.get_soup()
        self.populate_parsed_strings()


    def render(self, size: tuple[int, int] = DEFAULT_SIZE, file_path: str = DEFAULT_OUTP_NAME, custom_css: str | None = None) -> None:
        self.screenshot_options['size'] = size
        self.screenshot_options['save_as'] = file_path
        self.clean_build()
        self.generate_symlinks(self.template)
        self.render_html(custom_css)
        self.render_image()
        self.clean_build()

    def get_soup(self):
        with open(f'templates/{self.template}/index.html') as html_file:
            content = html_file.read()
            self.soup = BeautifulSoup(content, features="html.parser")


    def translate_duration(self, duration_value: int, is_action: bool = False) -> str:
        if is_action:
            if duration_value == 2:
                return RussianTranslations.Actions.bonus_action
            if duration_value == 4:
                return RussianTranslations.Actions.action
            if duration_value == 6:
                return RussianTranslations.Actions.action + 'и' + RussianTranslations.Actions.bonus_action
        if duration_value%(3600*7*24) == 0:
            return f'{int(duration_value/(3600*7*24))} {RussianTranslations.Time.week}'
        if duration_value%(3600*24) == 0:
            return f'{int(duration_value/(3600*24))} {RussianTranslations.Time.day}'
        if duration_value%(3600) == 0:
            return f'{int(duration_value/(3600))} {RussianTranslations.Time.hour}'
        if duration_value%(60) == 0:
            return f'{int(duration_value/(60))} {RussianTranslations.Time.minute}'
        if duration_value != -1:
            return f'{int(duration_value)} {RussianTranslations.Time.second}'
        return RussianTranslations.Time.other

    def translate_distance(self, distance_value: int) -> str:
        match distance_value:
            case 0:
                return RussianTranslations.Distance.on_self
            case 5:
                return RussianTranslations.Distance.on_touch
            case _:
                return f'{distance_value} {RussianTranslations.Distance.ft}'


    def populate_parsed_strings(self) -> None:
        for key in self.parsed_strings.keys():
            self.parsed_strings[key] = self.find_elements_by_box(key)

    def append_tag_to_element(self, element_name: str, new_tag: Tag) -> None:
        if element_name == self.CONSTANT_BOX_NAMES.description:
            print("Can't add element to description box, as it is a <p> tag. Please use 'set_element_text' instead")
            raise Exception()
        element = self.parsed_strings[element_name]
        if element:
            element.append(new_tag)
        else:
            print(f'Element with name {element_name} is not found in template, skipping')

    def append_picture(self, element_name: str,  relative_path: str) -> None:
        new_picture_element = self.soup.new_tag('img')
        new_picture_element['src'] = relative_path
        self.append_tag_to_element(element_name, new_picture_element)

    def set_element_text(self, element_name: str, new_text: str) -> None:
        element: Tag | None = self.parsed_strings[element_name]
        if element:
            markup = element.string = new_text.replace('\n', '<br>')
            element.string.replace_with(BeautifulSoup(markup, "html.parser"))
        else:
            print(f'Element with name {element_name} is not found in template, skipping')

        pass

    def get_level_tag(self, level: int, add_as_picture: bool = False) -> Tag:
        if add_as_picture:
            level_tag: Tag = self.soup.new_tag("img")
            level_picture_string = f'src/lvl_{level}_spell.png'
            level_tag['src'] = level_picture_string
        else:
            level_tag: Tag = self.soup.new_tag("p")
            level_tag.string = RussianTranslations.SPELL_LEVELS[level]

        return level_tag

    def decorate_material_component(self, material_component: str) -> str:
        string_to_return: str = RussianTranslations.Components.material_component_text
        string_to_return = f'<em><b>{string_to_return}</b>{material_component}</em>\n\n'
        return string_to_return



    def find_elements_by_box(self, box_value: str) -> Tag | None:
        found_boxes: list[Tag] = self.soup.find_all(box= box_value)
        if len(found_boxes) > 1:
            print(f"More than 1 box of same type found in {self.template}!")
            print(found_boxes)
            exit(1)
        if found_boxes:
            return found_boxes[0]
        return None

    def clean_build(self):
        build_dir: str = 'build'
        files: list[str] = os.listdir(build_dir)
        for file in files:
            if os.path.islink(build_dir+ '/' + file):
                os.remove(build_dir+ '/'+file)
        if not os.path.exists(f'{build_dir}/html_outp'):
            os.mkdir(f'{build_dir}/html_outp')

    def render_html(self, custom_css: str | None = None):
        if custom_css:
            style = self.soup.new_tag("style")
            style.string = custom_css
            head = self.soup.find("head")
            if head:
                head.append(style)
        with open('build/html_outp/outp.html', 'wb') as outp_file:
            outp_file.write(self.soup.encode())



    def generate_symlinks(self, template_name: str) -> None:
        files: list[str] = os.listdir('templates/'+template_name)
        for file in files:
            os.symlink(f"../templates/{template_name}/{file}", f'build/{file}', os.path.isdir(f'templates/{template_name}/{file}'))
                       

    def render_image(self):
        def recursive_find_files(directory_path: str) -> list[str] :
            file_list: list[str] = []
            files = os.listdir(directory_path)
            for file in files:
                realfile = directory_path + '/'+  file
                if os.path.isdir(realfile):
                    file_list.extend(recursive_find_files(realfile))
                else:
                    file_list.append(realfile)

            return file_list

        file_path: str = self.screenshot_options['save_as']
        file_name_index: int = file_path[::-1].find('/')
        file_name = file_path[-file_name_index:]
        self.screenshot_options['save_as'] = file_name
        hti = Html2Image(temp_path='build', custom_flags=['--disable-logging', '--log-level 3'], disable_logging=True) # , '--headless=new'
        hti.screenshot(**self.screenshot_options)
        shutil.move(file_name, file_path)


