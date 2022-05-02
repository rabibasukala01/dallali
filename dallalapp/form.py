from django.forms import ModelForm
from .models import Dhani


class PostForm(ModelForm):
    class Meta:
        model = Dhani
        # fields = '__all__'
        fields = ('phone_number', 'about', 'latitude',
                  'longitude', 'Type', 'quantity', 'price', 'address')
