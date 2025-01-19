from template_handler import TemplateHandler
from spell_data_handler import SpellData



def main():

    sd = SpellData()
    spell_data = sd.get_spell_json()


    th = TemplateHandler()
    soup = th.soup
    components_element = soup.new_tag("p")
    components_element.string = str(spell_data.get('components'))
    duration_element = soup.new_tag("p")
    duration_element.string = str(spell_data.get('duration'))
    distance_element = soup.new_tag("p")
    distance_element.string = str(spell_data.get('distance'))
    casting_time_element = soup.new_tag("p")
    casting_time_element.string = str(spell_data.get('casting_time'))
    description_element = soup.new_tag("p")
    description_element.string = str(spell_data.get('description'))


    th.components.append(components_element)
    th.duration.append(duration_element)
    th.spell_range.append(distance_element)
    th.casting_time.append(casting_time_element)
    th.description.append(description_element)

    th.render()


    # soup.b



if __name__ == "__main__":
    main()

