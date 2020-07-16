
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('password-reset/confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_rest_confirm.htm'),name='password_reset_confirm'),
    path('account/', include('account.urls')),
    path('', include('homesite.urls')),
    path('admin/', admin.site.urls),
    path('booking/', include('bookings.urls')),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='reset-password.htm'), name='password_reset'),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='reset-password-complete.htm'), name='password_reset_complete'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='reset-password-done.htm'),name='password_reset_done'),

]
