from apps.subscriptions.models import SubscriptionPlan
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates the Premium subscription plan"

    def handle(self, *args, **options):

        if SubscriptionPlan.objects.filter(name="Premium").exists():
            self.stdout.write(self.style.WARNING("Premium plan already exists"))
            return

        plan = SubscriptionPlan.objects.create(
            name="Premium",
            description="Unlimited access to all Tech Hive features",
            price=5000.00,
            billing_cycle="MONTHLY",
            paystack_plan_code="PLN_PLACEHOLDER",
            features={
                "unlimited_articles": True,
                "priority_support": True,
                "analytics_dashboard": True,
                "ad_free": True,
                "early_access": True,
                "max_articles_per_month": None,  # None = unlimited
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
