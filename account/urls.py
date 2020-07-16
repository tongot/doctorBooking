from django.urls import path
from . import views
urlpatterns = [
  path('register', views.register),
  path('login', views.login_user),
  path('register_dependent', views.register_dependent),
  path('logout', views.logout_user),
  path('delete_dependend/<int:id>', views.delete_dependence),
  path('update_dependent/<int:id>', views.update_dependence)
]
