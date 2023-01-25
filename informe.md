# Red de distribución de recursos. Red eléctrica


## Integrantes

- Jesús Santos Capote [@sheldon05](https://github.com/sheldon05)
- Kenny Villalobos [@KennyVillalobos](https://github.com/KennyVillalobos)
- Darío Fragas [@dfg-98](https://github.com/dfg-98)


## Introducción:

La construcción y mantenimiento de sistemas electroenergéticos constituye una problemática a optimizar en la actualidad.
¿Cómo diseñar una red eléctrica de forma que el desabastecimiento sea mínimo? ¿Cómo se puede optimizar el uso de los recursos? 
A estas dos interrogantes se pretende dar respuesta con este proyecto.

## Modelación:

La modelación de la red eléctrica se ha hecho mediante nodos que pueden ser del tipo `Consumidores`, `Generadores` o `Productores`.

Los nodos `Consumidores` son los que consumen energía de la red. Se definen dos tipos de nodos consumidores:

- `MinMaxConsumerNode`: su consumo está dado por una variable aleatoria uniforme entre un valor mínimo y un máximo.
- `TurnBasedConsumer`: consume por turnos, es decir tiene asociado un tiempo de consumo y un tiempo de espera. Durante el tiempo de consumo su consumo está dado por una variable aleatoria uniforme en una vecindad de un valor medio, durante el tiempo de espera no consume.

Los nodos `Consumidores` también generan recursos en forma proporcional a la energía consumida a modo de cobro de electricidad.

Los nodos `Generadores` son los que generan energía para la red. Tienen asociado una capacidad de generación máximo, una cantidad de recursos máxima, un costo de producción de energía y la cantidad de recursos actuales en el node para producir. Además tiene asociada una variable de salud que indica
una probabilidad de que no se genere electricidad en un momento dado. La salud se ve afectada por la cantidad de energía generado en un factor determinado como `generation_damage_rate`.

Los nodos `Productores` son los que producen energía para la red. Tienen asociado una capacidad de producción máxima y un costo de energía para producir. Al igual que los generadores, presentan salud que indica la probabilidad de que se produzca o no y se ve afectada por la cantidad de recursos producidos en un factor determinado como `production_damage_rate`.
Los nodos `Productores` son a su vez `Consumidores` cuyo consumo está dado por la energía necesaria para producir sus recursos.

La red eléctrica está representada como un grafo cuyos vértices son estos nodos y las aristas representan las conexiones entre los nodos. Las aristas tienen asociado un costo de conexión y una salud que indica la probabilidad de que la conexión falle en un momento dado (no pase corriente por ahí). La salud se ve afectada por la cantidad de energía que pasa por la conexión en un factor determinado como `edge_damage_rate`.

Todos los elementos con salud pueden ser reparados usando recursos y tienen costos variables de reparación.

## Simulación:

Dada una red eléctrica la simulación de su comportamiento es la siguiente:

- Un agente se encarga de asignar recursos a los nodos generadores para la producción de energía.
- Cada nodo consumidor establece su consumo en el turnos
- Un agente determina que nodos y aristas reparar y qué recursos usar para ello.
- Un agente determina para cada nodo `Generador` la cantidad de energía que debería generar (la generación real puede verse afectado por las condiciones propias del generador como recursos disponibles, salud, etc).
- Se genera energía y se distribuye por la red alimentando cada nodo consumidor.
- Se recolectan los recursos generados.
- Se le asigna a una evaluación a la red basado en el abastecimiento y la salud de sus elementos.


## Inteligencia Artificial:

Para la construcción de la red se usa un algoritmo genético cuyas soluciones son redes eléctricas y su función de fitness está dada mediante 
la simulación del comportamiento de la red y la evaluación de la misma.


Durante la simulación se tienen varios agentes inteligentes que se encargan de diferentes tareas:

- `ResourceAssigner`: se encarga de asignar recursos a los nodos generadores para la producción de energía.
- `GenarationEstimator`: se encarga de determinar para cada nodo `Generador` la cantidad de energía que debería generar.
- `ReparationAgent`: se encarga de determinar que nodos y aristas reparar y qué recursos usar para ello.

## Resultados:

## Conclusiones:

Aunque la modelación del problema es bastante simple permite dar una idea de cómo se puede modelar un problema más complejo y cómo se puede usar la inteligencia artificial para resolverlo.
Con este proyecto se ha podido ver que la inteligencia artificial puede ser usada para resolver problemas de optimización y que es posible construir redes eléctricas que funcionen de forma eficiente.
