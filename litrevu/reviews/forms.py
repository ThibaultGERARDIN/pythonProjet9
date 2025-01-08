from django import forms
from reviews.models import Review, Ticket, UserFollows


class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = "__all__"


class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = "__all__"


class FollowUserForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = "__all__"
