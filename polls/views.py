from django.template.loader import get_template
from django.template import Context
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import datetime
from .models import Question
from django.db.models import F


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# Create your views here.
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    template = 'polls/detail.html'
    return render(request, template ,context)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        #Using F() to avoid race condition!!!
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('polls/current_datetime.html', {'current_date': now})


def hours_ahead(request, hours):
    dt = datetime.datetime.now() + datetime.timedelta(hours=hours)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (hours, dt)
    return HttpResponse(html)
