# 🏋️‍♂️ GYMPRO - Sistema de Gestión de Gimnasio

### 📋 Descripción
**GYMPRO** es un sistema de backend robusto y escalable diseñado para centralizar y automatizar las operaciones diarias de un gimnasio. La plataforma permite una administración integral de personal y clientes, facilitando el control de altas, bajas y la organización de actividades deportivas en tiempo real.


![Python](https://img.shields.io/badge/PYTHON-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FASTAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Supabase](https://img.shields.io/badge/SUPABASE-PostgreSQL-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Docker](https://img.shields.io/badge/DOCKER-5.1-2496ED?style=for-the-badge&logo=docker&logoColor=white)

**API REST profesional para la gestión integral de entrenamientos y usuarios**

[Características](#-características-principales) • [Instalación](#-instalación-local) • [Análisis de Datos](#-análisis-del-modelo-de-datos) • [API](#-endpoints-principales) • [Despliegue](#-dockerización)

### 🎯 Objetivo del Proyecto
Proporcionar una herramienta administrativa eficiente que permita gestionar el ciclo de vida de usuarios (alumnos, entrenadores y administradores) y la programación de clases, garantizando la integridad de los datos mediante una arquitectura moderna y segura.

---


## 📊 Análisis del Modelo de Datos



**¿Qué representa este diagrama?** Este esquema define la arquitectura relacional de la base de datos de **GYMPRO**.  
Se basa en una estructura de cuatro entidades clave interconectadas que permiten el flujo  
de información entre el personal administrativo, los instructores y los alumnos.

### 📋 Resumen de Entidades

**`users`** Es la tabla maestra. Almacena la identidad de cada persona (nombre, email, hash de contraseña)  
y define su permiso mediante un campo `role` (Admin/User).

**`trainers`** Una extensión de la tabla de usuarios. Aquí se guarda la información específica de los  
profesionales, como su `specialty`, vinculándolos directamente a su perfil de usuario.

**`classes`** El catálogo de actividades disponibles. Define el nombre y la descripción de  
cada entrenamiento ofrecido por el gimnasio.

**`user_class`** La tabla de unión (Many-to-Many). Es el motor del sistema, ya que conecta a un  
**usuario** (alumno) con una **clase** específica y le asigna un **entrenador** responsable.

---

### 💡 Beneficios Técnicos

**1. Integridad Referencial** La base de datos evita la duplicidad de información. Si un entrenador cambia su especialidad,  
se actualiza en un solo lugar y se refleja en todo el sistema automáticamente.

**2. Escalabilidad de Roles** El diseño permite separar la lógica de un usuario común de la de un entrenador,  
facilitando la adición de nuevos perfiles profesionales en el futuro.

**3. Trazabilidad Total** Permite saber exactamente qué alumnos están inscritos en cada clase y quién es el  
instructor a cargo, facilitando reportes de asistencia y desempeño.

**4. Seguridad de Datos** La separación de credenciales permite implementar políticas de seguridad (JWT)  
de manera centralizada, protegiendo la información sensible del gimnasio.

---



 <img src="https://github.com/Bootcamp-IA-P6/proyecto2_equipo3_gym_server/blob/main/docs/img/diagrama.png?raw=true" alt="Diagrama de Base de Datos GYMPRO" width="850">

### ✨ Características Principales

**👥 Gestión de Usuarios y Roles**
* ✅ **CRUD Completo:** Registro, consulta, edición y eliminación de Alumnos, Entrenadores y Administradores.
* ✅ **Control de Estado:** Visualización y gestión de usuarios activos e inactivos (altas/bajas).
* ✅ **Sistema de Roles:** Permisos diferenciados según el tipo de perfil dentro del sistema.

**📅 Control de Actividades**
* ✅ **Gestión de Clases:** Creación, actualización de horarios y cancelación de sesiones.
* ✅ **Asignaciones:** Vinculación directa de entrenadores a clases específicas y alumnos a sus respectivas membresías.

**🛡️ Persistencia y Seguridad**
* ✅ **Sincronización Real-Time:** Integración con Supabase para actualización instantánea de datos.
* ✅ **Validación Estricta:** Uso de Pydantic para asegurar que los datos de entrada cumplan con los requisitos del negocio.
* ✅ **Seguridad JWT:** Infraestructura preparada para la validación de tokens y protección de rutas.




---

### 🚀 Tecnologías

| Categoría | Tecnologías |
| :--- | :--- |
| **Runtime** | Python 3.10+ |
| **Framework** | FastAPI |
| **Base de Datos** | Supabase (PostgreSQL) |
| **ORM** | SQLAlchemy |
| **Validación** | Pydantic |
| **Contenerización** | Docker, Docker Compose |
| **Servidor ASGI** | Uvicorn |

---

### 📦 Instalación Local

**1️⃣ Clonar el repositorio**
```bash
git clone [https://github.com/Bootcamp-IA-P6/proyecto2_equipo3_gym_server.git]


2️⃣ Configurar variables de entorno Crea un archivo .env en la raíz del proyecto con tus credenciales de Supabase:

Fragmento de código

SUPABASE_URL=tu_url_de_supabase
SUPABASE_KEY=tu_anon_key
DATABASE_URL=postgresql://postgres:password@db.supabase.co:5432/postgres

3️⃣ Instalar dependencias
Bash
pip install -r requirements.txt

4️⃣ Ejecutar la aplicación

Bash
uvicorn app:app --reload
💡 La documentación automática estará disponible en: http://localhost:8000/docs

🐳 Dockerización
El proyecto está completamente preparado para entornos de contenedores, lo que garantiza que funcione de manera idéntica en cualquier máquina.

Dockerfile: Configura la imagen base de Python, instala dependencias y optimiza el entorno de ejecución.

Docker Compose: Orquesta el backend, mapea los puertos (8000:8000) y carga automáticamente las variables de entorno.

Comandos rápidos:

Bash
# Construir la imagen
docker-compose build

# Levantar el sistema
docker-compose up -d
📁 Estructura del Proyecto
Plaintext
GYMPRO-BACKEND/
├── src/
│   ├── routes/          # Endpoints de la API (usuarios, clases, entrenadores)
│   ├── controllers/     # Lógica de negocio (Cerebro que une rutas y modelos)
│   ├── models/          # Modelos de base de datos (SQLAlchemy)
│   ├── schemas/         # Validación de datos entrada/salida (Pydantic)
│   ├── database/        # Conexión a Supabase y configuración de DB
│   ├── core/            # Seguridad (Validación de JWT, Roles y permisos)
│   ├── config/          # Ajustes globales (Variables de entorno, CORS)
│   ├── utils/           # Funciones de apoyo (Exportación CSV, Helpers)
├── tests/               # Pruebas unitarias y de integración
├── docs/                # Especificaciones técnicas adicionales
├── .github/workflows/   # Automatización y CI/CD
├── Dockerfile           # Configuración de imagen Docker
├── docker-compose.yml   # Orquestación de contenedores
└── requirements.txt     # Dependencias del proyecto
📝 Scripts Disponibles
npm run dev (o el comando equivalente en Python):

uvicorn app:app --reload: Inicia el servidor de desarrollo.

pytest: Ejecuta la suite de pruebas.

docker-compose up: Levanta la infraestructura completa.

👩‍💻 Equipo de Desarrollo
Tu Nombre - GitHub - LinkedIn

## 🔌 Endpoints Principales

### Base URL
`http://localhost:8000`

### 🔐 Autenticación y Usuarios
| Método | Endpoint | Descripción | Auth |
| :--- | :--- | :--- | :---: |
| POST | `/auth/login` | Iniciar sesión y obtener token | ❌ |
| GET | `/users` | Listar todos los usuarios (Alumnos/Entrenadores) | ✅ Admin |
| POST | `/users` | Crear un nuevo usuario | ✅ Admin |
| GET | `/users/:id` | Obtener detalle de un usuario específico | ✅ Admin |
| DELETE | `/users/:id` | Dar de baja a un usuario | ✅ Admin |

**Ejemplo: Crear Usuario (Alumno/Entrenador)**
`POST /users`

```json
{
  "username": "jdoe_gym",
  "email": "jdoe@example.com",
  "full_name": "John Doe",
  "role": "alumno",
  "status": "activo",
  "password": "SecurePassword123"
}
🏋️‍♂️ Gestión de ClasesMétodoEndpointDescripciónAuthGET/classesListar todas las clases programadas❌POST/classesCrear una nueva sesión de entrenamiento✅ AdminPUT/classes/:idActualizar horario o entrenador de una clase✅ AdminDELETE/classes/:idCancelar/Eliminar una clase✅ AdminEjemplo: Crear ClasePOST /classesJSON{
  "name": "Crossfit Avanzado",
  "schedule": "2024-05-20T10:00:00",
  "trainer_id": 5,
  "capacity": 20,
  "room": "Sala A"
}
🛡️ Seguridad y Buenas PrácticasEn GYMPRO, la seguridad es nuestra prioridad. Hemos implementado:✅ Validación de Datos: Cada entrada es filtrada por modelos de Pydantic para evitar datos corruptos.✅ Haseo de Contraseñas: Las claves nunca se guardan en texto plano, usamos algoritmos de encriptación fuerte.✅ Protección de Rutas: Middleware especializado que verifica el rol del usuario antes de permitir acciones CRUD.✅ CORS: Configurado para permitir peticiones únicamente desde el dominio de tu Frontend oficial.