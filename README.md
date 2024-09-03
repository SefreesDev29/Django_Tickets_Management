# SISTEMA DE BOLETERÍA

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=101010)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2+-092E20?style=for-the-badge&logo=django&logoColor=white&labelColor=101010)](https://www.djangoproject.com/)

El aplicativo cuenta con:
- **Login de autenticación**
- **Validación de máximo 3 intentos** o bloqueo de cuenta
- **Reseteo de contraseña por correo**
- **Log de accesos** con una captura de datos del usuario logueado
- **Actualización de perfil** para actualizar información personal y contraseña
- **Manejo de roles** para acceder a módulos
- **Gestión de usuarios** para actualizar datos y roles
- **Auditoría por modelos** para rastrear acciones (creación, actualización y eliminación)
- **Configuración de sistema** para modificar el título del aplicativo, autor, logo, fondo y dashboard

Basado en una plantilla de Bootstrap 4, con el uso de JQuery y Ajax, entre otros plugins.

## Instalación

### 🛠️ 1.1 Instalar MySQL

- **[Link de descarga](https://dev.mysql.com/downloads/installer/)**: Descargar la versión "mysql-installer-community" (opción web si la conexión de red es fuerte)
- Hacer clic en "No thanks, just start my download."
- Ejecutar el paquete de instalación, seleccionar tipo "Custom" y elegir MySQL server y Workbench (opcional). Hacer clic en "Execute".
- Configurar el puerto (default) y establecer una contraseña segura. Recuerda la contraseña para más adelante.

### 🛠️ 1.2 Instalar PostgreSQL

- **[Link de descarga](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)**
- Elegir la opción recomendada según el SO y arquitectura de tu equipo
- Ejecutar el paquete de instalación, seleccionar la carpeta de guardado
- Elegir los componentes a instalar: PostgreSQL Server y Command Line Tools
- Configurar el puerto (default) y establecer una contraseña segura. Recuerda la contraseña para más adelante.
- Seleccionar la región (default) e instalar.

### 🗄️ 2.1 Configuración MySQL

Usar Workbench, línea de comandos o tu gestor de preferencia:

```sql
CREATE DATABASE nombreDB CHARACTER SET utf8mb4;
CREATE USER nombreusuario@localhost IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON nombreDB.* TO nombreusuario@localhost;
FLUSH PRIVILEGES;
```

### 🗄️ 2.2 Configuración PostgreSQL

Usar CMD o tu gestor de preferencia. Si te conectas por CMD, primero configura el PATH (ver enlaces de referencia):

```sh
psql -U postgres
CREATE DATABASE "nombreDB" ENCODING "UTF8"; # Usa "" en caso el nombre de la BD use mayúsculas
CREATE USER nombreusuario WITH PASSWORD 'password'; # Usa "" en caso el nombre del usuario use mayúsculas
GRANT ALL PRIVILEGES ON DATABASE "nombreDB" TO nombreusuario;
\c "nombreDB";
GRANT ALL PRIVILEGES ON SCHEMA public TO nombre_usuario;
```

### ⚙️ 3. Configuración estándar del proyecto

- Clona o descarga el proyecto y ábrelo con tu editor de código preferido.
- Instala `virtualenv`:
  ```sh
  pip install virtualenv
  ```
- Ubica la raíz del proyecto y crea el entorno virtual:
  ```sh
  virtualenv -p python venv
  ```
- Activa el entorno virtual:
  ```sh
  & .\venv\Scripts\activate
  ```
- Ejecuta el siguiente comando solo si se presenta error:
  ```sh
  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser powershell
  ```
- Instala las dependencias necesarias:
  ```sh
  pip install -r requirements.txt
  ```
- Genera una nueva `SECRET_KEY` ejecutando el código comentado en el archivo `manage.py`
- Crea un archivo `.env` y establece los valores de tus variables de entorno. Configurar estos valores es crítico antes de ejecutar los comandos posteriores. Estos valores serán consumidos en `Config/settings.py`.
- Crear una carpeta `media` en la raíz del proyecto, al mismo nivel de la carpeta `static`
- Ejecuta las migraciones:
  ```sh
  python manage.py makemigrations
  python manage.py makemigrations <nameapp> # Especificar el nombre del app solo si no se crea la carpeta migrations
  python manage.py migrate auth
  python manage.py migrate
  python manage.py migrate --run-syncdb # Usar solo si se presenta error en migrate
  ```
- Crea un superusuario:
  ```sh
  python manage.py createsuperuser
  ```

### 🚀 Ejecutar el proyecto

- Ejecuta el servidor:
  ```sh
  python manage.py runserver 0.0.0.0:8000 # Especificar el puerto solo si quieres usar uno diferente al 8000
  ```

## Enlaces de Referencia

- **[Conectar Django con MySQL](https://www.scaler.com/topics/django/mysql-with-django/)**
- **[Django con MySQL - Guía](https://medium.com/@a01207543/django-conecta-tu-proyecto-con-la-base-de-datos-mysql-2d329c73192a)**
- **[Instalar PostgreSQL](https://www.enterprisedb.com/docs/supported-open-source/postgresql/installing/windows/)**
- **[Guía rápida de GitHub](https://training.github.com/downloads/es_ES/github-git-cheat-sheet/)**
- **[Guía GitHub-linguist](https://github.com/github-linguist/linguist/blob/master/docs/overrides.md)**