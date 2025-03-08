from django.contrib import admin
from django.urls import path
from . import views  # Import your views file
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='homepage'),  # Root URL mapped to index view
    path('index', views.index, name='homepage'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('parkinson', views.parkinson, name='parkinson'),
    path('test', views.test, name='test'),
]
#from django.urls import path
