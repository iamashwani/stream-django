# streams/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('stream/<int:stream_id>/', views.live_stream, name='view_stream'),
    path('create_stream/', views.create_live_stream, name='create_stream'),
    path('my_streams/', views.view_my_streams, name='view_my_streams'),
    path('', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('signup/', views.user_signup, name='user_signup'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


