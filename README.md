# TTRPG Handout Toolbox

## Overview

This project aims to provide an easy way to prepare handout materials for players of Tabletop Role Play Games.

# Features
> [!NOTE]
> Currently only supports spell cards. For planned features see `Planned` section

- Support for `json` library of spells (loaded from folder with jsons)
- API for rendering spells from library into pictures, using html template and `html2picture` library
    - builtin customisable translations for time, distance and casting time from integer values (60 => 60 ft, 3600 => 1 hour)

# Usage

## Suggested pipeline

1. Get spell `json`s
2. Prepare html template, css and other src (like icons)
3. Import them using `TTRPG_HTB.SpellDatabase` class
    - _(optional)_ Modify Translations for your locale 
4. Modify template using `TTRPG_HTB.template_handler.TemplateHandler`, to set spell attributes
5. Render picture, using `TemplateHandler.render()`


## Example

``` python 

from TTRPG_HTB import SpellDatabase
from TTRPG_HTB.template_handler import TemplateHandler
from TTRPG_HTB.translations import Translations


sdb = SpellDatabase() # Optional, but recommended: instantiate database
sdb.load_spell_from_json('path/to/spell.json') # load individual spell
sdb.load_spell_from_directory('path/to/spell_directory') # load spells in bulk from directory

sdb.process_spells() # populates necessary dictionaries

print(sdb.spells) # prints all loaded spells

cantrips: list[Spell] = sdb.level_to_spells[0]

th = TemplateHandler('path/to/template_directory', Translations)

for spell in spells:
    soup = th.soup
    # set name in template
    th.set_element_text(th.CONSTANT_BOX_NAMES.spell_name, spell.get_name())

    file_name: str = 'build/' + spell.get_file_name() + '.png'
    th.render((800, 400), file_name, custom_css=custom_css)
```

# Documentation
