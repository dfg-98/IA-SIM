# Red de distribución de recursos. Red electríca

[Ver informe](https://github.com/dfg-98/IA-SIM/blob/c16b44a01b72a24bf2f74a2e68fe6e410998b8f2/informe.md)

## Integrantes

- Jesús Santos Capote [@sheldon05](https://github.com/sheldon05)
- Kenny Villalobos [@KennyVillalobos](https://github.com/KennyVillalobos)
- Darío Fragas [@dfg-98](https://github.com/dfg-98)
  
# Descripción del problema

Se tienen N nodos que representan una red, de estos nodos se tendrán nodos generadores y consumidores. 
Los nodos generadores son los que producen el recurso, la producción del recurso será un proceso estocástico
que se modelará con una distribución de probabilidad -en inicio podría ser ficticia pero se plantea evaluarlo 
considerando las condiciones de un recurso real como electricidad- y permitirá tener en
cuenta factores extras para complejizar el modelo. Estos nodos generadores tendrán además necesidades de mantenimientos
asociadas a un costo variable durante el tiempo de simulación de otro tipo de recurso (al que llamaremos recurso primario o dinero).
Para la producción del recurso se necesita consumir dinero, en dependencia del consumo estará dada la solución.


Los nodos consumidores son los que consumen el recurso,
estos tendrán una demanda que también se comporte de forma estocástica. Además estos nodos producirán el recurso primario. (Esto último sirva en caso de recursos como la electricidad tener nodos 
consumidores de tipo casas y nodos consumidores de tipo industria, donde las casas no producen dinero mientras las industrias sí)

Se establecen varios problemas:
1- Dado un conjunto de nodos y el costo asociado de las conexiones cuál es la manera más eficiente de conectarlos garantizando
el abastecimiento y el correcto funcionamineto de la red así como la minimización de los costos.

2- Dada una conexión desarrollar algoritmos que permitan la predicción del consumo diario 

3- Desarrollar agentes inteligentes que tomen decisiones en momentos de déficet para hacer desconexiones a la red garantizando
la menor cantidad de nodos afectados y maximizando la producción.


# Modelación del problema

Se tiene un grafo de N nodos de distintos tipos, se tiene una matriz de pesos que representa el costo en dinero de la conexión 
entre dos nodos. Se tiene además una cantidad de dinero inicial que se puede usar para construir la red.

## Problema 1

Las soluciones al problema serían grafos dirigidos de la forma $G<V, E>$ donde $V$ es el conjunto de nodos de tamaño $N$ y $E$ es el conjunto de aristas,
donde cada arista $e = <i, j>$ tiene un peso $w_{ij}$ que representa el costo de construir la conexión entre los nodos $i$ y $j$. Ademas $\sum w_{ij} \le M$  siendo $M$ la cantidad de dinero inicial.

Se desea encontrar la mejor de estas soluciones donde "mejor" se refiere a que la red sea estable y que no se presenten problemas de deficet a largo plazo de acuerdo al criterio dado por la simulación.

Se plantea usar algoritmos de metaheurística que generen soluciones y evalúen la mejor de estas mediante un proceso de simulación.

## Problema 2

En cada iteración de una simulación debe predecirse el consumo que se va a tener dado que el tipo de recurso que vamos a estudiar es la electricidad
y está no puede almacenarse en grandes cantidades, por lo que su producción debe estar de acuerdo a la necesidad. Se desea provar varios algoritmos 
que permitan la predicción y evaluar resultados en la simulación como un todo.

## Problema 3

En circunstancias de déficet habrá circuitos que desconectar. Dada unas condiciones de generación y la predicción de la demanda se quiere desarrollar 
un algoritmo que determine qué secciones del circuito desconectar en caso que exista déficet. Aquí se le adicionará una variable a cada nodo 
consumidor que será agotamiento, este aumenta cuando un nodo está desabastecido y disminuye cuando se le abstece. El objetivo es mantener el agotamiento
general lo más bajo posible y que la producción de dinero sea la más alta. 


# Objetivos del proyecto

- Utilizar métodos de Inteligencia Artificial para la resolución de los problemas comprobando su eficiencia mediante 
simulación.
- Estudiar el comportamiento de un recurso real e implementar una solución del problema para dicho recurso (teniendo en cuenta distribución de probabilidad de las variables involucradas en el proceso y características propias del recurso)


# Ejecutar

Para ejecutar el proyecto se debe tener instalado python 3.8 o superior y las librerías de python que se encuentran en el archivo requirements.txt

Para instalar las librerías se debe ejecutar el siguiente comando en la carpeta del proyecto:

`pip install -r requirements.txt`

Para ejecutar el proyecto se debe ejecutar el siguiente comando en la carpeta del proyecto:

`python main.py data.json`

Donde data.json es un fichero en json con la siguiente estructura:
```json
{
    "nodes": [
        {
            "id": 0,
            "type": "Producer",
            "max_production": 500,
            "production_rate": 1.0,
            "production_bias": 10.0,
            "resources": 0.0,
            "max_resources": 100.0
        },
        {
            "id": 1,
            "type": "Consumer",
            "min_consumption": 10,
            "max_consumption": 20
        },
        ...
    ],
    "weights": [
        { "node1": 0, "node2": 0, "weight": "inf" },
        { "node1": 0, "node2": 1, "weight": 1.0 },
        ...
    ]
}
```

Además se aceptan varios parametros para configurar la simulación y la ejecución general del programa