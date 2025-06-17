from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from flask import redirect

from base.models import Tarea
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class Logueo(LoginView):
    template_name = "base/login.html"
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('pendientes')


class PaginaRegistro(FormView):
    template_name = "base/registro.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('pendientes')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(PaginaRegistro, self).form_valid(form)

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect("pendientes")
        return super(PaginaRegistro, self).get(*args,**kwargs)


class ListaPendientes(LoginRequiredMixin, ListView):
    model = Tarea
    context_object_name = 'tareas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tareas"] = context["tareas"].filter(usuario=self.request.user)
        context["count"] = context["tareas"].filter(completo=False).count()

        valor_buscado = self.request.GET.get("area-buscar") or ""
        if valor_buscado:
            context["tareas"] = context["tareas"].filter(titulo__icontains=valor_buscado)
        context["valor_buscado"] = valor_buscado
        return context


class DetalleTarea(LoginRequiredMixin, DetailView):
    model = Tarea
    context_object_name = 'tarea'


class CrearTarea(LoginRequiredMixin, CreateView):
    model = Tarea
    fields = ["titulo", "descripcion", "completo"]
    success_url = reverse_lazy('pendientes')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(CrearTarea, self).form_valid(form)

class UpdateTarea(LoginRequiredMixin, UpdateView):
    model = Tarea
    fields = '__all__'
    success_url = reverse_lazy('pendientes')

class DeleteTarea(LoginRequiredMixin, DeleteView):
    model = Tarea
    context_object_name = 'tareas'
    success_url = reverse_lazy('pendientes')