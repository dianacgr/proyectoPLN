================================================
INSTRUCCIONES DE INSTALACION PROYECTO DJANGO
================================================

Dependencias
===============

- Django 1.10.4
- django-bootstrap3

Plantilla utilizada
===================
https://startbootstrap.com/template-overviews/sb-admin-2/

Instrucciones:
===============

Instalar Django 1.10.4 sobre Python 2.7, preferiblemente sobre pip

Instalar las dependencias, en este caso::

    pip install django-bootstrap3
    
Ingresar a la carpeta del proyecto y correr el comando::

    python manage.py migrate
    
Correr el servidor de pruebas::
    
    python manage.py runserver
    
Ingresar en el navegador a http://localhost:8000
