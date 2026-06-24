# IoT-Wearable-Health-Monitoring-System  

Prototipo de wearable que mide cuatro variables de una persona y su entorno —**frecuencia cardíaca, oxigenación (SpO₂), temperatura y humedad**— las almacena en una base de datos y las visualiza en una página web con gráficas en tiempo real.

Proyecto desarrollado para el curso **Internet de las Cosas** (Tecnológico de Monterrey, Campus Estado de México).

---

## ¿Cómo funciona?

El flujo de datos va del hardware a la web en tres etapas:

```
[ ESP1 + ESP2 ]  ──MQTT──>  [ Mosquitto ]  ──>  [ Node-RED ]  ──>  [ phpMyAdmin / MySQL ]  ──>  [ Flask + HTML ]
   sensores                   broker             flujo de datos        base de datos              página web
```

1. **ESP1** lee los sensores (MAX30102 y AHT10) y publica las mediciones por MQTT.
2. **ESP2** se suscribe a esos tópicos y muestra los valores en una pantalla OLED + anillo de LEDs.
3. **Mosquitto** es el broker MQTT que transporta los mensajes localmente.
4. **Node-RED** captura los datos y los inserta en la base de datos.
5. **phpMyAdmin / MySQL** almacena las mediciones junto con los datos del usuario.
6. **Flask + HTML** sirve la página web, que grafica los datos con un selector de periodo (semana / día / hora).

---

## Hardware

| Componente | Variable que mide / función |
|---|---|
| **MAX30102** | Frecuencia cardíaca y oxigenación (SpO₂) |
| **AHT10** | Temperatura y humedad |
| **ESP8266 (×2)** | Microcontroladores: ESP1 lee, ESP2 muestra |
| **Pantalla OLED SSD1306** | Muestra el valor de la fase activa |
| **Anillo NeoPixel WS2812 (16 LEDs)** | Feedback visual por color según la medición |

---

## Estructura del repositorio

```
.
├── README.md
├── .gitignore
│
├── firmware/
│   ├── esp1/
│   │   └── ESP1.ino          # Lectura de sensores + publicación MQTT
│   └── esp2/
│       └── ESP2.ino          # Pantalla OLED + LEDs + suscripción MQTT
│
└── web/
    ├── main.py               # Punto de entrada de la app Flask
    ├── requirements.txt
    └── Pagina/
        ├── __init__.py       # create_app() y registro de blueprints
        ├── auth.py           # Login y creación de cuenta
        ├── views.py          # Rutas de las 4 gráficas
        ├── templates/
        │   ├── MENU.html
        │   ├── LOGIN.html
        │   ├── CREAR.html
        │   ├── FREC.html     # Frecuencia cardíaca
        │   ├── OXIG.html     # Oxigenación
        │   ├── TEMPE.html    # Temperatura
        │   └── HUME.html     # Humedad
        └── static/
            ├── imgs/          # hum.jpg, temp.jpg, cocoro.jpg, oxi.jpg
            └── musica/        # audio del dashboard
```

> **Nota:** la carpeta `Pagina/` debe llamarse exactamente así, porque `main.py` la importa con `from Pagina import create_app`. Igual `templates/` y `static/`, que son los nombres por defecto de Flask.

---

## Requisitos

**Firmware (Arduino IDE):**
- Librerías: `ESP8266WiFi`, `PubSubClient`, `DFRobot_MAX30102`, `Adafruit_AHT10`, `Adafruit_NeoPixel`, `Adafruit_GFX`, `Adafruit_SSD1306`
- Soporte para placas ESP8266

**Web (Python 3):**
```
Flask
mysql-connector-python
```

**Infraestructura:**
- Broker MQTT Mosquitto
- Node-RED
- MySQL / phpMyAdmin con la base de datos `retov_1_0`

---

## Puesta en marcha

### 1. Base de datos
Crea la base `retov_1_0` con las tablas `usuario`, `pulso`, `oxigenacion`, `temperatura`, `humedad` y `wearable`.

### 2. Broker y flujo
Levanta **Mosquitto** y **Node-RED**, y configura el flujo que toma los tópicos MQTT y los inserta en la base.

### 3. Firmware
Abre cada sketch en el Arduino IDE, ajusta tus credenciales de red y la IP del broker, y carga:
- `ESP1.ino` en la primera placa
- `ESP2.ino` en la segunda

### 4. Página web
```bash
cd web
pip install -r requirements.txt
python main.py
```
La app corre en `http://127.0.0.1:5000`.

---

## Configuración a editar antes de usar

En los `.ino`:
```cpp
const char* SSID        = "TU_RED_WIFI";
const char* PASSWORD    = "TU_CONTRASEÑA";
const char* MQTT_SERVER = "IP_DEL_BROKER";
```

En `views.py` y `auth.py`:
```python
mysql_host     = "localhost"
mysql_user     = "root"
mysql_password = ""
mysql_database = "retov_1_0"
```

---

## Funcionalidades de la página

- Inicio de sesión por ID de usuario y creación de cuenta.
- Dashboard con acceso a las cuatro gráficas.
- Cada gráfica (Chart.js) con selector de periodo: última semana, último día o última hora.
- Estética retro/neón con un color por variable (rojo, azul, amarillo, verde).

---

## Mejoras pendientes

Cosas a tener en cuenta si el proyecto crece o el repo se hace público:

- **Credenciales en código:** la contraseña del WiFi está escrita directamente en los `.ino`. Conviene moverla a un archivo de configuración aparte (ignorado por git) antes de subir.
- **Inyección SQL:** los queries se arman concatenando texto con f-strings. Pasarlos a consultas parametrizadas haría la app mucho más segura.
- **Ideas que quedaron fuera por tiempo:** salida de audio que dicte el valor medido al cambiar de fase, y un diagnóstico personalizado por usuario (requiere validación médica y un sensor de pulso más preciso).
- **Sustentabilidad:** imprimir la carcasa con filamento de PET reciclado.

---

## Autores

- Ivan Alexander Melo Salgado
- Marco Antonio González Fernández
