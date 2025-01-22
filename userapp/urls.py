
from django.urls import path
from userapp import views
from userapp.views import about

urlpatterns = [
    path('login/',views.login),
    path('logout/',views.logout),
    path('signup/',views.signup),
    path('home/',views.home),
    path('',views.login_home),
    path('about/',views.about)

]