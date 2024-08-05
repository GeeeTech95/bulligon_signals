from rest_framework import generics
from rest_framework.response import Response

from django.contrib.auth import get_user_model


from .serializers import ProfileSerializer

class UpdateProfile(generics.RetrieveUpdateAPIView) :
    serializer_class = ProfileSerializer
    model = get_user_model()
    
    
    def get_object(self,**kwargs) :
        return self.request.user



 

    

