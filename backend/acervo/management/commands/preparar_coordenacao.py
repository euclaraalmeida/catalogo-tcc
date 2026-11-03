from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = 'Cria as duas contas demonstrativas da coordenação e exibe seus tokens.'

    def handle(self, *args, **options):
        User = get_user_model()
        senha = 'RadTcc2026!'
        for username in ('coordenacao1', 'coordenacao2'):
            user, _ = User.objects.get_or_create(username=username)
            user.set_password(senha)
            user.is_active = True
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
            self.stdout.write(f'Usuário: {username} | Senha: {senha} | Token: {token.key}')
