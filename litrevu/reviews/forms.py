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
        self.fields["rating"] = forms.RadioSelect()

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]


class FollowUserForm(forms.Form):

    user_to_follow = forms.CharField(max_length=128)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["user_to_follow"].label = "Nom de l'utilisateur à suivre"
