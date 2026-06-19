from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *


class RegisterView(CreateView):
    """Регистрация нового пользователя"""
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')


class UserLoginView(LoginView):
    """Вход в систему"""
    template_name = 'login.html'


class UserLogoutView(LogoutView):
    """Выход из системы"""
    next_page = 'login'


class DashboardView(LoginRequiredMixin, ListView):
    """Личный кабинет — история заявок"""
    model = Application
    template_name = 'dashboard.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)


class ApplicationCreateView(LoginRequiredMixin, CreateView):
    """Создание заявки"""
    model = Application
    form_class = ApplicationForm
    template_name = 'application.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def admin_panel(request):
    """Панель администратора (только для Admin26)"""
    if request.user.username != 'Admin26':
        return redirect('dashboard')

    applications = Application.objects.all()

    if request.method == 'POST':
        app_id = request.POST.get('app_id')
        new_status = request.POST.get('status')
        app = get_object_or_404(Application, id=app_id)
        app.status = new_status
        app.save()
        return redirect('admin_panel')

    return render(request, 'admin_panel.html', {'applications': applications})

@login_required
def add_review(request, app_id):

    app = get_object_or_404(Application, id=app_id, user=request.user)

    if app.status == 'new':
        return redirect('dashboard')

    if Review.objects.filter(application=app, user=request.user).exists():
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.application = app
            review.save()
            return redirect('dashboard')
    else:
        form = ReviewForm()
    
    return render(request, 'review.html', {'form': form, 'app': app})