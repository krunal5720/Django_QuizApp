import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Poll, Choice, Vote, Result


@login_required()
def polls_list(request):
    Q_no = []
    all_polls = []
    p_q = Poll.objects.all()
    for no in range(5):
        rand_num = random.randint(0,19)
        Q_no.append(rand_num)
    for i in range(len(Q_no)):
        all_polls.append(p_q[i])
    paginator = Paginator(all_polls, 5)  # Show 6 contacts per page
    page = request.GET.get('page')
    polls = paginator.get_page(page)
    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
    print(params)

    context = {
        'polls': polls,
        'params': params,
    }
    return render(request, 'polls/polls_list.html', context)


def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if not poll.active:
        return render(request, 'polls/poll_result.html', {'poll': poll})
    loop_count = poll.choice_set.count()
    context = {
        'poll': poll,
        'loop_time': range(0, loop_count),
    }
    return render(request, 'polls/poll_detail.html', context)


@login_required
def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choice_id = request.POST.get('choice')
    if not poll.user_can_vote(request.user):
        messages.error(
            request, "You already voted this poll!", extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect("polls:list")
    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        user_result = False

        if choice.poll_result == True:
            user_result = True
        vote = Vote(user=request.user, poll=poll, choice=choice,user_result = user_result)
        vote.save()
        return redirect("polls:list")
    else:
        messages.error(
            request, "No choice selected!", extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect("polls:detail", poll_id)
    return render(request, 'polls/poll_detail.html', {'poll': poll + 1})


def poll_result(request):
    count = 0
    all_votes = Vote.objects.filter(user = request.user)
    for i in all_votes:
        if i.user_result == True:
            count +=1
    percentage = count / 5 * 100
    result = Result(user=request.user,count=count,percentage = percentage)
    result.save()
    if count == 0 or count == 1 or count == 2:
        messages.error(
            request, "Please try again! You are not passed this exam", extra_tags='alert alert-danger alert-dismissible fade show')
    elif count == 3:
        messages.success(request,"Good job!",extra_tags='alert alert-success alert-dismissible fade show')
    elif count == 4:
        messages.success(request, "Excellent work!", extra_tags='alert alert-success alert-dismissible fade show')
    elif count ==5:
        messages.success(request, "You are a genius!", extra_tags='alert alert-success alert-dismissible fade show')
    context = {
        'votes': all_votes,
        'percentage':percentage,
        'count':count,
    }
    return render(request, 'polls/poll_result.html', context)


@login_required
def end_poll(request):
    all_votes = Vote.objects.filter(user = request.user)
    all_votes.delete()
    return redirect("polls:list")

def quiz_history(request):
    percentage=[]
    all_results = Result.objects.all()
    for i in all_results:
        percentage.append(i.percentage)
    maximum_percentage = max(percentage)
    minimum_percentage = min(percentage)
    average_percentage =sum(percentage)/len(percentage)
    context = {
        'result':all_results,
        'maximum_percentage':maximum_percentage,
        'minimum_percentage':minimum_percentage,
        'average_percentage':average_percentage,
    }
    return render(request, 'polls/quiz_history.html', context)

