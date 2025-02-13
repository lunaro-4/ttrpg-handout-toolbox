
from html2image.html2image import os
from spell_data_handler import Spell


class SpellDatabase:
    def __init__(self) -> None:
        self.spells: list[Spell] = []

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





if __name__ == "__main__":
    sdb = SpellDatabase()
    sdb.load_spells_form_directory('spell_data_from_dndsu')
    print(len(sdb.spells))

