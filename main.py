from bs4 import BeautifulSoup
import imgkit
import shutil
import os

DEFAULT_TEMPLATE = "basic-template"
OUTP_HTML = "build/outp.html"


class CONSTANT_BOX_NAMES:
    components: str = "components"
    casting_time: str = "casting-time"
    spell_range: str = "range"
    duration: str = "duration"

    @staticmethod
    def populate_box_vars(soup):
        components_list = find_elements_by_box(soup, CONSTANT_BOX_NAMES.components)
        casting_time_list = find_elements_by_box(soup, CONSTANT_BOX_NAMES.casting_time)
        spell_range_list = find_elements_by_box(soup, CONSTANT_BOX_NAMES.spell_range)
        duration_list = find_elements_by_box(soup, CONSTANT_BOX_NAMES.duration)
        for i in [components_list, casting_time_list, spell_range_list, duration_list]:
            if len(i) > 1:
                print("More than 1 box of same type found!")
                print(i)
                exit(1)
        return (components_list[0], casting_time_list[0], spell_range_list[0], duration_list[0])

def find_elements_by_box(soup: BeautifulSoup, box_value: str) -> list:
    return soup.find_all(box= box_value);

def prepare_build(template_name: str = DEFAULT_TEMPLATE):
    if os.path.exists('build/template'):
        shutil.rmtree('build/template')
    shutil.copytree(f"templates/{template_name}", 'build/template')

def render_html(soup: BeautifulSoup):
    with open('build/template/outp.html', 'wb') as outp_file:
        outp_file.write(soup.encode())

def render_image():
    render_options = {
            'enable-local-file-access': None,
            'width':408,
            'height':700,
            }
    imgkit.from_file('build/template/outp.html', 'build/outp.png', options=render_options)


def main():
    with open('templates/basic-template/index.html') as html_file:
        content = html_file.read()
        soup = BeautifulSoup(content, features="html.parser")

    components, casting_time, spell_range, duration_list = CONSTANT_BOX_NAMES.populate_box_vars(soup)

    components_value = soup.new_tag("p")
    components_value.string = "123"
    components.append(components_value)

    prepare_build()
    render_html(soup)
    render_image()


    # soup.b



if __name__ == "__main__":
    main()

