- Crear Entorno Virtual:

	python -m venv 'nombre_entorno_virtual'

- Activar Entorno Virtual:

	'nombre_entorno_virtual'\Scripts\activate

- Desactivar Entorno Virtual:

	'nombre_entorno_virtual'\Scripts\deactivate

- Instalar librerías en el entorno virtual:

	pip install Django
	python -m pip install --upgrade pip
	pip install djangorestframework
	pip install psycopg2-binary
	pip install djangorestframework_simplejwt
	pip install django-coreapi
	pip install django-cors-headers

- Correr servidor:
	
	python manage.py runserver
	
- Hacer migración:
	
	python manage.py makemigrations
	python manage.py migrate

- Crear super usuario

	python manage.py createsuperuser

- Ejecutar pruebas:

	py manage.py test apps.'nombre_app'.tests.'nombre_test_class'

