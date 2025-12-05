from apps.subscriptions.models import SubscriptionPlan
from apps.subscriptions.services import paystack_service
from django.core.management.base import BaseCommand


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
        
        paystack_response = paystack_service.create_plan(self, name, interval, amount, description)
        plan_code = paystack_response["plan_code"]
        
        plan = SubscriptionPlan.objects.create(
            name=name,
            description=description,
            price=amount,
            billing_cycle=interval,
            paystack_plan_code=plan_code,  
            features={
                "priority_support": True,
                "analytics_dashboard": True,
                "ad_free": True,
                "early_access": True,
            },
        )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created Premium plan: {plan}")
        )
        self.stdout.write(
            self.style.WARNING(
                "\nIMPORTANT: Update paystack_plan_code after creating plan in Paystack dashboard!"
            )
        )
