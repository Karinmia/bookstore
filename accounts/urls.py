from django.urls import path

from accounts.views import (SignInView, SignUpView, UserList, UserUpdateView,
                            ChangePasswordView, ForgotPasswordView, ResetPasswordView,
                            )


urlpatterns = [
    path('signin/', SignInView.as_view()),
    path('signup/', SignUpView.as_view()),
    path('users/', UserList.as_view()),
    path('update-user/', UserUpdateView.as_view()),
    # path('update-photo/', UserUpdatePhotoView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
]
