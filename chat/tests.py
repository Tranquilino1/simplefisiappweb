import pytest
from django.contrib.auth.models import User
from chat.models import Room, Message
from django.urls import reverse

@pytest.mark.django_db
class TestChatModelAndViews:

    def setup_method(self):
        self.user = User.objects.create_user(username='chatuser', password='password123')
        self.room = Room.objects.create(name='TestRoom')
        self.message = Message.objects.create(room=self.room, sender=self.user, content='Hello World')

    def test_room_model(self):
        assert self.room.name == 'TestRoom'
        assert self.room.is_group == False

    def test_message_model(self):
        assert self.message.content == 'Hello World'
        assert self.message.sender.username == 'chatuser'
        assert self.message.room.name == 'TestRoom'

    def test_chat_index_view_authenticated(self, client):
        client.login(username='chatuser', password='password123')
        response = client.get(reverse('chat:index'))
        assert response.status_code == 200
        assert 'TestRoom' in response.content.decode()

    def test_chat_room_view_authenticated(self, client):
        client.login(username='chatuser', password='password123')
        response = client.get(reverse('chat:room', args=['TestRoom']))
        assert response.status_code == 200
        assert 'TestRoom' in response.content.decode()
        assert 'Hello World' in response.content.decode()
