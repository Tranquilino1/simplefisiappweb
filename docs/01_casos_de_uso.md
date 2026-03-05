# 1. Especificación de Requisitos y Casos de Uso

## Descripción Narrativa del Caso de Uso General

El sistema **DeLasGargolasChat** es una plataforma de comunicación en tiempo real. 
Los participantes en este sistema son los usuarios registrados (Actores).
El usuario puede:
- **Registrarse e iniciar sesión** en el sistema para acceder a sus funciones y proteger su privacidad.
- **Personalizar su perfil**, incluyendo cambiar su foto de perfil y el nombre a mostrar.
- **Iniciar una conversación (Chat Directo)** con otro usuario registrado para mantener comunicación cara a cara (texto o WebRTC).
- **Crear y participar en un Chat Grupal** para colaboración en equipo.
- **Enviar mensajes de texto** de forma instantánea.
- **Compartir archivos** (documentos, imágenes) dentro de la conversación.
- **Grabar y enviar mensajes de voz / audio** dentro del chat.
- **Consultar el historial de chat**, el sistema debe registrar y resguardar todas las conversaciones.
- **Realizar una videollamada / llamada de voz** (Comunicación cara a cara).

---

## Diagrama completo de Casos de Uso

```mermaid
usecaseDiagram
    actor Usuario

    package "DeLasGargolasChat" {
        usecase "Registrarse e Iniciar Sesión" as UC1
        usecase "Personalizar Perfil (Foto/Ajustes)" as UC2
        usecase "Iniciar Chat Directo" as UC3
        usecase "Participar en Chat Grupal" as UC4
        usecase "Enviar Mensaje de Texto" as UC5
        usecase "Compartir Archivos" as UC6
        usecase "Grabar/Enviar Nota de Voz" as UC7
        usecase "Consultar Historial de Chat" as UC8
        usecase "Realizar Llamada/Videollamada" as UC9
    }

    Usuario --> UC1
    Usuario --> UC2
    Usuario --> UC3
    Usuario --> UC4
    Usuario --> UC5
    Usuario --> UC6
    Usuario --> UC7
    Usuario --> UC8
    Usuario --> UC9
    
    UC5 ..> UC3 : extends
    UC5 ..> UC4 : extends
    UC6 ..> UC3 : extends
    UC6 ..> UC4 : extends
    UC7 ..> UC3 : extends
    UC7 ..> UC4 : extends
    UC9 ..> UC3 : extends
    UC9 ..> UC4 : extends
```
