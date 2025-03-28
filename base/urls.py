from django.urls import path
from .views import register_user, login_user, upload_art, list_arts, art_detail, place_bid, get_bids

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('upload-art/', upload_art, name='upload_art'),
    path('arts/', list_arts, name='list_arts'),
    path('arts/<int:art_id>/', art_detail, name='art_detail'),  # Changed uuid to int for art_id
    path('arts/<int:art_id>/bid/', place_bid, name='place_bid'),  # Changed uuid to int for art_id
    path('arts/<int:art_id>/bids/', get_bids, name='get_bids'),  # Changed uuid to int for art_id
]
