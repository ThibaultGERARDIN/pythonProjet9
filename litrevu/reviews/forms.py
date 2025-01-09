from django import forms
from reviews.models import Review, Ticket, UserFollows


class CreateTicketForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class CreateReviewForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]


class FollowUserForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = "__all__"
