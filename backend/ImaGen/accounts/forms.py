from django import forms
from .models import *


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username', 'name')

    def clean(self):
        # Check that the two password entries match
        cleaned_data = super(UserCreationForm, self).clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm Password does not match!"
            )


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'photo', 'bio', 'url', 'location']

class UserProfileForm(forms.ModelForm):
    name = forms.CharField(max_length = 255, 
        help_text="Your name may appear around ImaGen where you show or are mentioned. You can remove it at any time.", 
        required=False
    )
    photo = forms.ImageField()
    url = forms.CharField(max_length=255 , help_text="", required=False)
    bio = forms.CharField(max_length=255, help_text="You can @mention other users and organizations to link to them. ",required=False)
    location = forms.CharField(max_length=255, help_text="Your location such country or localization", required=False)
    class Meta:
        model = User
        fields = ['name', 'photo', 'url', 'bio', 'location']


# Feedback form
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }
