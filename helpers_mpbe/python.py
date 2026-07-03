# -*- coding: utf-8 -*-


'''
Modulo de clases de funciones adicionales para python.\n
B{Created:} 05/01/2014
'''

import os
import sys
import re
import codecs
import shutil
from string import Template
import json


def compose(obj, cls, acept_none=True, use_default=False, default=None):
    '''compose(objeto, clase)->clase
    **Parameters:**
    - obj (object): Objeto a verificar
    - cls (class): Clase del objeto
    - acept_none (bool): Indica si el objeto acepta None
    - use_defautl (bool): Indica si debe aplicarse el valor por default
    - default (objet): Valor por defecto y el objeto con corresponde a la clase
    '''
    if acept_none and obj is None:
        return obj
    # if isinstance(cls, list):
    #     for cl in cls:
    #         if isinstance(obj, cl):
    #             return obj
    # else:
    if isinstance(obj, cls):
        return obj
    if use_default:
        return default
    raise TypeError('%s is not type %s' % (type(obj), cls))


def check_list(lst, cls_child, acept_none=False):
    for it in lst:
        if not (acept_none and it is None) and not (isinstance(it, cls_child) or issubclass(it, cls_child)):
            raise TypeError('%s is not type %s' % (type(it), cls_child))


def compose_dict(dct, key, cls, default=None, acept_none=False):
    """extrae un objeto de un diccionario y verifica el tipo
    args:
        dct (dictionary): Diccionario origen
        key (str): Llave del objeto
        cls (class): Clase del objeto
        default : Valor por defecto a devolver si no existe la llave
        acept_none (bool): Indica si se acepta None como valor del objeto
    """
    if key in dct:
        var = dct.pop(key)
        return compose(var, cls, acept_none)
    else:
        return default


def frange(start, end=None, inc=None):
    ''' A range function, that does accept float increments...
    @var start: valor inicial
    @type start: float
    @var end: valor final
    @type end: float
    @var inc: incremento
    @type inc: float
    @version: 1.0 20/09/13
    '''
    if end is None:
        end = start + 0.0
        start = 0.0

    if inc is None:
        inc = 1.0

    L = []
    while 1:
        nx = start + len(L) * inc
        if inc > 0 and nx > end:
            break
        elif inc < 0 and nx < end:
            break
        L.append(nx)

    return L


def call_back_path(path):
    '''
    El 1 indica la cantidad de directorios a volver
    @version: 1.0 20/09/13
    '''
    path.rsplit('/', 1)[0]


class FolderWrapper(object):  # ENVOLTURA DE DIRECTORIO
    '''
    Envoltura del archivo para colocar en wx.TreeItemData()
    @version: 1.00 28/12/14
    Attributes:
        path (string): Camino del archivo.
    '''

    def __init__(self, path, log=sys.stdout):
        '''
        @version: 1.00 01/01/15
        Attributes:
            path (string): Camino del archivo.
        '''
        self.log = log  # LOG:
        if self.validatePath(path):
            self.path = path
        else:
            raise OSError

    def __str__(self):
        return self.getFullName()

    """ Geters and Seters -------------------------------------------"""
    def setPath(self, str_path):
        self.path = str_path

    def getPath(self):
        return self.path

    def getFolderName(self):
        if self.path:
            rtn = self.path.split(os.sep)[-1]
        else:
            rtn = None
        return rtn

    """ Funciones sobre el path -------------------------------------"""
    def isHidden(self):
        return (lambda x: True if x[0] == '.' else False)(self.getFolderName())

    def isNone(self):
        if self.path is None:
            return True
        else:
            return False

    def validatePath(self, path):
        '''Devuelve True o False'''
        try:
            rtn = os.path.exists(path)
        except:
            rtn = False
        return rtn

    def getChildsNames(self, sorted_f=True, show_hidden=False, filters = ['*']):
        '''Devuelve dos listas con los nombres de los directorios y archivos hijos del path de la clase.
        Si el path no es un directorio lanza un error.'''
        path = self.path
        inserta = lambda x, ff: lstd.append(ff) if x else lstf.append(ff)
        lst = os.listdir(self.path)
        lstd = []
        lstf = []
        for ff in lst:
            isdir = os.path.isdir(self.path + os.sep + ff)
            # ext = ff.split('.')[-1]
            if isdir or self._matches_filters(ff, filters):
                if ff[0]!='.':
                    inserta(isdir, ff)
                elif show_hidden:
                    inserta(isdir, ff)
        if sorted_f:
            lstd = sorted(lstd)
            lstf = sorted(lstf)
        return lstd, lstf

    def _matches_filters(self, filename, filters):  # Chequea coincidencia de filtros
        if '*' in filters:
            return True
            # Regex para extraer la extensión del archivo (o vacío si no tiene)
        pattern = re.compile(r'\.([^.]+)$')
        match = pattern.search(filename)
        # Si hay una extensión, extraerla; si no, usar una cadena vacía para archivos sin extensión
        file_extension = match.group(1) if match else ''
        # Verificar si la extensión está en la lista de filtros
        return file_extension in filters

    def getParentPath(self):
        actual = self.path.split(os.sep)[-1]
        ppath = self.path[:-len(actual)-1]
        return ppath

    def getParentFolderName(self):
        par = self.getParentPath()
        return par.split(os.sep)[-1]

    def getParentFileWrapper(self):
        return FileWrapper(self.getParentPath())

    """ Funciones sobre el sistema de archivos"""
    def mkDir(self, name_new_dir, nro=0):
        '''Crea un directorio nuevo dentro del path del FileWrapper
        @ivar name_new_dir: Nombre del nuevo directorio
        @ivar nro: Que incrementa si el directorio existe hasta encontar uno nuevo.
                   Si es indica -1 lanza un error de existir el archivo. Default = 0.
        '''
        try:
            if nro > 0:
                nn = ' ' + str(nro)
            else:
                nn = ""
            fp = self.path + os.sep + name_new_dir + nn
            os.mkdir(fp)
            return FileWrapper(fp)
        except OSError as err: # errno = 17 Ya existe el archivo
            if err.errno == 17:  # Existe el archivo aumenta la numeracion
                return self.mkDir(name_new_dir, nro+1)
            else:
                self.log.write("OSError: ")
                self.log.write(str(err.errno))
                self.log.write(err.strerror + '\n')
                return None
        except:
            self.log.write("Error creando el directorio: ")
            self.log.write(sys.exc_info()[0] + '\n')
            self.log.write(sys.exc_info()[1] + '\n')
            return None

    def rename(self, new_name):
        try:
            if self.isDir():
                new_path = self.getParentPath() + os.sep + new_name
            else:
                new_path = self.path + os.sep  + new_name + '.' + self.ext
            if not(os.path.exists(new_path)):
                os.rename(self.getFullName(), new_path)
                self.name = new_name
                return True
            else:
                return False
        except:
            self.log.write("Error creando el directorio:\n")
            self.log.write(str(sys.exc_info()[0]) + '\n')
            self.log.write(str(sys.exc_info()[1]) + '\n')
            return None

    def remove(self):
        try:
            if self.isDir():
                shutil.rmtree(self.path)
            else:
                os.remove(self.getFullName())
            self.path = None
            self.name = None
            self.ext = None
            return True
        except:
            self.log.write("Error borrando el archivo:\n")
            self.log.write(str(sys.exc_info()[0]) + '\n')
            self.log.write(str(sys.exc_info()[1]) + '\n')
            return False

    def copy(self, dst):
        try:
            src = self.getFullName()
            if self.isDir():
                shutil.copytree(src, dst)
            else:
                shutil.copy(src, dst)
            return FileWrapper(dst)
        except:
            self.log.write("Error copiando el archivo:\n")
            self.log.write(str(sys.exc_info()[0]) + '\n')
            self.log.write(str(sys.exc_info()[1]) + '\n')
            return False


class FileWrapper(object):  # ENVOLTURA DEL ARCHIVO
    '''
    Envoltura del archivo para colocar en wx.TreeItemData()
    @version: 1.00 28/12/14
    @ivar path: Camino del archivo.
    @type path: string
    @ivar name: Nombre del archivo sin extension. Si apunta a un directorio es None.
    @type name: string
    @ivar ext: Extencion del archivo. Si apunta a un directorio es None.
    @type ext: string
    '''

    def __init__(self, full_name, log = sys.stdout):
        '''
        @version: 1.00 01/01/15
        @ivar path: Camino del archivo.
        @type path: string
        @ivar file_name: Nombre del archivo con extension. Si apunta a un directorio es None.
        @type file_name: string
        '''
        self.log = log  # LOG:
#        self.log.write("FW =" + self.__class__.__name__ + ".__init__()\n")  # LOG:
        self.path = None
        self.name = None
        self.ext = None
        try:
            self.setFullName(full_name)
        except OSError:
            raise OSError
        except:
            raise

    def __str__(self):
        return self.getFullName()

    """ Geters and Seters -------------------------------------------"""
    def setPath(self, str_path):
        self.path = str_path
        self.name = None
        self.ext = None

    def getPath(self):
        return self.path

    def getPathFileWrapper(self):
        return FileWrapper(self.path)

    def setName(self, str_name):
        if '.' in str_name and str_name[0] != '.':
            self.ext = str_name.split('.')[-1]
            self.name = str_name[:-len(self.ext)-1]
        else:
            self.name = str_name
            self.ext = None

    def getName(self):
        if not self.isDir():
            return self.name
        else:
            return self.getCurrentDirName()

    def setExt(self, str_ext):
        self.ext = str_ext

    def getExt(self):
        return self.ext

    def getNameExt(self):
        if not self.isDir():
            if self.ext != None:
                return self.name + '.' + self.ext
            else:
                return self.name
        else:
            return self.getCurrentDirName()

    def setFullName(self, str_fname):
            # Existe el camino pasado
        if str_fname == '' or str_fname == None:
            # Wraper Null
            self.path = None
            self.name = None
            self.ext = None
        elif not os.path.isdir(str_fname):
            # No es un directorio
            namext = str_fname.split(os.sep)[-1]
            self.path = str_fname[:-len(namext)-1]
            self.setName(namext)
        else:
            # Es un directorio
            self.path = str_fname
            self.name = None
            self.ext = None

    def getFullName(self):
        fl = lambda x,s: s+x if x!=None else ""
        nn = fl(self.name, os.sep)
        ee = fl(self.ext, '.')
        if self.path:
            fname = self.path + nn + ee
        else:
            fname = None
        return fname

    """ Funciones sobre el path -------------------------------------"""
    def isDir(self):
        return (lambda x: True if x==None else False)(self.name)

    def isHidden(self):
        ishd = lambda x: True if x[0]=='.' else False
        if self.name != None:
            res = ishd(self.getName())
        else:
            res = ishd(self.getCurrentDirName())
        return res

    def isNone(self):
        if self.ext == None and self.name == None and self.path == None:
            return True
        else:
            return False

    def validatePath(self):
        try:
            path = os.path.exists(self.getFullName())
        except:
            path = False
        return path

    def getChildsNames(self, sorted_lst=True, show_hidden=False, ext_filter = ['*']):
        '''Devuelve dos listas con los nombres de los directorios y archivos hijos del path de la clase.
        Si el path no es un directorio lanza un error.'''
        inserta = lambda x, ff: lstd.append(ff) if x else lstf.append(ff)
        lst = os.listdir(self.path)
        lstd = []
        lstf = []
        for ff in lst:
            isdir = os.path.isdir(self.path + os.sep + ff)
            ext = ff.split('.')[-1]
            if isdir or ext in ext_filter or ext_filter[0] == '*':
                if ff[0]!='.':
                    inserta(isdir, ff)
                elif show_hidden:
                    inserta(isdir, ff)
        if sorted_lst:
            lstd = sorted(lstd)
            lstf = sorted(lstf)
        return lstd, lstf

    def getParentPath(self):
        actual = self.path.split(os.sep)[-1]
        ppath = self.path[:-len(actual)-1]
        return ppath

    def getParentDirName(self):
        par = self.getParentPath()
        return par.split(os.sep)[-1]

    def getParentFileWrapper(self):
        return FileWrapper(self.getParentPath())

    def getCurrentDirName(self):
        if self.path:
            rtn = self.path.split(os.sep)[-1]
        else:
            rtn = None
        return rtn

    """ Funciones sobre el sistema de archivos"""
    def mkDir(self, name_new_dir, nro=0):
        '''Crea un directorio nuevo dentro del path del FileWrapper
        @ivar name_new_dir: Nombre del nuevo directorio
        @ivar nro: Que incrementa si el directorio existe hasta encontar uno nuevo.
                   Si es indica -1 lanza un error de existir el archivo. Default = 0.
        '''
        try:
            if nro > 0:
                nn = ' ' + str(nro)
            else:
                nn = ""
            fp = self.path + os.sep + name_new_dir + nn
            os.mkdir(fp)
            return FileWrapper(fp)
        except OSError as err: # errno = 17 Ya existe el archivo
            if err.errno == 17:  # Existe el archivo aumenta la numeracion
                return self.mkDir(name_new_dir, nro+1)
            else:
                self.log.write("OSError: ")
                self.log.write(str(err.errno))
                self.log.write(err.strerror + '\n')
                return None
        except:
            self.log.write("Error creando el directorio: ")
            self.log.write(sys.exc_info()[0] + '\n')
            self.log.write(sys.exc_info()[1] + '\n')
            return None

    def rename(self, new_name):
        try:
            if self.isDir():
                new_path = self.getParentPath() + os.sep + new_name
            else:
                new_path = self.path + os.sep  + new_name + '.' + self.ext
            if not(os.path.exists(new_path)):
                os.rename(self.getFullName(), new_path)
                self.name = new_name
                return True
            else:
                return False
        except:
            self.log.write("Error creando el directorio:\n")
            self.log.write(str(sys.exc_info()[0]) + '\n')
            self.log.write(str(sys.exc_info()[1]) + '\n')
            return None

    def remove(self):
        try:
            if self.isDir():
                shutil.rmtree(self.path)
            else:
                os.remove(self.getFullName())
            self.path = None
            self.name = None
            self.ext = None
            return True
        except:
            self.log.write("Error borrando el archivo:\n")
            self.log.write(str(sys.exc_info()[0]) + '\n')
            self.log.write(str(sys.exc_info()[1]) + '\n')
            return False

    def copy(self, dst):
        try:
            src = self.getFullName()
            if self.isDir():
                shutil.copytree(src, dst)
            else:
                shutil.copy(src, dst)
            return FileWrapper(dst)
        except:
            self.log.write("Error copiando FileWrapper:\n")
            self.log.write(str(sys.exc_info()[0]) + '\n')
            self.log.write(str(sys.exc_info()[1]) + '\n')
            return False


class JsonObject(object):
    '''@version: 0.00 23/12/14'''
    def __init__(self):
        raise TypeError('La clase ObjectLst es abstracta y no se puede inicializar')
        self.app.Exit()

    def copy(self):
        '''Devuelve una copia de la clase'''
        raise TypeError('Metodo copy() no definido en %s' % self.__class__)
        self.app.Exit()

    def toDict(self):
        '''Devuelve un diccionario con los campos de la clase'''
        raise TypeError('Metodo toDict() no definido en %s' % self.__class__)
        self.app.Exit()

    def fromDict(self, di):
        '''Coloca los items del diccionario en la clase'''
        raise TypeError('Metodo fromDict() no definido en %s' % self.__class__)
        self.app.Exit()

    def actualizeDict(self, di):
        '''Actualiza los datos del dictionario pasado y devuelve una copia'''
        raise TypeError('Metodo actualizeDict() no definido en %s' % self.__class__)
        self.app.Exit()

    def toJsonStr(self):
        '''Devuelce un string con los campos de la clase en formato JSON'''
        di = self.toDict()
        return json.dumps(di, indent=2)

    def toJsonFile(self, fl_name):
        di = self.toDict()
        fl = codecs.open(fl_name, 'w', 'utf-8')
        json.dump(di, fl, indent=2)
        fl.close()

    def fromJsonStr(self, txt):
        '''Coloca los items del string(en formato JSON) en la clase'''
        di = json.loads(txt)
        self.fromDict(di)

    def fromJsonFile(self, fl_name):
        '''Coloca los items del archico JSON en la clase'''
        if os.path.exists(fl_name):
            fl = codecs.open(fl_name, 'r', 'utf-8')
            di = json.load(fl)
            fl.close()
            self.fromDict(di)
            return True
        else:
            return False

    def actualizeJsonFile(self, fl_name):
        # actualiza o crea el diccionario
        if os.path.exists(fl_name):
            fl = codecs.open(fl_name, 'r', 'utf-8')
            di_ant = json.load(fl)
            di = self.actualizeDict(di_ant)
            fl.close()
        else:
            di = self.toDict()
        # guarda el diccionario
        fl = codecs.open(fl_name, 'w', 'utf-8')
        json.dump(di, fl, indent=2)
        fl.close()


class StateIndicator(object):
    '''
    Clase que define un estado que se transfiere a la clase padre
    @type state: boolean
    @version: 1.0 20/09/13
    '''

    def __init__(self, state=False):
        self.state = state

    def copy(self):
        return StateIndicator(self, self.state)


class Report (JsonObject):
    '''
    Clase donde guardar los resutados de la verificacion y crear los informes
    @version: 1.00 10/05/15
    @ivar variables: Diccionario con la informacion del calculo
    @type variables: dict()
    @ivar opciones: Diccionario con opciones del calculo y del informe
    @type opciones: dict()
    '''
    def __init__(self,
                 variables=dict(), opciones=dict(),
                 report_html="", report_txt="",
                 notes_html="", notes_txt=""):
        self.variables = variables
        self.opciones = opciones
        self.report_html = report_html
        self.report_txt = report_txt
        self.notes_html = notes_html
        self.notes_txt = notes_txt

    """ Funciones de la clase ------------------------------------------------"""
    def copy(self):
        return Report(self.variables.copy(), self.opciones.copy(),
                      self.report_html, self.report_txt,
                      self.notes_html, self.notes_txt)

    def clear(self):
        self.variables = dict()
        self.opciones = dict()
        self.report_html = ""
        self.report_txt = ""
        self.notes_html = ""
        self.notes_txt = ""

    def setReportFromTemplate(self, plt_html=None, plt_txt=None):
        di = dict()
        for cl, va in self.variables.iteritems():
            di[cl] = va
        for cl, va in self.opciones.iteritems():
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
        di = {}
        di["variables"]=self.variables
        di["opciones"]=self.opciones
        di["report html"]=self.report_html
        di["report txt"]=self.report_txt
        di["notes html"]=self.notes_html
        di["notes txt"]=self.notes_txt
        return di

    def fromDict(self, di):
        '''Coloca los items del diccionario en la clase'''
        try:
            self.variables = di["variables"]
            self.opciones = di["opciones"]
            self.report_html = di["report html"]
            self.report_txt = di["report txt"]
            self.notes_html = di["notes html"]
            self.notes_txt = di["notes txt"]
        except:
            return 100001 # ERROR al leer el resultado de la verificacion


class ObjectLst(object):
    '''@version: 1.0 20/09/13'''
    def __init__(self):
        raise TypeError('La clase ObjectLst es abstracta y no se puede inicializar')
        self.app.Exit()

    def get_list(self):
        """get_lista(self)"""
        raise TypeError('Metodo get_lista() no definido en %s' % self.__class__)
        self.app.Exit()

    def set_list(self, lst):
        """set_lista(self, list lst)
        """
        raise TypeError('Metodo set_lista(lst) no definido en %s' % self.__class__)
        self.app.Exit()

    def set_col_value(self, col, value):
        """set_col_value(int col, object value)
        colocar el valor en la columna indicada"""
        lst = self.get_list()
        lst[col] = value
        self.set_list(lst)


class ChangedList(list):
    '''Deifine una lista con un indicador de cambio'''
    def __init__(self, iterable, changed:StateIndicator=StateIndicator()):
        list.__init__(self, iterable)
        self.changed = changed

    def append(self, *args, **kwargs):
        self.changed.state = True
        list.append(self, *args, **kwargs)

    def clear(self, *args, **kwargs):
        self.changed.state = True
        list.clear(self, *args, **kwargs)

#     def copy(self, *args, **kwargs):
#         return list.copy(self, *args, **kwargs)
#
#     def count(self, *args, **kwargs):
#         return list.count(self, *args, **kwargs)

    def extend(self, *args, **kwargs):
        self.changed.state = True
        list.extend(self, *args, **kwargs)

#     def index(self, *args, **kwargs):
#         return list.index(self, *args, **kwargs)

    def insert(self, *args, **kwargs):
        self.changed.state = True
        list.insert(self, *args, **kwargs)

    def pop(self, *args, **kwargs):
        self.changed.state = True
        return list.pop(self, *args, **kwargs)

    def remove(self, *args, **kwargs):
        self.changed.state = True
        list.remove(self, *args, **kwargs)

    def reverse(self, *args, **kwargs):
        self.changed.state = True
        list.reverse(self, *args, **kwargs)

    def sort(self, *args, **kwargs):
        self.changed.state = True
        list.sort(self, *args, **kwargs)


# class object_with_type_control(object):
#     def __init__(self, cls, default_value, acept_none=None):
#         self.acept_none = acept_none
#         self.__cls = cls
#         self.default = default_value
#         self.__value = compose(default_value, cls, acept_none)
#
#     # def __getstate__(self):
#     #     return  self.__value
#
#     # def __setattr__(self, key, value):  # Llama cuando se crea la variable
#     #     print(key, value)
#
#     def __getattribute__(self, item):
#         print(item)
#
#     def __repr__(self):
#         print("Repr")
#         return "999"
#
#     def __
#         print("Set Atrib")
#
#
#         # if self.acept_none and value == None:
#         #     self.__value = None
#         # if isinstance(self.__cls, list):
#         #     for cl in self.__cls:
#         #         if isinstance(value, self.__cls):
#         #             self.__value = value
#         # else:
#         #     if isinstance(value, self.__cls):
#         #         self.__value = value
#         # raise TypeError('%s is not type %s' % (type(value), self.__cls))
#
#
if __name__ == "__main__":
    cc = 20
    aa = compose(cc, int, acept_none=True, use_default=False)
    b = 5
    print (aa+b)
