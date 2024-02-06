from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Duck, Feeding
from .serializers import DuckSerializer, FeedingSerializer

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