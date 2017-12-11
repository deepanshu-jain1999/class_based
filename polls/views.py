from django.shortcuts import render, redirect
from .forms import SignupForm
from .models import User
from django.views.generic import ListView
from django.contrib.auth.views import login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import Http404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token


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
            username = form.cleaned_data.get('username')
            current_site = get_current_site(request)
            if User.objects.filter(email=email).exists():
                return render(request, self.template_name, {'form': form})
            else:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                print('user-->',user.pk)
                print(urlsafe_base64_encode(force_bytes(user.pk)))
                print(account_activation_token.make_token(user))
                message = 'hello how are you'
                msg_html = render_to_string('polls/email_content.html', {
                    'user': username,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),

                })
                subject = 'Activate your account'
                from_mail = 'mp3converter2017@gmail.com'
                to_mail = [email]
                send_mail(subject, message, from_mail, to_mail, html_message=msg_html, fail_silently=False)
                return render(request, 'polls/after_email_send.html')
        else:
            form = self.form_class
        return render(request, self.template_name, {'form': form})


class Activate(ListView):

    def get(self, request, *args, **kwargs):
        try:
            x = self.kwargs['uidb64']
            # decode the uid from 64 base to normal text
            uid = force_text(urlsafe_base64_decode(x))
            # fetch user information
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        print("------>", user)
        if user is not None and account_activation_token.check_token(user, self.kwargs['token']):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'polls/email_link_invalid.html')


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


class ValidateUsername(ListView):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            username = request.GET.get('username', None)
            data = {
                'is_taken': User.objects.filter(username__iexact=username).exists()
            }
            return JsonResponse(data)
        else:
            raise Http404


class ValidateEmail(ListView):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            email = request.GET.get('email', None)
            data = {
                'is_taken': User.objects.filter(email__iexact=email).exists()
            }
            return JsonResponse(data)
        else:
            raise Http404




