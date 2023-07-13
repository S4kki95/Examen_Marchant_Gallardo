from django.shortcuts import render, redirect
from .models import Producto, Boleta, detalle_boleta
from .forms import ProductoForm,RegistroUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from productos.compra import Carrito
# Create your views here.
def index(request):
     return render(request, 'index.html')

@login_required
def otra(request):
     compras = Producto.objects.raw('select * from productos_producto')
     datos={
          'productos':compras
     }
     return render(request, 'otra.html', datos)

     '''
     vehiculos = Vehiculo.objects.all() #similar a select * from vehiculo
     datos ={'autitos':vehiculos}
     return render(request, 'otra.html',datos)
     '''
@login_required
def crear(request):
     if request.method=="POST":    
          productoform = ProductoForm(request.POST, request.FILES)    #creamos un objeto de tipo Formulario
          if productoform.is_valid():
               productoform.save()      #similar al insert de sql en función 
               return redirect('otra')
     else: 
          productoform=ProductoForm()
     return render(request, 'crear.html', {'producto_form':productoform})



@login_required
def eliminar(request, id):
     productoEliminado = Producto.objects.get(patente=id)   #select * from Producto where objeto=id
     productoEliminado.delete()
     return redirect ('otra')

@login_required
def modificar(request, id):
     productoModificado=Producto.objects.get(patente=id)
     datos = {
          'form' : ProductoForm(instance=productoModificado)
     }
     if request.method=='POST':
          formulario = ProductoForm(data=request.POST, instance=productoModificado)
          if formulario.is_valid:
               formulario.save()
               return redirect('otra')
     return render(request, 'modificar.html', datos)


def registrar(request):
     data={
          'form' : RegistroUserForm()
     }
     if request.method=="POST":
          formulario = RegistroUserForm(data=request.POST)
          if formulario.is_valid():
               formulario.save()
               user=authenticate(username=formulario.cleaned_data["username"],
                                 password=formulario.cleaned_data["password1"])
               login(request, user)
               return redirect('index')
          data["form"]=formulario
     return render(request, 'registration/registrar.html',data)

def mostrar(request):
     compras = Producto.objects.all()
     datos={
          'compras':compras
     }
     return render(request, 'mostrar.html', datos)

def tienda(request):
    compras = Producto.objects.all()
    datos={
        'compras':compras
    }
    return render(request, 'tienda.html', datos)


def agregar_producto(request,id):
    carrito_compra= Carrito(request)
    producto = Producto.objects.get(objeto=id)
    carrito_compra.agregar(producto=producto)
    return redirect('tienda')

def eliminar_producto(request, id):
    carrito_compra= Carrito(request)
    producto = Producto.objects.get(objeto=id)
    carrito_compra.eliminar(producto=producto)
    return redirect('tienda')

def restar_producto(request, id):
    carrito_compra= Carrito(request)
    producto = Producto.objects.get(objeto=id)
    carrito_compra.restar(producto=producto)
    return redirect('tienda')

def limpiar_carrito(request):
    carrito_compra= Carrito(request)
    carrito_compra.limpiar()
    return redirect('tienda')    


def generarBoleta(request):
    precio_total=0
    for key, value in request.session['carrito'].items():
        precio_total = precio_total + int(value['precio']) * int(value['cantidad'])
    boleta = Boleta(total = precio_total)
    boleta.save()
    productos = []
    for key, value in request.session['carrito'].items():
            producto = Producto.objects.get(objeto = value['producto_id'])
            cant = value['cantidad']
            subtotal = cant * int(value['precio'])
            detalle = detalle_boleta(id_boleta = boleta, id_producto = producto, cantidad = cant, subtotal = subtotal)
            detalle.save()
            productos.append(detalle)
    datos={
        'productos':productos,
        'fecha':boleta.fechaCompra,
        'total': boleta.total
    }
    request.session['boleta'] = boleta.id_boleta
    carrito = Carrito(request)
    carrito.limpiar()
    return render(request, 'detallecarrito.html',datos)
