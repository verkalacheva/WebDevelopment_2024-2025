from django.shortcuts import render
from .forms import ContactForm
from .models import ContactMessage

def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    success = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Сохраняем данные формы в базу
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            success = True
            form = ContactForm()  # Очищаем форму после отправки
    else:
        form = ContactForm()

    return render(request, 'main/contact.html', {'form': form, 'success': success})
