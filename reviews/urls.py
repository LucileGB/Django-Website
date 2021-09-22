from django.urls import path

from . import views


urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('new_account', views.new_account, name='new_account'),
    path('new_review', views.new_review, name='new_review'),
    path('new_ticket', views.new_ticket, name='new_ticket'),
    path('own_posts', views.own_posts, name='own_posts'),
    path('subscriptions', views.subscriptions, name='subscriptions'),
    path('answer_ticket/<int:ticket_id>/', views.answer_ticket, name='answer_ticket'),
    path('ticket/<int:ticket_id>/', views.ticket, name='ticket'),
    path('review/<int:review_id>/', views.review, name='review'),
    path('ticket_delete/<int:ticket_id>/', views.ticket_delete, name='ticket_delete'),
    path('review_delete/<int:review_id>/', views.review_delete, name='review_delete'),
    path('follow/<int:followee_id>/', views.follow, name='follow'),
    path('unfollow/<int:relationship_id>/', views.unfollow, name='unfollow'),
]
