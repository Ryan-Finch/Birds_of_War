from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Finch, Armor, Photo
from .forms import SightingForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required 
import uuid
import boto3
# Create your views here.

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'catcollector02'

class FinchCreate(CreateView):
    model = Finch
    fields = ['name', 'species', 'description', 'age']

    def form_valid(self, form):
        form.instance.user= self.request.user
        return super().form_valid(form)

class FinchUpdate(UpdateView):
    model = Finch
    fields = ['species','description','age']

class FinchDelete(DeleteView):
    model = Finch
    success_url = '/finches/'

def add_sighting(request, finch_id):
    form = SightingForm(request.POST)
    if form.is_valid():
        new_sighting = form.save(commit=False)
        new_sighting.finch_id = finch_id
        new_sighting.save()
    return redirect('detail', finch_id=finch_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - Please try again'
    form = UserCreationForm()
    context= {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def add_photo(request, finch_id):
    photo_file = request.FILES.get('photo_file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]

        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url= f'{S3_BASE_URL}{BUCKET}/{key}'
            photo = Photo(url=url, finch_id=finch_id)
            photo.save()
        except:
            print('An error occured uploading file to S3')
    return redirect('detail', finch_id=finch_id)

def home(request):
    return render(request, 'home.html')

def about(request):
   return render(request, 'about.html')

def finches_index(request):
    finches = Finch.objects.filter(user=request.user)
    return render(request, 'finches/index.html', {'finches': finches})

def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    sighting_form = SightingForm() 
    armor_finch_doesnt_have = Armor.objects.exclude(id__in = finch.armor.all().values_list('id'))
    return render(request, 'finches/detail.html', {
        'finch': finch,
        'sighting_form': sighting_form,
        'armor': armor_finch_doesnt_have,
        })
def assoc_armor(request, finch_id, armor_id):
    Finch.objects.get(id=finch_id).armor.add(armor_id)
    return redirect('detail', finch_id=finch_id)
# Class for Armor

class ArmorCreate(CreateView):
    model = Armor
    fields = '__all__'

class ArmorList(ListView):
    model = Armor
    

class ArmorDetail(DetailView):
    model = Armor

class ArmorUpdate(UpdateView):
    model = Armor
    fields = ['style', 'material']

class ArmorDelete(DeleteView):
    model = Armor
    success_url = '/armor/'