from typing import Any
from bs4 import BeautifulSoup, Tag
from bs4.element import TemplateString
from html2image import Html2Image
import shutil
import os

DEFAULT_TEMPLATE = "basic-template"
OUTP_HTML = "build/outp.html"
DEFAULT_OUTP_NAME = "build/outp.png"
DEFAULT_SIZE = (408, 700)

class TemplateHandler:
    screenshot_options: dict = {
            "html_file": 'build/html_outp/outp.html',

            "save_as": 'outp.png',
            "size": (408, 700)
            }
    class CONSTANT_BOX_NAMES:
        components: str = "components"
        casting_time: str = "casting-time"
        spell_range: str = "range"
        duration: str = "duration"
        description: str = "description"
        spell_info:str = "spell_info"
        spell_name: str = "spell_name"


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
        def __getitem__(self, name: str, /) -> TemplateString | None:
            return self.__raw_dict[name]

        def __setitem__(self, name: str, value: TemplateString | None, /) -> None:
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


    def render(self, size: tuple[int, int] = DEFAULT_SIZE, file_path: str = DEFAULT_OUTP_NAME) -> None:
        self.screenshot_options['size'] = size
        self.screenshot_options['save_as'] = file_path
        self.clean_build()
        self.generate_symlinks(self.template)
        self.render_html()
        self.render_image()
        self.clean_build()

    def get_soup(self):
        with open(f'templates/{self.template}/index.html') as html_file:
            content = html_file.read()
            self.soup = BeautifulSoup(content, features="html.parser")





    def populate_parsed_strings(self) -> None:
        for key in self.parsed_strings.keys():
            self.parsed_strings[key] = self.find_elements_by_box(key)

    def append_tag_to_element(self, element_name: str, new_tag: Tag) -> None:
        element = self.parsed_strings[element_name]
        if element:
            element.append(new_tag)
        else:
            print(f'Element with name {element_name} is not found in template, skipping')



    def find_elements_by_box(self, box_value: str) -> TemplateString | None:
        found_boxes: list[TemplateString] = self.soup.find_all(box= box_value)
        if len(found_boxes) > 1:
            print(f"More than 1 box of same type found in {self.template}!")
            print(found_boxes)
            exit(1)
        if found_boxes:
            return found_boxes[0]
        return None

    def clean_build(self):
        # if os.path.exists('build/template'):
        #     os.remove('build/template')
        # os.symlink(f"../templates/{template_name}", 'build/template', True)
        # if not os.path.exists('build/src'):
        #     os.symlink('template/src', 'build/src', True)
        build_dir: str = 'build'
        files: list[str] = os.listdir(build_dir)
        for file in files:
            if os.path.islink(build_dir+ '/' + file):
                os.remove(build_dir+ '/'+file)
        if not os.path.exists(f'{build_dir}/html_outp'):
            os.mkdir(f'{build_dir}/html_outp')

    def render_html(self):
        with open('build/html_outp/outp.html', 'wb') as outp_file:
            outp_file.write(self.soup.encode())

    def generate_symlinks(self, template_name: str) -> None:
        files: list[str] = os.listdir('templates/'+template_name)
        for file in files:
            os.symlink(f"../templates/{template_name}/{file}", f'build/{file}', os.path.isdir(f'templates/{template_name}/{file}'))
                       

    def render_image(self):
        # render_options = {
        #         'enable-local-file-access': None,
        #         'width':408,
        #         'height':700,
        #         }
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
        file_name = file_path[file_path.find('/')+1:]
        self.screenshot_options['save_as'] = file_name
        # build_dir_path = os.path.realpath('build/template')
        # file_list: list[str] = recursive_find_files(os.path.realpath(build_dir_path))

        hti = Html2Image(temp_path='build')
        # hti = Html2Image(temp_path='build/template')

        # hti: Html2Image = Html2Image()
        # for file in file_list:
        #     dot_index: int = ''.join(reversed(file)).find('.')
        #     if dot_index == -1:
        #         continue
        #     file_extension: str = file[-dot_index-1:]
        #     if file_extension == ".svg" or file_extension == ".png":
        #         hti.load_file(file)
            
        # hti.load_file(os.path.realpath('/home/lunaro/git/dnd-card-spell-template/templates/basic-template/src/ritual.png'))



        hti.screenshot(**self.screenshot_options)
        shutil.move(file_name, file_path)


