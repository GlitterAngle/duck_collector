from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Duck
from .serializers import DuckSerializer

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
  lookup_field = 'id'

