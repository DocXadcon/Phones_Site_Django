from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .utils import *
from .forms import *
from .models import *
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Продать телефон", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': 'Корзина', 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


def welcome(request):
    return HttpResponse("<h1>Welcome to the site<h1>")


def telephones(request, model):
    if model <= 5:
        return HttpResponse(f"<li>This page is information about phones model {model} of Samsung")
    elif 10 >= model >= 5:
        return HttpResponse(f"This page about phones from Iphone model {model}")
    return redirect('/', permanent=True)


def pageNotFound(request, exception):
    return HttpResponseNotFound("This page not found")


class PhoneHome(DataMixin, ListView):
    model = Phone
    template_name = 'Site/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Phone.objects.filter(is_published=True).select_related('cat')


# def index(request):
#     posts = Phone.objects.all()
#
#     context = {'posts': posts,
#                'menu': menu,
#                'title': "Главная страница",
#                'cat_selected': 0}
#     return render(request, 'Site/index.html', context=context)

def about(request):
    contact_list = Phone.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Site/about.html', {'page_obj': page_obj, 'menu': menu, 'title': "О сайте"})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'Site/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление смартфона')
        return dict(list(context.items()) + list(c_def.items()))


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'Site/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})

#
# def contact(request):
#     return HttpResponse('Обратная связь')


#
# def login(request):
#     return HttpResponse('Авторизация')


class ShowPost(DataMixin, DetailView):
    model = Phone
    template_name = 'Site/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


# def show_post(request, post_slug):
#     post = get_object_or_404(Phone, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'Site/post.html', context=context)


class PhoneCategory(DataMixin, ListView):
    model = Phone
    template_name = 'Site/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Phone.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


# def show_category(request, cat_slug):
#     posts = Phone.objects.filter(cat__slug=cat_slug)
#     # if len(posts) == 0:
#     #     raise Http404()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': "Отображение по рубрикам",
#         'cat_selected': cat_slug,
#     }
#     return render(request, 'Site/index.html', context=context)
class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'Site/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'Site/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'Site/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class Basket(DataMixin, FormView):
    form_class = BasketForm
    template_name = 'Site/basket.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Товары в вашей корзине")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        return redirect('home')
