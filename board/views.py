from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Ad, Response
from .forms import AdForm, ResponseForm
from datetime import datetime


class AdsList(ListView):
    """ Представление списка объявлений. """
    model = Ad
    ordering = 'dateCreation'
    template_name = 'flatpages/ads_list.html'
    context_object_name = 'ads'
    paginate_by = 3
    media = 'uploads'

    def image_update(request):
        if request.method == 'POST':
            form = AdForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                img_obj = form.instance
                return render(request, 'ad.html', {'form': form, 'img_obj': img_obj})
        else:
            form = AdForm()
        return render(request, 'ad.html', {'form': form})


class AdDetail(DetailView):
    """ Представление отдельного объявления. """
    model = Ad
    template_name = 'flatpages/ad.html'
    context_object_name = 'ad'
    media = 'uploads'


class AdCreate(LoginRequiredMixin, CreateView):
    """ Представление создания нового объявления. """
    permission_required = ('board.add_ad',)
    raise_exception = True
    form_class = AdForm
    model = Ad
    template_name = 'flatpages/ad_create.html'
    media = 'uploads'

    def form_valid(self, form):
        ad = form.save(commit=False)
        ad.author = self.request.user
        ad.save()
        return super().form_valid(form)


class AdEdit(LoginRequiredMixin, UpdateView):
    """ Представление редактирования объявления. """
    permission_required = ('board_add_ad',)
    raise_exception = True
    form_class = AdForm
    model = Ad
    template_name = 'flatpages/ad_update.html'
    success_url = reverse_lazy('ads_list')
    media = 'uploads'


class AdDelete(LoginRequiredMixin, DeleteView):
    """ Представление удаления объявления. """
    permission_required = ('ad.delete_ad',)
    raise_exception = True
    model = Ad
    template_name = 'flatpages/ad_delete.html'
    success_url = reverse_lazy('ads_list')
    media = 'uploads'


class AdResponse(LoginRequiredMixin, CreateView):
    """ Представление создания отклика. """
    permission_required = ('board.response',)
    form_class = ResponseForm
    model = Response
    template_name = 'flatpages/response.html'
    raise_exception = True
    success_url = reverse_lazy('ads_list')

    def form_valid(self, form):
        response = form.save(commit=False)
        response.sender = self.request.user
        ad_id = self.kwargs['ad_id']
        response.ad = Ad.objects.get(pk=ad_id)
        response.save()
        send_mail(
            subject='Ваше сообщение вызвало отклик',
            message=f'Здравствуйте "{response.ad.author.username}".\n\n На ваше объявление: "{response.ad.title}" получен отклик от "{response.sender.username}"',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[response.ad.author.email],
        )
        return super().form_valid(form)


class MyResponse(LoginRequiredMixin, ListView):
    raise_exception = True
    model = Response
    template_name = 'flatpages/my_responses.html'
    context_object_name = 'responses'

    def get_queryset(self):
        queryset = super().get_queryset()
        return Response.objects.filter(ad__author=self.request.user)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


def my_responses(request):
    user = request.user
    if request.method == 'POST':
        if 'accept_response' in request.POST:
                response_id = request.POST.get('accept_response')
                response = Response.objects.get(pk=response_id)
                response.save()

        if 'delete_response' in request.POST:
                response_id = request.POST.get('delete_response')
                response = Response.objects.get(pk=response_id)
                response.delete()

    responses = Response.objects.filter(ad__author=user)
    ad = Ad.objects.filter(author=user)
    return render(request, 'my_responses.html', {'responses': responses, 'ad': ad})


def delete_responses(request, pk):
    response = get_object_or_404(Response, pk=pk)
    if response.ad.author == request.user:
        response.delete()
        send_mail(
            subject='На Ваш отклик отреагировали',
            message=f'Здравствуйте "{response.sender}". Ваш отклик "{response.message}" к объявлению"{response.ad.title}" был удалён.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[response.sender.email],
        )

    return redirect('my_responses')


def accept_responses(request, pk):
    response = get_object_or_404(Response, pk=pk)
    if response.ad.author == request.user:
        ad = response.ad
        response.is_accepted = True
        response.save()
        ad.save()
        send_mail(
            subject='На Ваш отклик отреагировали',
            message=f'Здравствуйте "{response.sender}". Ваш отклик "{response.message}" к объявлению"{response.ad.title}" был принят.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[response.sender.email],
        )

        return redirect('my_responses')

