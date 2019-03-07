from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from .models import Thread, Message
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy

# Create your views here.
@method_decorator(login_required, name='dispatch')
class ThreadList(TemplateView):
    template_name = 'messenger/thread_list.html'

    # # Filtrar un queryset por defecto
    # def get_queryset(self):
    #     queryset = super(ThreadList, self).get_queryset()
    #     # Filtrar el queryset por el usuario que esta identíficado en este momento
    #     return queryset.filter(users=self.request.user)

@method_decorator(login_required, name='dispatch')
class ThreadDetai(DetailView):
    model = Thread

    def get_object(self):
        obj = super(ThreadDetai, self).get_object()
        if self.request.user not in obj.users.all():
            raise Http404()
        return obj

def add_message(request, pk):
    json_response = {'created':False}
    if request.user.is_authenticated:
        content = request.GET.get('content', None)
        if content:
            thread = get_object_or_404(Thread, pk=pk)
            message = Message.objects.create(user=request.user, content=content)
            thread.messages.add(message)
            json_response['created'] = True
            if len(thread.messages.all()) is 1:
                json_response['first'] = True
    else:
        raise Http404("User is not authenticated")
    return JsonResponse(json_response)

@login_required # Cuando no es una vista de clase, se puede poner el decorador sin el método decorador
def start_thread(request, username):
    user = get_object_or_404(User, username=username)
    thread = Thread.objects.find_or_create(user, request.user)
    return redirect(reverse_lazy('messenger:detail', args=[thread.pk]))