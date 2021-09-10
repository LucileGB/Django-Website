from itertools import chain

from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value
from django.shortcuts import render
from django.template import loader

from .models import Ticket, Review

def login(request):
    return render (request, 'reviews/login.html')

def register(request):
    return render (request, 'reviews/register.html')

#@login_required()
def new_ticket(request):
    return render (request, 'reviews/new_ticket.html')

def ticket(request, ticket_id):
    try:
        ticket = Ticket.objects.get(pk=ticket_id)
    except Ticket.DoesNotExist:
        raise Http404("Ce ticket n'existe pas")
    return render(request, 'reviews/snippets/ticket.html', {'ticket': ticket})

#@login_required()
def review(request, review_id):
    try:
        review = Review.objects.get(pk=review_id)
    except Review.DoesNotExist:
        raise Http404("Ce commentaire n'existe pas")
    return render(request, 'reviews/snippets/review.html', {'review': review})

@login_required()
def accueil(request):
    return render(request, 'reviews/feed.html')
"""    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_users_viewable_tickets(request.user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'reviews/feed.html', context={'posts': posts})"""
