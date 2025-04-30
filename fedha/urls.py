from django.contrib import admin
from django.urls import path
from . import views
from .views import dashboard_view
from .views import user_logout

urlpatterns = [ 
    path('',views.homepage, name=""),

    path('register',views.register, name="register"),

    path('login',views.login, name="login"),

    path('login',views.login_view, name="login"),

    path('dashboard',views.dashboard_view, name="dashboard"),

    path('user_logout', views.user_logout, name="user_logout"),
    
    path('dashboard', views.dashboard_view, name="dashboard"),

    path('dashboard', views.dashboard, name='dashboard'),

    path('add_policy/', views.add_policy, name='add_policy'),

    path('apply_policy/', views.apply_policy, name='apply_policy'),

    path('submit_claim/<int:policy_id>/', views.submit_claim, name="submit_claim"),
    path('claim_success/', views.claim_success, name='claim_success'),

    path('claims/', views.claims_view, name='claims_view'),
    
    path('review-claim/<int:claim_id>/', views.review_claim, name='review_claim'),

<<<<<<< HEAD:fedha/urls.py
=======
    path('admin/', admin.site.urls),

    path('dashboard/', dashboard_view, name='dashboard'),
    
>>>>>>> 8433222 (Better):insu/fedha/urls.py

    path('dashboard/', dashboard_view, name='dashboard'),
    path('contact/', views.contact_view, name='contact_form'),
    path('thanks/', views.thanks_view, name='thanks'),
    
    ]



