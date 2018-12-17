from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.views import View
from .forms import ChoicesForm
from django.db import IntegrityError, transaction

import logging

logger = logging.getLogger(__name__)

from .models import Question, Choice, Person, Task

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    form = ChoicesForm(initial={
        'pk':question_id
    })
    
    choices = question.choice_set.all
    question_id = question.id
    question_text = question.question_text

    return render(request, 'polls/detail.html', {
        'question_id': question_id,
        'choices':choices,
        'question_text':question_text,
        'title': "Detail",
        'form':form,
    })

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    context_object_name = 'question'
        
    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)
        context['choices'] = context['question'].choice_set.all
        context['question_text'] = context['question'].question_text
        context['question_id'] = context['question'].id
        return context

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all
    question_id = question.id
    form = ChoicesForm(data=request.POST,initial={'pk':question_id})

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        messages.add_message(request, messages.ERROR, "You didn't select a choice.", "alert alert-danger")
        return render(request, 'polls/detail.html', {
            'question': question,
            'question_id': question_id,
            'choices':choices,
            'title':'Vote result',
            'form':form
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

class TestFormView(View):
    model = Question
    context_object_name = 'question'
    form_class = ChoicesForm
    template_name = 'polls/testForm.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={
            'pk':kwargs['pk']
        })

        return render(request, self.template_name, {'form': form, 'question_id':kwargs['pk']})

    def post(self, request, *args, **kwargs):

        form = ChoicesForm(data=request.POST,initial={'pk':kwargs['pk']})

        if form.is_valid():
            if request.POST.get('choice') != None:
                choice = get_object_or_404(Choice, pk=request.POST.get('choice'))
                choice.votes += 1
                choice.save()

                return HttpResponseRedirect(reverse('polls:results', args=(kwargs['pk'],)))
            messages.add_message(request, messages.ERROR, "You didn't select a choice.", "alert alert-danger")

        return render(request, self.template_name, {'form': form})

@transaction.atomic
def createPerson(request):

    try:
        with transaction.atomic():
            person = Person.objects.create(name="Person8")
            task = Task.objects.create(title="Task6",person=person)
    except IntegrityError:
        messages.add_message(request, messages.ERROR, "Smth went wrong, obcjet was not crated", "alert alert-danger")
        return HttpResponseRedirect(reverse('polls:index'))

    messages.add_message(request, messages.ERROR, "You created an object", "alert alert-info")

    return HttpResponseRedirect(reverse('polls:index'))