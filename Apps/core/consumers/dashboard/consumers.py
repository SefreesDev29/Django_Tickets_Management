import json
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Count
from django.db.models.functions import ExtractYear, ExtractMonth
from Apps.core.models import Purchase, Driver
from Apps.utils import months_names_es
from asgiref.sync import sync_to_async

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['action'] == 'get_data_graph':
            response_data = await self.get_chart_data()
            await self.send(text_data=json.dumps(response_data))

    @sync_to_async
    def get_purchases_by_year(self, min_year):
        return list(
            Purchase.objects.filter(date_joined__year__gt=min_year)
            .annotate(year=ExtractYear('date_joined'))
            .values('year')
            .annotate(total=Count('id'))
            .order_by('year')
        )

    @sync_to_async
    def get_purchases_by_driver(self):
        return list(
            Purchase.objects.values('driv_id')
            .annotate(total=Count('id'))
            .order_by('-total')
        )

    @sync_to_async
    def get_drivers(self, driver_ids):
        return list(Driver.objects.filter(id__in=driver_ids))

    @sync_to_async
    def get_purchases_by_month(self):
        return list(
            Purchase.objects.filter(date_joined__year=datetime.now().year)
            .annotate(month=ExtractMonth('date_joined'))
            .values('month')
            .annotate(total=Count('id'))
            .order_by('month')
        )

    async def get_chart_data(self):
        min_year = (datetime.now() - relativedelta(years=5)).year

        purchases_by_year = await self.get_purchases_by_year(min_year)
        years = [p['year'] for p in purchases_by_year]
        total_purchases_by_year = [p['total'] for p in purchases_by_year]

        purchases_by_driver = await self.get_purchases_by_driver()
        driver_ids = [p['driv_id'] for p in purchases_by_driver]
        drivers = await self.get_drivers(driver_ids)
        user_data = {
            driver.get_full_name(): next(p['total'] for p in purchases_by_driver if p['driv_id'] == driver.id)
            for driver in drivers
        }

        purchases_by_month = await self.get_purchases_by_month()
        monthly_purchases = [
            {'month': months_names_es[month_data['month']], 'total': month_data['total']}
            for month_data in purchases_by_month
        ]
        months = [str(m['month']) for m in monthly_purchases]
        total_purchases_by_month = [m['total'] for m in monthly_purchases]

        return {
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