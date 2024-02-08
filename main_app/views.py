from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
# include the following imports for auth
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
# again because user is built in model add it like so 
from django.contrib.auth.models import User
from .models import Duck, Feeding, Feather
from .serializers import DuckSerializer, FeedingSerializer, FeatherSerializer, UserSerializer

# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the duck-collector api home route!'}
    return Response(content)

class DuckList(generics.ListCreateAPIView):
  serializer_class = DuckSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    user = self.request.user
    return Duck.objects.filter(user=user)

  def perform_creat(self, serializer):
    serializer.save(user=self.request.user)

class DuckDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = DuckSerializer
  # this here will be looking for something that just says id just a number
  lookup_field = 'id'

  def get_queryset(self):
    user = self.request.user
    return Duck.objects.filter(user=user)

  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)

    # id__in is one such field lookup that checks if the model's id is in a list and that list is being created with this code: the underscore in __ needs to be double
    feathers_not_associated = Feather.objects.exclude(id__in=instance.feathers.all())
    feathers_serializer = FeatherSerializer(feathers_not_associated, many=True)

    return Response({
      'duck': serializer.data,
      'feathers_not_associated': feathers_serializer.data
    })
  
  def perform_updat(self, serializer):
    duck = self.get_object()
    if duck.user != self.request.user:
      raise PermissionDenied({"message": "You do not have permission to edit this cat."})
    serializer.save()
  
  def perform_destroy(self, instance):
    if instance.user != self.request.user:
      raise PermissionDenied({"message": "You do not have permission to delete this cat."})
    instance.delete()



class FeedingListCreate(generics.ListCreateAPIView):
  serializer_class = FeedingSerializer

  def get_queryset(self):
    duck_id = self.kwargs['duck_id']
    return Feeding.objects.filter(duck_id=duck_id)
  
  def perform_create(self, serializer):
    duck_id = self.kwargs['duck_id']
    duck = Duck.objects.get(id= duck_id)
    serializer.save(duck=duck)

class FeedingDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = FeedingSerializer
  lookup_field = 'id'

  def get_queryset(self):
    duck_id = self.kwargs['duck_id']
    return Feeding.objects.filter(duck_id = duck_id)
  
class FeatherList(generics.ListCreateAPIView):
  queryset = Feather.objects.all()
  serializer_class = FeatherSerializer

class FeatherDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Feather.objects.all()
  serializer_class = FeatherSerializer
  lookup_field = 'id'

class AddFeatherToDuck(APIView):
  def post(self, request, duck_id, feather_id):
    duck = Duck.objects.get(id=duck_id)
    feather = Feather.objects.get(id=feather_id)
    duck.feathers.add(feather)
    return Response({'message': f'Feather {feather.type} added to Duck {duck.name}'})
  
class RemoveFeatherFromDuck(APIView):
  def post(self, request, duck_id, feather_id):
    duck = Duck.objects.get(id=duck_id)
    feather = Feather.objects.get(id=feather_id)
    duck.feathers.remove(feather)
    return Response({'message': f'Feather {feather.type} removed from Duck {duck.name}'})
  
class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response ({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })
  
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user: 
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
  
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)
    refresh = RefreshToken.for_user(request.user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })