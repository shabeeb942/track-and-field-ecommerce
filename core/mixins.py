from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import models as model_forms
from django.views.generic import DetailView
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin


def check_access(request, permissions):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user in permissions:
            return True
    return False



class CustomModelFormMixin:
    exclude = None

    # Rewriting get_form_class to support exclude attribute
    def get_form_class(self):
        model = getattr(self, "model", None)
        if self.exclude:
            exclude = getattr(self, "exclude", None)
            return model_forms.modelform_factory(model, exclude=exclude)
        return super().get_form_class()


class HybridDetailView( DetailView):
    pass


class HybridCreateView( CustomModelFormMixin, CreateView):
    def get_success_url(self):
        return self.object.get_list_url()

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class HybridUpdateView( CustomModelFormMixin, UpdateView):
    def get_success_url(self):
        return self.object.get_list_url()


class HybridDeleteView( DeleteView):
    template_name = "app/common/confirm_delete.html"

    def get_success_url(self):
        return self.object.get_list_url()


class HybridListView( ExportMixin, SingleTableMixin, FilterView, ListView):
    table_pagination = {"per_page": 50}

    def get_queryset(self):
        return super().get_queryset().all()


class HybridFormView( TemplateView):
    pass


class HybridTemplateView( TemplateView):
    template_name = "app/common/object_view.html"


class HybridView(View):
    pass


class OpenView(TemplateView):
    pass
