# Flying Plane 3D

Flying Plane 3D es un proyecto creado para el curso CC3501 - Modelación y Computación Gráfica para Ingenieros, del Departamento de Ciencias de la Computación de la Universidad de Chile.

El objetivo de este proyecto es crear un clon en 3D del conocido videojuego [Flappy Bird](https://flappybird.io/), aplicando generación de formas en 3D, texturas, técnicas de iluminación y utilizando el patrón de diseño Modelo-Vista-Controlador para la arquitectura de la aplicación.

## Instalación y uso

Para jugar a Flying Plane 3D se requiere Python 3.8 o superior y las librerías pyopengl, numpy, glfw y pillow. Si ya cumple estos requisitos:

- Descargue o clone este repositorio localmente.
- Ingrese a la carpeta descargada a través de la terminal.
- Dentro de la carpeta, ejecute el siguiente comando:

  ``` 
  python flying_plane_3D.py N L
  ```
  donde el parámetro `N` lo debe reemplazar por la cantidad de puntos con los que se ganará el juego y `L` por la duración en segundos de un ciclo día/noche en el juego. Se ejecuta con dichos parámetros para testear la iluminación y para que el juego no sea infinito.
- Una vez cargue la ventana del juego, por defecto la cámara estará en tercera persona. Con las teclas `2` y `3` puede cambiar a una cámara lateral y en primera persona, respectivamente. Con la tecla `1` puede volver a la cámara por defecto.
- Al presionar la tecla `W` comenzará el juego y deberá seguir presionando dicha tecla para lograr evitar los obstáculos. Puede mover hacia dónde apunta la cámara con el mouse, siempre y cuando ésta se encuentre en tercera persona.