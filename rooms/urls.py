from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.rooms, name='rooms'),
    path('room-detail/<int:id>', views.room_detail, name='room_detail'),
    path('confirm-now-booking',views.book_confirm,name="book_confirm"),
    path('cancel-room/<str:id>',views.cancel_room,name='cancel_room'),
    # path('delete-room/<str:id>',views.delete_room,name='delete-room'),

]