from dataclasses import dataclass


@dataclass
class Breadcrumb:
    title: str
    url: str = None


@dataclass
class TitleButton:
    label: str
    url: str
    target: str = ""
    button_class: str = "light"


@dataclass
class NavigationItem:
    name: str
    url: str
    help_text: str = ""


@dataclass
class NavigationDivider:
    pass


@dataclass
class NavigationGroup:
    name: str
    items: list[NavigationItem | NavigationDivider]
    help_text: str = ""
