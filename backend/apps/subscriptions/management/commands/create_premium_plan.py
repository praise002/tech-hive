from apps.subscriptions.models import SubscriptionPlan
from apps.subscriptions.services import paystack_service
from django.core.management.base import BaseCommand

from backend.apps.subscriptions.services import subscription_service


class Command(BaseCommand):
    help = "Creates the Premium subscription plan"

    def handle(self, *args, **options):
        name = "Premium"

        if SubscriptionPlan.objects.filter(name=name).exists():
            self.stdout.write(self.style.WARNING("Premium plan already exists"))
            return

        interval = "monthly"
        amount = 5000.00
        description = "Unlimited access to all Tech Hive features"
        features = {
            "priority_support": True,
            "analytics_dashboard": True,
            "ad_free": True,
            "early_access": True,
        }

        subscription_service.create_plan(self, name, interval, amount)

        paystack_service.create_plan(
            self, name, interval, amount, description, features, description
        )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created Premium plan: {plan}")
        )
        self.stdout.write(
            self.style.WARNING(
                "\nIMPORTANT: Update paystack_plan_code after creating plan in Paystack dashboard!"
            )
        )
