from django.shortcuts import render, redirect, reverse
from .forms import SignupForm, ProfileForm
from .models import User, Profile
from django.views.generic import ListView, DetailView, FormView, TemplateView
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
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView,  CreateView
from django.template import Context, Template, RequestContext
from django.http import HttpResponse


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
            # if User.objects.filter(email=email).exists():
            #     return render(request, self.template_name, {'form': form})
            #
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            message = 'hello how are you'
            msg_html = render_to_string('polls/email_content.html', {
                'user': username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
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
class Home(TemplateView):
    template_name = 'polls/home.html'
    model = User

    def get_queryset(self):
        self.user = User.objects.filter(user=self.request.user)
        return User.objects.filter(user=self.user)

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['all_user'] = User.objects.all()
        print(context['all_user'])
        return context

    # def get(self, request, *args, **kwargs):
    #     return render(request, 'polls/home.html')


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


# class EditProfile(CreateView):
#     template_name = 'polls/edit_profile.html'
#     form_class = ProfileForm
#     model = Profile
#     success_url = reverse_las
#     def form_valid(self, form):
#         form.save(self.request.user)
#         return super(EditProfile, self).form_valid(form)
#
#     def get_success_url(self, *args, **kwargs):
#         return reverse('home')

# class CreateProfile(CreateView):
#     template_name = 'polls/edit_profile.html'
#     if d
#     form_class = ProfileForm
#
#     model = User
#     success_url = reverse_lazy('home')
#
#     def form_valid(self, form):
#         form = self.form_class(self.request.POST)
#         if form.is_valid():
#             profile = form.save(commit=False)
#
#             profile.user_id = self.request.user.id
#             profile.save()
#             print('form is save')
#             return redirect('home')


class UpdateProfile(UpdateView):
    print("hello")
    model = User
    template_name = 'polls/edit_profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        obj = Profile.objects.get_or_create(user=self.request.user)[0]
        return obj

class About(TemplateView):
    model = User
    template_name = 'polls/about_user.html'

    def get_context_data(self, **kwargs):
        context = super(About, self).get_context_data(**kwargs)
        search_user = User.objects.get(username=self.kwargs['username'])
        context['search_profile'] = Profile.objects.get_or_create(user=search_user)[0]
        return context


def ip_address_processor(request):
    return {'ip_address': request.META['REMOTE_ADDR']}


def learn(request):
    template = Template("hello {{name}}: {{ip_address}}")
    context = RequestContext(request, {'name': 'deep'}, [ip_address_processor])
    return HttpResponse(template.render(context))


