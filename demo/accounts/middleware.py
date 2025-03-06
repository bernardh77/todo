from .models import ModProfile

class ThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_mod:
            mod_profile = ModProfile.objects.filter(user=request.user).first()
            request.session["theme"] = mod_profile.theme if mod_profile else "light"
        else:
            request.session["theme"] = "light"

        return self.get_response(request)
