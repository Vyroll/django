# from django.http import HttpResponseRedirect
# from django.shortcuts import get_object_or_404, render
# from django.urls import reverse
from django.http import HttpResponse
from django.views import generic
from .models import Departure

class ScheduleList(generic.ListView):
    model = Departure
    context_object_name = 'schdule_list'
    template_name='schedule/index.html'

class LandingView(generic.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')