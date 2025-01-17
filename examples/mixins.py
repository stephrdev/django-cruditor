from django.urls import reverse_lazy


class ExamplesMixin:
    menu_title = "Examples Demo"
    menu_template_name = "menu.html"
    index_url = reverse_lazy("home")
    logout_url = reverse_lazy("logout")
    change_password_url = reverse_lazy("change-password")
