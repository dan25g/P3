# Practica 3 Equipo 1

Servicio web simple usado para la practica 3 de la materia Computación en la nube

# Instrucciones para Arrancar y Ejecutar el Proyecto

Este documento proporciona una guía paso a paso para arrancar y ejecutar la práctica 3

# Requisitos Previos

## Se deben tener instalados los siguientes programas:

1. Docker - se puede descargar e instalar desde aquí: https://www.docker.com/get-started/

2.  Docker compose - Normalmente viene incluído con la instalación de Docker 

Se debe clonar el repositorio directamente desde la rama main

# Construir y Ejecutar el Proyecto con Docker Compose

## Paso 1: Construir las Imágenes de Docker

Abrir un terminal y construir las imágenes de Docker especificadas en el archivo docker-compose.yml utilizando el siguiente comando:

docker compose build

## Paso 2: Iniciar los Servicios

Iniciar los servicios definidos en el archivo docker-compose.yml con el comando:

docker compose up

Este comando levantará los contenedores de la aplicación web y la base de datos. La aplicación web estará disponible en http://localhost:4000.

# Probar la Aplicación

Una vez que los contenedores estén en funcionamiento, se puede probar la aplicación utilizando un navegador web 

http://localhost:4000

La base de datos estará disponible en puerto http://localhost:5433

# Integrantes 

## Ascanio Paola

## García Daniel

