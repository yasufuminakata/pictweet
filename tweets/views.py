from django.shortcuts import render
from django.views.generic import ListView,CreateView,DeleteView,UpdateView,DetailView
from django.urls import reverse_lazy
from .models import Tweet
from .forms import TweetForm
from django.views.generic.edit import FormMixin
from comments.forms import CommentForm
from comments.models import Comment
from .forms import TweetForm, SearchForm

class IndexView(ListView, FormMixin):
    model = Tweet
    template_name = 'tweets/index.html'
    context_object_name = 'tweets'
    ordering = '-created_at'
    form_class = SearchForm

class CreateView(CreateView):
    form_class = TweetForm
    template_name = 'tweets/create.html'
    success_url = reverse_lazy("Tweets:index")

    def form_valid(self, form):
        tweet = form.save(commit=False)
        tweet.user = self.request.user
        tweet.save()
        return super().form_valid(form)

class DetailView(FormMixin,DetailView):
    model = Tweet
    success_url = reverse_lazy('Tweets:index')
    form_class = CommentForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(tweet=self.object)
        context['comments'] = comments
        context['form'] = self.get_form()
        return context

class UpdateView(UpdateView):
    model = Tweet
    form_class = TweetForm
    template_name = 'tweets/update.html'
    success_url = reverse_lazy('Tweets:index')
class DetailView(DetailView):
    model = Tweet
    template_name = 'tweets/detail.html'

def tweet_search(request):
    form = SearchForm(request.GET or None)
    if form.is_valid():
        keyword = form.cleaned_data.get('keyword', '')
        tweets = Tweet.objects.filter(text__icontains=keyword)
    else:
        tweets = Tweet.objects.all()
    return render(request, 'tweets/search.html', {'form': form, 'tweets': tweets})
