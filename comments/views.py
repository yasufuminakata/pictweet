from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.edit import CreateView
from .models import Comment
from .forms import CommentForm
from tweets.models import Tweet

class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        tweet_id = self.kwargs['pk']
        tweet = get_object_or_404(Tweet, pk=tweet_id)
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.tweet = tweet
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('Tweets:detail', kwargs={'pk': self.kwargs['pk']})