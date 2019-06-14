from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Question, Choice

# Create your views here.
def main_index(request):
    return render(request, 'main_index.html')

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     return render(request, 'polls/index.html', {'latest_question_list': latest_question_list})
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choice_num = request.POST.get('choice', None)
    if choice_num is None:
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You did not select a choice.",
        })
    else:
        selected_choice = question.choice_set.get(pk=choice_num)
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:result', args=(question_id,)))
