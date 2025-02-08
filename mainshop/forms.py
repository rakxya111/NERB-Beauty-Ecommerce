from django_summernote.widgets import SummernoteWidget
from django import forms
from mainshop.models import Product,Contact,Newsletter,ReviewRating

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = "__all__"

class Newsletterform(forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = "__all__"

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'rating', 'review', 'user_image']