Title: Programando con QT (1)
Date: 2021-06-28 18:20
Category: Blog
Slug: qtforpython-parteuno
Authors: Antonio Ramirez
Tags: UI,Qt for Python
Extract: Programando interfaces gráficas con Python y Qt

Ahora que se acercan las Navidades y vamos a tener todos algo más de tiempo libre **(¡mentira!)**, ¿por qué no aprovechar para aprender a
programar interfaces gráficas para nuestros proyectos en Python?

Este artículo es el primero de una serie donde iremos explicando, paso a paso, cómo podemos escribir una interfaz gráfica para nuestros programas y scripts en Python, utilizando para ello las librerías de Qt for Python.

## PARTE 1 - Historia y preparativos

### Historia de Qt for Python.

**(TL;DR)** Baste decir que Qt es una librería originalmente escrita en C++ para desarrollo de interfaces gráficas. El *proyecto KDE* la tomó como base, y la empresa original, *Trolltech*, fue comprada por *Nokia*, que después fue absorbida por *Microsoft*, que luego la vendió a *Digia*, que después se estableció como *The Qt Company*.

Después de todo esto, surgieron *bindings* de la librería para Python como los módulos *PySide2* y *PySide6*.

### Preparativos

No vamos a necesitar demasiado para empezar:

- *Python 3.6 o superior.* En mi caso, utilizaré Python 3.10, así que el código puede verse extraño. Si veis un *match case*, recordad que se convierte en un bloque *if elsif*.
- *Pipenv:* Para gestionar y manejar el entorno virtual. Podéis utilizar cualquier otro gestor de entornos virtuales, o incluso directamente *virtualenv*, *venv* y *pip*. Yo lo empleo por comodidad.
- *Qt Creator:* Herramienta de Qt para trabajar con interfaces gráficas.

#### Instalando Qt Creator.

Si estás en *Ubuntu*, puedes instalarlo desde consola:

    :::console
    sudo apt install qtcreator

En el caso de emplear *Fedora o derivados de RedHat*:
    
    :::console
    sudo dnf install qt-creator

o el equivalente con *yum*:

    :::console
    sudo yum install qt-creator

En el caso de *Windows o MacOS*, debes de utilizar los instaladores oficiales de Qt. Para ello, tienes que ir a [su página web](https://www.qt.io/download), y seleccionar la opción **Go open source**, para luego buscar abajo en la página el enlace de **Download the Qt Online Installer**. Ojo con esto, ya que Qt funciona con una licencia dual de tipo Comercial / Open Source, y si intentamos descargar la versión comercial nos pedirá que rellenemos un formulario y darnos de alta como cliente.

Una vez tengamos descargados el instalador online, podemos ejecutarlo y, tras crearnos una cuenta de Qt en caso de no tenerla (tranquilos, que es gratuita), podremos seleccionar aquellas herramientas que queramos. *Qt Creator* está en el apartado de *Tools* (Herramientas), así que nos aseguramos de seleccionarlo y descargarlo. A partir del mismo instalador podemos actualizar a nuevas versiones o instalar otros paquetes en caso de necesitarlos.

### Preparando nuestro entorno.

Para empezar, crearemos una carpeta para nuestro pequeño proyecto, donde vamos a definir un *.gitignore* básico para Python (podemos sacarlo [de GitHub](https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore) o de cualquier otro proyecto que tengamos por ahí)

    :::console
    mkdir tutorialQt
    cd tutorialQt
    nano .gitignore

Una vez tengamos preparado el .gitignore, podemos empezar a preparar nuestro Pipfile con el entorno que necesitemos:

    :::console
    pipenv --python 3.10
    pipenv install pyside6

Esto nos prepara un entorno virtual y nos instala las dependencias para las librerías de Qt 6; si queremos usar las librerías de la versión 5.12,
usaríamos *pipenv install pyside2*. Al final, nuestro archivo Pipfile debe de parecerse a esto:

    :::ini
    [[source]]
    url = "https://pypi.org/simple"
    verify_ssl = true
    name = "pypi"

    [packages]
    pyside6 = "*"

    [dev-packages]

    [requires]
    python_version = "3.10"

### Esqueleto de la aplicación

Nuestro siguiente paso va a ser crear un punto de entrada y la ventana principal para nuestra aplicación.

#### Creando la ventana principal

Vamos a crear un módulo llamado *mainwindow* dentro del proyecto:

    :::console
    mkdir mainwindow
    touch mainwindow/__init__.py

Después lanzamos el Qt Creator, seleccionamos **Nuevo archivo o proyecto**, y luego dentro del menú de *Qt*, la opción de *Qt Designer Form* para poder crear un nuevo *widget* o componente a partir de una plantilla previa:

![Menú de capturas]({static}/images/qt_creator_01.jpg)

Luego, debemos de seleccionar el tipo de *widget* o componente que queremos usar como base de nuestro nuevo componente, en este caso queremos una ventana principal o *main window*, y la queremos guardar dentro del módulo que acabamos de crear, así que seleccionamos la ruta del módulo para que nos guarde ahí el archivo:

![Seleccionar main window]({static}/images/qt_creator_02.jpg)

Por último, vamos a incluir en nuestra pantalla principal un pequeño texto que diga 'Hello World!'. Para ello, en la columna de la izquierda buscamos y seleccionamos **Label**, y arrastramos y soltamos dentro de nuestro widget. Lo colocamos centrado, y luego si pulsamos dos veces en ese label, podemos editar el texto para que diga *Hello World!*

![Añadir un label]({static}/images/qt_creator_03.jpg)

Una vez lo tenemos listo, le damos a guardar. Deberíamos de tener ahora en nuestro módulo *mainwindow* un archivo llamado *mainwindow.ui*, el cual representa nuestra interfaz gráfica. Este arhcivo aún no lo podemos usar tal cual, sino que debemos decirle a Python que lo cargue y lo asocie a nuestro código (las interfaces con extensión .UI son, en realidad, código XML). Existen varias formas de lograr eso, pero vamos a ir a la más sencilla y simple.

Para poder cargar nuestra interfaz y asociarla a una clase, activamos nuestro entorno virtual y lanzamos la instrucción *pyside6-uic* (*pyside2-uic* si estamos trabajando con PySide2 y Qt 5.12):

    :::console
    pipenv shell
    pyside6-uic mainwindow/mainwindow.ui > mainwindow/ui_mainwindow.py

Esto nos generará un archivo llamdo **ui_mainwindow.py** el cual permitirá cargar la interfaz. Para poder usarlo, ahora sí, creamos un archivo **mainwindow.py** dentro del módulo:

    :::python
    # mainwindow/mainwindow.py

    from PySide6.QtWidgets import QMainWindow

    from .ui_mainwidow import Ui_MainWindow

    class MainWindow(QMainWindow):

        def __init__(self):
            super().__init__()
            self.ui =Ui_MainWindow()

            self.ui.setupUi(self)

Cuando necesitemos acceder a algún elemento de la interfaz, podemos hacerlo a través de *self.ui*.

#### Creando el punto de entrada.

Nuestro punto de entrada va a ser un archivo llamado **app.py** en la raíz del proyecto. En este archivo escribiremos el código necesario para lanzar nuestra aplicación:

    :::console
    # app.py

    import sys

    from PySide6 import QtWidgets

    from mainwindow.mainwindow import MainWindow

    if __name__ == '__main__':

        app = QtWidgets.QApplication([])

        mainWindow = MainWindow()
        mainWindow.show()

        sys.exit(app.exec())

Con esto, ya podemos lanzar nuestra interfaz gráfica desde la consola en la que tenemos activado el entorno virtual:

    :::console
    python app.py

Si todo ha ido bien, deberíamos de ver nuestra pequeña interfaz gráfica.
