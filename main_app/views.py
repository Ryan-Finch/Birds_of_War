from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Finch
from .forms import SightingForm
# Create your views here.

class FinchCreate(CreateView):
    model = Finch
    fields = '__all__'

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

def home(request):
    return HttpResponse('<h1>Hello Finch People</h1>')

def about(request):
   return render(request, 'about.html')

def finches_index(request):
    finches = Finch.objects.all()
    return render(request, 'finches/index.html', {'finches': finches})

def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    sighting_form = SightingForm() 

    return render(request, 'finches/detail.html', {
        'finch': finch,
        'sighting_form': sighting_form
        })