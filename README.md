# Compilador OVEJOTA
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

# Avance 6

En este sexto avance: se ceo la maquina virtual con la ejecución de expresiones aritméticas, estatutos secuenciales y llamadas a funciones. 

- Se creó el archivo object.p con los cuádruplos, directorio de funciones y tabla de constantes. 
- Se creó el archivo VirtualMachine.py en donde se recorren los cuádruplos, respetando sus saltos adecuados.
- En el mismo archivo se crearon varios objetos Memory los cuales van guardando los valores de las variables y los resultados de los cuádruplos para implementar el Data segment, Stack segment y Extra segment. 
- Se recorren todos los cuádruplos en un ciclo utilizando un instruction pointer y con varios casos condicionales dependiendo del cuádruplo. 

# Avance 7

En este séptimo avance: se realizó el manejo de arreglos, tanto su creación como su indexación. 
- Se agregaron los puntos neurales para la creación e indexación de arreglos, tanto vectores como matrices. 
- Se agregaron los cuádruplos de tipo verify y se revisa en Virtual Machine la verificación de que se esté dentro de los límites. 
- Se agregaron espacios en memoria para poder manejar los datos de tipo pointer.
- Se creó una función para revisar si la dirección es de tipo pointer y regresar ya sea la dirección o el valor al que apunta está variable. 
- Se probó exitosamente la multiplicación de matrices. 