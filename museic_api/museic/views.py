from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Song, Album, Artist, CustomUser
from .serializers import SongSerializer, AlbumSerializer, ArtistSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed



class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]  # Herkes kayıt olabilir

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = CustomUser.objects.create_user(
                    email=serializer.validated_data['email'],
                    password=serializer.validated_data['password'],  # Şifre otomatik hashlenecek
                    gender=serializer.validated_data.get('gender'),
                    username=serializer.validated_data.get('username')
                )
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Artist API Views
class ArtistListCreate(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [AllowAny]  


class ArtistDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [AllowAny]  

# Album API Views
class AlbumListCreate(generics.ListCreateAPIView):
    queryset = Album.objects.select_related('artist')
    serializer_class = AlbumSerializer
    permission_classes = [AllowAny]  


class AlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.select_related('artist')
    serializer_class = AlbumSerializer
    permission_classes = [AllowAny]  

# Song API Views
class SongListCreate(generics.ListCreateAPIView):
    queryset = Song.objects.select_related('artist', 'album')
    serializer_class = SongSerializer
    permission_classes = [AllowAny]  


class SongDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.select_related('artist', 'album')
    serializer_class = SongSerializer
    permission_classes = [AllowAny]  



class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            raise AuthenticationFailed('Invalid credentials.')

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
