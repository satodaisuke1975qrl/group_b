from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from .forms import CommentCreateForm, CommentUpdateForm


# # Create your views here.
#
#
class Home(generic.TemplateView):
    template_name = 'tvasahi/home.html'
#
#
#
# class TvListView(generic.ListView):
#
#
# class TvDetailView(generic.DetailView):
#
#
# class CommentCreateView(generic.CreateView):
#
#
# class CommentListView(generic.ListView):
#
#
# class CommentUpdateView(generic.UpdateView):
#
#
# class CommentDeleteView(generic.DeleteView):
#
