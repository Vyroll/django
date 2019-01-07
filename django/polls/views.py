from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.views import View
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required, permission_required

from .forms import ChoicesForm
from .models import Question, Choice

import logging
logger = logging.getLogger(__name__)

def CreateGroupPermissions(request):
    premium, created = Group.objects.get_or_create(name='premium')
    content_type = ContentType.objects.get_for_model(Question)
    permission = Permission.objects.create(codename='can_premium',
                                    name='can perform premium actions',
                                    content_type=content_type)
    premium.permissions.add(permission)

    messages.add_message(request, messages.SUCCESS, "Created group and added permision!", "alert alert-success")
    return HttpResponseRedirect(reverse('polls:index'))

def RegisterView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # create user
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=raw_password)

            # add permisons
            content_type = ContentType.objects.get_for_model(Question)
            permission = Permission.objects.get(
                codename='view_question',
                content_type=content_type,
            )
            user.user_permissions.add(permission)

            # redirect
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "You have successfully created your account!", "alert alert-success")
                messages.add_message(request, messages.SUCCESS, "You have successfully loged in!", "alert alert-success")
            else:
                messages.add_message(request, messages.ERROR, "Somethink went wrong, your account wasn't created.", "alert alert-danger")

            return HttpResponseRedirect(reverse('polls:index'))
    else:
        form = UserCreationForm()
    return render(request, 'polls/register.html', {'form': form})

def logoutView(request):
    messages.add_message(request, messages.SUCCESS, "You have successfully loged out!", "alert alert-success")
    logout(request)
    return HttpResponseRedirect(reverse('polls:index'))

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

# @login_required(login_url='/polls/accounts/login')
@permission_required('polls.view_question', login_url='/polls/accounts/login')
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

        form = self.form_class(data=request.POST,initial={'pk':kwargs['pk']})

        if form.is_valid():
            if request.POST.get('choice') != None:
                choice = get_object_or_404(Choice, pk=request.POST.get('choice'))
                choice.votes += 1
                choice.save()

                return HttpResponseRedirect(reverse('polls:results', args=(kwargs['pk'],)))
            messages.add_message(request, messages.ERROR, "You didn't select a choice.", "alert alert-danger")

        return render(request, self.template_name, {'form': form})