from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PickupBooking, QuoteRequest, ContactMessage, ScrapPrice, SCRAP_TYPES, Comment


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email= email).exists():
            raise forms.ValidationError("email already exists")
        return email


class PickupBookingForm(forms.ModelForm):
    class Meta:
        model = PickupBooking
        fields = ['name','phone', 'address', 'scrap_type', 'pickup_date', 'notes']
        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date'}),
            'scrap_type': forms.Select(choices=SCRAP_TYPES),
        }

class QuoteRequestForm(forms.ModelForm):

    class Meta:
        model = QuoteRequest
        fields = ['name', 'phone', 'scrap_type', 'weight_kg','estimated_price']
        widgets = {
            'scrap_type': forms.Select(choices=SCRAP_TYPES),
        }

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write a comment...',
                'class': 'form-control',
            })
        }
        labels = {'content': ''}