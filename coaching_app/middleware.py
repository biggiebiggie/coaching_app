from django.conf import settings
from django.contrib.auth.models import User


class UserTypeMiddleware:
    def __init__(self, get_response):
      self.get_response = get_response
      # One-time configuration and initialization.

    def __call__(self, request):
      # Before

      if request.user.id == None:
            user_type = 'Not logged in'
      else:
            user_type = 'logged in'

      response = self.get_response(request)

      # After

      response['User-type'] = user_type
      print('Middleware says' , user_type)

      return response