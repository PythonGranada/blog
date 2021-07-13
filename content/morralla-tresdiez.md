Title: Qué de morralla en el changelog de Python 3.10
Date: 2021-06-28 18:20
Category: Blog
Slug: morralla-tresdiez
Authors: Antonio Ramirez
Tags: 3.10
Extract: Veamos qué trae de nuevo Python 3.10

Dentro de poco se nos viene la nueva Python 3.10 (bueno, dentro de poco según los tiempos de desarrollo, que todavía colea Pyhton 2.7 por ahí), así que es
un buen momento para repasar qué trae de nuevo e interesante.. o no interesante.

### Podemos usar paréntesis con los gestores de contexto

Vale, esta novedad parece un poco extraña... ¿a qué se refiere con los gestores de contexto?

Si alguna vez has tenido que acceder al contenido de un archivo de texto, esto te tiene que sonar:

    :::python
    with open(file_path,'r') as origen:
        data = origen.read()

Bien, ese *open* que aparece dentro del *with* es un gestor de contexto o **context manager**. En este caso, nos proporciona un acceso al archivo mientras estemos dentro del contexto de *with* (no nos salgamos de la indentación). Cuando termina el contexto de *with*, es decir, abandonamos la indentación, se cierra el acceso al archivo.

Con los cambios de Python 3.10, ahora podemos hacer algo como esto:

    :::python
    with (
        open(file_path_a, 'r') as origen_a,
        open(file_path_b, 'w') as destino_b,
    ):
        destino_b.write(origen_a.read())

Es decir, podemos encerrar los contextos en múltiples líneas usando paréntesis. ¿Es interesante? Podemos decir que sí, ya que nos permite reducir el númnero de anidamientos si estamos utilizando múltiples contextos. ¿Lo usaremos mucho en el día a día? Puede que no.

### Mejores mensajes de error

En la versión 3.10, los mensajes de error que devuelve el interprete de Python son más claros y nos dan más información. Por ejemplo, los *SyntaxError* ahora nos marcarán toda la expresión que ha fallado, en lugar de indicar la posición donde se ha detectado el error:

    :::python 
    File "<stdin>", line 1
        foo(x, z for z in range(10), t, w)
               ^^^^^^^^^^^^^^^^^^^^
        SyntaxError: Generator expression must be parenthesized

Otros errores también se beneficiarán de esto, como por ejemplo *IndentationError*, *AttributeErrors* y *NameErrors*.

¿Es interesante? Mucho, ya que mejores mensajes de error nos facilitan mucho el trabajo. ¿Lo usaremos día a día? Siempre.

Aunque siempre queda la duda de qué se entiende por *mensajes de error más claros*, ya que eso no significa que de primeras vayamos a leer el error y encontrar el fallo.

### Soporte de switch-case

Aunque en el changelog aparezca como **Structural Pattern Matching**, la idea general viene a ser la misma: tendremos por fin la posibilidad de hacer un *switch-case* como estamos acostumbrados en otros lenguajes. Esta será la sintaxis:

    :::python
    match subject:
        case <pattern_1>:
            <action_1>
        case <pattern_2>:
            <action_2>
        case _:
            <action_wildcard>

¿Y cómo funcionará? Veámoslo con un ejemplo:

    :::python
    r = requests.get('http://localhost')

    status = r.status

    match status:
        case 200:
            return 'Todo correcto'
        case 400:
            return 'Bad request'
        case 404:
            return 'Not found'
        case _:
            return 'Vete a saber qué ha pasado'

En caso de tener el código de arriba en una función, si la petición HTTP nos devuelve un status 400, la función devuelve un 'Bad Request', un 200 devuelve un 'Todo correcto', y así. El *case _* es opcional, y se pueden encadenar opciones con el operador *|* u *or*:

    :::python
    case 400 | 404:
        return 'Cosas chungas con la petición'


Podremos evaluar tipos un poco más complejos, como tuplas o diccionarios, y evaluar valores literales y también mediante variables. Veamos un ejemplo con una tupla:

    :::python
    point = (12,33)

    match point:
        case (0,0):
            print('Origen')
        case (0,y):
            print(f'Y={y}')
        case (x,0):
            print(f'X={x}')
        case (x,y):
            print(f'X={x}, Y={y}')

Dentro del *match*, si la tupla es (0,0), saltará el primer *case*, pero si el primer elemento de la tupla es un valor literal (en este caso, 0) y el segundo es diferente, entonces saltará el segundo.

También se aplicará a clases, e incluso se podrá usar con listas... ¡y también añadiendo guardas!

    :::python
    point = Point(2,15)

    match point:
        case Point(x,y) if x==y:
            print(f'Punto en la diagonal de {x}')
        case Point(x,y):
            print('Punto fuera de la diagonal')

Muy interesante y muy útil, ya que nos permitirá reducir el código usado para selecciones que hasta ahora dependía de múltiples sentencias **if**, a veces anidadas.

### ¿Y qué más cosas?

Bien, también trae mejoras para los *type hints*. ¿Y qué son los *type hints*? Puede que te suenen más por el nombre de **anotaciones**, si en algún momento te has encontrado con cosas similares a estas:

    :::python
    def funcion_retorno(iteracion: int, timestamp: datetime) -> str:
        return 'ok'

Las anotaciones son indicaciones acerca de los tipos empleados, tanto en la declaración de las variables como de los valores retornados por funciones, que se utiliza sobre todo por analizadores sintácticos de código. No afectan al funcionamiento básico de Python (es decir, una anotación no implica una restricción fuerte para el tipo empleado, puedes declarar iteracion como *int* y aún así pasarle un *float* o un *Decimal* o un *str*), sino que se entiende más como una indicación al programador... aunque algunas librerías como por ejemplo [pydantic](https://pydantic-docs.helpmanual.io/) hagan uso de estas anotaciones para trabajar.

No voy a extenderme con las anotaciones porque... bueno, sé que hay poca gente que las use. Símplemente echadle un vistazo a [este artículo](https://betterprogramming.pub/twenty-type-hinting-techniques-and-tools-for-better-python-code-e877e0b0c679) para ver cómo funciona la cosa.

¿Otras partes que han recibido cariño? Muchas, por eso este artículo habla de *morralla*... y aquí tenéis, [toda la morralla](https://docs.python.org/3.10/whatsnew/3.10.html) para que la podáis leer a gusto.