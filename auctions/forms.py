from django import forms
from django.forms.utils import ErrorList

from .models import Listing, Comment, Bid


class DivErrorList(ErrorList):
        def __str__(self):
            return self.as_divs()
        def as_divs(self):
            if not self: return ''
            return ''.join(['<div class="alert alert-danger py-2 my-2" role="alert">%s</div>' % e for e in self])

class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('title', 'category', 'img_url', 'description', 'starting_bid')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'category': forms.Select(attrs={'class': 'form-control mb-2'}),
            'img_url': forms.URLInput(attrs={'class': 'form-control mb-2'}),
            'description': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'starting_bid': forms.NumberInput(attrs={'class': 'form-control mb-2'}),
        }

    def clean_starting_bid(self):
        starting_bid = self.cleaned_data["starting_bid"]

        if starting_bid < 0.01:
            raise forms.ValidationError('Starting bid should be more than 0')

        return starting_bid


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control mb-3', 'placeholder': 'Add comment...', 'rows': '3'})
        }

        labels = {
            'text': ''
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('amount',)

        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Enter your bid'})
        }

        labels = {
            'amount': ''
        }
