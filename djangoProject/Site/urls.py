from django.urls import path

from Site.views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', PhoneHome.as_view(), name='home'),
    path('phones/<int:model>/', telephones, name='telephones'),
    path('home/phones/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('bascet/', Basket.as_view(), name='basket'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', PhoneCategory.as_view(), name='category')
]
