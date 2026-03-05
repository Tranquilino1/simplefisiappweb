from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Room, Message, Attachment

@login_required
def index(request):
    rooms = Room.objects.all()
    return render(request, 'chat/index.html', {'rooms': rooms})

@login_required
def room(request, room_name):
    # Retrieve or create a room based on the name passed in the URL
    room_obj, created = Room.objects.get_or_create(name=room_name)
    
    # Get last 50 messages
    messages = room_obj.messages.all().order_by('-timestamp')[:50]
    messages = reversed(messages) # Show oldest to newest

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'messages': messages,
    })

@login_required
def upload_attachment(request, room_name):
    if request.method == 'POST' and request.FILES.get('file'):
        file_obj = request.FILES['file']
        msg_type = request.POST.get('msg_type', 'file')

        room_obj = Room.objects.get(name=room_name)
        
        # Guardar en BD
        message = Message.objects.create(
            room=room_obj,
            sender=request.user,
            content=file_obj.name,
            msg_type=msg_type
        )
        Attachment.objects.create(
            message=message,
            file=file_obj,
            file_type=file_obj.content_type
        )

        # Obtener avatar del sender
        avatar_url = '/static/css/default_avatar.svg'
        if hasattr(request.user, 'profile') and request.user.profile.profile_picture:
            avatar_url = request.user.profile.profile_picture.url

        # Configurar mensaje para el front end según tipo
        if file_obj.content_type.startswith('image/'):
            html_msg = f'<img src="{message.attachment.file.url}" style="max-width:200px; border-radius:8px;">'
        elif msg_type == 'voice' or file_obj.content_type.startswith('audio/'):
            html_msg = f'<audio controls src="{message.attachment.file.url}" style="max-height:40px;"></audio>'
        else:
            html_msg = f'<a href="{message.attachment.file.url}" target="_blank" style="color:white;text-decoration:underline;">📎 {file_obj.name}</a>'

        message.content = html_msg
        message.save()

        # Broadcast via websocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{room_name}',
            {
                'type': 'chat_message',
                'message': html_msg,
                'username': request.user.username,
                'avatar_url': avatar_url,
                'msg_type': msg_type
            }
        )

        return JsonResponse({'status': 'ok', 'url': message.attachment.file.url})
    return JsonResponse({'status': 'error'}, status=400)
