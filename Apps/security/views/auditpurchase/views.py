import os
from datetime import datetime, timedelta

from django.utils.timezone import make_aware
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from Apps.security.mixins import ValidatePermissionRequiredMixin
from Apps.core.models import Purchase,DetPurchase

class AuditPurchaseListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Purchase.history.model
    template_name = 'auditpurchase/list.html'
    permission_required = 'view_historicalpurchase'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date'] 
                queryset = Purchase.history.all()
                if len(start_date) and len(end_date):
                    start_datetime = make_aware(datetime.combine(datetime.strptime(start_date,'%Y-%m-%d'), datetime.min.time()))
                    end_datetime = make_aware(datetime.combine(datetime.strptime(end_date,'%Y-%m-%d'), datetime.max.time()))
                    queryset = queryset.filter(history_date__range=[start_datetime,end_datetime])
                for record in queryset:
                    data.append(self.get_audit_record(record))
            elif action == 'search_details':
                data = []
                for record in Purchase.history.filter(history_id=request.POST['id']):
                    data = self.get_audit_record(record,True)
            elif action == 'search_details_items':
                data = []
                date = datetime.strptime(str(request.POST['date']),'%d/%m/%Y %H:%M:%S')
                for record in DetPurchase.history.filter(Q(purchase_id=request.POST['id']) &
                                                            Q(history_date__year=date.year) &
                                                            Q(history_date__month=date.month) &
                                                            Q(history_date__day=date.day) &
                                                            Q(history_date__hour=date.hour) &
                                                            Q(history_date__minute=date.minute) &
                                                            (Q(history_date__second=date.second) 
                                                             | Q(history_date__second=(date + timedelta(seconds=1)).second) 
                                                             | Q(history_date__second=(date + timedelta(seconds=2)).second)
                                                            )):
                    dict_item = self.get_audit_record(record,True,True)
                    if isinstance(dict_item, list):
                        [data.append(item) for item in dict_item]
                    else:
                        data.append(dict_item)
                data = [item for item in data if item]
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_audit_record(self,record, details = False, itemsdetails = False):
        item = {}
        if not details:
            item['history_id'] = record.history_id
            item['purchase_id'] = record.id
            item['history_date'] = (record.history_date - timedelta(hours=5)).strftime('%d/%m/%Y %H:%M')
            item['history_date_full'] = (record.history_date - timedelta(hours=5)).strftime('%d/%m/%Y %H:%M:%S')
            item['history_user'] = record.history_user.toJSON() if record.history_user else {'username': '-', 'full_name': '-'}
            item['history_type'] = record.history_type
        else:
            field_verbose_names = {field.name: field.verbose_name for field in record._meta.fields}
            if not itemsdetails:
                item = []
                if record.history_type == '+':
                    item = [{'field': '-', 'old': '-', 'new': '-', 
                        'remark' : 'Registro creado: ' + 'Chofer-{} | File-{}'.format(record.driv.dni, os.path.basename(record.file) if record.file else 'N.A.')
                    }]
                elif record.history_type == '-':
                    item = [{'field': '-', 'old': '-', 'new': '-',
                        'remark' : 'Registro eliminado: ' + 'Chofer-{} | File-{}'.format(record.driv.dni, os.path.basename(record.file) if record.file else 'N.A.')
                    }]
                else:
                    if record.prev_record:
                        changes = record.diff_against(record.prev_record).changes
                        item = [
                            {'field': field_verbose_names.get(change.field, change.field), 
                            'old': str(change.old).replace('files/', '') if 'files/' in change.old else change.old, 
                            'new': str(change.new).replace('files/', '') if 'files/' in change.new else change.new, 
                            'remark' : 'Registro actualizado'} 
                            for change in changes if change.field != 'user_updated'
                        ]
                        if len(item) == 0:
                            item= [{'field': '-', 'old': '-', 'new': '-', 'remark' : 'Ítems actualizados'}]
                    else:
                        item= [{'field': '-', 'old': '-', 'new': '-', 'remark' : 'Registro actualizado'}]
            else:
                if record.history_type == '+':
                    item = {'field': '-', 'old': '-', 'new': '-', 
                        'remark' : 'Ítem agregado: ' + 'Ticket-{} | Cant-{} | Serie-({})({})'.format(record.prod.name, record.cant, record.serieinicial, record.seriefinal)
                    }
                elif record.history_type == '-':
                    item = {'field': '-', 'old': '-', 'new': '-',
                        'remark' : 'Ítem eliminado: ' + 'Ticket-{} | Cant-{} | Serie-({})({})'.format(record.prod.name, record.cant, record.serieinicial, record.seriefinal)
                    }
                else:
                    if record.prev_record:
                        changes = record.diff_against(record.prev_record).changes
                        item = [
                            {'field': field_verbose_names.get(change.field, change.field), 
                             'old': change.old, 'new': change.new,
                             'remark' : 'Ítem actualizado: ' + 'Ticket-{}'.format(record.prod.name)} 
                            for change in changes if change.field != 'user_updated'
                        ]
                    else:
                        item= {'field': '-', 'old': '-', 'new': '-', 'remark' : 'Ítem actualizado'}
            
        return item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Auditoría de Compras'
        context['list_url'] = reverse_lazy('security:audit_purchase_list')
        context['entity'] = 'HistoricalPurchases'
        return context