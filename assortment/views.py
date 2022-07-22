from django.forms import ModelChoiceField
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

LoginRequiredMixin.login_url = '/login/'


class IndexPageView(generic.TemplateView):
    template_name = 'assortment/index.html'


def mock(request):
    return HttpResponse("Just empty page. Fuck off!")


class AboutMotoView(LoginRequiredMixin, generic.DetailView):
    model = Motorcycle
    template_name = 'assortment/about_motorcycle.html'


class MotorcyclesListView(LoginRequiredMixin, generic.ListView):
    template_name = 'assortment/motorcycle_list.html'
    context_object_name = 'motorcycle_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return Motorcycle.objects.all()
            return Motorcycle.objects.all().order_by('-pub_date').filter(show_to__in=[self.request.user])
        return None


class LoginView(auth_views.LoginView):
    template_name = 'assortment/login.html'


class LogoutView(auth_views.LogoutView):
    template_name = 'assortment/logout.html'


class AddMotorcycleView(LoginRequiredMixin, generic.CreateView):
    model = Motorcycle
    template_name = 'assortment/add_motorcycle.html'
    fields = ['name', 'year', 'description', 'photo', 'show_to', 'price', 'model']

    def form_valid(self, form):
        form.instance.pub_user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('motorcycles_list')


class EditMotorcycleView(LoginRequiredMixin, generic.UpdateView):
    model = Motorcycle
    template_name = 'assortment/add_motorcycle.html'  # TODO: переписать на изменение мотоцикла
    fields = ['name', 'year', 'description', 'photo', 'show_to', 'price', 'model']

    def dispatch(self, request, *args, **kwargs):
        if request.user != Motorcycle.objects.get(pk=kwargs['pk']).pub_user and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('motorcycles_list'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("about_moto", kwargs={'pk': self.kwargs['pk']})


class DeleteMotorcycleView(LoginRequiredMixin, generic.DeleteView):
    model = Motorcycle
    template_name = 'assortment/delete_confirm.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user != Motorcycle.objects.get(pk=kwargs['pk']).pub_user and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('motorcycles_list'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('motorcycles_list')


class AddUserView(LoginRequiredMixin, generic.CreateView):
    model = User
    template_name = 'assortment/add_user.html'
    fields = ['username', 'password', 'email', 'first_name', 'last_name', 'is_staff']

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('index'))

    def get_success_url(self):
        return reverse('motorcycles_list')  # TODO: добавить проверку формы на валидность


class AddFeatureView(LoginRequiredMixin, generic.CreateView):
    model = MotorcycleFeature
    template_name = 'assortment/add_feature.html'
    fields = ['photo', 'description']

    def dispatch(self, request, *args, **kwargs):
        if request.user != Motorcycle.objects.get(pk=kwargs['pk']).pub_user and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('motorcycles_list'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.motorcycle = Motorcycle.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("about_moto", kwargs={'pk': self.kwargs['pk']})


class RemoveFeatureView(LoginRequiredMixin, generic.DeleteView):
    model = MotorcycleFeature
    template_name = 'assortment/delete_confirm.html'
    motorcycle = None

    def dispatch(self, request, *args, **kwargs):
        self.motorcycle = MotorcycleFeature.objects.get(pk=kwargs['pk']).motorcycle
        if request.user != MotorcycleFeature.objects.get(
                pk=kwargs['pk']).motorcycle.pub_user and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('motorcycles_list'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("about_moto", kwargs={'pk': self.motorcycle.pk})


class AddManufacturerView(LoginRequiredMixin, generic.CreateView):
    model = Manufacturer
    template_name = 'assortment/add_manufacturer.html'
    fields = ['name']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('motorcycles_list'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('motorcycles_list')


class AddModelView(LoginRequiredMixin, generic.CreateView):
    model = Model
    template_name = 'assortment/add_model.html'
    fields = ['manufacturer', 'name']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('motorcycles_list'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('motorcycles_list')



