from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from .forms import CommentCreateForm, CommentUpdateForm
from .models import Tv


# # Create your views here.
#
#
class Home(generic.TemplateView):
    template_name = 'tvasahi/home.html'


class TvListView(generic.ListView):
    model = Tv
    template_name = 'tvasahi/tv_list.html'
    

"""
    
class TvDetailView(generic.DetailView):


class CommentCreateView(generic.CreateView):


class CommentListView(generic.ListView):


class CommentUpdateView(generic.UpdateView):


class CommentDeleteView(generic.DeleteView):

"""