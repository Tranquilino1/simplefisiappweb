# 6. Anexos y Fuentes Bibliográficas

## 6.1 Funcionamiento de la Aplicación y Chat Grupal
El proyecto **DeLasGargolasChat** es un sistema híbrido que funciona tanto con tecnología síncrona (Django MVT) para las páginas estáticas (Registro, Perfil) como asíncrona (Django Channels + WebSockets) para las comunicaciones en Vivo. 

- **Chat Grupal:** Se resuelve a través del modelo de grupos (`room_group_name`) de Channels. Cuando un usuario envía un mensaje a la URI `/chat/GargolasTeam/`, el *Broker* (En memoria o Redis) distribuye el *payload* simultáneamente a todas las tuberías de red (*Channels*) suscritas a la clave `chat_GargolasTeam`. Así es como múltiples usuarios escuchan el mismo buzón en formato multipunto.
- **Archivos, Audios, WebRTC:** El sistema está preparado para señalización. La subida de un archivo utiliza HTTP para almacenar el *blob* en disco, y propaga el enlace generado (*download URL*) vía WebSocket a los participantes para reducir el overhead en el canal WS en tiempo real.

---

## 6.2 Instrucciones de Git y Subida a GitHub

Se asume que la cuenta de GitHub está creada y el repositorio remoto preparado. Los pasos a ejecutar en consola son los siguientes:

```bash
# 1. Inicializar el repositorio en la carpeta base
git init

# 2. Agregar todos los archivos al índice (Ignorando venv con .gitignore)
git add .

# 3. Guardar los cambios documentando la acción
git commit -m "First commit: DeLasGargolasChat - Django Channels Websockets & Auth"

# 4. Enlazar la carpeta local con el servidor de GitHub
git remote add origin https://github.com/tu-usuario/DeLasGargolasChat.git

# 5. Enviar el código fuente a la rama principal (main)
git branch -M main
git push -u origin main
```

---

## 6.3 Fuentes Bibliográficas y Tecnológicas
- **Python Software Foundation.** *Python 3.10+ Documentation.* URL: https://docs.python.org/
- **Django Software Foundation.** *Django 6.x Documentation.* URL: https://docs.djangoproject.com/
- **Django Channels.** *Asynchronous Server Gateway Interface (ASGI) Guide.* URL: https://channels.readthedocs.io/
- **Mozilla Developer Network (MDN).** *The WebSocket API (WebSockets).* URL: https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API
