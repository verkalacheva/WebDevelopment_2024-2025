from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Ваше имя',
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border rounded',
        })
    )
    email = forms.EmailField(
        label='Ваш email',
        widget=forms.EmailInput(attrs={
            'class': 'w-full p-2 border rounded',
        })
    )
    message = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(attrs={
            'class': 'w-full p-2 border rounded',
            'rows': 5,
        })
    )
