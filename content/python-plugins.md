Title: Plugins en Python
Date: 2010-12-03 10:20
Category: Python

Vamos a proponer un pequeño caso de uso. Supongamos estamos trabajando en un programa que necesita generar una serie de gráficas. Para poder generar estas gráficas, debemos de acceder a una base de datos y desde ahí, recuperar un conjunto de datos, agruparlos según un criterio temporal (por ejemplo, días u horas),
y además, en algunos casos, realizar transformaciones sobre esos datos para generar otros datos.

En principio, no parece demasiado complicado, ¿verdad? Incluso podemos parametrizar parcialmente los datos que vamos a utilizar de entrada (por ejemplo, los periodos temporales). Pero, **¿qué ocurre cuando las bases de datos por debajo cambian?** Si cambia la nomenclatura de las tablas, o las relaciones entre ellas, o incluso pasamos de trabajar con bases de datos a hojas de cálculo EXCEL...

En algunos casos la solución puede ser sencilla, como por ejemplo crear una pequeña base de datos para volcar los datos del EXCEL y trabajar con ella; en otros, quizás tengamos que modificar el core de nuestra librería para cambiar la forma en que se recuperan los datos. Pero, **¿qué pasaría si las soluciones deben de coexistir entre ellas?** Lo más probable es que terminemos con una capa de código intermedia dedicada a la selección de los mecanismos de generación de gráficas, y luego un conjunto de librerías, funciones o clases que lleven a cabo el duro trabajo de lidiar con las capas inferiores.

Aquí se plantea otro problema adicional: si utilizamos la misma base de código para generar todos estos mecanismos, tendremos problemas para paralelizar el trabajo entre diferentes equipos y también para poder ampliar de cara al futuro dicha librería, y el mantenimiento se puede volver más complejo.

Para resolver todo esto, **vamos a utilizar plugins**.

### Qué entendemos por plugins:

Por ahora, vamos a considerar **plugin** como *un componente de código, en forma de clase, que posee una interfaz común con otros componentes de código y realiza una función similar a estos*. Es una definición un poco rara o rebuscada, y seguramente poco académica, pero que nos vendrá bien.

### Preparando el plugin

Para poder usar el plugin, necesitaremos:

- **Buscar los plugins**
- **Seleccionar el plugin**
- **Programar el plugin**

#### Busqueda de plugins.

Hay varias formas de buscar automáticamente los plugins disponibles. Nosotros vamos a centrarnos en el uso de los *paquetes de espacios de nombre* o **namespace packages**. Para ello, debemos de usar las librerías **importlib** y **pkgutil**.

El procedimiento es sencillo: supongamos que hemos creado un paquete con nuestro plugin, y ese paquete está usando un espacio de nombres vacio, por ejemplo *graficas.plugins*. Usando **importlib** y **pkgutil**, lo que vamos a hacer es buscar en ese espacio de nombres todos los módulos que existan. La ventaja es que ese *espacio de nombre* puede ser compartido y poblado por diferentes librerías, las cuales pueden añadir sus propios módulos que cuelgan debajo de *graficas.plugins*:

    :::python
    import importlib
    import pkgutil

    import graficas.plugins

    def iter_namespace(ns_pkg):
        return pkgutil.iter_modules(ns_pkg.__path__, ns.pkg.__name__ + '.')

    
    discovered_plugins = {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in iter_namespace(graficas.plugins)
    }

Pero esto sólo nos soluciona una parte del problema, porque lo que hemos recuperado son los módulos, no las clases. Para poder recuperar las clases, necesitamos revisar los módulos y recuperar dichas clases, lo cual podemos hacer usando la librería **inspect**:

    :::python
    import inspect

    listado_plugins = list()
    for _,module in discovered_plugins.items():
        #Cuidado, ya que getmembers devuelve una tupla de dos elementos
        listado_plugins += inspect.getmembers(module, inspect.isclass)

De esta forma, podremos recuperar todas las clases que haya en los módulos recuperados, las cuales deben de ser los plugins. Este código se puede ampliar, por ejemplo, para que sólo recupere ciertas clases, o recupere únicamente funciones, pero cualquiera de estas operaciones debería de realizarse usando **mecanismos de reflexión**.

#### Seleccionar el plugin

¿Recordáis lo que decíamos antes, de que un plugin debe de contar con una interfaz común al resto de plugins? Es en esta interfaz donde podemos añadir información sobre nuestro plugin, la cual nos permita realizar una seleccion. Si programamos **métodos de clase** que nos proporcionen esa información, podemos consultarlos a través del listado de plugins y seleccionar el correcto:

    :::python
    class MiNuevoPlugin(PluginBase):
        def __init(self, data_init: Dict):
            super().__init__(data_init)
        
        @classmethod
        def nombre_plugin(cls):
            return 'MiNuevoPlugin'
        
        @classmethod
        def formatos_soportados(cls):
            return ['xlsx','csv']

Este seria el proceso por el cual podemos recuperar nuestros plugins consultando estos datos:

    :::python
    plugins_soportados = [p for p in listado_plugins if 'xlsx' in p[1].formatos_soportados()]

    #Tambien por nombre
    plugin_por_nombre = next((p for p in listado_plugins if p[1].nombre_plugin() == 'MiNuevoPlugin'),None)

Podemos ampliar estos métodos de clase para que proporcionen cualquier información relevante que necesitemos para seleccionar nuestros plugins.

#### Programar el plugin

Ya hemos adelantado mucho sobre lo que requiere el programar nuestro plugin. Por un lado, hemos visto que necestiamos una **clase base**. Esto no es imprescindible, podemos hacerlo sin una clase base, pero debemos de cuidar que **todos los plugins deben de compartir parte de la interfaz**, y la forma más sencilla de hacer esto es empleando *herencia de clases* y, en mi caso y porque soy así de especial, utilizo también *clases abstractas* para ello.

    :::python
    from abc import ABC, abstractmethod

    class PluginBase(ABC):
        def __init__(self,data_init: Dict):
            self.data_init = data_init #Datos de inicialización, puedes usar args y kwargs si quieres, pero voy con prisa :D
    
    @classmethod
    @abstractmethod
    def nombre_plugin(cls):
        pass
    
    @classmethod
    @abstractmethod
    def formatos_soportados(cls):
        pass
    
    @abstractmethod
    def run(self):
        pass

Esto debería de ser suficiente paraa nuestra clase base. Así, obligamos a que todos los plugins que compartan esta interfaz implementen los métodos de *nombre_plugin*, *formatos_soportados* y *run*, donde pondríamos el grueso de nuestro código.

### Empaquetar y distribuir.

En mi caso, me gusta que el código de selección de plugins esté en el proyecto principal, y colocar cada plugin en una librería diferente; igualmente, tengo una librería adicional aparte de los plugins donde tengo programado el plugin base con la interfaz que debe de implementar cada plugin.

A la hora de programar estos paquetes, utilizo **poetry** para ello. Se puede hacer también con *setup.py*, o con otros empaquetadores, pero ya estoy acostumbrado a usar **poetry**.

Para ello, debemos de modificar ligeramente la estructura que nos genera poetry: si nuestro proyecto se llama *graficas-plugins-mysql*, nos creará una carpeta llamada *graficas-plugins-mysql*, en la cual tendremos nuestro código y nuestro módulo. Debemos de bajar ese módulo un nivel, renombrando la carpeta superior como *graficas-plugins* y creando una nueva carpeta *mysql* dentro de esa carpeta. Y dejar *graficas-plugins* vacía. Luego, ajustar el código y modificar el archivo *pyproject.toml* de esta manera: 

    :::toml
    [tool.poetry]
    name = "graficas-plugins-mysql"
    version = "0.0.1"
    description = ""
    authors = ["bletter <aramirez@letteringenieros.es>"]
    packages = [
        { include = "graficas_plugins/mysql" }
    ]

De esta forma, estaremos creando un **namespace package** en toda regla. Sólo tenemos que ajustar el resto del código para que no nos falle, y ya tendríamos funcionando un esquema de plugins.

### Ventajas:

- Es más fácil de mantener y ampliar.
- Permite paralelizar el trabajo entre diferentes equipos de desarrollo.
- Mejora la distribución del código, si en diferentes máquinas es necesario que haya diferentes versiones de la librería para atender las necesidades de diferentes clientes.

### Inconvenientes:

- Requiere de una planificación previa, para elaborar la interfaz común
- Infraestructura para distribuir correctamente el código.
- Para un único equipo o equipos muy pequeños, puede resultar demasiado engorroso.