from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from Apps.core.forms import TicketForm
from Apps.core.models import Ticket
from Apps.security.mixins import ValidatePermissionRequiredMixin

class TicketListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Ticket
    template_name = 'ticket/list.html'
    permission_required = 'view_ticket'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                position = 1
                for i in Ticket.objects.all():
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
        context['title'] = 'Listado de Boletos'
        context['create_url'] = reverse_lazy('core:ticket_create')
        context['list_url'] = reverse_lazy('core:ticket_list')
        context['entity'] = 'Tickets'
        return context

class TicketCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'form.html'
    success_url = reverse_lazy('core:ticket_list')
    permission_required = 'add_ticket'
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
        context['title'] = 'Creación de Boleto'
        context['entity'] = 'Tickets'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class TicketUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'form.html'
    success_url = reverse_lazy('core:ticket_list')
    permission_required = 'change_ticket'
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
        context['title'] = 'Edición un Boleto'
        context['entity'] = 'Tickets'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class TicketDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Ticket
    template_name = 'ticket/delete.html'
    success_url = reverse_lazy('core:ticket_list')
    permission_required = 'delete_ticket'
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
        context['title'] = 'Eliminación de un Boleto'
        context['entity'] = 'Tickets'
        context['list_url'] = self.success_url
        return context
