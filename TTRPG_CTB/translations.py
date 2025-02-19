from abc import ABC, abstractmethod

from better_abc import abstract_attribute

class Translations_1(ABC):
    class Actions(ABC):
        @property
        @abstractmethod
        def bonus_action(self) -> str:
            """The bonus_action property."""
            return ""

        @property
        @abstractmethod
        def action(self) -> str:
            """The bonus_action property."""
            return ""
        @property
        @abstractmethod
        def other(self) -> str:
            """The bonus_action property."""
            return ""

    class Time(ABC):
        @property
        @abstractmethod
        def hour(self) -> str:
            """The hour property"""
            return ""
        @property
        @abstractmethod
        def minute(self) -> str:
            """The minute property"""
            return ""

        @property
        @abstractmethod
        def second(self) -> str:
            """The second property"""
            return ""

        @property
        @abstractmethod
        def day(self) -> str:
            """The day property"""
            return ""


        @property
        @abstractmethod
        def week(self) -> str:
            """The week property"""
            return ""

        @property
        @abstractmethod
        def month(self) -> str:
            """The month property"""
            return ""

        @property
        @abstractmethod
        def other(self) -> str:
            """The other property"""
            return ""

    class Distance(ABC):
        @property
        @abstractmethod
        def on_self(self) -> str:
            """The on_self property"""
            return ""

        @property
        @abstractmethod
        def on_touch(self) -> str:
            """The on_touch property"""
            return ""

        @property
        @abstractmethod
        def ft(self) -> str:
            """The ft property"""
            return ""

        @property
        @abstractmethod
        def other(self) -> str:
            """The other property"""
            return ""


    # class SpellLevels:
    #     cantrip: str = "Заговор"
    #     leveled_spell_level: str = "Уровень"
    class Components(ABC):
        @property
        @abstractmethod
        def verbal(self) -> str:
            """The verbal property"""
            return ""

        @property
        @abstractmethod
        def somatic(self) -> str:
            """The somatic property"""
            return ""

        @property
        @abstractmethod
        def material(self) -> str:
            """The material property"""
            return ""

        @property
        @abstractmethod
        def material_component_text(self) -> str:
            """The material_component_text property"""
            return ""



    @property
    @abstractmethod
    def SPELL_LEVELS(self)-> dict[int, str]:
        return {
            0: "",
            1: "",
            2: "",
            3: "",
            4: "",
            5: "",
            6: "",
            7: "",
            8: "",
            9: "",
            }

class Translations(type):

    class Actions(ABC):
        bonus_action: str
        action: str
        other: str
    class Time(ABC):
        hour: str
        minute: str
        second: str
        day: str
        week: str
        month: str 
        other: str 
    class Distance:
        on_self: str 
        on_touch: str 
        ft:str
        other: str

    # class SpellLevels:
    #     cantrip: str = "Заговор"
    #     leveled_spell_level: str = "Уровень"
    class Components:
        verbal: str
        somatic: str
        material: str
        material_component_text: str

    SPELL_LEVELS: dict[int, str]= {
            0: "",
            1: "",
            2: "",
            3: "",
            4: "",
            5: "",
            6: "",
            7: "",
            8: "",
            9: "",
            }
