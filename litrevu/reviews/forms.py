from django import forms
from reviews.models import Review, Ticket


class CreateTicketForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class CreateReviewForm(forms.ModelForm):
    CHOICES = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5}
    note = forms.ChoiceField(widget=forms.RadioSelect(attrs={"class": "review-note"}), choices=CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["note"].label = "Note"
        if self.instance:
            self.fields["note"].initial = self.instance.rating
        self.label_suffix = ""

    class Meta:
        model = Review
        fields = ["headline", "body"]

    field_order = ["headline", "note", "body"]


class FollowUserForm(forms.Form):

    user_to_follow = forms.CharField(max_length=128)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["user_to_follow"].label = "Nom de l'utilisateur à suivre"
        self.fields["user_to_follow"].widget.attrs["placeholder"] = self.fields["user_to_follow"].label
