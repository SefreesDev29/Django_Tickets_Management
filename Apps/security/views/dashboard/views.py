from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from Apps.security.mixins import ValidatePermissionRequiredMixin
from Apps.security.models import Dashboard
from Apps.security.forms import DashboardForm

class DashboardCreateOrUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Dashboard
    form_class = DashboardForm
    template_name = 'form.html'
    success_url = reverse_lazy('core:dashboard')
    permission_required = 'change_dashboard'
    url_redirect = success_url

    def get_object(self, queryset=None):
        obj, created = Dashboard.objects.get_or_create(id=1, defaults={
            'name': 'Sistema Web',
            'author': 'Dev',
            'interv_graph_barline' : 1,
            'grade_graph_circular': 360
        })
        return obj
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            if form.is_valid():
                form.save()
                data['success'] = True
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Configuración del Dashboard'
        context['entity'] = 'Dashboard'
        context['action'] = 'edit'
        context['list_url'] = self.success_url
        return context

def page_not_found404(request, exception):
    return render(request, '404.html')