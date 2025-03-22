from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'input input-bordered w-full',
                'placeholder':'Name'
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class':'input input-bordered w-full',
                'placeholder':'Email'
            }
        )
    )
    document = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class':'file-input file-input-bordered w-full',
                'placeholder':'Contact Doc'
            }
        ),
        required=False
    )
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Contact.objects.filter(user=self.initial.get('user') ,email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email
    
    class Meta:
        model = Contact
        fields = ['name','email','document']