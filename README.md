# Compilador
Proyecto final para la clase de compiladores

# Avance #1

En este primer avance se construyo el analizador léxico y el sintáctico. Se hicieron decisiones sobre que tokens dejar y cuales eliminar, entre lo mas destacado fue que incluimos tokens como var y function que nos ayudaron a reducir una gran cantidad de errores en la declaración de variables y funciones.

Otra decisión que se tomo, fue solo permitir vectores en lugar de matrices como previamente habíamos definido.

Hasta ahorita el programa funciona para un archivo de prueba que incluye declaración de clases, declaración de variables globales y declaración de funciones.

En los siguientes días la idea es seguir haciendo iteraciones sobre nuestro compilador, para poder eliminar la mayor cantidad de bugs antes de la siguiente entrega.

# Avance #2 

En este segundo avance se creo el directorio de funciones como variable global. 

Tambien se insertaron puntos dentro de las reglas para poder implementar el funcionamiento correcto. 

Se guardan las funciones, en el directorio, asi como las variables en una tabla de variables la cual esta dentro de la funcion correspondiente. 


# Avance #3

Mayo 1 - Se agrego el cubo Semantico


# Avance #4

# Avance #5

En este quinto avance se realizaron los puntos para la generación de código de funciones en nuestro lenguaje. 

Se crearon los puntos necesarios para:

-	Verificar donde empieza y donde terminan las funciones.
-	Contar la cantidad de parámetros de una función y almacenar los tipos y cantidad de parámetros en el directorio de funciones. 
-	Se creo caso especial para cuando la función no es de tipo void
-	Los puntos necesarios para la llamada de funciones tanto void como de algún otro tipo.
-	Checar la existencia de una función cuando es llamada.

