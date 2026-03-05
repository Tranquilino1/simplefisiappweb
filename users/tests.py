import pytest
from django.contrib.auth.models import User
from users.models import Profile
from django.urls import reverse

@pytest.mark.django_db
class TestUsersModelAndViews:

    def setup_method(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_profile_creation(self):
        # Profil is automatically created via the register view in real usage, 
        # but here we manually assert relations
        profile = Profile.objects.create(user=self.user, display_name="Test Display")
        assert profile.user.username == 'testuser'
        assert profile.display_name == 'Test Display'

    def test_login_view(self, client):
        response = client.get(reverse('users:login'))
        assert response.status_code == 200
        
    def test_authenticated_profile_view(self, client):
        client.login(username='testuser', password='password123')
        # Simulate the profile created in register view behavior so it won't crash
        Profile.objects.get_or_create(user=self.user)
        response = client.get(reverse('users:profile'))
        assert response.status_code == 200

    def test_unauthenticated_profile_view_redirects(self, client):
        response = client.get(reverse('users:profile'))
        assert response.status_code == 302 # Redirect to login
