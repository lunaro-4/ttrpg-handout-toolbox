from bs4 import BeautifulSoup
from bs4.element import TemplateString
from html2image import Html2Image
import shutil
import os

DEFAULT_TEMPLATE = "basic-template"
OUTP_HTML = "build/outp.html"
DEFAULT_OUTP_NAME = "build/outp.png"
DEFAULT_SIZE = (408, 700)

class TemplateHandler:
    soup: BeautifulSoup
    components: TemplateString
    casting_time: TemplateString
    spell_range: TemplateString
    duration: TemplateString
    description: TemplateString
    template: str
    screenshot_options: dict = {
            "html_file": 'build/template/outp.html',
            "css_file": 'build/template/style.css',
            "save_as": 'outp.png',
            "size": (408, 700)
            }

    def __init__(self, template_name: str | None = None) -> None:
        if not template_name:
            template_name = DEFAULT_TEMPLATE
        self.template = template_name
        self.get_soup()
        self.populate_box_vars()

    def render(self, size: tuple[int, int] = DEFAULT_SIZE, file_path: str = DEFAULT_OUTP_NAME) -> None:
        self.screenshot_options['size'] = size
        self.screenshot_options['save_as'] = file_path
        self.prepare_build(self.template)
        self.render_html()
        self.render_image()

    def get_soup(self):
        with open(f'templates/{self.template}/index.html') as html_file:
            content = html_file.read()
            self.soup = BeautifulSoup(content, features="html.parser")




    class CONSTANT_BOX_NAMES:
        components: str = "components"
        casting_time: str = "casting-time"
        spell_range: str = "range"
        duration: str = "duration"
        description: str = "description"

    def populate_box_vars(self) -> None:
        components_list = self.find_elements_by_box(self.CONSTANT_BOX_NAMES.components)
        casting_time_list = self.find_elements_by_box(self.CONSTANT_BOX_NAMES.casting_time)
        spell_range_list = self.find_elements_by_box(self.CONSTANT_BOX_NAMES.spell_range)
        duration_list = self.find_elements_by_box(self.CONSTANT_BOX_NAMES.duration)
        description_list = self.find_elements_by_box(self.CONSTANT_BOX_NAMES.description)
        for i in [components_list, casting_time_list, spell_range_list, duration_list]:
            if len(i) > 1:
                print(f"More than 1 box of same type found in {self.template}!")
                print(i)
                exit(1)
        self.components=components_list[0]
        self.casting_time=casting_time_list[0]
        self.spell_range=spell_range_list[0]
        self.duration=duration_list[0]
        self.description=description_list[0]

    def find_elements_by_box(self, box_value: str) -> list:
        return self.soup.find_all(box= box_value)

    def prepare_build(self, template_name: str | None):
        if os.path.exists('build/template'):
            os.remove('build/template')
        os.symlink(f"../templates/{template_name}", 'build/template', True)

    def render_html(self):
        with open('build/template/outp.html', 'wb') as outp_file:
            outp_file.write(self.soup.encode())

    def render_image(self):
        # render_options = {
        #         'enable-local-file-access': None,
        #         'width':408,
        #         'height':700,
        #         }
        file_path: str = self.screenshot_options['save_as']
        file_name = file_path[file_path.find('/')+1:]
        self.screenshot_options['save_as'] = file_name

        hti = Html2Image()
        hti.screenshot(**self.screenshot_options)
        shutil.move(file_name, file_path)


