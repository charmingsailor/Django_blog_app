from django.urls import path
from . import views


urlpatterns = [
    path('',views.home, name="home"),
    path('room/<str:pk>/',views.room, name="room"),
    path('profile/<str:pk>/', views.profilePage, name="user_profile"),
    path('edit_user/', views.editUser, name="edit-user"),
    path('create_room/', views.createRoom, name="create_room"),
    path('update_room/<str:pk>', views.updateRoom, name="update_room"),
    path('delete_room/<str:pk>', views.deleteRoom, name="delete_room"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('delete_message/<str:pk>/<str:sd>', views.deleteMessage, name="delete_message"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
]