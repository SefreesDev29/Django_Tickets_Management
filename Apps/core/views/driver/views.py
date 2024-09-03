from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from Apps.core.forms import DriverForm
from Apps.security.mixins import ValidatePermissionRequiredMixin
from Apps.core.models import Driver

class DriverListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Driver
    template_name = 'driver/list.html'
    permission_required = 'view_driver'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                position = 1
                for i in Driver.objects.all():
                    item = i.toJSON()
                    item['position'] = position
                    data.append(item)
                    position += 1
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Choferes'
        context['create_url'] = reverse_lazy('core:driver_create')
        context['list_url'] = reverse_lazy('core:driver_list')
        context['entity'] = 'Drivers'
        return context

class DriverCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Driver
    form_class = DriverForm
    template_name = 'driver/create.html'
    success_url = reverse_lazy('core:driver_list')
    permission_required = 'add_driver'
    url_redirect = success_url

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de Chofer'
        context['entity'] = 'Drivers'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class DriverUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Driver
    form_class = DriverForm
    template_name = 'driver/create.html'
    success_url = reverse_lazy('core:driver_list')
    permission_required = 'change_driver'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Chofer'
        context['entity'] = 'Drivers'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class DriverDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Driver
    template_name = 'driver/delete.html'
    success_url = reverse_lazy('core:driver_list')
    permission_required = 'delete_driver'
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
        context['title'] = 'Eliminación de un Chofer'
        context['entity'] = 'Drivers'
        context['list_url'] = self.success_url
        return context
