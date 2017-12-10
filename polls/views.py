from django.shortcuts import render, redirect
from .forms import SignupForm
from .models import User
from django.views.generic import ListView
from django.contrib.auth.views import login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class Signup(ListView):
    template_name = 'polls/signup.html'
    form_class = SignupForm
    model = User

    # dispatch override get and post function
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super(Signup, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                return render(request, self.template_name, {'form': form})
            else:
                form.save()
            return redirect('home')
        else:
            form = self.form_class
        return render(request, self.template_name,{'form': form})


class Login(ListView):
    template_name = 'polls/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super(Login, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return login(request, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        return login(request, template_name=self.template_name)


@method_decorator(login_required, name='get')
class Home(ListView):
    template_name = 'polls/home.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'polls/home.html')









