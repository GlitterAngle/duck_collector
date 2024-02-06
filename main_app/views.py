from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Duck, Feeding, Feather
from .serializers import DuckSerializer, FeedingSerializer, FeatherSerializer

# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the duck-collector api home route!'}
    return Response(content)

class DuckList(generics.ListCreateAPIView):
  queryset = Duck.objects.all()
  serializer_class = DuckSerializer

class DuckDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Duck.objects.all()
  serializer_class = DuckSerializer
  # this here will be looking for something that just says id just a number
  lookup_field = 'id'

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