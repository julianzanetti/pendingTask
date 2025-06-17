from django.urls import path
from .views import ListaPendientes, DetalleTarea, CrearTarea, UpdateTarea, DeleteTarea, Logueo, PaginaRegistro
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", ListaPendientes.as_view(), name="pendientes"),
    path("crear-tarea/", CrearTarea.as_view(), name="crear-tarea"),
    path("editar-tarea/<int:pk>", UpdateTarea.as_view(), name="editar-tarea"),
    path("eliminar-tarea/<int:pk>", DeleteTarea.as_view(), name="eliminar-tarea"),
    path("login/", Logueo.as_view(), name="login"),
    path("registro/", PaginaRegistro.as_view(), name="registro"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
]