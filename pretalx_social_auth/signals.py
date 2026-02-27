from django.dispatch import receiver
from django.template.loader import get_template
from pretalx.common.signals import auth_html, profile_bottom_html
from pretalx.person.signals import delete_user

from .utils import all_backends, backend_friendly_name, user_backends


@receiver(auth_html)
def render_login_auth_options(sender, request, next_url=None, **kwargs):
    backends = {
        class_name: backend_friendly_name(be_class)
        for class_name, be_class in all_backends().items()
    }
    if not backends:
        return ""

    url_params = ""
    next_path = request.GET.get("next", next_url)
    if next_path:
        url_params = f"?next={next_path}"

    context = {"backends": backends, "url_params": url_params}
    template = get_template("pretalx_social_auth/login.html")
    return template.render(context=context, request=request)


@receiver(profile_bottom_html)
def render_user_options_backends(sender, user, **kwargs):
    user_backend_data = user_backends(user)
    associated = [
        {
            "provider_name": backend_friendly_name(assoc.provider),
            "backend": assoc.provider,
            "id": assoc.id,
        }
        for assoc in user_backend_data["associated"]
    ]
    if not associated:
        return ""
    context = {"associated_accounts": associated}
    template = get_template("pretalx_social_auth/profile_settings.html")
    return template.render(context=context)


@receiver(delete_user)
def delete_user_data(sender, user, **kwargs):
    user.social_auth.all().delete()
