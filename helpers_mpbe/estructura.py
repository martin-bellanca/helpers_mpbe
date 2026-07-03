# -*- coding: utf-8 -*-


'''
Modulo de funciones comunes de projecto CEH.\n
B{Created:} 23/05/2015
@notas: 
'''


import os
import sys
import shutil
import string
from enum import Enum
# import unicodedata Agregado Python 3
from string import Template
#from jinja2 import Template
import json
# imports de mpbe-helpers ----------------------------------------------------
from helpers_mpbe.python import compose, JsonObject, Report


class STATE_VERIFICATION(Enum):
    NO_APLICA = 'No_Aplica'
    RECALCULAR = 'Recalcular'
    VERIFICA = 'Verifica'
    NO_VERIFICA = 'No Verifica'
    ERROR = 'Error'

    def describe(self):
        # self is the member here
        return self.name, self.value

    def __str__(self):
        return '{0}'.format(self.value)

    @staticmethod
    def get_str_list():
        return ["No_Apilca", "Recalcular", "Verifica", "Error"]

    @staticmethod
    def get_enum_from_str(txt):
        if txt == "NO_APLICA":
            return STATE_VERIFICATION.NO_APLICA
        elif txt == "RECALCULAR":
            return STATE_VERIFICATION.RECALCULAR
        elif txt == "VERIFICA":
            return STATE_VERIFICATION.VERIFICA
        elif txt == "ERROR":
            return STATE_VERIFICATION.ERROR
        else:
            raise ValueError("Error: No existe la constante")


class StateVerification(JsonObject):
    '''
    Clase que define un estado de verificacion que se transfiere a la clase padre
    @type state: mpbe.helpers.const.STATE_VERIFICATION
    @type note: Texto sobre el estado de la verificacion
    @version: 1.0 20/09/13
    '''

    def __init__(self, estado=STATE_VERIFICATION.RECALCULAR, note=''):
        self._estado = compose(estado, STATE_VERIFICATION)
        self.note = note

    """ Propiedades ----------------------------------------------------------"""
    def _getState(self):
        return self._estado
    def _setState(self, value):
        self._estado = compose(value, STATE_VERIFICATION)
    state = property(fget = _getState, fset = _setState, doc = "estado")

    """ Funciones de la clase ------------------------------------------------"""
    def setState(self, value, note=''):
        self._estado = compose(value, STATE_VERIFICATION)
        self.note = note

    def setStateFromText(self, text):
        if text == 'No_Aplica': res = STATE_VERIFICATION.NO_APLICA
        elif text == 'Recalcular': res = STATE_VERIFICATION.RECALCULAR
        elif text == 'Verifica': res = STATE_VERIFICATION.VERIFICA
        elif text == 'No Verifica': res = STATE_VERIFICATION.NO_VERIFICA
        elif text == 'Error': res = STATE_VERIFICATION.ERROR
        else: raise Exception('valor invalido')
        return res

    def toString(self):
        return self._estado.value

    def copy(self):
        return StateVerification(self._estado, self.note)

    """ Funcion JSON ---------------------------------------------------------"""
    def toDict(self):
        '''Devuelve un diccionario con los campos de la clase'''
        di = {}
        di["estado"] = self._estado.value
        di["nota"] = self.note
        return di
    
    def fromDict(self, di):
        '''Coloca los items del diccionario en la clase'''
        try:
            self._estado = self.setStateFromText(di["estado"])
            self.note = di["nota"]
        except:
            return "001" # ERROR al leer el estado


class ReportVerification(Report):
    '''
    Clase donde guardar los resutados de la verificacion y crear los informes
    @version: 1.00 10/05/15
    @ivar estado: Clase que indica el estado de la verificacion
    @type estado: mpbe.helpers.python.State_Verification()
    @ivar variables: Diccionario con la informacion del calculo
    @type variables: dict()
    @ivar opciones: Diccionario con opciones del calculo y del informe
    @type opciones: dict()
    '''
    def __init__(self, estado=StateVerification(),
                 variables=dict(), opciones=dict(),
                 report_html=None, report_txt=None,
                 notes_html="", notes_txt=""):
        Report.__init__(self, variables, opciones, report_html, report_txt, notes_html, notes_txt)
        self.estado = estado
        
    """ Funciones de la clase ------------------------------------------------"""
    def copy(self):
        return ReportVerification(self.estado.copy(), self.variables.copy(), self.opciones.copy(),
                      self.report_html, self.report_txt, self.notes_html, self.notes_txt)

    def clear(self):
        Report.clear(self)
        self.estado.state = STATE_VERIFICATION.RECALCULAR

    def setReportFromTemplate(self, plt_html=None, plt_txt=None):
        di = {'estado':self.estado.toString()}
        for cl, va in self.variables.items():
            di[cl] = va
        for cl, va in self.opciones.items():
            di[cl] = va
        if compose(plt_html, str):
            self.report_html = Template(plt_html).safe_substitute(di)
        else:
            self.report_html = ""
        if compose(plt_txt, str):
            self.report_txt = Template(plt_txt).safe_substitute(di)
        else:
            self.report_txt = ""

    """ Funciones JSON -------------------------------------------------------"""
    def toDict(self):
        '''Devuelve un diccionario con los campos de la clase'''
        di = Report.toDict(self)
        di["estado"]=self.estado.toDict()
        return di
    
    def fromDict(self, di):
        '''Coloca los items del diccionario en la clase'''
        try:
            self.estado.fromDict(di["estado"])
            Report.fromDict(self, di)
        except:
            return 100002 # ERROR al leer el resultado de la verificacion


class BaseVerification(object):
    def __init__(self, plt_html="", plt_txt="", info_html=""):
        self.plt_html = plt_html  # Plantilla para mostrar el resultado en html
        self.plt_txt = plt_txt  # Plantilla para mostrar el resultado en txt
        self.info_html = info_html  # Informacion sobre el proceso de calculo

    def verificarSeccion(self, unidades, seccion, opciones=dict(), avance = 0):
        raise NotImplementedError("Should have implemented this")


""" Clases de la Integral de Area de Seccion_Hormigon()"""
class FuncionDeIntegral ():  # Ex. Funcion_Area
    '''Clase abstracta para definir funciones para incorporar a la integral de area.
    @ivar sum: valor a sumar al diferencial de la integral
    @type sum: double
    '''
    def __init__(self):
        self.sum = 0

    def ejecutar(self, y, b, h):
        ''' Funcion que devuelve un multiplicador a aplicar a la integral.
        @var y: Posicion vertical del diferecial de calculo
        @type y: double
        @var b: Ancho. Longitud de la franja
        @type b: double
        @var h: Altura del diferencial. Igual al valor de intervalo de calculo.
        '''
        raise NotImplementedError("Should have implemented this")


class FuncionA (FuncionDeIntegral):
    ''' Clase que aplicada a hormigon.integral_de_area devuelve el area de la seccion.'''
    def ejecutar(self, y, b, h):
        return 1.0


class FuncionMtoEstatico (FuncionDeIntegral):
    ''' Clase que aplicada a hormigon.integral_de_area devuelve el Mto Estatico de la Seccion.'''
    def ejecutar(self, y, b, h):
        ''' Funcion que devuelve un multiplicador a aplicar a la integral.
        @var y: Posicion vertical del diferecial de calculo
        @type y: double
        @var b: Ancho. Longitud de la franja
        @type b: double
        @var h: Altura del diferencial. Igual al valor de intervalo de calculo.
        '''
        return y


class FuncionInercia (FuncionDeIntegral):
    '''Clase que aplicada a hormigon.integral_de_area devuelve Inercia de la Seccion.'''
    def ejecutar(self, y, b, h):
        ''' Funcion que devuelve un multiplicador a aplicar a la integral.
        @var y: Posicion vertical del diferecial de calculo
        @type y: double
        @var b: Ancho. Longitud de la franja
        @type b: double
        @var h: Altura del diferencial. Igual al valor de intervalo de calculo.
        '''
        self.sum = b * h ** 3 / 12
        return y ** 2

