from django.urls import path
# import Home view from the views file
from .views import Home, DuckList, DuckDetail, FeedingListCreate ,FeedingDetail, FeatherList, FeatherDetail, AddFeatherToDuck, RemoveFeatherFromDuck, CreateUserView, LoginView, VerifyUserView

urlpatterns = [
  path('', Home.as_view(), name='home'),
  # this allows you to get and post
  path('ducks/', DuckList.as_view(), name='cat-list'),
  # this allows you to create delete and put
  path('ducks/<int:id>/', DuckDetail.as_view(), name='duck-detail'),
  path('ducks/<int:duck_id>/feedings/', FeedingListCreate.as_view(), name='feeding-list-create'),
  path('ducks/<int:duck_id>/feedings/<int:id>/', FeedingDetail.as_view(), name='feeding-detail'),
  path('ducks/<int:duck_id>/add_feather/<int:feather_id>/', AddFeatherToDuck.as_view(), name= 'add-featehr-to-duck'),
  path('ducks/<int:duck_id>/remove_feather/<int:feather_id>/', RemoveFeatherFromDuck.as_view(), name='remove-feather-from-duck'),
  path('feathers/', FeatherList.as_view(), name='feather-list'),
  path('feathers/<int:id>/', FeatherDetail.as_view(), name='feather-detail'),
  path('users/register/', CreateUserView.as_view(), name='register'),
  path('users/login/', LoginView.as_view(), name='login'),
  path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
]
