from django.shortcuts import render, redirect
from .forms import SignupForm
from .models import User
from django.views.generic import ListView


class Signup(ListView):
    template_name = 'polls/signup.html'
    form_class = SignupForm
    model = User

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            form = self.form_class
        return render(request, self.template_name,{'form': form})


class Home(ListView):
    template_name = 'polls/home.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'polls/home.html')







