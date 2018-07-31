from django.template.loader import get_template
from django.template import Context
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render_to_response
from django.http import HttpResponse
import datetime
from .models import Question


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
    return HttpResponse("You're voting on question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('polls/current_datetime.html', {'current_date': now})

def hours_ahead(request, hours):
    #hours = int(hours)
    dt = datetime.datetime.now() + datetime.timedelta(hours=hours)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (hours, dt)
    return HttpResponse(html)
