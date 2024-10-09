from ._default import DefaultModel
from .order_reconciliation_item import OrderReconciliationItem


class OrderReconciliationList(DefaultModel):
    items: list[OrderReconciliationItem]
