from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from orders.models import Order


class Command(BaseCommand):
    help = "Atualiza automaticamente o status dos pedidos"

    def handle(self, *args, **kwargs):
        now = timezone.now()

        orders = Order.objects.exclude(status__in=["delivered", "canceled"])

        for order in orders:
            time_diff = now - order.status_updated_at

            # pending → paid (10 minutos)
            if order.status == "pending" and time_diff >= timedelta(minutes=10):
                order.status = "paid"
                order.save()
                continue

            # paid → shipped (30 minutos)
            if order.status == "paid" and time_diff >= timedelta(minutes=30):
                order.status = "shipped"
                order.save()
                continue

            # shipped → delivered (1 dia)
            if order.status == "shipped" and time_diff >= timedelta(days=1):
                order.status = "delivered"
                order.save()
                continue

        self.stdout.write(self.style.SUCCESS("Status atualizados com sucesso"))