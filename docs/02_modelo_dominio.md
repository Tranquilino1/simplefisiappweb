# 2. Análisis del Problema: Modelo de Dominio

El modelo de dominio define la estructura conceptual de la aplicación DeLasGargolasChat y las relaciones entre entidades.

## Entidades Principales:
1. **User (Usuario):** Participante que usa el sistema.
2. **Profile (Perfil):** Configuración visual e información adicional del usuario (foto).
3. **Room / Chat (Sala):** Representa un hilo de conversación. Puede ser `Directo` (entre dos usuarios) o `Grupal` (entre varios).
4. **Message (Mensaje):** La unidad básica de comunicación. Puede ser de texto, archivo adjunto o mensaje de voz.
5. **Attachment (Adjunto):** Entidad que representa el archivo físico subido en un mensaje.

---

## Diagrama de Clases Conceptuales (Modelo de Dominio)

```mermaid
classDiagram
    class User {
        +String username
        +String email
        +String password
        +register()
        +login()
        +logout()
    }
    
    class Profile {
        +String displayName
        +Image profilePicture
        +String status
        +updateProfile()
    }
    
    class Room {
        +String name
        +Boolean isGroup
        +Date createdAt
        +addParticipant()
        +removeParticipant()
    }
    
    class Message {
        +String content
        +Date timestamp
        +Boolean isRead
        +MessageType type
        +send()
        +delete()
    }
    
    class Attachment {
        +String fileUrl
        +String fileType
        +Float fileSize
        +upload()
        +download()
    }
    
    User "1" -- "1" Profile : has
    User "1..*" -- "0..*" Room : participates in
    Room "1" *-- "0..*" Message : contains
    User "1" -- "0..*" Message : sends
    Message "1" *-- "0..1" Attachment : has
```
