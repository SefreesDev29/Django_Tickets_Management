from datetime import datetime, timedelta

from django.utils.timezone import make_aware
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from Apps.security.mixins import ValidatePermissionRequiredMixin
from Apps.core.models import Driver

class AuditDriverListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Driver.history.model
    template_name = 'auditdriver/list.html'
    permission_required = 'view_historicaldriver'

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
                queryset = Driver.history.all()
                if len(start_date) and len(end_date):
                    start_datetime = make_aware(datetime.combine(datetime.strptime(start_date,'%Y-%m-%d'), datetime.min.time()))
                    end_datetime = make_aware(datetime.combine(datetime.strptime(end_date,'%Y-%m-%d'), datetime.max.time()))
                    queryset = queryset.filter(history_date__range=[start_datetime,end_datetime])
                for record in queryset:
                    data.append(self.get_audit_record(record))
            elif action == 'search_details':
                data = []
                for record in Driver.history.filter(history_id=request.POST['id']):
                    data = self.get_audit_record(record,True)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_audit_record(self, record, details = False):
        if not details:
            item = {}
            item['history_id'] = record.history_id
            item['record_id'] = record.id
            item['history_date'] = (record.history_date - timedelta(hours=5)).strftime('%d/%m/%Y %H:%M')
            item['history_user'] = record.history_user.toJSON() if record.history_user else {'username': '-', 'full_name': '-'}
            item['history_type'] = record.history_type
        else:
            item = []
            if record.history_type == '+':
                item = [{'field': '-', 'old': '-', 'new': '-', 
                    'remark' : 'Registro creado: ' + 'Chofer-{} | {} {}'.format(record.dni, record.names, record.surnames)
                }]
            elif record.history_type == '-':
                item = [{'field': '-', 'old': '-', 'new': '-',
                    'remark' : 'Registro eliminado: ' + 'Chofer-{} | {} {}'.format(record.dni, record.names, record.surnames)
                }]
            else:
                if record.prev_record:
                    changes = record.diff_against(record.prev_record).changes
                    item = [
                        {'field': change.field, 'old': change.old, 'new': change.new, 'remark' : 'Registro actualizado'} 
                        for change in changes if change.field != 'user_updated'
                    ]
                else:
                    item= [{'field': '-', 'old': '-', 'new': '-', 'remark' : 'Registro actualizado'}]
            
        return item
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Auditoría de Choferes'
        context['list_url'] = reverse_lazy('security:audit_driver_list')
        context['entity'] = 'HistoricalDrivers'
        return context