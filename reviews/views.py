from itertools import chain

from django import forms
from .forms import SignUpForm, ReviewForm, TicketForm

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import CharField, Value
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.views.generic.edit import UpdateView

from .models import Ticket, Review, UserFollows, user_follows


@login_required()
def answer_ticket(request, ticket_id):
    new_review = None

    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if request.method == 'POST':
        review_form = ReviewForm(data=request.POST)

        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.ticket = ticket
            new_review.user = request.user
            new_review.save()
            return redirect('own_posts')

    else:
        review_form = ReviewForm()

    return render(request, 'reviews/review_create.html', {'ticket': ticket,
                'review_form': review_form, 'new_review': new_review, 'ticket_id': ticket_id})


@login_required()
def new_ticket(request):
    new_ticket = None

    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)

        if ticket_form.is_valid():
            new_ticket = ticket_form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.save()
            return redirect('own_posts')

    else:
        ticket_form = TicketForm()

    return render(request, 'reviews/ticket_create.html', {'ticket_form': ticket_form, 'new_ticket': new_ticket})

@login_required()
def feed(request):
    reviews = Review.get_users_viewable_reviews(request)
    own_reviews = Review.get_users_own_reviews(request)
    tickets = Ticket.get_users_viewable_tickets(request)
    own_tickets = Ticket.get_users_own_tickets(request)

    # returns queryset of reviews
    if len(reviews) > 0:
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    if len(own_reviews) > 0:
        own_reviews = own_reviews.annotate(content_type=Value('REVIEW', CharField()))

    # returns queryset of tickets
    if len(tickets) > 0:
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    if len(own_tickets) > 0:
        own_tickets = own_tickets.annotate(content_type=Value('TICKET', CharField()))
    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets, own_reviews, own_tickets),
        key=lambda post: post.time_created,
        reverse=True)

    answered = [review.ticket_id for review in own_reviews]

    return render(request, 'reviews/feed.html', context={'posts': posts, 'answered': answered})

@login_required()
def own_posts(request):
    reviews = Review.get_users_own_reviews(request)
    # returns queryset of reviews
    if len(reviews) > 0:
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = Ticket.get_users_own_tickets(request)
    # returns queryset of tickets
    if len(tickets) > 0:
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True)

    return render(request, 'reviews/feed.html', context={'posts': posts})

def new_account(request):
    form = UserCreationForm(request.GET)
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            form = UserCreationForm(request.POST)

            return render(request,'reviews/new_account.html', {'form':form})
        form = UserCreationForm(request.POST)

    return render(request,'reviews/new_account.html', {'form':form})

@login_required
def subscriptions(request):
    following = UserFollows.objects.filter(followed_user__id__contains=request.user.id)
    followed = UserFollows.objects.filter(user__id__contains=request.user.id)
    friends = user_follows(request)

    """Shows followers and followees, with a search function."""
    if request.method == "POST":
        query_name = request.POST.get('username', None)
        if query_name:
            results = User.objects.filter(username__contains=query_name)
            if len(results) == 0:
                messages.error(request, "Aucun résultat.")

            return render(request, 'reviews/subscriptions.html',
                        {"results":results, "following": following, "followed": followed, "friends": friends})

    return render(request, 'reviews/subscriptions.html', {"following": following, "followed": followed})

@login_required
def ticket_delete(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if request.user != ticket.user:
        raise PermissionDenied

    if request.method == 'POST':
        Ticket.objects.get(id=ticket_id).image.delete(save=True)
        ticket.delete()
        messages.success(request,"Votre ticket a bien été supprimé.")
        return redirect('/')

    return render(request, 'reviews/feed_own.html', {'ticket': ticket})

@login_required
def review_delete(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    if request.user != review.user:
        raise PermissionDenied

    if request.method == 'POST':
        review.delete()
        messages.success(request,"Votre critique a bien été supprimée.")
        return redirect('/')

    return render(request, 'reviews/feed_own.html', {'review': review})

def unfollow(request, relationship_id):
    follow = get_object_or_404(UserFollows, pk=relationship_id)
    unfollowed = follow.followed_user

    if request.method == 'POST':
        follow.delete()
        messages.success(request,f"Vous avez arrêté de suivre {unfollowed}.")
        return redirect('/')

    return render(request, 'reviews/feed_own.html', {'follow': follow})

def follow(request, followee_id):
    followee = get_object_or_404(User, pk=followee_id)

    if request.method == 'POST':
        UserFollows.objects.create(user=request.user, followed_user=followee)
        messages.success(request,f"Félicitations ! Vous suivez maintenant {followee}.")
        return redirect('/')

    return render(request, 'reviews/subscriptions.html', {'follow': follow})

from django.core.exceptions import PermissionDenied

@login_required
def ticket_edit(request, ticket_id):
    original = get_object_or_404(Ticket, pk=ticket_id)
    if request.user != original.user:
        raise PermissionDenied

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)

        if form.is_valid():
            updated = form.save(commit=False)
            updated.ticket = ticket
            original.title = updated.title
            original.description = updated.description
            original.image = updated.image
            original.save()
            return redirect('/')

    else:
        form = TicketForm(instance=original)

    return render(request, 'reviews/ticket_edit.html', {'form': form,
                'ticket_id': ticket_id})

@login_required
def review_edit(request, review_id):
    original = get_object_or_404(Review, pk=review_id)
    if request.user != original.user:
        raise PermissionDenied

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            updated = form.save(commit=False)
            updated.review = review
            original.headline = updated.headline
            original.rating = updated.rating
            original.body = updated.body
            original.save()
            return redirect('/')

    else:
        form = ReviewForm(instance=original)

    return render(request, 'reviews/review_edit.html', {'form': form,
                'review_id': review_id, 'original': original})

@login_required()
def spontaneous_review(request):
    new_review = None
    new_ticket = None

    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if review_form.is_valid() and ticket_form.is_valid():
            new_ticket = ticket_form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.save()

            new_review = review_form.save(commit=False)
            new_review.ticket = new_ticket
            new_review.user = request.user
            new_review.save()
            return redirect('own_posts')

    else:
        review_form = ReviewForm()
        ticket_form = TicketForm()

    return render(request, 'reviews/ticket_and_review.html', {'review_form': review_form,
                'ticket_form': ticket_form, 'new_review': new_review, 'new_ticket': new_ticket})
