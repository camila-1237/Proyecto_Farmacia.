from django import forms
from .models import Producto, Venta, Transaccion
from datetime import date

class ProductoForm(forms.ModelForm):
    fecha_caducidad = forms.DateField()

    class Meta:
        model = Producto
        fields = ['nombre', 'codigo_barras', 'precio', 'fecha_caducidad', 'cantidad_inventario', 'tipo']

    def clean_fecha_caducidad(self):
        fecha_caducidad = self.cleaned_data.get('fecha_caducidad')
        if fecha_caducidad and fecha_caducidad < date.today():
            error_message = "No puedes seleccionar una fecha anterior a la actual."
            error_style = 'color: red; font-weight: bold;'
            raise forms.ValidationError(f'<span style="{error_style}">{error_message}</span>', code='invalid')
        return fecha_caducidad

class ActualizarProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'codigo_barras', 'precio', 'fecha_caducidad', 'cantidad_inventario', 'tipo']

class BuscadorProductos(forms.Form):
    consulta = forms.CharField(label='Buscar')

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['finalizada']
        widgets = {
            'finalizada': forms.CheckboxInput(),
        }

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['id_producto', 'cantidad', 'finalizada']
        widgets = {
            'id_venta': forms.HiddenInput(),
            'finalizada': forms.CheckboxInput(),
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        id_producto = self.cleaned_data.get('id_producto')

        if cantidad and id_producto:
            if cantidad > id_producto.cantidad_inventario:
                raise forms.ValidationError("No hay suficiente inventario para esta transacción.")

            return cantidad

class TextInputWithHiddenForeignKey(forms.TextInput):
    def _init_(self, *args, **kwargs):
        kwargs['attrs'] = {'type': 'text', 'readonly': True}
        super()._init_(*args, **kwargs)

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['id_producto', 'cantidad', 'finalizada']
        widgets = {
            'id_producto': TextInputWithHiddenForeignKey,  # Usar el widget personalizado aquí
            'finalizada': forms.CheckboxInput(),
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        id_producto = self.cleaned_data.get('id_producto')

        if cantidad and id_producto:
            if cantidad > id_producto.cantidad_inventario:
                raise forms.ValidationError("No hay suficiente inventario para esta transacción.")

            return cantidad