import json
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render


def index(request):
    user = request.user
    if user.is_authenticated:
        return redirect(dashboard)
    return render(request, "index.html")


@login_required
def dashboard(request):
    user = request.user
    auth0user = user.social_auth.get(provider="auth0")
    userdata = {
        "user_id": auth0user.uid,
        "name": user.first_name,
        "picture": auth0user.extra_data["picture"],
        "email": auth0user.extra_data["email"],
    }
    if user.is_staff:
        return HttpResponseRedirect("/admin")
    return render(
        request,
        "dashboard.html",
        {"auth0User": auth0user, "userdata": json.dumps(userdata, indent=4)},
    )


@login_required
def logout(request):
    log_out(request)
    return_to = urlencode({"returnTo": request.build_absolute_uri("/")})
    logout_url = "https://%s/v2/logout?client_id=%s&%s" % (
        settings.SOCIAL_AUTH_AUTH0_DOMAIN,
        settings.SOCIAL_AUTH_AUTH0_KEY,
        return_to,
    )
    return HttpResponseRedirect(logout_url)
