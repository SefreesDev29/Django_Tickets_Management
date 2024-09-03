import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from Apps.core.forms import PurchaseForm, DriverForm
from Apps.security.mixins import ValidatePermissionRequiredMixin
from Apps.core.models import Purchase, Ticket, DetPurchase, Driver

class PurchaseListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Purchase
    template_name = 'purchase/list.html'
    permission_required = 'view_purchase'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Purchase.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in DetPurchase.objects.filter(purchase_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Compras'
        context['create_url'] = reverse_lazy('core:purchase_create')
        context['list_url'] = reverse_lazy('core:purchase_list')
        context['entity'] = 'Purchases'
        return context

class PurchaseCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'purchase/create.html'
    success_url = reverse_lazy('core:purchase_list')
    permission_required = 'add_purchase'
    url_redirect = success_url

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                products = Ticket.objects.all()
                if len(term):
                    products = products.filter(name__icontains=term)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.name
                    # item['text'] = i.name
                    data.append(item)
            elif action == 'search_autocomplete':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                try:
                    term = request.POST['term'].strip()
                except:
                    term = ''
                data.append({'id': term, 'text': term})
                products = Ticket.objects.filter(name__icontains=term)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.name
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    purchases = json.loads(request.POST['purchases'])
                    purchase_file = request.FILES
                    purchase = Purchase()
                    purchase.date_joined = purchases['date_joined']
                    purchase.driv_id = purchases['driv']
                    if purchase_file=={}:
                        purchase.file = None
                    else:
                        purchase.file = purchase_file['file']
                    purchase.save()
                    for i in purchases['products']:
                        det = DetPurchase()
                        det.purchase_id = purchase.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.serieinicial = int(i['serieinicial'])
                        det.seriefinal = int(i['seriefinal'])
                        det.save()
                        det.prod.save()
                    data = {'id': purchase.id}
            elif action == 'search_drivers':
                data = []
                try:
                    term = request.POST['term'].strip()
                except:
                    term = ''
                drivers = Driver.objects.filter(
                    Q(names__icontains=term) | Q(surnames__icontains=term) | Q(dni__icontains=term))[0:10]
                for i in drivers:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_driver':
                with transaction.atomic():
                    frmDriver = DriverForm(request.POST)
                    data = frmDriver.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Compra'
        context['entity'] = 'Purchases'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        # context['det'] = []
        context['frmDriver'] = DriverForm()
        return context

class PurchaseUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'purchase/create.html'
    success_url = reverse_lazy('core:purchase_list')
    permission_required = 'change_purchase'
    url_redirect = success_url

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = PurchaseForm(instance=instance)
        form.fields['driv'].queryset = Driver.objects.filter(id=instance.driv.id)
        return form

    def get_details_product(self):
        data = []
        try:
            for i in DetPurchase.objects.filter(purchase_id=self.get_object().id):
                item = i.prod.toJSON()
                item['cant'] = i.cant
                item['serieinicial'] = i.serieinicial
                item['seriefinal'] = i.seriefinal
                data.append(item)
        except:
            pass
        return data

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.GET.get('action') == 'get_details':
            return JsonResponse(self.get_details_product(), safe=False)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                products = Ticket.objects.all()
                if len(term):
                    products = products.filter(name__icontains=term)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.name
                    # item['text'] = i.name
                    data.append(item)
            elif action == 'search_autocomplete':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                try:
                    term = request.POST['term'].strip()
                except:
                    term = ''
                data.append({'id': term, 'text': term})
                products = Ticket.objects.filter(name__icontains=term)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.name
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    purchases = json.loads(request.POST['purchases'])
                    purchase_file = request.FILES
                    purchase = self.get_object()
                    purchase.date_joined = purchases['date_joined']
                    purchase.driv_id = purchases['driv']
                    if 'file-clear' in request.POST:
                        purchase.file = None
                    else:
                        if 'file' in purchase_file:
                            purchase.file = purchase_file['file']
                    purchase.save()

                    existing_dets = {det.prod_id: det for det in purchase.detpurchase_set.all()}
                    new_dets = {item['id']: item for item in purchases['products']}

                    for prod_id, item in new_dets.items():
                        if prod_id in existing_dets:
                            det = existing_dets.pop(prod_id)
                            det.cant = int(item['cant'])
                            det.serieinicial = int(item['serieinicial'])
                            det.seriefinal = int(item['seriefinal'])
                            det.save()
                        else:
                            det = DetPurchase(
                                purchase=purchase,
                                prod_id=prod_id,
                                cant=int(item['cant']),
                                serieinicial=int(item['serieinicial']),
                                seriefinal=int(item['seriefinal'])
                            )
                            det.save()

                    for det in existing_dets.values():
                        det.delete()

                    data = {'id': purchase.id}
            elif action == 'search_drivers':
                data = []
                try:
                    term = request.POST['term'].strip()
                except:
                    term = ''
                drivers = Driver.objects.filter(
                    Q(names__icontains=term) | Q(surnames__icontains=term) | Q(dni__icontains=term))[0:10]
                for i in drivers:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_driver':
                with transaction.atomic():
                    frmDriver = DriverForm(request.POST)
                    data = frmDriver.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Compra'
        context['entity'] = 'Purchases'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        # context['det'] = json.dumps(self.get_details_product())
        context['frmDriver'] = DriverForm()
        return context

class PurchaseDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Purchase
    template_name = 'purchase/delete.html'
    success_url = reverse_lazy('core:purchase_list')
    permission_required = 'delete_purchase'
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
        context['title'] = 'Eliminación de una Compra'
        context['entity'] = 'Purchases'
        context['list_url'] = self.success_url
        return context
