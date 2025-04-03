
from django.contrib import admindocs
from django.contrib import admin
from django.urls import path, include
from . import views
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fedha.urls')),
    path('contact/', views.contact_view, name='contact'),
       
]
