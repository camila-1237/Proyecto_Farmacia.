from django import forms
from .models import Producto
from datetime import date

#Fer
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 
                'codigo_barras',
                'precio', 
                'fecha_caducidad', 
                'cantidad_inventario', 
                'tipo']
    fecha_caducidad = forms.DateField()

    def clean_fecha_caducidad(self):
        fecha_caducidad = self.cleaned_data.get('fecha_caducidad')
        if fecha_caducidad and fecha_caducidad < date.today():
            raise forms.ValidationError("No puedes seleccionar una fecha anterior a la actual.")
        return fecha_caducidad

class ActualizarProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'codigo_barras', 'precio', 'fecha_caducidad', 'cantidad_inventario', 'tipo']


#JuanJo
class BuscadorProductos(forms.Form):
    consulta = forms.CharField(label='Buscar')
