# prueba_bia
Este repositorio es una prueba tecnica para Bia energy

## Limpieza de datos
Lo primero que se hizo fue limpiar los datos recibidos.
Active energy se limpio para que solo fuera el numero.

Meter date, se cambio el formato en excel para que fuera yyyy-mm-dd hh:mm:ss

Meter id, se cambio el formato para que no tuviera comas.

Se exporta este archivo al csv que se puede ver en este repositorio.

Ese csv se toma como archivo de importacion a la bd.

## Base de datos
La base de datos esta alojada en postgres, los detalles se pueden ver en bia_project/bia_project/settings.py linea 80

```
'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mydb', 
        'USER': 'newuser', 
        'PASSWORD': 'password',
        'HOST': 'localhost', 
        'PORT': '5432',
    }
```
