from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

import logging

logger = logging.getLogger(__name__)

from .models import Question, Choice

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

    choices = question.choice_set.all
    question_id = question.id
    question_text = question.question_text

    return render(request, 'polls/detail.html', {
        'question_id': question_id,
        'choices':choices,
        'question_text':question_text,
        'title': "Detail",
    })

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    context_object_name = 'question'
        
    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)
        context['choices'] = context['question'].choice_set.all
        context['question_text'] = context['question'].question_text
        return context

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all
    question_id = question.id

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        messages.error(request, 'You didn\'t select a choice.')
        return render(request, 'polls/detail.html', {
            'question': question,
            'question_id': question_id,
            'choices':choices,
            'title':'Vote result'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))