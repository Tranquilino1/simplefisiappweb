# 3. Diagramas de Secuencia del Sistema DeLasGargolasChat

Este diagrama de secuencia ilustra de forma general la interacción del Emisor (Cliente A), el Sistema Base (Django Server & WebSocket) y el Receptor (Cliente B) durante el envío de un mensaje de texto.

## Secuencia: Enviar Mensaje (Chat en Tiempo Real)

```mermaid
sequenceDiagram
    actor Cliente A
    participant Frontend
    participant WS Route (Django Channels)
    participant Consumer
    participant Base de Datos
    actor Cliente B

    Cliente A ->> Frontend: Escribe un mensaje y pulsa Enviar
    Frontend ->> WS Route (Django Channels): Envía JSON (tipo, contenido, sala) vía WebSocket
    WS Route (Django Channels) ->> Consumer: Enruta al Asynchronous Consumer
    Consumer ->> Base de Datos: Guarda el mensaje en History
    Base de Datos -->> Consumer: OK (Mensaje persistido)
    Consumer ->> Consumer: Broadcast (difunde al Channel Group de la sala)
    Consumer -->> Frontend: Confirma envío a Cliente A
    Consumer -->> WS Route (Django Channels): Envía JSON a los integrantes de la sala
    WS Route (Django Channels) -->> Cliente B: Recibe JSON (Nuevo Mensaje) por su WebSocket
    Cliente B ->> Cliente B: Actualiza la interfaz del Chat (DOM)
```
