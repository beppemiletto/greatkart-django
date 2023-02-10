from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name' , 'phone', 'email', 'address_line_1',
        'address_line_2' ,  'country', 'state' ,
        city = models.CharField(max_length=50)
        order_note = models.CharField(max_length=100, blank=True)
        order_total = models.FloatField()
        tax = models.FloatField()
        status = models.CharField(max_length=10, choices=STATUS, default='New')
        ip = models.CharField(max_length=20, blank=True)
        is_ordered = models.BooleanField(default=False)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):]
