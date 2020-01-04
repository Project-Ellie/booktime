from django.forms import inlineformset_factory
from main import models, widgets

BasketLineFormSet = inlineformset_factory(
    models.Basket,
    models.BasketLine,
    fields=('quantity', ),
    extra=0,
    widgets={'quantity': widgets.PlusMinusNumberInput}
)
