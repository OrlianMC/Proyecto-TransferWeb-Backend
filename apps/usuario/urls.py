from django.urls import path, include
from apps.usuario.views import usuarios_registrar, usuarios_modificar, cargar_usuario_formulario, login_user, logout_user, usuarios_eliminar
# from transfermovil_app.api.login import buscar_usuario

urlpatterns = [
    path('registrar/', usuarios_registrar, name='usuarios-registrar'),
    path('eliminar/', usuarios_eliminar, name='usuarios-eliminar'),
    path('modificar/', usuarios_modificar, name='usuarios-modificar'),
    path('modForm/', cargar_usuario_formulario, name='cargar-usuario-formulario'), #Devuelve datos de usuario para llenar formulario de modificar
    path('login/', login_user, name='login-user'),#Login
    path('logout/', logout_user, name='logout-user'),#Logout
]

#http://127.0.0.1:8000/usuario/login/