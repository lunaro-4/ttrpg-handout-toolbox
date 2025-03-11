from TTRPG_HTB.translations import Translations, Translations_1

class CLASS_SUBCLASS_MAP:  
    druid_class_name: str = 'druid'
    druid_archetype_names: dict[str, str] = {
            'circle_of_spores': 'circle_of_spores',
            'circle_of_stars': 'circle_of_stars',
            'circle_of_wildfire': 'circle_of_wildfire',
            'circle_of_the_land': 'circle_of_the_land',

            }
    ranger_class_name: str = 'ranger'
    ranger_archetype_names: dict[str, str] = {
            'drakewarden': 'drakewarden',
            'swarmkeeper': 'swarmkeeper',
            'fey_wanderer': 'fey_wanderer',
            'monster_slayer': 'monster_slayer',
            'gloom_stalker': 'gloom_stalker',
            'horrizon_walker': 'horrizon_walker',
            }
    paladin_class_name: str = 'paladin'
    paladin_archetype_names: dict[str, str] = {
            'oath_of_the_watchers': 'oath_of_the_watchers',
            'oath_of_glory': 'oath_of_glory',
            'oath_of_conquest': 'oath_of_conquest',
            'oath_of_redemption': 'oath_of_redemption',
            'oath_of_the_crown': 'oath_of_the_crown',
            'oathbreaker': 'oathbreaker',
            'oath_of_vengeance': 'oath_of_vengeance',
            'oath_of_the_ancients': 'oath_of_the_ancients',
            'oath_of_devotion': 'oath_of_devotion',
            }
    wizard_class_name: str = 'wizard'
    wizard_archetype_names: dict[str, str] = {
            'graviturgy': 'graviturgy',
            'chronurgy': 'chronurgy',
            }
    fighter_class_name: str = 'fighter'
    fighter_archetype_names: dict[str, str] ={
            'psi_warrior': 'psi_warrior',
            'arcane_archer': 'arcane_archer',
            }
    cleric_class_name: str = 'cleric'
    cleric_archetype_names: dict[str, str] = {
            'twilight_domain': 'twilight_domain',
            'order_domain': 'order_domain',
            'peace_domain': 'peace_domain',
            'grave_domain': 'grave_domain',
            'forge_domain': 'forge_domain',
            'arcana_domain': 'arcana_domain',
            'death_domain': 'death_domain',
            'light_domain': 'light_domain',
            'nature_domain': 'nature_domain',
            'trickery': 'trickery',
            'knowlege_domain': 'knowlege_domain',
            'life_domain': 'life_domain',
            'war_domain': 'war_domain',
            'tempest_domain': 'tempest_domain',

            }
    artificer_class_name: str = 'artificer'
    artificer_archetype_names: dict[str, str] = {
            'armorer': 'armorer',
            'battle_smith': 'battle_smith',
            'artillerist': 'artillerist',
            'alchemist': 'alchemist',
            }
    warlock_class_name: str = 'warlock'
    warlock_archetype_names: dict[str, str] = {
            'undead': 'undead',
            'genie': 'genie',
            'fathomless': 'fathomless',
            'celestial': 'celestial',
            'hexblade': 'hexblade',
            'undying': 'undying',
            'great_old_one': 'great_old_one',
            'fiend': 'fiend',
            'archfey': 'archfey',
            }
    monk_class_name: str = 'monk'
    monk_archetype_names: dict[str, str] = {
            'way_of_sun_soul': 'way_of_sun_soul',

            'way_of_four_elements': 'way_of_four_elements',
            'way_of_shadow': 'way_of_shadow',
            }
    rogue_class_name : str = 'rogue'
    rogue_archetype_names: dict[str, str] = {
            'arcane_trickster': 'arcane_trickster',
            }

    barbarian_class_name: str = 'barbarian'
    barbarian_archetype_names: dict[str, str] = {

            'path_of_the_giant': 'path_of_the_giant',
            }
    sorcerer_class_name: str = 'sorcerer' 
    sorcerer_archetype_names: dict[str, str] = {
            'lunar_sorcery': 'lunar_sorcery',
            'clockwork_soul': 'clockwork_soul',
            'abbrant_mind': 'abbrant_mind',
            'shadow_magic': 'shadow_magic',
            'divine_soul': 'divine_soul',
            }
    bard_class_name: str = 'bard'
    bard_archetype_names: dict[str,str] = {
            'college_of_spirits': 'college_of_spirits',
            }

    @staticmethod
    def get_archetypes_to_classes() -> dict[str, str]:
        outp: dict[str, str] = {}





        return outp

class RussianTranslations_1(Translations_1):
    class Actions(Translations_1.Actions):
        @property
        def bonus_action(self) -> str:
            """The bonus_action property."""
            return "Бонусное действие"
        # bonus_action: str = "Бонусное действие"
        @property
        def action(self) -> str:
            return "Действие"
        @property
        def other(self) -> str:
            return "Особое"

    class Time(Translations_1.Time):
        @property
        def hour(self) -> str:
            return "часов"
        @property
        def minute(self) -> str:
            return "минут"
        @property
        def second(self) -> str:
            return "секунд"
        @property
        def day(self) -> str:
            return "дней"
        @property
        def week(self) -> str:
            return "недель"
        @property
        def month(self) -> str:
            return "месяцев"
        @property
        def other(self) -> str:
            return "Особое"

    class Distance(Translations_1.Distance):
        @property
        def on_self(self) -> str:
            return "На себя"
        @property
        def on_touch(self) -> str:
            return "Касание"
        @property
        def ft(self) -> str:
            return "футов"
        @property
        def other(self) -> str:
            return "Особое"

    class Components(Translations_1.Components):
        @property
        def verbal(self) -> str:
            return "В"
        @property
        def somatic(self) -> str:
            return "С"
        @property
        def material(self) -> str:
            return "М"
        @property
        def material_component_text(self) -> str:
            return "Материальный компонент: "
    @property
    def SPELL_LEVELS(self) -> dict[int, str]:
        return {
            0: "Заговор",
            1: "Уровень I",
            2: "Уровень II",
            3: "Уровень III",
            4: "Уровень IV",
            5: "Уровень V",
            6: "Уровень VI",
            7: "Уровень VII",
            8: "Уровень IIX",
            9: "Уровень IX",
            }



class RussianTranslations(Translations):
    class Actions(Translations.Actions):
        bonus_action: str = "Бонусное действие"
        action: str = "Действие"
        other: str = "Особое"

    class Time(Translations.Time):
        hour: str = "часов"
        minute: str = "минут"
        second: str = "секунд"
        day: str = "дней"
        week: str = "недель"
        month: str = "месяцев"
        other: str = "Особое"

    class Distance(Translations.Distance):
        on_self: str = "На себя"
        on_touch: str = "Касание"
        ft: str = "футов"
        other: str = "Особое"

    class Components(Translations.Components):
        verbal: str = "В"
        somatic: str = "С"
        material: str = "М"
        material_component_text: str = "Материальный компонент: "

    SPELL_LEVELS: dict[int, str]= {
            0: "Заговор",
            1: "Уровень I",
            2: "Уровень II",
            3: "Уровень III",
            4: "Уровень IV",
            5: "Уровень V",
            6: "Уровень VI",
            7: "Уровень VII",
            8: "Уровень IIX",
            9: "Уровень IX",
            }





class BasicTemplateColorschemes:
    circle_of_spores_colorscheme: str = """
    :root {
    --primary-color:#642D0F;
    --secondary-color:#CDA88E;
    --accent-color:#995A39;
    --text-color:#000000
    }

    """
    druid_colorscheme: str = """
    :root {
    --primary-color:#5C2A21;
    --secondary-color:#F7A45E;
    --accent-color:#B25033;
    --text-color:#000000
    }

    """
    warrior_colorscheme: str = """
    :root {
    --primary-color:#923626;
    --secondary-color:#F3F0F8;
    --accent-color:#E1DDE4;
    --text-color:#000000;
    }
    """




