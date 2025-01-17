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
