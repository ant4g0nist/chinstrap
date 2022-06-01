from enum import Enum


class TemplateOptions(Enum):
    jsligo = "JsLIGO"
    pascaligo = "PascaLIGO"
    cameligo = "CameLIGO"
    religo = "ReasonLIGO"
    smartpy = "SmartPy"

    def __str__(self):
        return self.value
