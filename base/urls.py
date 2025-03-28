from django.urls import path
from .views import register_user, login_user, upload_art, list_arts, art_detail, place_bid, get_bids

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('upload-art/', upload_art, name='upload_art'),
    path('arts/', list_arts, name='list_arts'),
    path('arts/<uuid:art_uuid>/', art_detail, name='art_detail'),
    path('arts/<uuid:art_uuid>/bid/', place_bid, name='place_bid'),
    path('arts/<uuid:art_uuid>/bids/', get_bids, name='get_bids'),
]
