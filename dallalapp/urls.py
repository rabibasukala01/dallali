from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('logout', views.log_out, name='logout'),
    path('add', views.add, name='add'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('allmap', views.allmap, name='allmap'),
    path('howto', views.howto, name='howto'),

    path('map/<str:pk>', views.map, name='map'),
    path('usercomments/<int:pk>', views.usercomments, name='usercomments'),
    path('update/update_post/<int:pk>', views.update_post, name='update_post'),
    path('delete_post/<int:pk>', views.delete_post, name='delete_post')

]
