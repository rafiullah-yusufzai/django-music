from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import FormView, TemplateView, UpdateView
from django.urls import reverse_lazy

from django_music.forms import LoginForm, ProfileForm
from django_music.models import Song, User

class HomeView(FormView):
    template_name = "home.html"
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("profile")
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs
    
    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect("profile")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["top_songs"] = (
            Song.objects.annotate(fan_count=Count("fans"))
            .select_related("album", "album__artist")
            .order_by("-fan_count")[:5]
        )
        query = self.request.GET.get("q", "").strip()
        ctx["query"] = query
        if query:
            ctx["search_results"] = (
                User.objects.filter(display_name__icontains=query)
                .exclude(is_superuser=True)
                .select_related("favorite_song", "favorite_song__album__artist")
            )
        else:
            ctx["search_results"] = None
        return ctx
    


class PublicProfileView(TemplateView):
    template_name = "public_profile.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        profile_user = get_object_or_404(
            User.objects.select_related(
                "favorite_song",
                "favorite_song__album",
                "favorite_song__album__artist",
            ),
            slug=kwargs["slug"],
        )
        ctx["profile_user"] = profile_user
        return ctx
    

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "profile.html"
    success_url = reverse_lazy("profile")
    login_url = "/"

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save(commit=False)
        old_song_id = User.objects.filter(pk=user.pk).values_list("favorite_song_id", flat=True).first()
        if user.favorite_song_id != old_song_id:
            user.favorite_song_since = timezone.now() if user.favorite_song else None
        user.save()
        messages.success(self.request, "Your profile has been updated.")
        return redirect("profile")
    

def logout_view(request):
    logout(request)
    return redirect("home")