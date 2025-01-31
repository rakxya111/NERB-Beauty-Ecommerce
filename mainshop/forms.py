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
        fields = "__all__"
        exclude = ['ip', 'status', 'created_at', 'updated_at']