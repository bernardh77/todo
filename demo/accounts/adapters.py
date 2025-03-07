from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed.
        """
        # Get email from social account
        email = sociallogin.account.extra_data.get('email')
        if email:
            # Check if user exists with this email
            try:
                user = User.objects.get(email=email)
                # If we get here, user exists but hasn't used social login
                # Connect social account to existing user
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                pass

    def get_login_redirect_url(self, request):
        """
        Return the URL to redirect to after a successful login via social accounts.
        """
        path = "/todo"
        return path

    def is_safe_url(self, url):
        from django.utils.http import url_has_allowed_host_and_scheme
        return url_has_allowed_host_and_scheme(url, allowed_hosts=None) 