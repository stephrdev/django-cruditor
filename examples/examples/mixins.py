from django.urls import reverse_lazy


class ExamplesMixin:
    menu_title = 'Examples Demo'
    logout_url = reverse_lazy('logout')
    change_password_url = reverse_lazy('change-password')
