from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login,get_user_model
from .forms import CustomUserCreationForm
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from tweets.models import Tweet

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('Tweets:index')  # 登録完了後にリダイレクトするURL
    template_name = 'users/sign_up.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response

class UserPageView(ListView):
    model = Tweet
    template_name = 'users/mypage.html'
    context_object_name = 'tweets'

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        self.user = get_object_or_404(get_user_model(), pk=user_id)
        return Tweet.objects.filter(user=self.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = self.user
        return context