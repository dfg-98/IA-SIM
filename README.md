# Resource Distribution Network


## Integrantes

- Jesús Santos Capote [@sheldon05](https://github.com/sheldon05)
- Kenny Villalobos [@KennyVillalobos](https://github.com/KennyVillalobos)
- Darío Fragas [@dfg-98](https://github.com/dfg-98)
  
# Descripción del problema


Se tienen N nodos que representan una red, de estos nodos se tendrán nodos generadores y nodos consumidores. 
Los nodos generadores son los que producen el recurso, la producción del recurso será un proceso estocástico
que se modelará con una distribución de probabilidad -en inicio podría ser ficticia pero se plantea evaluarlo 
considerando las condiciones de un recurso real como electricidad, agua o combustible - y permitirá tener en
cuenta factores extras para complejizar el modelo. Estos nodos generadores tendrán además necesidades de mantenimientos
asociadas a un costo variable durante el tiempo de simulación de otro tipo de recurso (como podría ser dinero).


Los nodos consumidores son los que consumen el recurso,
estos tendrán una demanda que también se comporte de forma estocástica. Además estos nodos producirán el recurso que se usa para
el mantenimiento de los nodos generadores en menor o mayor medida. (Esto último sirva en caso de recursos como la electricidad tener nodos 
consumidores de tipo casas y nodos consumidores de tipo industria, donde las casas no producen dinero mientras las industrias sí)

El problema consiste en tener una red donde todos los nodos consumidores queden abastecidos y mediante una simulación
se compruebe que el sistema es estable y que no se presentan problemas de deficet a largo plazo. La conexión entre los nodos
consume recursos de dinero por lo que entre los objetivos está minimizar el costo de construcción de la red. 

# Modelación del problema

Se tiene un grafo de N nodos de distintos tipos, se tiene una matriz de pesos que representa el costo en dinero de la conexión 
entre dos nodos. Se tiene además una cantidad de dinero inicial que se puede usar para construir la red.

Las soluciones al problema serían grafos dirigidos de la forma $G<V, E>$ donde $V$ es el conjunto de nodos de tamaño $N$ y $E$ es el conjunto de aristas,
donde cada arista $e = <i, j>$ tiene un peso $w_{ij}$ que representa el costo de construir la conexión entre los nodos $i$ y $j$. Ademas $\sum w_{ij} \le M$  siendo $M$ la cantidad de dinero inicial.

Se desea encontrar la mejor de estas soluciones donde "mejor" se refiere a que la red sea estable y que no se presenten problemas de deficet a largo plazo de acuerdo al criterio dado por la simulación.

# Objetivos del proyecto

- Utilizar métodos de Inteligencia Artificial para la construcción de dicha red comprobando su eficiencia mediante 
simulación.
- Estudiar el comportamiento de un recurso real e implementar una solución del problema para dicho recurso (teniendo en cuenta distribución de probabilidad de las variables involucradas en el proceso y características propias del recurso)

