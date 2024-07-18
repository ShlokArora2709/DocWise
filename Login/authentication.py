from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import Doctor

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
            if user.check_password(password):
                # Check if the user is a doctor and approved
                if user.is_doctor:
                    doctor = Doctor.objects.get(username=user.username)
                    if not doctor.is_approved:
                        return None  # Doctor not approved
                return user
        except UserModel.DoesNotExist:
            return None
        except Doctor.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None