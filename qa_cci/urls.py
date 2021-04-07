from django.contrib import admin
from django.urls import path
import pipelines.views
import accounts.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', pipelines.views.home, name='home'),
    path('signup/', accounts.views.signupuser, name='signup'),
    path('login/', accounts.views.loginuser, name='login'),
    path('logout/', accounts.views.logoutuser, name='logout'),
    path('addToken/', accounts.views.addToken, name='addToken'),
    path('runall/', pipelines.views.runAll, name='runAll'),
]
