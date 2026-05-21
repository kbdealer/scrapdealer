from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('prices/', views.prices, name='prices'),
    path('quote/', views.get_quote, name='get_quote'),
    path('pickup/', views.book_pickup, name='book_pickup'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='_about'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('comment/add/', views.add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment')
]