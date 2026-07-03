# -*- coding: utf-8 -*-


'''
Modulo de clases para calculos geometricos.\n
B{Created:} 10/09/2013
@note: Agregado de estado a Parametro
'''

import math
from array import array
from helpers_mpbe import const
from helpers_mpbe.python import ObjectLst
from helpers_mpbe.python import JsonObject
from helpers_mpbe.const import ORIENTACION, TIPO_COTA



class Punto(ObjectLst, JsonObject):
    '''
    Define punto basico
    @version: 1.0 15/09/13

    @ivar x: Coordenada X del punto
    @type x: double

    @ivar y: Coordenada Y del punto
    @type y: double
    '''

    # Constructores
    def __init__(self, x=0.0, y=0.0, id:int=-1):
        self.id = id
        self.x = x
        self.y = y

    """ Funciones sobre el punto -----------------------"""
    def mover(self, x, y):
        '''
        Devuelve un punto trasladado las distancias indicadas el punto
        @param x: Desplazamiento X
        @param y: Desplazamiento Y
        @return: Punto()
        '''
        return Punto(self.x + x, self.y + y)

    def rotar(self, origen, angulo):
        '''
        Devuelve un punto trasladado rotado alrededor del punto origen el angulo indicado
        @return: Punto()
        '''
        new_x = (self.x - origen.x) * math.cos(angulo) - (self.y-origen.y) * math.sin(angulo) + origen.x
        new_y = (self.y - origen.y) * math.cos(angulo) + (self.x-origen.x) * math.sin(angulo) + origen.y
        return Punto(new_x, new_y)

    def distancia(self, p2):
        '''
        Devuelve la distancia al punto ingresado
        @param p2: Punto a calcular la distancia
        @type p2: mpbe.Geometria.Punto
        '''
        return math.sqrt(math.pow((p2.x - self.x), 2) + math.pow((p2.y - self.y), 2))

    def into_rectangulo(self, pi:tuple, pf:tuple):
        '''Devuelve True si el punto esta dentro del rectangulo'''
        if (pi[0]>self.x>pf[0] or pi[0]<self.x<pf[0]) and (pi[1]>self.y>pf[1] or pi[1]<self.y<pf[1]):
            return True
        else:
            return False

    def set_nulo(self):
        '''Carga un punto nulo'''
        self.x = 0
        self.y = 0

    def isNulo(self):
        return self.x == 0.0 and self.y == 0.0

    def set_unitario(self):
        '''Carga un punto unitario'''
        self.x = 1
        self.y = 1

    def copy(self):
        return Punto(self.x, self.y, self.id)

    def copy_into(self, punto):
        '''
        Copia el punto
        @param punto: variable de salida
        '''
        punto.id = self.id
        punto.x = self.x
        punto.y = self.y

    """ Geters and Seters ------------------------------"""
    def set(self, x, y):
        '''Carga los valores x,y en el puento'''
        self.x = x
        self.y = y

    def get(self):
        return self

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y

    def set_id(self, id:int):
        self.id = id

    def get_id(self):
        return self.id

    """ Funciones derivadas de ObjectLst ------------------------------------"""
    def get_tupla(self):
        '''Devuelve una tupla con las coordenadas [x, y] del punto'''
        return (self.x, self.y)
    
    def get_list(self):
        '''Devuelve una lista con las coordenadas [x, y] del punto'''
        return [self.x, self.y]

    def set_list(self, lst):
        '''Coloca los items de la lista en la carga.
        La lista debe tener el siguiente formato:
        X, Y
        0  1'''
        self.x = lst[0]
        self.y = lst[1]

    def set_col_value(self, col, value):
        """set_col_value(int col, object value)
        colocar el valor en la columna indicada"""
        if col == 0:
            self.x = value
        elif col == 1:
            self.y = value

    """ Funciones JSON ------------------------------------------------------"""
    def toDict(self):
        '''Devuelve un diccionario con los campos de la clase'''
        di = {}
        di["id"] = self.id
        di["x"] = self.x
        di["y"] = self.y
        return di

    def fromDict(self, di):
        try:
            self.id = di["id"]
            self.x = di["x"]
            self.y = di["y"]
        except:
            pass

    """ Sobre carga de operadores -------------------------------------------"""
    def __add__(self, punto):
        '''Operador de Adicion'''
        return Punto(self.x+punto.x, self.y+punto.y)

    def __mul__(self, value):
        return Punto(self.x * value, self.y *value)

    def __str__(self, *args, **kwargs):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


class Limites (JsonObject):
    '''
    Define limites sup e inf
    @version: 1.0 15/09/13

    @ivar min: Valor minimo del limite
    @ivar max: Valor Maximo del limite
    '''
    def __init__(self, minimo=0, maximo=0):
        self.min = minimo
        self.max = maximo

    """ Funciones internas -----------------------------"""
    def set_limites(self, minimo, maximo):
        self.min = minimo
        self.max = maximo

    def set_limites_punto(self, punto):
        self.min = punto.getX()
        self.max = punto.getY()

    def get_punto(self):  # Ex getValor()
        return Punto(self.min, self.max)

    def get_longitud(self):
        return (self.max - self.min)

    def get_baricentro(self):
        return (self.max + self.min)/2

    def in_to(self, valor:float):
        '''
        Devuelve True y el valor se encuentra dentro de los limites en caso
        contrario devuelve False 
        @return: boolean
        '''
        if self.min < valor < self.max:
            return True
        else:
            return False

    def copy(self):  # Ex getLimite
        return Limites(self.min, self.max)

    def copy_into(self, limite):
        limite.max = self.max
        limite.min = self.min

    """ Operaciones ----------------------------------------------------------"""
    def agrandar(self, valor):
        self.min -= valor
        self.max += valor

    def escalar(self, valor):
        self.min *= valor
        self.max *= valor
        
    """ Funciones JSON -------------------------------------------------------"""
    def toDict(self):
        '''Devuelve un diccionario con los campos de la clase'''
        di = {}
        di["min"] = self.min
        di["max"] = self.max
        return di

    def fromDict(self, di):
        try:
            self.min = di["min"]
            self.max = di["max"]
        except:
            pass


class LineaGuia (ObjectLst, JsonObject):
    '''
    Define una linea horizontal o vertical
    @version: 1.0 15/09/13

    @ivar posicion: Coordenada de ubicacion de la linea
    @type pisicion: float

    @ivar orientacion: Indica la si la linea es vertical u horizontal
    @type orientacion: mpbe.helpers.const.ORIENTACION (puede ser Vertical u Horizontal)

    @ivar visible: Indica si la linea se encuentra visible
    @type visible: boolean
    '''

    def __init__(self, orientacion=const.ORIENTACION.HORIZONTAL, posicion=0.0, visible=True, id=None):
        '''Constructor'''
        self.id = id
        self.posicion = posicion
        self.orientacion = orientacion
        self.visible = visible

    """ Setters and Getters ----------------------------"""
    def get_pos(self):
        return self.posicion

    def set_pos(self, posicion):
        self.posicion = posicion

    def get_orientacion(self):
        '''@return: mpbe.helpers.const.ORIENTACION (Puede ser Vertical u Horizontal)'''
        return self.orientacion

    def set_orientacion(self, orientacion):
        '''@type orientacion: mpbe.helpers.const.ORIENTACION (Puede ser Vertical u Horizontal)'''
        self.orientacion = orientacion

    def is_visible(self):
        '''@return: boolean'''
        return self.visible

    def set_visible(self, visible):
        '''@type visible: boolean'''
        self.visible = visible

    """ Funciones derivadas de ObjectLst ------------------------------------"""
    def get_list(self):
        '''Devuelve una lista varialbes de la clase
        0           | 1        | 2
        Orientacion | Posicion | Visible'''
        return [self.orientacion.name, self.posicion, self.visible]

    def set_list(self, lst):
        '''Coloca los items de la lista varialbes de la clase.
        La lista debe tener el siguiente formato:
        0           | 1        | 2
        Orientacion | Posicion | Visible'''
        if lst[0] == 'HORIZONTAL':
            self.orientacion = const.ORIENTACION.HORIZONTAL
        elif lst[0] == 'VERTICAL':
            self.orientacion = const.ORIENTACION.VERTICAL
        self.posicion = lst[1]
        self.visible = lst[2]

    def set_col_value(self, col, value):
        """set_col_value(int col, object value)
        colocar el valor en la columna indicada"""
        if col == 0:
            if value == 'HORIZONTAL':
                self.orientacion = const.ORIENTACION.HORIZONTAL
            elif value == 'VERTICAL':
                self.orientacion = const.ORIENTACION.VERTICAL
        elif col == 1:
            self.posicion = value
        elif col == 2:
            self.visible = value

    """ Funcion JSON --------------------------------------------------------"""
    def toDict(self):
        '''Devuelve un diccionario con los campos de la clase'''
        di = {}
        di['posicion'] = self.posicion
        di['orientacion'] = self.orientacion.name
        di['visible'] = self.visible
        return di

    def fromDict(self, di):
        '''Coloca los items del diccionario en la clase'''
        try:
            self.posicion = di['posicion']
            self.visible = di['visible']
            name = di['orientacion']
            if name == 'HORIZONTAL':
                self.orientacion = ORIENTACION.HORIZONTAL
            elif name == 'VERTICAL':
                self.orientacion = ORIENTACION.VERTICAL
            else:
                raise AttributeError("can't set attribute")
        except:
            print("Error: fromDict de la linea guia")

    """ Funciones de la clase -----------------------------------------------"""
    def __str__(self, *args, **kwargs):
        return "{oo:^11s} | {po:+4.2f} | {vi:b}".format(oo=self.orientacion.name, po=self.posicion, vi=self.visible)
    
    def copy(self):
        '''@return: mpbe.Geometria.LineaGuia()'''
        oo = ORIENTACION.HORIZONTAL if self.orientacion.value == 0 else ORIENTACION.VERTICAL
        return LineaGuia(oo, self.posicion, self.visible)

    """ Funciones de la Recta -----------------------------------------------"""
    def distancia(self, punto):
        '''Devuelde la menor distancia del punto a la recta.
        @return: double'''
        if self.orientacion.name == 'HORIZONTAL':
            return math.fabs(self.posicion - punto.y)
        elif self.orientacion.name == 'VERTICAL':
            return math.fabs(self.posicion - punto.x)
        else:
            raise ValueError ("ERROR: Valor de orientacion erronea")


class Parametro (ObjectLst):
    '''
    Define un parametro
    @version: 1.0 15/09/13

    @ivar designacion: Texto que describe el parametor
    @ivar valor: guarda el valor del parametro
    @ivar valor_dfault: guarda el valor por defecto del paramatro para el blanqueo
    @ivar acceso: Indica si es el parametro es de solo lectura o lectura escritura
    @type acceso: string
    '''

    def __init__(self, designacion="Nueva Propiedad", valor=0, valor_default=0, flag=None, acceso='RW'):
        '''Constructor'''
        self.designacion = designacion
        self.valor = valor
        self.valor_default = valor_default
        self.flag = flag
        self.acceso = acceso

    """ Setters and Getters ----------------------------"""
    def set(self, designacion, valor, valor_def, flag=None, acceso='RW'):
        self.designacion = designacion
        self.valor = valor
        self.valor_default = valor_def
        self.flag = flag
        self.acceso = acceso

    def set_valor_default(self):
        self.valor = self.valor_default

    def copy(self):
        return Parametro(self.designacion, self.valor, self.valor_default, self.flag, self.acceso)

#     def copy_into(self, parametro):
#         '''Copia los valores del parametro actual en parametro'''
#         parametro = self.copy()

    def __str__(self, *args, **kwargs):
        return self.designacion +"=" + str(self.valor)

    """ Funciones derivadas de ObjectLst -------------------------------------"""
    def get_list(self):
        '''Devuelve una lista con los campos de la carga en el siguiente orden:
        
                0                  1            2                    3'''
        return [self.designacion, self.valor, self.valor_default, self.flag, self.acceso]

    def set_list(self, lst):
        '''Coloca los items de la lista en la carga.
        La lista debe tener el siguiente formato:
        designacion, valor, valor_default, acceso
        0            1      2              3'''
        self.designacion = lst[0]
        self.valor = lst[1]
        self.valor_default = lst[2]
        self.flag = lst[3]
        self.acceso = lst[4]

    def set_col_value(self, col, value):
        """set_col_value(int col, object value)
        colocar el valor en la columna indicada"""
        rt = False
        if col == 0:
            self.designacion = value
            rt = True
        elif col == 1:
            self.valor = value
            rt = True
        elif col == 2:
            self.valor_default = value
            rt = True
        elif col == 3:
            self.flag = value
            rt = True
        elif col == 4:
            self.acceso = value
            rt = True
        return rt

    """ Funciones JSON -------------------------------------------------------"""
    def toDict(self):
        '''Devuelve un diccionario con los campos de la clase'''
        di = {}
        di["designacion"] = self.designacion
        di["valor"] = self.valor
        di["valor_default"] = self.valor_default
        di["flag"] = self.flag
        di["acceso"] = self.acceso
        return di

    def fromDict(self, di):
        try:
            self.designacion = di["designacion"]
            self.valor = di["valor"]
            self.valor_default = di["valor_default"]
            self.flag = di["flag"]
            self.acceso = di["acceso"]
        except:
            pass


class Rectangulo(object):
    '''
    Define un rectangulo
    @version: 1.00 08/04/17
    @ivar x: Coordenada X del vertice inferior izquierdo del rectangulo
    @type x: double
    @ivar y: Coordenada Y del vertice inferior izquierdo del rectangulo
    @type y: double
    @ivar ancho: ancho del rectangulo
    @type ancho: double
    @ivar alto: alto del rectangulo
    @type alto: double
    @ivar angulo: Agulo recpecto a la horizontal del rectangulo
    @type angulo: double
    '''
    def __init__(self, x, y, ancho, alto, angulo=0.00):
        
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.angulo = angulo
    
    """ Geters and Setters -----------------------------"""
    def set(self,x ,y, ancho, alto, angulo=0.00):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.angulo = angulo
        
    def get(self):
        return self.x, self.y, self.ancho, self.alto, self.angulo
    
    def set_from_puntos(self, p1, p2):
        '''Genera el rectangulo a partir de 2 puntos diagonales. Supone el angulo = 0.0'''
        self.x = p1.x
        self.y = p1.y
        self.ancho = p2.x - p1.x
        self.alto = p2.y - p1.y
        self.angulo = 0.0
        return True
        
    def set_from_list2(self, lst1, lst2):
        '''Genera el rectangulo a partir de 2 listas o tuplas de 2 elementos. 
        Supone el angulo = 0.0'''
        try:
            self.x = lst1[0]
            self.y = lst1[1]
            self.ancho = lst2[0] - lst1[0]
            self.alto = lst2[1] - lst1[1]
            self.angulo = 0.0
            return True
        except:
            return False
        
    def set_from_list(self, lst):
        '''Genera el rectangulo a partir de una lista o tupla de 4 elementos
        0:x, 1:y, 2:ancho, 3:alto 4:angulo
        Si la lista es de 4 elementos el angulo se establece en 0.0'''
        try:
            self.x = lst[0]
            self.y = lst[1]
            self.ancho = lst[2]
            self.alto = lst[3]
            if len(lst) == 5:
                self.angulo = lst[4]
            else:
                self.angulo = 0.0
            return True
        except:
            return False
        
    def set_from_recta_diagonal(self, recta):
        '''Genera el rectangulo a partir de la recta diagonal del rectangulo.
        Supone el angulo = 0.0'''
        self.set_puntos(recta.pi, recta.pf)    
        
    def set_from_limites(self, lim_h:Limites(), lim_v:Limites(), angulo:float=0.0):
        '''Genera el rectangulo a partir de un limite vertical y uno horizontal'''
        self.x = lim_h.min
        self.y = lim_v.min
        self.angulo = angulo
        self.ancho = lim_h.get_longitud()
        self.alto = lim_v.get_longitud()
    
    def set_from_3puntos(self, p1:Punto(), p2:Punto(), p3:Punto()):
        '''Genera el rectangulo tomando p1 como punto inicial, el ancho como la recta p1-p2,
        el alto la distancia de p3 a p1-p2 y el angulo de la recta p1-p2'''
        r = Recta(p1, p2)
        self.x = p1.x
        self.y = p1.y
        self.ancho = r.get_radio_vector()
        self.alto = r.distancia(p3)
        self.angulo = r.get_angulo()

    def set_from_2puntos(self, p1:Punto(), p2:Punto(), h:float):
        '''Genera el rectangulo tomando p1 como punto inicial, el ancho como la recta p1-p2,
        el alto la distancia de p3 a p1-p2 y el angulo de la recta p1-p2'''
        r = Recta(p1, p2)
        self.x = p1.x
        self.y = p1.y
        self.ancho = r.get_radio_vector()
        self.alto = h
        self.angulo = r.get_angulo()

    def get_2puntos(self):
        '''Retorna 2 puntos con los puntos diagonales del rectangulos si
        el angulo es 0.0 en caso contrario retorna None
        @return: Punto(), Punto()'''
        if self.angulo == 0.0:
            return Punto(self.x, self.y), Punto(self.x+self.ancho, self.y+self.alto)
        else:
            return None

    def get_vertices(self):
        '''Retorna una lista de 4 puntos que son los vertices del rectangulo en sentido horario
        @return: Punto(), Punto(), Punto(), Punto()'''
        p1 = Punto(self.x, self.y)
        r1 = Recta().set_long_ang(p1, self.ancho, self.angulo)
        p4 = r1.pf
        an = self.angulo + math.pi / 2
        r2 = Recta().set_long_ang(p1, self.alto, an)
        p2 = r2.pf
        r3 = Recta().set_long_ang(p4, self.alto, an)
        p3 = r3.pf
        return [p1, p2, p3, p4]

    def get_parametros(self):
        '''Retorna una tupla de 5 elementos con los parametros del rectangulo
        (x, y, ancho, alto, angulo)
        @return: list()'''
        return (self.x, self.y, self.ancho, self.alto, self.angulo)

    """ Delegados --------------------------------------"""
    def copy_into(self, rec):
        '''
        @type rec: mpbe.Geometria.Rectangulo()
        '''
        rec.x = self.x
        rec.y = self.y
        rec.ancho = self.ancho
        rec.alto = self.alto
        rec.angulo = self.angulo
        
    def copy(self):
        '''@return: mpbe.Geometria.Rectangulo()'''
        return Rectangulo(self.x, self.y, self.ancho, self.alto, self.angulo)
    
    """ Funciones sobre el Rectangulo ----------------------"""
    def get_apect(self):
        '''Relacion ancho/alto del rectangulo
        @return: double'''
        return math.fabs(self.ancho)/math.fabs(self.alto)

    def get_limites(self):
        '''Retorna los limites horizontal y vertical a partir del rectangulo
        @return: Recta()'''
        lst = self.get_4puntos()
        xma = xmi = yma = ymi = 0
        for pp in lst:
            if pp.x < xmi:
                xmi = pp.x
            if pp.x > xma:
                xma = pp.x
            if pp.y < ymi:
                ymi = pp.y
            if pp.y > yma:
                yma = pp.y
        return Limites(xmi, xma), Limites(ymi, yma)

    def mover(self, delta_x:float=0.0, delta_y:float=0.0):
        '''
        Devuelve un rectangulo trasladado los valores indicados
        @return: Retangulo
        '''
        return Rectangulo(self.x + delta_x, self.y + delta_y,
                          self.ancho, self.alto, self.angulo)

    def rotar(self, centro:Punto(), angulo:float):
        '''
        Devuelve un rectangulo rotado el angulo indicado respecto a centro
        @return: Rectangulo()
        '''
        lst = self.get_vertices()
        for pp in lst:
            pp.rotar(centro, angulo)
        return Rectangulo().set_from_2puntos(lst[0], lst[3], self.alto)
    
    def rotar_a_horiz(self):
        '''
        Devuelve un rectangulo rotado sobre p1 hasta la horizontal
        @return: Rectangulo()
        '''
        return Rectangulo(self.x, self.y, self.ancho, self.alto, 0.00)

    def in_to(self, p:Punto()):
        '''
        Devuelve True si el punto esta dentro del rectangulo y False en caso contrario
        @return: boolean
        '''
        po = p.mover(-self.x, -self.y)
        ro = self.mover(-self.x, -self.y)
        pr = po.rotar(Punto(0.,0.), -self.angulo)
        rr = ro.rotar_a_horiz()
        lh, lv = rr.get_limites()
        if lh.in_to(pr.x) and lv.in_to(pr.y):
            return True
        else:
            return False    


class Vector (object):
    '''
    Define un vector
    @version: 1.01 08/04/17

    @ivar x: Coordenada X del vector
    @type x: double

    @ivar y: Coordenada Y del vector
    @type y: double
    '''

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    """ Geters and Setters -----------------------------"""
    def getPunto(self):
        '''Transforma el vector en un punto'''
        return Punto(self.x, self.y)

    def setNulo(self):
        self.x = 0
        self.y = 0

    def setUnitario(self):
        self.x = 1
        self.y = 1

    def set(self, x, y):
        self.x = x
        self.y = y

    def set_punto(self, punto):
        '''@type punto: mpbe.Geometria.Punto()'''
        self.x = punto.getX()
        self.y = punto.getY()

    def set_to_puntos(self, p1:Punto, p2:Punto):
        self.x = p2.x - p1.x
        self.y = p2.y - p1.y
        
    def set_to_rectangulo(self, rec:Rectangulo):
        self.x = rec.ancho
        self.y = rec.alto

    def get_signoX(self):
        '''
        Devuelve el signo del eje X del vector
        @return: int
        '''
        return (self.x / math.fabs(self.x))

    def get_signoY(self):
        '''
        Devuelve el signo del eje Y del vector
        @return: int
        '''
        return (self.y / math.fabs(self.y))

    def is_Nulo(self):
        if self.x == 0 and self.y == 0:
            return True
        else:
            return False

    """ Delegados --------------------------------------"""
    def copy_into(self, vector):
        '''
        @type vector: mpbe.Geometria.Vector()
        '''
        vector.x = self.x
        vector.y = self.y

    """ Fundiones JSON ---------------------------------"""
    """
    public void put_JSON(JSONObject jo){
        X = (Double) jo.get("X");
        Y = (Double) jo.get("Y");
    }
    public JSONObject get_JSONObject() {
        JSONObject jo = new JSONObject();
        jo.put("X", X);
        jo.put("Y", Y);
        return jo;
    }
    public String get_JSONString() {
        String res = "{\"X\":"+X+", ";
        res += "\"Y\":"+Y+"}";
        return res;
    }
    """

    """ Funciones sobre el vector ----------------------"""
    def get_radio_vector(self):
        '''
        Calcula la longitud del vector
        @return: double'''
        return (math.sqrt(self.x * self.x + self.y * self.y))

    def get_angulo(self):
        '''
        Devuelve el angulo del vector en radiantes respecto a la horizontal
        @return: double'''
        return math.atan2(self.y, self.x)

    def get_cuadrante(self):
        '''
        Calcula el cuadrante donde se encuentra el vector
        1: sup-der
        2: sup-izq
        3: inf-izq
        4: inf-der
        @return: int'''
        a = self.get_angulo()
        if 0 <= a < math.pi/2:
            return 1
        elif math.pi/2 <= a < math.pi:
            return 2
        elif math.pi <= a < math.pi * 3 / 2:
            return 3
        elif math.pi * 3 / 2 <= a < math.pi * 2:
            return 4 

    def get_director(self, x, y):
        '''
        @return: mpbe.Geometria.Vector()
        @type X: double
        @type Y: double
        '''
        hip = self.get_radio_vector()
        return Vector(x / hip, y / hip)

    def rotar(self, angulo_rad):
        '''
        @return: mpbe.Geometria.Vector()
        @type angulo_rad: double
        '''
        r = self.get_radio_vector()
        alf = math.atan2(self.y, self.x) - math.pi / 2
        return Vector((math.sin(alf) * r), (math.cos(alf) * r))

    def rotar_centro(self, centro, angulo_rad):
        '''
        @return: mpbe.Geometria.Vector()
        @type centro: mpbe.Geometria.Punto()
        @type angulo_rad: double
        '''
        p = Vector(self.x - centro.x, self.y - centro.y)
        p = p.rotar(angulo_rad)
        return Vector(centro.x + p.x, centro.y + p.y)

    def perpendicular(self):
        '''
        @return: mpbe.Geometria.Vector()
        '''
        return Vector(self.y, -self.x)

    def mover(self, x, y):
        '''
        @return: mpbe.Geometria.Vector()
        @type x: double
        @type y: double
        '''
        return Vector(self.x + x, self.y + y)

    def escalar(self, valor):
        '''
        @return: mpbe.Geometria.Vector()
        @type valor: double
        '''
        return Vector(self.x * valor, self.y * valor)

    def escalar_x_y(self, valorX, valorY):
        '''
        @return: mpbe.Geometria.Vector()
        @type valorX: double
        @type valorY: double
        '''
        return Vector(self.x * valorX, self.y * valorY)
    
    def __add__(self, vv):
        '''Suma de Vectores'''
        return Vector(self.x+vv.x, self.y+vv.y)


class Recta (object):
    '''
    Define una recta basica
    @version: 1.0 16/09/13

    @ivar pi: Punto inicial de la recta
    @type pi: mpbe.Geometria.Punto()

    @ivar pf: Punto final de la recta
    @type pf: mpbe.Geometria.Punto()
    '''

    def __init__(self, pi=Punto(), pf=Punto()):
        self.pi = pi
        self.pf = pf

    """ Setters and Getters ----------------------------"""
    def set_long_ang(self, pi:Punto(), long:float, angulo:float):
        '''Genera la recta a partir de pi, la longitud y el angulo respecto a la horizontal'''
        self.pi = pi
        if long != 0:
            dx = math.cos(angulo) * long
            dy = math.sin(angulo) * long
            self.pf = Punto(pi.x+dx, pi.y+dy)
        else:
            self.pf = pi.copy()

    def set_tupla(self, t1 , t2):
        self.pi.x = t1[0]
        self.pi.y = t1[1]
        self.pf.x = t2[0]
        self.pf.y = t2[1]

    def set_coord(self, xi , yi, xf , yf):
        self.pi.x = xi
        self.pi.y = yi
        self.pf.x = xf
        self.pf.y = yf

    def get_punto_inicial(self):
        '''@return: double'''
        return self.pi

    def set_punto_inicial(self, pi=Punto()):
        '''@type pf: mpbe.Geometria.Punto()'''
        self.pi = pi

    def get_punto_final(self):
        '''@return: double'''
        return self.pf

    def set_punto_final(self, pf=Punto()):
        '''@type pf: mpbe.Geometria.Punto()'''
        self.pf = pf

    def get_delta_X(self):
        '''@return: double'''
        return (self.pf.x - self.pi.x)

    def get_delta_Y(self):
        '''@return: double'''
        return (self.pf.y - self.pi.y)

    def get_radio_vector(self):
        '''@return: double'''
        return (math.sqrt(math.pow(self.get_delta_X(), 2) + math.pow(self.get_delta_Y(), 2)))

    def get_longitud(self):
        self.get_radio_vector()

    def get_angulo(self):  # OK. Testeado
        '''Devuelve el angulo en radianes respecto a la horizontal'''
        dx = self.get_delta_X()
        dy = self.get_delta_Y()
        rv = self.get_radio_vector()
        se = dy/rv
        co = dx/rv
        if dx>0 and dy>=0:  # Cuadrante 1
            an = math.asin(se)
        elif dx<=0 and dy>0:  # Cuadrante 2
            an = math.pi - math.asin(se)
        elif dx<0 and dy<=0:  # Cuadrante 3
            an = math.pi - math.asin(se)
        else:  # Cuadrante 4
            an = 2 * math.pi - math.acos(co)
        return an

    def get_vector(self):
        '''@return: mpbe.Geometria.Vector()'''
        return Vector(self.get_delta_X(), self.get_delta_Y())

    def get_normal(self):
        '''@return: mpbe.Geometria.Vector()'''
        return Vector(self.get_delta_Y(), -1 * self.get_delta_X())

    def get_director(self):
        '''@return: mpbe.Geometria.Vector()'''
        return Vector(self.get_delta_X() / self.get_radio_vector(), self.get_delta_Y() / self.get_radio_vector())

    def get_director_normal(self):
        '''@return: mpbe.Geometria.Vector()'''
        if self.get_radio_vector():
            return Vector(self.get_delta_Y() / self.get_radio_vector(), -1 * self.get_delta_X() / self.get_radio_vector())
        else:
            return 0

    def get_Y(self, X):
        '''@return: double'''
        dx = self.get_delta_X()
        dy = self.get_delta_Y()
        if (dx != 0):
            return (X - self.pi.x) * dy / dx + self.pi.y
        elif (X == self.pi.x):
            return 0
        else:
            return float('Inf')  # retorna un valor infinito

    def get_punto_interior(self, distancia):
        '''
        Devuelve un punto ubicado a la distancia indicada desde el punto inicial
        sobre la recta
        @ivar distancia: distancia sobre la recta desde el punto inicial
        '''
        an = self.get_angulo()
        pp = Punto(self.pi.x+distancia, self.pi.y)
        return pp.rotar(self.pi, an)

    def get_punto_medio(self):
        return Punto((self.pi.x+self.pf.x)/2, (self.pi.y+self.pf.y)/2)

    def copy_into(self, recta):
        '''@return: mpbe.Geometria.Recta()'''
        recta.pi = self.pi.copy()
        recta.pf = self.pf.copy()

    """ Funciones de la recta --------------------------"""
    def mover(self, x, y):
        new_pi = self.pi.mover(x, y)
        new_pf = self.pf.mover(x, y)
        return Recta(new_pi, new_pf)

    def rotar(self, origen, angulo):
        new_pi = self.pi.rotar(origen, angulo)
        new_pf = self.pf.rotar(origen, angulo)
        return Recta(new_pi, new_pf)
    
    def offset(self, dist):
        '''@return: mpbe.Geometria.Recta()'''
        r = self.get_director_normal().escalar(dist)
        pio = self.pi.mover(r.x, r.y)
        pfo = self.pf.mover(r.x, r.y)
        return Recta(pio, pfo)

    def distancia(self, punto):
        '''Devuelde la menor distancia del punto a la recta
        @return: mpbe.Geometria.Vector()'''
        vp = self.get_normal()
        rp = Recta(punto, punto.mover(vp.x, vp.y))
        pi = self.interseccion(rp)
        return Vector(pi.x-punto.x, pi.y-punto.y)

    def into(self, punto):
#     def into(self, punto, banda=None):
        '''Devuelve True si el punto se encuentra dentro del area de la recta
        y False en caso contrario
        @return: bool'''
#         if banda == None:
#             banda = self.get_radio_vector()*.1
# #         r1 = Recta(self.pi, Punto(self.get_radio_vector()+self.pi.x, self.pi.y))
#         an = 2*math.pi-self.get_angulo()
#         rr = self.rotar(self.pi, an)
#         p1 = punto.rotar(self.pi, an)
#         if (rr.pi.x < p1.x < rr.pf.x) and (rr.pi.y-banda < p1.y < rr.pf.y+banda):
#             return True
#         else:
#             return False
        x1 = self.pi.x
        x2 = self.pf.x
        if x1>x2:
            x2, x1 = x1, x2
        y1 = self.pi.y
        y2 = self.pf.y
        if y1>y2:
            y2, y1 = y1, y2
        if (x1<=punto.x<=x2) and (y1<=punto.y<=y2):
            return True
        else:
            return False

    def into_rectangulo(self, pi:tuple, pf:tuple, inscripta:bool=True, circunscripta=False):
        '''Devuelve True si la recta esta dentro del rectangulo.
        Si insnscripta es True incluye las recta donde uno de los puntos este dentro del rectangulo.
        Si circunscripta es True incluye las rectas que corten al rectangulo interiormente entre los puntos de la recta'''
        ni = self.pi.into_rectangulo(pi, pf)
        nf = self.pf.into_rectangulo(pi, pf)
        if inscripta and ni and nf:
            return True
        if not(inscripta) and (ni or nf):
            return True
        if circunscripta:
            rr = Recta()  # Verifico la diagonal 1 del rectangulo de seleccion
            rr.set_tupla(pi, pf)
            nn = self.interseccion_into(rr)
            if nn!=None:
                return True
            rr.set_coord(pi[0], pf[1], pf[0], pi[1])
            nn = self.interseccion_into(rr)  # Verifico la diagonal 2 del rectangulo de seleccion
            if nn!=None:
                return True
        return False

    def distancia_into(self, punto):
        '''Devuelde la menor distancia del punto a la recta si el punto se encuentra
        dentro del area de la recta. En caso contrario devuelve Math.inf
        @return: double'''
        ve = self.distancia(punto)
        p1 = punto + ve.getPunto()
        if self.into(p1):
            return (ve.get_radio_vector())
        else:
            return math.inf

    def interseccion(self, recta2):
        '''Devuelve la interseccion de con la recta2
        @return: mpbe.Geometria.Punto()'''
        if self.get_delta_X() == 0 and recta2.get_delta_X() == 0:
            px = math.inf
            py = math.inf
        elif self.get_delta_X() == 0:  # Recta 1 vertical
            px = self.pi.x
            alf2 = recta2.get_delta_Y() / recta2.get_delta_X()
            py = (px - recta2.pi.x) * alf2 + recta2.pi.y
        elif recta2.get_delta_X() == 0:  # Recta 2 vertical
            px = recta2.pi.x
            alf1 = self.get_delta_Y() / self.get_delta_X()
            py = (px - self.pi.x) * alf1 + self.pi.y
        else:
            alf1 = self.get_delta_Y() / self.get_delta_X()
            alf2 = recta2.get_delta_Y() / recta2.get_delta_X()
            if (alf1 != alf2):  # Verifica paralelismo entre rectas
                p2 = recta2.pi
                px = (self.pi.y - p2.y - alf1 * self.pi.x + alf2 * p2.x) / (alf2 - alf1)
                py = (px - self.pi.x) * alf1 + self.pi.y
            else:
                return None
        return Punto(px, py)

    def interseccion_into(self, recta2):
        '''Devuelve la interseccion de con la recta2 dentro de los limites de los puntos de las rectas
        @return: mpbe.Geometria.Punto()'''
        punto = self.interseccion(recta2)
        if punto != None and (self.pi.x<punto.x<self.pf.x or self.pi.x>punto.x>self.pf.x or self.pi.y<punto.y<self.pf.y or self.pi.y>punto.y>self.pf.y):
            if recta2.pi.x<punto.x<recta2.pf.x or recta2.pi.x>punto.x>recta2.pf.x or recta2.pi.y<punto.y<recta2.pf.y or recta2.pi.y>punto.y>recta2.pf.y:
                return punto
        return None

    def intersecion_con_recta_horizontal(self, y):
        '''@return: double'''
        dy = self.get_delta_Y()
        dx = self.get_delta_X()
        diy = y - self.pi.y
        if (dy != 0):
            resx = dx * diy / dy + self.pi.x
        else:  # rectas paralelas
            resx = float('inf')
        return resx

    def is_paralela(self, recta2):
        '''@return: boolean'''
        dx = self.get_delta_X()
        dy = self.get_delta_Y()
        d2x = recta2.get_delta_X()
        d2y = recta2.get_delta_Y()

        if ((dx == 0 & d2x == 0) | (dy == 0 & d2y == 0)):
            return True
        elif ((dx / d2x) == (dy / d2y)):
            return True
        else:
            return False

    def is_colineal(self, recta2):
        if ((self.get_Y(self.pi.x) == recta2.get_Y(self.pi.x)) & self.is_paralela(recta2)):
            return True
        else:
            return False

    def is_vertical(self):
        if self.pi.x == self.pf.x:
            return True
        else:
            return False
        
    def is_horizontal(self):
        if self.pi.y == self.pf.y:
            return True
        else:
            return False


class Poligono (object):
    '''
    Define un poligono formado por una lista de puntos
    @version: 1.0 20/09/13

    @ivar puntos: lista de puntos
    @type puntos: [] mpbe.Geometria.Punto()
    '''

    def __init__(self, puntos=None):
        if puntos == None:
            puntos = []
        self.puntos = puntos

    """ Setters and Getters ----------------------------"""
    def get_puntos(self):
        return self.puntos

    def set_puntos(self, puntos=[Punto()]):
        '''@type puntos: [] mpbe.Geometria.Punto()'''
        self.puntos = puntos

    def get_array(self):
        '''
        Devuelve un array double formado por los componentes x e y de la lista de puntos
        @return: array.array()
        '''
        res = array('L', [])
        for ii in range(len(self.puntos)):
            res.append(self.puntos[ii].x)
            res.append(self.puntos[ii].y)
        return res

    def get_array_int(self):
        '''
        Devuelve un array unsigned int formado por los componentes x e y de la lista de puntos
        @return: array.array()
        '''
        res = array('L', [])
        for ii in range(len(self.puntos)):
            res.append(self.puntos[ii].x)
            res.append(self.puntos[ii].y)
        return array('L', res)

    def get_list_tupla(self):
        '''
        Devuelve un array formado por tuplas con los componentes x e y de la lista de puntos
        @return: array.array()
        '''
        res = []
        for ii in range(len(self.puntos)):
            res.append((self.puntos[ii].x, self.puntos[ii].y))
        return res

    def get_copy(self):  # Ex getArrayPuntos
        '''@return: [] mpbe.Geometria.Punto()'''
        return Poligono(self.puntos[:])

    def set(self, index, punto):
        '''
        Coloca el punto en la posicion "index"
        @type index: int
        @type punto: mpbe.Geometria.Punto
        '''
        self.puntos[index] = punto
        return self.puntos[index]

    def first_element(self):
        '''@return: mpbe.Geometria.Punto()'''
        return self.puntos[0]

    def get(self, index):
        '''
        Retorna el punto de la posicion "index"
        @type index: int
        @return: mpbe.Geometria.Punto()
        '''
        return self.puntos[index]

    def last_element(self):
        '''@return: [] mpbe.Geometria.Punto()'''
        return self.puntos[-1]

    def get_recta(self, index):
        '''
        Devuelve la recta del poligono ubicada en la posicion "index". Valor inicial 0.
        @type index: int
        @return: [] mpbe.Geometria.Recta()
        '''
        res = Recta()
        if (index > -1 & index < len(self.puntos)):
            pi = self.puntos[index]
            if (index != (len(self.puntos) - 1)):
                pf = self.puntos[index + 1]
            else:
                pf = self.puntos[0]
            res = Recta(pi, pf)
        else:
            res = None
        return res

    """ Delegate Metod ---------------------------------"""
    def add(self, index, punto):
        '''
        @type index: int
        @type punto: mpbe.Geometria.Punto()
        '''
        self.puntos[index:index] = [punto]

    def append(self, punto):  # Ex add(punto)
        '''@param punto: mpbe.Geometria.Punto()'''
        self.puntos.append(punto)

    # public int capacity() {return puntos.capacity();}
    def clear(self):
        del self.puntos[:]

    def clone(self):
        '''@return: [] mpbe.Geometria.Punto()'''
        return self.puntos[:]

    def copy_into(self, poligono):
        poligono.clear
        poligono.puntos = self.puntos[:]

    def index_of(self, value, start=0):
        '''
        Devuelve la posición en la que se encontró la primera ocurrencia de value. Si se especifica, start define la posicion de inicio.
        @return: int

        @type value: mpbe.Geometria.Punto()
        @type start: int
        '''
        return self.puntos.index(value, start)

    def is_empty(self):
        if (len(self.puntos) == 0):
            return True
        else:
            return False

    def remove(self, index):
        '''
        @return: mpbe.Geometria.Punto()
        @type index: int
        '''
        del self.puntos[index]

    def remove_punto(self, punto):
        '''
        Eliminar la primera ocurrencia de punto en la lista.
        @type punto: mpbe.Geometria.Punto()
        '''
        self.puntos.remove(punto)

    def set_size(self, value):
        '''
        Extiende la cantidad de puntos del poligono a value
        @type value: int
        '''
        sz = len(self.puntos)
        if (sz < value):  # corta la lista a value
            del(self.puntos[value:])
        elif (sz > value):  # extiende la lisata value con puntos nulos
            ag = value - sz
            self.puntos = self.puntos + [Punto()] * ag

    def size(self):
        '''
        Retorna la cantidad de puntos del poligono
        @return: int
        '''
        return len(self.puntos)

    def subList(self, from_id, to_id):
        '''
        Retorna una sublista de puntos
        @return: [] mpbe.Geometria.Punto()

        @type from_id: int
        @type to_id: int
        '''
        return self.puntos[from_id:to_id]

    """ Operaciones sobre el poligono ------------------"""
    def offset(self, dist):
        '''
        Devuelve un nuevo poligono con un offset al poligono actual
        @return: mpbe.Geometria.Poligono()
        @param dist: Distancia del offset
        @type dist: double
        '''
        r1 = Recta()
        ro1 = Recta()
        resP = Poligono()
        pi = Punto()
        # obtiene la primer recta anterior
        rf = Recta(self.puntos[len(self.puntos) - 1], self.puntos[0])
        ro0 = rf.offset(dist)
        # obtiene la recta actual
        for ii in range(1, len(self.puntos) + 1):
            # obtiene la recta actual
            if (ii != len(self.puntos)):
                r1 = Recta(self.puntos[ii - 1], self.puntos[ii])
            else:
                r1 = rf
            ro1 = r1.offset(dist)
            # obtiene el punto de interseccion y lo guarda en resP
            pi = ro0.interseccion(ro1)
            resP.append(pi)
            # guarda la recta anterior
            ro0 = ro1
        return resP

    def rotar(self, centro, angulo_rad):
        '''
        Devuelve un nuevo poligono rotado
        @return: mpbe.Geometria.Poligono()
        @param centro: Centro de rotación
        @type dist: mpbe.Geometria.Punto()
        @param angulo_rad: Angulo de rotacion en radianes
        @type angulo_rad: double
        '''
        res = Poligono()
        p = Vector()
        for p in self.puntos:
            res.append(p.rotar(centro, angulo_rad).getPunto())
        return res

    def escalar(self, valor):
        '''
        Devuelve un nuevo poligono escalado
        @return: mpbe.Geometria.Poligono()
        @param valor: Valor de escala a aplicar
        @type valor: double
        '''
        res = Poligono()
        for p in self.puntos:
            res.append(p.escalar(valor).getPunto())
        return res

    def escalar_por_coord(self, valorX, valorY):
        '''
        Devuelve un nuevo poligono escalado por coordenadas
        @return: mpbe.Geometria.Poligono()
        @param valorX: Valor de escala X a aplicar
        @type valorX: double
        @param valorY: Valor de escala Y a aplicar
        @type valorY: double
        '''
        res = Poligono()
        for p in self.puntos:
            res.append(p.escalar(valorX, valorY).getPunto())
        return res

    def mover(self, x, y):
        '''
        Devuelve un nuevo poligono movido una distancia x e y
        @return: mpbe.Geometria.Poligono()
        @param x: Valor X a mover
        @type x: double
        @param y: Valor Y a mover
        @type y: double
        '''
        res = Poligono()
        for p in self.puntos:
            res.append(p.mover(x, y))
        return res

    def distancias(self, punto):
        '''
        Devuelve una lista de vectores con las distancia de los lados del poligono a punto
        @return: [mpbe.Geometria.Vector()]
        @param punto: Punto al que calcular las distancias
        @type punto: mpbe.Geometria.Punto()
        '''
        r = Recta()
        pi = Punto()
        pf = Punto()

        res = [0] * len(self.puntos)  # mpbe.Geometria.Vector() []
        for ii in range(len(self.puntos)):
            # obtiene la recta actual
            pi = self.puntos[ii - 1]
            if (ii != len(self.puntos)):
                pf = self.puntos[ii]
            else:
                pf = self.puntos[0]
            r = Recta(pi, pf)
            # buscar la distancia
            res[ii - 1] = r.distancia(punto)
        return res


class Cota(ObjectLst, JsonObject):
    '''
    Define una cota mediante 2 objetos
    @version: 1.0 03/12/17

    @ivar punto_i: Punto inicial.
    @ivar punto_f: Punto final.
    @ivar posicion: Punto que indica la posicion de la linea de cota 
    @type tipo: Tipo de cota entre los objetos. Puede ser Horizontal, Vertical o Alineada
    @nota: Derivar los objetos acotables de AcotableObject
    '''

    def __init__(self, punto_i=None, punto_f=None, posicion=None, tipo=TIPO_COTA.HORIZONTAL):
        '''
        Define una cota mediante 2 objetos
        @ivar punto_i: peto inicial. Puede ser Punto, Nudo, Barra
        @ivar punto_f: Objeto final. Puede ser Punto, Nudo, Barra
        @type tipo: Tipo de cota entre los objetos. Puede ser Horizontal, Vertical o Alineada
        '''
        self.punto_i = punto_i
        self.punto_f = punto_f
        self.posicion = posicion
        self.tipo = tipo
    
    def set_punto_i(self, punto:Punto):
        self.punto_i = punto

    def get_punto_i(self):
        return self.punto_i

    def set_punto_f(self, punto:Punto):
        self.punto_f = punto

    def get_punto_f(self):
        return self.punto_f
    
    def set_posicion(self, punto:Punto):
        self.posicion = punto

    def get_posicion(self):
        return self.posicion

    def set_tipo(self, tipo:TIPO_COTA):
        self.tipo = tipo
    
    def get_tipo(self):
        return self.tipo

    def get_value(self):
        '''Devuelve el valor de la cota'''
        l = 0.0
        try:
            pi = self.punto_i
            pf = self.punto_f
            if self.tipo == TIPO_COTA.HORIZONTAL:
                l = math.fabs(pi.x - pf.x)
            if self.tipo == TIPO_COTA.VERTICAL:
                l = math.fabs(pi.y - pf.y)
            if self.tipo == TIPO_COTA.ALINEADA:
                dx = pi.x - pf.x
                dy = pi.y - pf.y
                l = math.sqrt(dx*dx + dy*dy)
        except:
            l = "ERROR"
        return l

    def copy(self):
        return Cota(self.punto_i, self.punto_f, self.posicion, self.tipo)
        
    """ Funciones derivadas de ObjectLst ------------------------------------"""
    def get_list(self):
        """Lista con los valores de la cota"""
        return [self.punto_i, self.punto_f, self.posicion, self.tipo, self.get_value()]

    def set_list(self, lst):
        """Asigna la lista al objeto"""
        self.punto_i = lst[0]
        self.punto_f = lst[1]
        self.posicion = lst[2]
        self.tipo = lst[3]

    def set_col_value(self, col, value):
        lst = self.get_list()
        lst[col] = value
        self.set_list(lst)

    """ Funciones JSON ------------------------------------------------------"""
    def toDict(self):
        '''Devuelve un diccionario con los campos de la clase'''
        di = {}
        di["punto_i"] = self.punto_i.toDict()
        di["punto_f"] = self.punto_f.toDict()
        di["posicion"] = self.posicion.toDict()
        di["tipo"] = self.tipo.name
        return di

    def fromDict(self, di):
        try:
            p = Punto()
            p.fromDict(di["punto_i"])
            self.punto_i = p.copy()
            p.fromDict(di["punto_f"])
            self.punto_f = p.copy()
            p.fromDict(di["posicion"])
            self.posicion = p.copy()
            self.tipo = TIPO_COTA.get_enum_from_str(di["tipo"])
        except:
            raise ValueError("Error al leer una Cota")

    def __str__(self, *args, **kwargs):
        return "[" + str(self.punto_i) + ", " + str(self.punto_f) + ", " + \
                str(self.get_value()) + ", " + self.tipo.name + "]"


class Nota(ObjectLst):
    '''
    Define una nota a un punto
    @version: 1.0 03/12/17

    @ivar punto: Punto al que apunta la nota.
    @ivar posicion: Posicion del texto de la nota
    @type texto: Texto de la nota
    '''

    def __init__(self, punto=Punto(0.0, 0.0), posicion=Punto(1.0, 1.0), texto=''):
        '''
        Define una nota a un punto
        @ivar punto: Punto al que apunta la nota.
        @ivar posicion: Posicion del texto de la nota
        @type texto: Texto de la nota
        '''
        self.punto = punto
        self.posicion = posicion
        self.texto = texto

    """ Funciones derivadas de ObjectLst ------------------------------------"""
    def get_list(self):
        """Lista con los valores de la cota"""
        return [self.punto, self.posicion, self.texto]

    def set_list(self, lst):
        """Asigna la lista al objeto"""
        self.punto = lst[0]
        self.posicion = lst[1]
        self.texto = lst[2]

    def set_col_value(self, col, value):
        lst = self.get_list()
        lst[col] = value
        self.set_list(lst)
        
        
    """ Funciones derivadas de JsonObject -----------------------------------"""
    # TODO: Agregar funciones de JsonObject


def distancia_entre_puntos(p1, p2):
        '''
        Devuelve la distancia al punto ingresado
        @param p1: Punto 1 a calcular la distancia
        @type p1: mpbe.Geometria.Punto
        @param p2: Punto 2 a calcular la distancia
        @type p2: mpbe.Geometria.Punto
        '''
        return math.sqrt(math.pow((p2.x - p1.x), 2) + math.pow((p2.y - p1.y), 2))


def area_barra(diametro):
    return (math.pi * diametro ^ 2 / 4)


def valor_trapecio(h1:float, h2:float, d1:float, d2:float, dc:float)->float:
    '''Devuelve el valor del trapecio formado por h1, h2, d1, d2
    a la distancia dc'''
    return h1+(h2-h1)*(dc-d1)/(d2-d1)


def area_trapecio(h1:float, h2:float, d1:float, d2:float):
    '''Devuelve el area y el CG (respecto a d2) del trapecio formado por h1, h2, d1, d2'''
    dd = d2 - d1
    hd = h2 - h1
    At = dd * hd / 2
    Ar = dd * h1
    A = At + Ar
    #dt = dd/3 if h2 > h1 else dd*2/3
    d = (At * (dd/3 if h2 > h1 else dd*2/3) + Ar * dd/2) / A
    return A, d
    