from datetime import datetime

from django.utils.timezone import make_aware
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DeleteView

from Apps.security.mixins import ValidatePermissionRequiredMixin
from Apps.security.models import AccessUser

class AccessUserListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = AccessUser
    template_name = 'accessuser/list.html'
    permission_required = 'view_accessuser'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date'] 
                queryset = AccessUser.objects.all()
                if len(start_date) and len(end_date):
                    start_datetime = make_aware(datetime.combine(datetime.strptime(start_date,'%Y-%m-%d'), datetime.min.time()))
                    end_datetime = make_aware(datetime.combine(datetime.strptime(end_date,'%Y-%m-%d'), datetime.max.time()))
                    queryset = queryset.filter(timestamp__range=[start_datetime,end_datetime])
                for i in queryset:
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Accesos de Usuarios'
        context['list_url'] = reverse_lazy('security:accessuser_list')
        context['entity'] = 'AccessUsers'
        return context

class AccessUserDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = AccessUser
    template_name = 'delete.html'
    success_url = reverse_lazy('security:accessuser_list')
    permission_required = 'delete_accessuser'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Accesos de Usuarios'
        context['list_url'] = reverse_lazy('security:accessuser_list')
        context['entity'] = 'AccessUsers'
        return context
