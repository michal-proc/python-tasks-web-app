from django.contrib import messages
from django.shortcuts import render, redirect
from main.controllers import main_controller
from main.forms.playground_form import PlaygroundForm


def home(request):
    return render(request, 'main/index.html', {
        'user': request.user
    })


def playground(request):
    form = PlaygroundForm()
    if request.method == 'POST':
        form = PlaygroundForm(request.POST or None)
        output = main_controller.playground(request, form)
        if output is None:
            messages.error(request, 'Error parsing given data')
        return render(request, 'main/playground.html', {"form": form, "output": output})

    return render(request, 'main/playground.html', {"form": form, "output": None})
