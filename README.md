# Sistema de Gestión de Seguros

Aplicación de escritorio para la gestión de seguros, construida con arquitectura en capas, interfaz gráfica en **Flet** y persistencia de datos en **MySQL** mediante **SQLModel**.

---

## Estructura del proyecto

```
.
├── assets/               # Recursos estáticos (logos, imágenes)
├── config/               # Configuración central y conexión a la base de datos
├── models/               # Esquema de datos con SQLModel
├── services/             # Lógica de negocio y autenticación
├── controllers/          # Controladores de interfaz y flujos de negocio
├── views/                # Páginas y componentes visuales
│   ├── componentes/      # Componentes de UI reutilizables
│   ├── asegurado/        # Vistas relacionadas con asegurados
│   └── seguimiento/      # Vistas de seguimiento de pólizas
├── scripts/              # Scripts SQL para inicialización de la base de datos
├── tests/                # Pruebas unitarias
│   ├── ui/               # Pruebas de interfaz
│   └── db/               # Pruebas de base de datos
├── main.py               # Punto de entrada de la aplicación
└── requirements.txt      # Dependencias del proyecto
```

---

## Requisitos previos

- Python 3.10 o superior
- MySQL 8.0 o superior
- pip

---

## Instalación y configuración


### 2. Crear y activar el entorno virtual

```powershell
python -m venv .venv
```

Activar en **PowerShell**:

```powershell
.venv\Scripts\Activate
```

Activar en **CMD**:

```cmd
.venv\Scripts\activate
```

### 3. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=3306
DB_NAME=aseguradora
```

### 5. Crear la base de datos

Ejecuta el script SQL para crear la base de datos y todas las tablas:

```powershell
mysql -u root -p < scripts/create_database.sql
```

---

## Ejecución

Con el entorno virtual activo, inicia la aplicación:

```powershell
python main.py
```

### Credenciales de acceso por defecto

| Campo        | Valor        |
|--------------|--------------|
| Clave agente | `admin1`   |
| Contraseña   | `1234` |

> ⚠️ Se recomienda cambiar estas credenciales antes de usar la aplicación en un entorno de producción.

---

## Pruebas

El proyecto incluye pruebas para la capa de interfaz y la lógica de base de datos.

Ejecutar **todas** las pruebas:

```powershell
pytest tests
```

Ejecutar pruebas por módulo:

```powershell
pytest tests/ui     # Pruebas de interfaz
pytest tests/db     # Pruebas de base de datos
```

### Vista previa del login

Para renderizar únicamente la pantalla de login sin cargar la aplicación completa:

```powershell
python tests/ui/run_login_example.py
```

---

## Tecnologías utilizadas

| Tecnología   | Uso                              |
|--------------|----------------------------------|
| Flet         | Interfaz gráfica de escritorio   |
| SQLModel     | ORM y definición del esquema     |
| MySQL        | Base de datos relacional         |
| python-dotenv| Gestión de variables de entorno  |
| pytest       | Pruebas unitarias                |