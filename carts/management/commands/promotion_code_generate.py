import random
import string
from django.core.management.base import BaseCommand
from carts.models import PromotionCode

class Command(BaseCommand):
    help = "プロモーションコードを生成する"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=1,
            help="生成するコードの数"
        )

    def handle(self, *args, **options):
        count = options["count"]

        for _ in range(count):
            code = self.generate_code()
            discount = random.randint(100, 1000)

            PromotionCode.objects.create(
                code=code,
                discount_amount=discount
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"生成: {code} (-¥{discount})"
                )
            )

    def generate_code(self):
        chars = string.ascii_uppercase + string.digits
        while True:
            code = "".join(random.choices(chars, k=7))
            if not PromotionCode.objects.filter(code=code).exists():
                return code
