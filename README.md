# Formulario de carga

Una aplicación web progresiva (PWA) diseñada para gestionar los registros de hallazgos e incidentes en ruta relaciones con operaciones logísticas y de seguridad

## Descripción 

Este proyecto permite a los usuarios registrar y administrar la información sobre hallazgos e incidentes en ruta de transporte. La aplicación está desarrollada en Python utilizando el framework Flask y está optimizada para dispositivos móviles. 

### Características principales:
- **Gestión de registros**: Permite registrar información sobre hallazgos e incidentes en ruta
- **Interfaz adaptativa**: Diseñada para usarse en dispositivos móviles.
- **PWA**: Puede instalarse en dispositivos como una aplicación nativa.
- **Seguridad y escalabilidad**: Diseñada para manejar más de 10.000 registros.

## Estructura del proyecto

FormularioCarga/
├── app/
│   ├── app.py              # Archivo principal de la aplicación
│   ├── config.py           # Configuración de la aplicación
│   ├── forms.py            # Lógica de los formularios y validaciones
│   ├── models.py           # Modelos de base de datos
│   ├── routes/             # Rutas de la aplicación
│   │   ├── hallazgos.py
│   │   ├── incidentes.py
│   │   └── __init__.py
│   └── templates/          # Plantillas HTML
│       ├── hallazgos/
│       │   ├── admin.html
│       │   └── formulario.html
│       ├── incidentes/
│       │   ├── admin.html
│       │   └── formulario.html
│       └── base.html
├── migrations/             # Migraciones de la base de datos
├── reports/                # Reportes generados
│   ├── hallazgos/
│   └── incidentes/
├── static/                 # Archivos estáticos
│   ├── css/
│   │   ├── bootstrap.min.css
│   │   └── style.css
│   ├── js/
│   │   ├── bootstrap.min.js
│   │   └── scripts.js
│   └── uploads/            # Imágenes subidas por los usuarios
├── .gitignore              # Archivos y carpetas ignorados por Git
├── requirements.txt        # Dependencias del proyecto
├── seed.py                 # Script para inicializar datos de prueba
└── README.md               # Documentación del proyecto

### 1. Requisitos previos 
1. **Python 3.10+**: Asegurarse de tener Python instalado en el sistema
2. **Entorno virtual**: El proyecto utiliza un entorno virtual para manejar dependencias

## Instalación
Seguir estos pasos para configurar el proyecto 

1. **Clonar el repositorio**:
´´´bash
git cloe <URL_DEL_REPOSITORIO>
CD FormularioCarga

2. **Crear y activar un entorno virtual**:

python -m venv venv
source venv/bin/activate #En Linux/Mac
venv\Scripts\activate #En Windows

3. **Instalar las dependencias**:

pip install -r requirements.txt

4. **Configurar las variables del entorno**:

Crear un archivo .evn en la raíz del proyecto con las siguientes variables:

FLASK_APP=app/app.py
FLASK_ENV=development
SECRET_KEY=tu_clave_secreta

5. **Realizar las migraciones de la base de datos**:

flask db init
flask db migrate -m "Inicialización de la base de datos"
flask db upgrade

6. **Ejecutar la aplicación**:

flask run 

## Dependencias instaladas 

El proyecto utiliza las siguientes librerías:

alembic==1.14.0
blinker==1.9.0
click==8.1.8
colorama==0.4.6
Flask==3.1.0
Flask-Migrate==4.0.7
Flask-SQLAlchemy==3.1.1
itsdangerous==2.2.0
Jinja2==3.1.5
Mako==1.3.8
MarkupSafe==3.0.2
SQLAlchemy==2.0.36
typing_extensions==4.12.2
Werkzeug==3.1.3
Flask-WTF==1.1.1
python-dotenv==1.0.0

## Estructura de la base de datos

El proyecto invluye dos apartados principales: 
1. **Hallazgos**:
    Hurto/Robo de mercadería 
    Consumo de mercadería 
    Consumo de sustancias ílicitas
    Malas practícas (Requiere detalles adicionales)
    Daños (Requiere detalles adicionales)

2. **Incidentes en ruta**:
    Robo parcial 
    robo total 
    Accidente
    Ruptura de sello
    Otros (Requiere detalles adicionales)

Ambos apartados están diseñados para soportar genereración de reportes y gráficos.

## Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles

## Historial de cambios 

Versión 1.0.0 (Enero de 2025)

    Creación de la estructura inicial del proyecto
    Implementación de formularios para registro de hallazgos e incidentes
    Configuración inicial de la base de datos y migraciones
    Configuración de ruta y planillas básicas
