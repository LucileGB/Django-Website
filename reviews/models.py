from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='images')
    time_created = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_users_viewable_tickets(request):
        return get_users_viewable_content(request, Ticket)

    @staticmethod
    def get_users_own_tickets(request):
        return Ticket.objects.filter(user__id__contains=request.user.id)

    def __str__(self):
        return self.title


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_users_viewable_reviews(request):
        return get_users_viewable_content(request, Review)

    @staticmethod
    def get_users_own_reviews(request):
        return Review.objects.filter(user__id__contains=request.user.id)

    @property
    def star_rating(self):
        return (self.rating*"★")

    def __str__(self):
        return self.headline


class UserFollows(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='following')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name='followed_by')

    class Meta:
        unique_together = ('user', 'followed_user')


#Model-related utilities to fetch view components
def user_follows(request):
    follows = UserFollows.objects.filter(user__id__contains=request.user.id)
    friends = [followed.followed_user.id for followed in follows]
    return(friends)


def get_users_viewable_content(request, Target):
    friends = user_follows(request)
    viewable_content = []
    for friend in friends:
        viewable_content = (Target.objects.filter(user__id__contains=friend))

    return viewable_content
