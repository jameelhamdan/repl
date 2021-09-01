from django.urls import path, reverse_lazy
from django.views import generic
from . import models


class IndexView(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        instance = models.Instance()
        instance.save()
        return reverse_lazy('core:detail', kwargs={'pk': instance.pk})


class DetailView(generic.DetailView):
    template_name = 'detail.html'
    queryset = models.Instance.objects.all()


app_name = 'core'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<str:pk>/', DetailView.as_view(), name='detail'),
]
