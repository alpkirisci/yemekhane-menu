from django.contrib.auth.backends import ModelBackend
from .models import User


class CustomBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, tshirt_color=None, **kwargs):

        print(username,password,tshirt_color)

        try:
            user = User.objects.get(username=username)
            if tshirt_color != user.tshirt_color:
                return None

            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            return None
        # print("AAAAAAAAAAAA",user.tshirt_color)







    def get_user(self, user_id):
        try:
            # Attempt to retrieve the user by their primary key (user_id)
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            # If the user does not exist, return None
            return None
