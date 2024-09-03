from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.models.functions import ExtractYear, ExtractMonth

from Apps.core.models import Purchase, Driver
from Apps.utils import months_names_es

from datetime import datetime
from dateutil.relativedelta import relativedelta

class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard.html'
        
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_data_graph':
                # Obtener los datos para el gráfico de barras (total de compras los últimos 5 años)
                min_year = (datetime.now() - relativedelta(years=5)).year
                purchases_by_year = Purchase.objects.filter(date_joined__year__gt=min_year).annotate(year=ExtractYear('date_joined')).values('year').annotate(total=Count('id')).order_by('year')
                years = [p['year'] for p in purchases_by_year]
                total_purchases_by_year = [p['total'] for p in purchases_by_year]
                
                # Obtener los datos para el gráfico circular (distribución de compras por chofer)
                purchases_by_driver = Purchase.objects.values('driv_id').annotate(total=Count('id')).order_by('-total')
                drivers = Driver.objects.filter(id__in=[p['driv_id'] for p in purchases_by_driver])
                user_data = {driver.get_full_name(): next(p['total'] for p in purchases_by_driver if p['driv_id'] == driver.id) for driver in drivers}

                # Obtener los datos para el gráfico de líneas (compras por mes en un año específico)
                purchases_by_month = Purchase.objects.filter(date_joined__year=datetime.now().year).annotate(month=ExtractMonth('date_joined')).values('month').annotate(total=Count('id')).order_by('month')
                monthly_purchases = [
                    {'month': months_names_es[month_data['month']], 'total': month_data['total']}
                    for month_data in purchases_by_month
                ]
                months = [str(m['month']) for m in monthly_purchases]
                total_purchases_by_month = [m['total'] for m in monthly_purchases]

                data = {
                    'bar_chart': {
                        'years': years,
                        'total_purchases': total_purchases_by_year
                    },
                    'pie_chart': {
                        'user_data': user_data
                    },
                    'line_chart': {
                        'months': months,
                        'total_purchases': total_purchases_by_month
                    }
                }
            else:
                data['error'] = 'No ha ingresado a ninguna opción.'
        except Exception as e:
            data['error'] = str(e) 
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        # now = datetime.now().strftime('%Y-%m-%d')
        # create_purchases = Purchase.objects.filter(date_joined=now).count()
        # active_users = User.objects.all().count()
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        # context['users'] = active_users
        # context['registro'] = create_purchases
        return context