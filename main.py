from template_handler import TemplateHandler
from spell_data_handler import Spell

def convert_components_to_string(component_dict: dict[str, bool]) -> str:
    return_list: list[str] = []
    if component_dict.get('verbal'):
        return_list.append('В')
    if component_dict.get('somatic'):
        return_list.append('С')
    if component_dict.get('material'):
        return_list.append('М')
    return ','.join(return_list)


def main():

    spell_data = Spell.load_from_json("spell_data_from_dndsu/Aid")


    th = TemplateHandler()
    soup = th.soup
    components_element = soup.new_tag("p")
    components_element.string = convert_components_to_string(spell_data.get_components())
    duration_element = soup.new_tag("p")
    duration_element.string = str(spell_data.get_duration())
    distance_element = soup.new_tag("p")
    distance_element.string = str(spell_data.get_distance())
    casting_time_element = soup.new_tag("p")
    casting_time_element.string = str(spell_data.get_casting_time())
    description_element = soup.new_tag("p")
    description_element.string = str(spell_data.get_description())


    th.append_tag_to_element(th.CONSTANT_BOX_NAMES.components, components_element)
    th.append_tag_to_element(th.CONSTANT_BOX_NAMES.duration, duration_element)
    th.append_tag_to_element(th.CONSTANT_BOX_NAMES.spell_range, distance_element)
    th.append_tag_to_element(th.CONSTANT_BOX_NAMES.casting_time , casting_time_element)
    th.append_tag_to_element(th.CONSTANT_BOX_NAMES.description , description_element)

    th.render()


    # soup.b



if __name__ == "__main__":
    main()

