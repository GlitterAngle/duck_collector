from django.urls import path
# import Home view from the views file
from .views import Home, DuckList, DuckDetail

urlpatterns = [
  path('', Home.as_view(), name='home'),
  # this allows you to get and post
  path('ducks/', DuckList.as_view(), name='cat-list'),
  # this allows you to create delete and put
  path('cats/<int:id>', DuckDetail.as_view(), name='duck-detail'),
]
