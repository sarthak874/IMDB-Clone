from rest_framework.decorators import api_view
from rest_framework.response import Response
from user_app.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from user_app import models

@api_view(['POST',])
def logout_view(request):
    if request.method=='POST':
        request.user.auth_token.delete()
        return Response("logout successful",status=status.HTTP_200_OK)

@api_view(['POST',])                                #for registeration
def registration_view(request):
    if request.method == 'POST':
        serializer=RegistrationSerializer(data=request.data)

        data={}

        if serializer.is_valid():
            account=serializer.save()

            data['username']=account.username
            data['email']=account.email

            token= Token.objects.get(user=account).key
            data['token']= token

        else:
            return serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)
