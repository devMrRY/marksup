from home.forms import *
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import *
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib import auth, messages
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.utils import translation

def login(request):
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['pas']
        try:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
            else:
                messages.error(request, 'username and password does not match')
        except ObjectDoesNotExist:
            messages.error(request, 'Invalid user')
    return HttpResponseRedirect(request.GET.get('next', '/'))

def signup(request):
    
    return SignUpForm()

def header(request):
    head = {}
    for cat in list(Category.objects.all()):
        head.update({cat.category:{}})
        for sub in list(cat.subcategory_set.filter(obj=cat).order_by('-postdate')):
            if sub.subcategory not in head[cat.category].keys():
                head[cat.category].update({sub.subcategory:[]})
            head[cat.category][sub.subcategory].append(sub.jobbycategory)
    
    login(request)
    head['form'] = signup(request)
    return head

def menu(request):
    head = header(request)
    context = {}
    obj = []
    jobs = {}
    admitcard = {}
    result = {}
    for cat in list(Category.objects.all()):
        context.update({cat.category:{}})
        for sub in list(cat.subcategory_set.filter(obj = cat)):
            obj.append(sub)
            if sub.subcategory not in context[cat.category].keys():
                context[cat.category].update({ sub.subcategory:[]})            
            context[cat.category][sub.subcategory].append(sub.jobbycategory)
            jobs[sub.pk] = sub.jobbycategory

            for admit in sub.admitcard_set.all():
                admitcard[admit.pk] = [admit.admitcard]
                admitcard[admit.pk].append(sub.jobbycategory)
            for res in sub.result_set.all():
                result[res.pk] = [res.result]
                result[res.pk].append(sub.jobbycategory)
    
    jobs = [value for(key, value) in sorted(jobs.items(), reverse=True)]
    admitcard = [value for(key, value) in sorted(admitcard.items(), reverse=True)]
    result = [value for(key, value) in sorted(result.items(), reverse=True)]
    
    return render(request, 'menu.html', {'context':context,
                                        'admitcard':admitcard,
                                        'result':result,
                                        'latestjobs':jobs,
                                        'head':head,
                                        })

def data(request, job_name):
    head = header(request)
    for j in Category.objects.all():
        for s in j.subcategory_set.filter(obj=j, jobbycategory=job_name):
            return render(request, 'data.html', {'obj':s,
                                               'head':head,})
            
def allcontent(request, allcontent_id):
    context=header(request)
    
    if allcontent_id == 'job': 
        head = 'Latest Jobs'
        jobs={}
        for j in Category.objects.all():
            for sub in j.subcategory_set.filter(obj=j):
                jobs[sub.pk]=[sub.jobbycategory]
                for date in sub.tarik_set.filter(allheading='Last date'):
                    jobs[sub.pk].append(date.alldates)  #date is also getting appended with job
                        
        content = [value for (key, value) in sorted(jobs.items(), reverse=True)]

    elif allcontent_id == 'admitcard':
        head ='AdmitCards'
        admitcard={}
        for j in Category.objects.all():
            for sub in j.subcategory_set.filter(obj=j):
                for admit in sub.admitcard_set.all():
                    admitcard[admit.pk]=[admit.admitcard]
                    admitcard[admit.pk].append(sub.jobbycategory)   #link is also getting appended with admitcard

        content = [value for (key, value) in sorted(admitcard.items(), reverse=True)]
    else: 
        head = 'Results'
        result={}
        for j in Category.objects.all():
            for sub in j.subcategory_set.filter(obj=j):
                for res in sub.result_set.all():
                    result[res.pk]=[res.result]
                    result[res.pk].append(sub.jobbycategory)    #link is also getting appended with result

        content = [value for (key, value) in sorted(result.items(), reverse=True)]
        
    return render(request, 'allcontent.html',{'content':content,
                                            'context':context,
                                            'head':head,
                                            })

def aboutus(request):
    head = header(request)
    return render(request, 'aboutus.html', {'head':head,})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.GET.get('next', '/'))
        
def search(request):
    if request.method == 'POST':
        data = request.POST['srh']
        if data:
            match=[]
            for cat in Category.objects.all():
                for sub in cat.subcategory_set.all():
                    if data.lower() in (sub.jobbycategory).lower():
                        match.append(sub.jobbycategory) 
            if match:
                return render(request, 'search.html', {'job':match,})
            else:
                return HttpResponse('no job found')
    
    return HttpResponseRedirect("/home/")
    
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'form updated successfully!')
            return redirect('home:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    content = {
        'u_form':u_form,
        'p_form':p_form,
    }
    return render(request, 'profile.html', {'content':content,})

def practice(request, practice_type, category_name, filterby):
    head=header(request)
    context=[]
    date=[]
    paper=[]
    for i in list(Category.objects.all()):
        context.append(i)
        if 'previous' in practice_type.lower():
            if i.category.lower() == category_name.lower():
                for j in i.subcategory_set.all():
                    if filterby == 'all':
                        for p in j.prevpaper_set.all():
                            date.append(p.paper_year)
                            paper.append(p)
                    if j.jobbycategory.lower() == filterby.lower():
                        for p in j.prevpaper_set.all():
                            date.append(p.paper_year)
                            paper.append(p)
        else:
            if i.category.lower() == category_name.lower():
                for j in i.subjectcategory_set.all():
                    if filterby == 'all':
                        for p in j.quiz_set.all():
                            date.append(p.quiz_created)
                            paper.append(p)
                    if j.subject.lower() == filterby.lower():
                        for p in j.quiz_set.all():
                            date.append(p.quiz_created)
                            paper.append(p)
        date = list(set(date))
        date.sort(reverse=True)

    return render(request, 'practice.html', {'head':head,
                                            'practice_type':practice_type.lower(),
                                            'category_name':category_name,
                                            'filterby':filterby,
                                            'date':date,
                                            'paper':paper,
                                            'context':context,
                                             })

def paper(request, practice_type, category_name, filterby, paper_name, time):
    
    if 'previous' in practice_type.lower() :
        for i in Category.objects.all():
            if (i.category).lower() == category_name.lower():
                for j in i.subcategory_set.all():
                    if (j.jobbycategory).lower() == filterby.lower():
                        for p in j.prevpaper_set.all():
                            if (p.paper_title).lower() == paper_name.lower() and str(p.paper_year) == str(time):
                                question = []
                                for q in p.prev_question_set.all():
                                    question.append(q)
                                return render(request, 'paper.html', {
                                                                    'context':p,
                                                                    'practice_type':practice_type,
                                                                    'category_name':category_name,
                                                                    'filterby':filterby,
                                                                    'paper_name':paper_name,
                                                                    'paper_year':time,
                                                                    'question':question,
                                                                    })
    
            
        
    if 'model' in practice_type.lower():
        for i in Category.objects.all():
            if (i.category).lower() == category_name.lower():
                for j in i.subjectcategory_set.all():
                    if (j.subject).lower() == filterby.lower():
                        for p in j.quiz_set.all():
                            if (p.quiz_title).lower() == paper_name.lower() and str(p.quiz_time) == str(time):
                                question = []
                                for q in p.quiz_question_set.all():
                                    question.append(q)
                                return render(request, 'paper.html', {
                                                                    'context':p,
                                                                    'practice_type':practice_type,
                                                                    'category_name':category_name,
                                                                    'filterby':filterby,
                                                                    'paper_name':paper_name,
                                                                    'paper_year':time,
                                                                    'question':question,
                                                                    })
    
    return HttpResponse("can't load")

def result(request, practice_type, category_name, filterby, paper_name, time):
    correct = 0
    incorrect = 0
    unattempted = 0
    if 'previous' in practice_type.lower() :
        for i in Category.objects.all():
            if (i.category).lower() == category_name.lower():
                for j in i.subcategory_set.all():
                    if (j.jobbycategory).lower() == filterby.lower():
                        for p in j.prevpaper_set.all():
                            if (p.paper_title).lower() == paper_name.lower() and str(p.paper_year) == str(time):
                                total_ques = p.total_question
                                for ques in p.prev_question_set.all():
                                    user_option = request.POST.get(str(ques.question_no))
                                    if user_option == None:
                                        unattempted+=1
                                    elif user_option == ques.correct_answer:
                                        correct+=1
                                    else:
                                        incorrect+=1


    if 'model' in practice_type.lower() :
        for i in Category.objects.all():
            if (i.category).lower() == category_name.lower():
                for j in i.subjectcategory_set.all():
                    if (j.subject).lower() == filterby.lower():
                        for p in j.quiz_set.all():
                            if (p.quiz_title).lower() == paper_name.lower() and str(p.quiz_time) == str(time):
                                total_ques = p.total_question
                                for ques in p.quiz_question_set.all():
                                    user_option = request.POST.get(str(ques.question_no))
                                    if user_option == None:
                                        unattempted+=1
                                    elif user_option == ques.correct_answer:
                                        correct+=1
                                    else:
                                        incorrect+=1

    return render(request, 'result.html', {'total_ques':total_ques,
                                            'correct':correct,
                                            'wrong':incorrect,
                                            'unattempted':unattempted,
                                            })

def contactus(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        name += str(email)
        name += str(message)

        send_mail('contact form',
                name,
                settings.EMAIL_HOST_USER,
                ['reticentrahul@gmail.com'],
                fail_silently=False)

    return render(request, 'contactus.html')
