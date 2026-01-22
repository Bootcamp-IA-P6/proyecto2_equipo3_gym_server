


🏋️‍♂️ GYMPRO - Sistema de Gestión de Gimnasio
Este es un sistema de backend robusto diseñado para gestionar las operaciones diarias de un gimnasio. Permite al  administrador dar de alta en el sistema a usuarios, entrenadores, alumnos y administradores y gestionar para poder visualizar quienes estan de alta o baja 

🚀 Tecnologías Utilizadas
Framework: FastAPI (Python)

Base de Datos: Supabase (PostgreSQL)

ORM: SQLAlchemy

Contenerización: Docker & Docker Compose

📂 Estructura del Proyecto (Jerarquía)
Plaintext
GYMPRO-BACKEND/
├── .github/                 Automatización y CI/CD
│   └── workflows/           Archivos YAML para pruebas y despliegues automáticos
├── config/                  Ajustes globales (Variables de entorno, CORS)
├── controllers/             Lógica de negocio (El cerebro que une rutas y modelos)
├── core/                    Seguridad (Validación de JWT, Roles y permisos)
├── database/                Conexión a Supabase y configuración de SQLAlchemy
├── docs/                    Especificaciones técnicas y documentación extra
├── models/                  Modelos de base de datos (Clases de SQLAlchemy)
├── routes/                  Endpoints de la API (usuarios, clases, entrenadores)
├── schemas/                 Validación de datos de entrada/salida (Pydantic)
├── tests/                   Pruebas unitarias y de integración (Auth, CRUD)
├── utils/                   Funciones de apoyo (Exportación CSV, Helpers)
├── app.py                   Punto de entrada principal de FastAPI
├── docker-compose.yml       Orquestación de contenedores
├── Dockerfile               Configuración de la imagen del backend
└── requirements.txt         Dependencias de Python

🛠️ Funcionalidades Principales (CRUD)
El sistema permite al Administrador realizar las siguientes acciones:

Gestión de Usuarios: Registro, modificación y eliminación de Alumnos, Entrenadores y otros Administradores.

Control de Clases: Crear nuevas sesiones de entrenamiento, actualizar horarios o cancelar clases.

Asignación de Roles: Vincular entrenadores específicos a clases y alumnos a membresías.

Persistencia: Todo se sincroniza en tiempo real con Supabase.

🐳 Dockerización y Despliegue
Para asegurar que el proyecto funcione en cualquier computadora, hemos implementado Docker siguiendo estos pasos:

1. Creación del Dockerfile
Configuramos la imagen base de Python, instalamos las dependencias de requirements.txt y definimos el comando para ejecutar Uvicorn. Esto garantiza que el entorno de ejecución sea siempre el mismo.

2. Configuración de docker-compose.yml
Para facilitar el desarrollo local, usamos Docker Compose. Este archivo orquesta nuestro backend:

Mapea los puertos (ej. 8000:8000).

Carga las variables de entorno necesarias para conectar con Supabase.

Permite levantar todo el sistema con un solo comando.

Pasos para ejecutar:

Construir la imagen: docker-compose build

Levantar el contenedor: docker-compose up

⚙️ Instalación Local
Clona el repositorio.

Crea un archivo .env con tus credenciales de Supabase.

Instala dependencias:

Bash
pip install -r requirements.txt
Ejecuta la aplicación:

Bash
uvicorn app:app --reload

GYMPRO-BACKEND/
├── .github/                # Automatización y CI/CD
│   └── workflows/          # Archivos YAML para pruebas y despliegues automáticos
├── config/                 # Ajustes globales (Variables de entorno, CORS)
├── controllers/            # Lógica de negocio (El cerebro que une rutas y modelos)
├── core/                   # Seguridad (Validación de JWT, Roles y permisos)
├── database/               # Conexión a Supabase y configuración de SQLAlchemy
├── docs/                   # Especificaciones técnicas y documentación extra
├── models/                 # Modelos de base de datos (Clases de SQLAlchemy)
├── routes/                 # Endpoints de la API (usuarios, clases, membresías)
├── schemas/                # Validación de datos de entrada/salida (Pydantic)
├── tests/                  # Pruebas unitarias y de integración (Auth, CRUD)
├── utils/                  # Funciones de apoyo (Exportación CSV, Helpers)
├── app.py                  # Punto de entrada principal de FastAPI
├── docker-compose.yml      # Orquestación de contenedores
├── Dockerfile              # Configuración de la imagen del backend
└── requirements.txt        # Dependencias de Python

🌟 Resumen del Proyecto: GYMPRO BackendGYMPRO no es solo un CRUD; es un ecosistema de gestión diseñado para la escalabilidad y la eficiencia operativa. 

    Hemos construido una infraestructura que permite a los administradores de gimnasios automatizar tareas complejas —desde la gestión hasta la asignación de entrenadores— bajo una arquitectura de "Cero Fricción".
    
       🛠️ El Stack Tecnológico (¿Por qué estas herramientas?)FastAPI (Python): Elegimos este framework por su velocidad asíncrona y la generación automática de documentación (Swagger). Nos permite manejar múltiples peticiones de usuarios al mismo tiempo sin degradar el rendimiento.
       
       
    Supabase (PostgreSQL): Proporciona la solidez de una base de datos relacional con la velocidad de un Backend-as-a-Service. Gracias a esto, la persistencia de datos de los alumnos y las clases es instantánea y segura.SQLAlchemy: Como ORM, nos permite interactuar con la base de datos usando objetos de Python, facilitando el mantenimiento del código y evitando errores en las consultas SQL.Docker & Docker Compose: Eliminamos el clásico "en mi computadora sí funciona". Todo el entorno está empaquetado para que el despliegue sea idéntico en desarrollo, pruebas y producción.
    
    
    💡 Beneficios ClaveBeneficioDescripción TécnicaSeguridad de Grado Empresarial Validación estricta de roles (Admin, Trainer, Student) mediante Tokens JWT y validación en el core.Escalabilidad Inmediata Gracias a la arquitectura por carpetas, añadir nuevas funciones (como pagos o reserva de máquinas) es modular y limpio.
    
    Documentación VivaAl estar basado en FastAPI, el sistema se documenta solo, permitiendo que otros desarrolladores se integren en minutos.Despliegue en 1 ClickCon Docker Compose, cualquier miembro del equipo puede levantar el backend completo con un solo comando.