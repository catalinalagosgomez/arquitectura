from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('menu_resid/', views.menu_resid, name='menu_resid'),
    path('agregar-residente/', views.agregar_residente, name='agregar_residente'),
    path('listar-residentes/', views.listar_residentes, name='listar_residentes'),
    path('eliminar-residente/<int:id>/', views.eliminar_residente, name='eliminar_residente'),
    path('editar-residente/<int:id>/', views.editar_residente, name='editar_residente'),
    path('registrar-pago/', views.registrar_pago, name='registrar_pago'),
    path('listar-pagos/', views.listar_pagos, name='listar_pagos'),
    path('recibo-pago/<int:id>/', views.recibo_pago, name='recibo_pago'),
    path('menu-pagos/', views.menu_pagos, name='menu_pagos'),
    path('procesar-pago/<int:pago_id>/', views.procesar_pago, name='procesar_pago'),
    path('menu-gestion/', views.menu_gest, name='menu_gest')
]
