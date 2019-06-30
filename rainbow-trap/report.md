1) Descrever a arquitetura de software
2) Refatorar com Design Patterns
    a) Descrever a motivação,
    b) Descrever a implementação: Ilustrar com um diagrama de classes e código,
    c) Explicar as consequências.
3) Documentar em um blog aberto ao público em geral, em inglês.
4) Cada membro da equipe deverá descrever pelo menos duas (2) aplicações de Design Patterns Distintos.

# Refactoring Rainbow-Trap with Design Patterns

- ESCREVER UMA INTRO AQUI

## Software Architecture

The software architecture chosen to this project was the Evend Driven Architechture (EDA), because this way it is possible to take advantage of PyGame already implemented events. This way, the game consists in an infinite loop in which, during each iteration, the game check if an event has happen and in this case executes the corresponding piece of code.

PyGame events are loaded with PyGame libraries during the imports as seen below:

``` python
import pygame
from pygame.locals import *
```

In the main loop, we check every event that happened in the current loop iteration and process them one by one. This can be done with a `for` loop.

``` python
for event in pygame.event.get():
    if if event.type == EVENT1:
        # code for event 1 here
     if if event.type == EVENT2:
        # code for event 2 here
     if if event.type == EVENT3:
        # code for event 3 here
    ...
```

In our application we will be monitoring the following PyGame events:

```
QUIT                : User tried to close the application
KEYDOWN             : User pressed some keyboard key
KEYUP               : User released keyboard key
JOYBUTTONDOWN       : User pressed xbox controller button
JOYHATMOTION        : User pressed xbox joypad direction
```

In addition to PyGame's already implemented events, we can define our own custom events in order to simplify code implementation. Nice events in our application would be:

```
COLOR_CHANGE        : Player color changed
COLLISION           : Player collided with a wall
DIFFICULT_ENHANCE   : Difficult has increased
```


## Design Patterns

- DESCREVER DOIS DESIGN PATTERNS AQUI
- UTILIZAR ESSES DESIGN PATTERNS NA REFATORAÇÃO DO CÓDIGO

## Refactoring the code
