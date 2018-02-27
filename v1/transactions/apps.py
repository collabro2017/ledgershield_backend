from django.apps import AppConfig


class TransactionsConfig(AppConfig):
    name = 'v1.transactions'

    def ready(self):
        import v1.transactions.signals