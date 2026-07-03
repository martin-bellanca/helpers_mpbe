#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
Package que guarda constantes generales.\n
B{Created:} 28/04/2013
'''


from enum import IntEnum


# Constantes ------------------------------------------------------------------
DIAM_HIERROS_STR = ["6", "8", "10", "12", "16", "20", "25", "32"]

class ORIENTACION (IntEnum):
    HORIZONTAL = 0
    VERTICAL = 1

    def __str__(self):
        if self.value == 0:
            return "HORIZONTAL"
        else:
            return "VERTICAL"
    
    @staticmethod
    def get_str_list():
        return ["HORIZONTAL", "VERTICAL"]

    @staticmethod
    def get_enum_from_str(txt):
        if txt == "HORIZONTAL":
            return ORIENTACION.HORIZONTAL
        elif txt == "VERTICAL":
            return ORIENTACION.VERTICAL
        else:
            raise ValueError("Error: No existe la constante")


class WITH_TYPE (IntEnum):
    VARIABLE = 0
    FIJO = 1

    def __str__(self):
        if self.value == 0:
            return "VARIABLE"
        else:
            return "FIJO"
    
    @staticmethod
    def get_str_list():
        return ["VARIABLE", "FIJO"]

    @staticmethod
    def get_enum_from_str(txt):
        if txt == "VARIABLE":
            return WITH_TYPE.VARIABLE
        elif txt == "FIJO":
            return WITH_TYPE.FIJO
        else:
            raise ValueError("Error: No existe la constante")


class TIPO_COTA(IntEnum):
    HORIZONTAL = 0
    VERTICAL = 1
    ALINEADA = 2
    
    def __str__(self):
        if self.value == 0:
            return "HORIZONTAL"
        elif self.value == 1:
            return "VERTICAL"
        else:
            return "ALINEADA"
    
    @staticmethod
    def get_str_list():
        return ["HORIZONTAL", "VERTICAL", "ALINEADA"]

    @staticmethod
    def get_enum_from_str(txt):
        if txt == "HORIZONTAL":
            return TIPO_COTA.HORIZONTAL
        elif txt == "VERTICAL":
            return TIPO_COTA.VERTICAL
        elif txt =="ALINEADA":
            return TIPO_COTA.ALINEADA
        else:
            raise ValueError("Error: No existe la constante")
