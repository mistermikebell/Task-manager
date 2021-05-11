from django.contrib.auth.models import User


class UserModel(User):

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
