Title: Feliz Halloween con Micropython y Pi Pico
Date: 2022-10-20 19:37
Modified: 2022-10-20 19:37
Category: Blog
Tags: pelican, publishing
Slug: halloween 
Authors: Antonio Ramírez
Summary: Controla luces LED con la ayuda de una Raspberry Pi Pico y Micropython 
Extract: Controla luces LED con la ayuda de una Raspberry Pi Pico y Micropython 6

## ¡La caja misteriosa!

Este es un ejemplo sencillo que podemos montar para Halloween con la ayuda de una Raspberry Pi Pico,
unas luces LED Neopixel, y un poquito de magia de Micropython. Así que preparad vuestro soldador, vuestros cables,
¡y vamos a ello!

### Lista de ingredientes:

- **Raspberry Pi Pico**: Pequeña placa microcontroladora de la Fundación Raspberry. A pesar de los problemas de stock
que hay para encontrar una Raspberry Pi, estas pequeñas maravillas son asequibles y fáciles de encontrar, y lo mejor es lo
fácil que resulta instalar MicroPython en ellas. Podéis haceros con una en [BricoGeek](https://tienda.bricogeek.com/placas-raspberry-pi/1513-raspberry-pi-pico.html?search_query=pi+pico&results=57) o en [Tiendatec](https://www.tiendatec.es/raspberry-pi-pico/1371-raspberry-pi-pico-5056561801445.html), pero si sois de fuera
de España seguro que las encontráis en alguno de los [proveedores](https://www.raspberrypi.com/products/raspberry-pi-pico/) oficiales de Raspberry o con un poco de búsqueda por Amazon.

![Pi Pico W]({static}/images/pi_pico_WEB.jpg)

- **LEDS de tipo Neopixel**: Los LEDS de tipo Neopixel, por Adrafruit, son RGB y direccionables, permitiendo cambiar el color de cada uno de ellos de forma independiente. Los que vamos a usar son de tipo WS2812 (existen variantes de estos como los WS2812b), utilizan tres cables (GND, DATA, VIN) y podemos encontrarlos en tira y en barra. Los podéis encontrar, de nuevo, en [Bricogeek](https://tienda.bricogeek.com/led-neopixel/660-barra-neopixel-8-x-ws2812.html?search_query=led&results=228). ¿Cual elegir, en tira o en barra? Depende, si los compráis en tira os vendrán con los conectores, pero en barra tendréis que soldar los cables... pero en tira os vendrán demasiados LEDS, y la Pi Pico no puede alimentar tantos, así que tendréis que cortar ocho. **NO PONGÁIS MÁS DE OCHO LEDS** con esta configuración que vamos a usar, ya que hay riesgo de que terminéis por quemar la placa.

![Barra de NeoPixels]({static}/images/neopixel_led_web2.jpg)

- **Soldador, cables, cables Dupont, placa de prototipado, lupa**: No son imprescindibles ni necesarios todos ellos, por ejemplo si compráis una Pi Pico con los pines soldados y tenéis la placa y una tira LED, no necesitáis el soldador, pero siempre bien tenerlos a mano.

### Instalar Thonny y Micropython

Lo primero que vamos a hacer es instalar **Micropython** en nuestra flamante Pi Pico. El método más sencillo e inmediato es hacerlo a través de [Thonny](https://thonny.org/). Es sencillo y amigable, y está pensado también para programar placas de este tipo. Desde la web, nos descargamos la versión que necesitemos para nuestro SO, y la instalamos siguiendo las indicadiones.

Una vez lo tenemos preparado, debemos de cargar Micropython en nuestra Pi Pico. Para ello, preparamos un cable MicroUSB a USB, conectamos un extremo a nuestra placa Pi Pico y, **manteniendo pulsado el único botón que tiene la Pi Pico**, la conectamos a nuestro ordenador. Esto hará que entre en el modo de carga compatible.

Ahora, lanzamos Thonny. En la esquina inferior derecha, veremos la versión de Python que estamos usando. Pulsando en ella con el ratón, nos saldrá un menú desplegable donde veremos, si lo hemos hecho correctamente, que aparece nuestra pequeña placa identificada.

![Thonny ve nuestra placa]({static}/images/thonny-micropython-pico-menu.png)

Si pulsamos en el nombre de nuestra placa, nos lanzará un menú para instalar la última versión del firmware de Micropython en nuestra Pi Pico. ¡Es así de fácil!


### Preparar el cableado

Cada agujero o pin que veis en los laterales de la placa, es un PIN de entrada y salida, y cada uno de ellos está numerado. De hecho, si le dáis la vuelta a la placa, podéis ver la numeración debajo. Lo mejor es que tengáis a mano un [diagrama](https://components101.com/sites/default/files/component_pin/Raspberry%20Pi-Pico-W-pinout.png) con los pines de conexión de la Pi Pico, y así no os perdéis. 

![Diagrama de pines](https://components101.com/sites/default/files/component_pin/Raspberry%20Pi-Pico-W-pinout.png)

Vamos a utilizar el pin **VBUS**, el primer **GND** de la derecha, y el **GP28**. Para que nos resulte más fácil, son el primer pin de la derecha, el tercer pin de la derecha, y el séptimo pin de la derecha, con el conector Micro USB de la placa orientado hacia arriba y el botón mirando hacia nosotros.

![Conexion Pi Pico]({static}/images/pi_pico_cableado_web.jpg)

El primer pin, **VBUS**, es el que nos proporciona corriente; el pin **GND** es el de tierra, y utilizaremos el **GP28** para mandar instrucciones a los LEDs. Así que debemos de conectar esos pines en el orden correcto en nuestra tira o barra de LEDs: el pin **VBUS** se conecta al **5VDC** de la barra, el pin **GND** se conecta al **GND**, y el **GP28** se conecta al **DIN**. Es importante tener en cuenta la orientación de nuestra tira o barra de LEDs, ya que la información fluye en un sentido único, normalmente indicado por una pequeña flecha en la tira. En el caso de la barra, podemos discernirlo si la nomenclatura del conector nos indica si es IN o OUT. **TODA ENTRADA DEBE DE HACERSE EN EL SENTIDO CORRECTO**.

![Conexion LEDs]({static}/images/neopixel_cableado_web.jpg)

Las tiras de LEDs normalmente vienen con un conector de tipo SM JST de 3 pines... uno como [estos](https://www.amazon.es/HUAZIZ-Conjuntos-Enchufe-Conector-Alambre/dp/B09LQ64HTG/ref=sr_1_2_sspa?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3QW9VLQ4TFW4F&keywords=sm+jst+3+pines&qid=1666528400&qu=eyJxc2MiOiIxLjk0IiwicXNhIjoiMC4wMCIsInFzcCI6IjAuMDAifQ%3D%3D&sprefix=sm+jst+3+pines%2Caps%2C85&sr=8-2-spons&psc=1). La barra de LEDs que he utilizado viene sin conector, pero como tenía cables conectores de esos, pues los he usado. Si no tenéis a mano, podéis usar cables de tipo Dupont, quitar el conector de un extremo, pelar el cable y soldarlo sobre el pad correspondiente de la barra de LEDs. Con los conectores SM JST, sólo hay que conectar el Dupont en el cable correspondiente. Los SM JST de 3 pines suelen seguir el esquema **ROJO - VERDE - BLANCO** o **ROJO - VERDE - NEGRO**, siendo el **VERDE** siempre el cable que corresponde al **DIN/DOUT**, el **ROJO** el cable del **VIN/5VDC**, y el **BLANCO/NEGRO** el que hace las veces del **GND**.

![Montaje final de placa]({static}/images/montaje_web.jpg)

Con esto, ya tenemos preparadas las conexiones. ¡Podemos pasar al código!

### Preparar el código

Para preparar el código, lo primero que debemos de hacer es abrir nuestro editor Thonny; nos aseguramos de que en la esquina inferior derecha
aparezca que estamos usando *MicroPython (Raspberry Pi Pico)*, lo cual significa que estamos conectados. Si nos da algún mensaje de error en
la parte de abajo, pulsaremos el botón de **Stop** que tenemos en la parte de arriba, para intentar volver a entrar en el ciclo REPL de la 
Pi Pico.

![Lanzando Thonny]({static}/images/thonny_01.png)

Pulsamos en **Abrir** u **Open** en caso de tenerlo en ingles, el segundo icono de la barra superior, y allí nos preguntará si queremos abrir
archivos en nuestra máquina o en la Pi Pico. Seleccionamos Pi Pico, y nos aparecerá un diálogo para abrir archivos.

![Abriendo archivos]({static}/images/thonny_2.png)

Debemos crear, como mínimo, dos archivos: un **main.py**, que contendrá el código que se ejecuta al encender la Pi Pico, y un archivo llamado **neopixel.py**. Este archivo **neopixel.py** corresponde a una librería para poder controlar LEDs de tipo Neopixel, y podemos descargarla de [blaz-r/pi_pico_neopixel](https://github.com/blaz-r/pi_pico_neopixel), un  repositorio de GitHub. Podemos copiar y pegar el contenido del archivo **neopixel.py**, o descargarnos el repositorio entero, descomprimir el archivo y copiar y pegar el archivo. Recordar guardar el contenido, pero para ello antes debemos de pulsar el botón de **Stop** para detener el ciclo REPL.

Una vez tenemos el archivo **neopixel.py** en nuestra Pi Pico, preparamos nuestro archivo **main.py** de la siguiente manera:

    :::python
    from neopixel import Neopixel

    # EVITA ERROR ENOENT
    rp2.PIO(0).remove_program()

    # Número de LEDs en nuestra barra o tira
    numpix = 8

    # Preparar nuestra barra
    # El primer argumento, es el numero de pixels
    # El segundo, es la maquina de estado a usar, dejarla a 0
    # El tercero, el pin GPIO que vamos a usar, en este caso el 28
    # El cuarto es el tipo de esquema de color, usaremos el GRB (Green Red Blue)
    # Consultar documentacion de blaz-r/pi_pico_neopixel
    strip = Neopixel(numpix, 0, 28, "GRB")

    # Ajustar el brillo de los pixels
    # Si reducimos el brillo, consumirán menos watios
    strip.brightness(100)

    # APAGAR PIXELS
    # Cuando detenemos el ciclo REPL, los pixels siguen encendidos.
    # Descomentar el siguiente codigo para apagarlos
    # while True:
    #     for i in range(numpix):
    #         strip.set_pixel(i,(0,0,0))
    #         strip.show()

    # PIXELS ROJOS, ENCENDIDO Y APAGADO GRADUAL
    # Utilizamos el espacio de color HSV (Tono, Saturacion, Valor)
    # a un Hue de 0, corresponde el color rojo; la saturación al máximo,
    # y el valor nos proporciona la transicion entre el encendido y el apagado.
    # Este esquema es lineal, pero con un poco de imaginacion podemos aplicar un
    # efecto si utilizamos una funcion sin() sobre el value para una variacion de la
    # iluminacion diferente.
    # De nuevo, consultar documentacion de blaz-r/pi_pico_neopixel para saber el funcionamiento
    # del espacio de color HSV en su librería. Enlaza a documentacion de Adafruit.
    hue = 0
    value = 0
    increment = 1
    decrement = -1
    current_operation = increment
    while(True):
        color = strip.colorHSV(hue, 255, value)
        strip.fill(color)
        strip.show()
        
        if value == 0:
            current_operation = increment
        if value == 255:
            current_operation = decrement
            
        value = value + current_operation

Y, ¡listo! Usando este código, podemos hacer un efecto de iluminación parecido a un latido, donde se enciende y se apaga poco a poco con
un tono rojo. Ahora podemos coger una caja de cartón, una calabaza o cualquier cosa que tengamos a mano, meter dentro nuestra tira, y conectar
un cargador de móvil con un cable MicroUSB a nuestra Pi Pico... ¡y tendremos una iluminación perfecta para Halloween!

![Happy Halloween]({static}/images/happy_hallowen.jpg)

¡Pasádlo bien!