from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        # now = datetime.now().strftime('%Y-%m-%d')
        # create_purchases = Purchase.objects.filter(date_joined=now).count()
        # active_users = User.objects.all().count()
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        # context['users'] = active_users
        # context['registro'] = create_purchases
        return context