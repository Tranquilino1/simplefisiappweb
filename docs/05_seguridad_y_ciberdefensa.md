# 5. Seguridad, Ciberseguridad y Ciberdefensa a Nivel de Aplicación

La confidencialidad, integridad y disponibilidad (Tríada CIA) son los pilares fundamentales del desarrollo de esta plataforma de **DeLasGargolasChat**. A continuación, detallamos las medidas aplicadas en el ciclo de vida del software:

## 5.1 Mecanismos de Seguridad Implementados

1. **Protocolo WSS (WebSockets Seguro) y HTTPS:**
   - La aplicación está preparada para operar sobre TLS/SSL. De este modo, los frames que viajan desde el navegador hacia *Daphne* se cifran, evitando ataques de intercepción (*Man in The Middle*).
2. **Autenticación en WebSockets (AuthMiddlewareStack):**
   - El canal de WebSocket rechaza silenciosamente (o no suscribe) a los usuarios no identificados. En `asgi.py` se ha envuelto el router bajo `AuthMiddlewareStack`, lo que extrae la cookie de sesión y puebla el objeto `scope['user']`, permitiendo validar que un canal pertenece exclusivamente a una sesión fiable.
3. **Prevención de XSS (Cross-Site Scripting):**
   - **En el backend:** El motor de plantillas de Django autoesquiva el contenido por defecto (`autoescape on`).
   - **En WebSockets:** El Frontend (`room.html`) recibe las cargas JSON e inyecta el contenido seguro limitando el parseo de HTML en la función JS que dibuja el texto proveniente del chat.
4. **Protección CSRF (Cross-Site Request Forgery):**
   - Todos los envíos de parámetros tipo `POST` y archivos se envían mediante formularios equipados con `{% csrf_token %}` o mediante el decorador `@csrf_exempt` sólo en puntos de API donde se manejan Web Tokens de forma específica y segura.

## 5.2 Sistema de Backup (Copia de Seguridad)

Para proteger la información (mensajes e historial) frente a corrupciones de disco o ataques (Ransomware), se ha dotado a la aplicación de un script integrado (`python manage.py backup_db`) situado en `chat/management/commands/backup_db.py`.

El comando se encarga de crear un directorio seguro local e insertar una copia sincronizada del archivo sqlite3. En infraestructuras de producción, este comando puede programarse (*cron job*) para sincronizar vía SCP/SFTP con un servidor remoto.
