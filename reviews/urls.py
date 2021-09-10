from django.urls import path

from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('new_ticket', views.new_ticket, name='new_ticket'),
    path('snippets/ticket/<int:ticket_id>/', views.ticket, name='ticket'),
    path('snippets/review/<int:review_id>/', views.review, name='review')
]
