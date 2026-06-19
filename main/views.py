from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import *
from .models import *


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')


class UserLoginView(LoginView):
    template_name = 'login.html'


class UserLogoutView(LogoutView):
    next_page = 'login'


class DashboardView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'dashboard.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviewed_ids'] = list(
            Review.objects.filter(user=self.request.user)
            .values_list('application_id', flat=True)
        )
        return context


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
    if request.user.username != 'Admin26':
        return redirect('dashboard')

    applications = Application.objects.select_related('user').all()

    status_filter = request.GET.get('status', '')
    transport_filter = request.GET.get('transport', '')
    if status_filter:
        applications = applications.filter(status=status_filter)
    if transport_filter:
        applications = applications.filter(transport=transport_filter)

    sort = request.GET.get('sort', '-created_at')
    allowed_sorts = ['created_at', '-created_at', 'start_date', '-start_date', 'status']
    if sort in allowed_sorts:
        applications = applications.order_by(sort)

    notified = False
    if request.method == 'POST':
        app_id = request.POST.get('app_id')
        new_status = request.POST.get('status')
        app = get_object_or_404(Application, id=app_id)
        old_status = app.get_status_display()
        app.status = new_status
        app.save()
        notified = True
        return redirect(f'/admin-panel/?notified=1&msg=Статус+изменён:+{old_status}+→+{app.get_status_display()}')

    paginator = Paginator(applications, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')

    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'transport_filter': transport_filter,
        'sort': sort,
        'query_string': query_params.urlencode(),
        'notified': request.GET.get('notified') == '1',
        'message': request.GET.get('msg', ''),
    }
    return render(request, 'admin_panel.html', context)

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