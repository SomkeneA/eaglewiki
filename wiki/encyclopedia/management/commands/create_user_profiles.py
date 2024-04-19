from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from encyclopedia.models import UserProfile

class Command(BaseCommand):
    help = 'Creates UserProfile objects for existing users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            if not hasattr(user, 'userprofile'):
                UserProfile.objects.create(user=user)
        self.stdout.write(self.style.SUCCESS('User profiles created successfully.'))
