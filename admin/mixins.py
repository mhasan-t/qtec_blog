from django.contrib.auth.mixins import UserPassesTestMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('admin:login'))
