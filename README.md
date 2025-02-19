# NeuralNetwork

**NeuralNetwork** es una implementación en **Python** de una red neuronal artificial. Este proyecto implementa una red neuronal básica capaz de realizar tareas de clasificación a través de un proceso de entrenamiento supervisado utilizando el algoritmo de retropropagación.

## Características

- **Arquitectura Flexible**: Permite definir una red neuronal con múltiples capas y un número configurable de neuronas por capa.
- **Entrenamiento Supervisado**: Usa retropropagación para ajustar los pesos de la red y minimizar el error de las predicciones.
- **Compatibilidad con Conjuntos de Datos Comunes**: El proyecto está preparado para entrenarse con datos como el conjunto MNIST.

## Requisitos Previos

Para ejecutar este proyecto, necesitas tener instaladas las siguientes bibliotecas:

- **Python 3.x**: Asegúrate de tener Python 3 o superior instalado en tu sistema.
- **NumPy**: Para el manejo de matrices y operaciones matemáticas.
- **Matplotlib** (opcional): Para la visualización de resultados y métricas durante el entrenamiento.

Puedes instalar las dependencias necesarias con `pip`:
   pip install numpy matplotlib

## Estructura del Proyecto
El proyecto está organizado de la siguiente manera:
-  Main.py: Contiene la implementación principal de la red neuronal, incluyendo las funciones de activación, la retropropagación y el entrenamiento.
-  CrearCSV.py: Script para crear los csv necesarios para la obtencion de datos.
-  WebScrapperFilmAffinity.py: Script para obtener los datos de https://www.filmaffinity.com/es/main.html.
-  scrap.csv: Fichero intermedio para la obtencion de datos validos.
-  sentimientos.csv: Fichero final con los datos obtenidos y almacenados de manera adecuada.

## Como ejecutar el Proyecto

1. **Clonar el repositorio**:
   git clone https://github.com/Methazod/NeuralNetwork.git
   cd NeuralNetwork
2. **Ejecutar en la terminal**:
   Main.py

## Contribuciones
Las contribuciones son bienvenidas. Si deseas mejorar este proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama para tu función o corrección:
   git checkout -b nombre-de-tu-rama
3. Realiza tus cambios y haz commits descriptivos.
4. Envía un pull request detallando tus modificaciones.
