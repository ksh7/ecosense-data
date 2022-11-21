from datetime import datetime
import os
import json
import random
import string

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from wsgiref.util import FileWrapper
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


from .models import Dataset, DataSource, CustomDataAPI, User, ResearchInsight
from . import forms
from .dataexchange import get_aws_dataset


class ResearchInsightDetailView(UserPassesTestMixin, DetailView):
    model = ResearchInsight
    slug_field = 'id'
    slug_url_kwarg = 'id'
    template_name = 'ecosense_app/research_detail.html'
    
    def test_func(self, *args, **kwargs):
        obj = super(ResearchInsightDetailView, self).get_object(*args, **kwargs)
        if self.request.user.id != obj.user.id:
            if not obj.is_public:
                return False
        return True

    def handle_no_permission(self):
        messages.info(self.request, 'Oops! This insight is not available publically!')
        return redirect('index')


class ResearchInsightListView(LoginRequiredMixin, ListView):
    template_name = 'ecosense_app/research_list.html'

    def get_queryset(self):
        return ResearchInsight.objects.filter(user__id=self.request.user.id).order_by('-updated_at')

class ResearchInsightAddView(LoginRequiredMixin, CreateView):
    model = ResearchInsight
    form_class = forms.ResearchAddForm
    slug_field = 'id'
    slug_url_kwarg = 'id'
    template_name = 'ecosense_app/research_add.html'

    def get_success_url(self):
        return reverse('my-insights')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class ResearchInsightEditView(LoginRequiredMixin, UpdateView):
    model = ResearchInsight
    form_class = forms.ResearchAddForm
    slug_field = 'id'
    slug_url_kwarg = 'id'
    template_name = 'ecosense_app/research_edit.html'

    def get_success_url(self):
        return reverse('my-insights')

    def get_queryset(self):
        return ResearchInsight.objects.filter(id=int(self.kwargs['id']))


def index(request):
    datasets = Dataset.objects.all()
    context = {'datasets': datasets}
    return render(request, 'ecosense_app/index.html', context)


def data(request, slug):
    dataset = Dataset.objects.filter(slug=slug).first()
    if not dataset:
        return redirect('index')

    context = {
        'dataset': dataset,
        'form': forms.DataSourceForm()
    }
    return render(request, 'ecosense_app/data.html', context)


def api(request, slug):
    dataset = Dataset.objects.filter(slug=slug).first()
    if not dataset:
        return JsonResponse({'success': False, 'dataset': slug, 'data': None})
    
    data = get_aws_dataset(dataset.data_sources.all(), 'REARC')
    
    return JsonResponse({'success': True, 'dataset': slug, 'data': data})


def api_custom_data(request, url):
    api = CustomDataAPI.objects.get(url=url)
    if not api:
        return JsonResponse({'success': False, 'dataset': 'invalid api', 'data': None})

    source_ids = [int(i) for i in api.topics.lstrip('[').rstrip(']').split(',')]
    if not source_ids:
        return JsonResponse({'success': False, 'dataset': 'invalid api', 'data': None})
    
    data = get_aws_dataset(DataSource.objects.filter(pk__in=source_ids), 'REARC')

    return JsonResponse({'success': True, 'dataset': api.name, 'data': data})


def api_custom(request):
    requested_ids = []

    if request.method == "POST":
        slug = request.POST.get("dataset_name")
        datasource_ids = [int(i) for i in request.POST.getlist("datasource_ids")]
        if slug and datasource_ids:
            dataset = Dataset.objects.filter(slug=slug).first()
            if not dataset:
                return JsonResponse({'success': False, 'dataset': slug, 'data': None})
            
            for source in dataset.data_sources.all():
                if source.id in datasource_ids:
                    requested_ids.append(source.id)
    
    if not requested_ids:
        return JsonResponse({'success': False, 'dataset': '', 'data': None})

    requested_ids.sort()
    
    api = CustomDataAPI.objects.filter(topics=str(requested_ids)).first()
    if not api:
        api = CustomDataAPI.objects.create(name=slug, url=''.join(random.choices(string.ascii_lowercase + string.digits, k=20)), topics=str(requested_ids))
        api.save()
    
    return redirect('api_custom_data', url=api.url)


def json_file(request, slug):
    dataset = Dataset.objects.filter(slug=slug).first()
    if not dataset:
        return JsonResponse({'success': False, 'dataset': slug, 'data': 'Invalid dataset request'})

    data = get_aws_dataset(dataset.data_sources.all(), 'REARC')
    json_obj = json.dumps({'success': True, 'dataset': slug, 'data': data}, indent=2)

    file_path = "/tmp/" + slug + "dataset-by-ecosense-" + datetime.now().strftime("%d-%m-%Y") + ".json"
    filename = os.path.basename(file_path)
    with open(file_path, "w+") as f:
        f.write(json_obj)

    chunk_size = 8192
    response = StreamingHttpResponse(
        FileWrapper(open(file_path, 'rb'), chunk_size),
        content_type="application/octet-stream"
    )
    response['Content-Length'] = os.path.getsize(file_path)    
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def registerUser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        organization = request.POST.get('organization')
        bio = request.POST.get('bio')

        user_exists = User.objects.filter(email=email).first()
        if user_exists:
            messages.info(request, 'Account exists with this email. Please login')
            return redirect('login')

        new_user = User.objects.create(email=email, password=make_password(password),
                                       first_name=first_name, last_name=last_name,
                                       organization=organization, bio=bio)
        new_user.save()
        messages.info(request, 'Account created successfully. Please login')
        return redirect('login')

    return render(request, 'ecosense_app/register.html')

def loginUser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            _next = request.GET.get('next', None)
            if _next:
                return redirect(_next)
            return redirect('index')
        else:
            messages.info(request, 'Email OR password is incorrect')

    context = {}

    return render(request, 'ecosense_app/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('index')