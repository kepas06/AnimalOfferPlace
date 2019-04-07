from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.urls import reverse

from django.views.generic import ListView,DetailView
from django.views.generic.edit import FormView, UpdateView, CreateView, DeleteView
from .forms import OfferForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Category, Offer

from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache

from django.http import HttpResponseRedirect


def signup(request):

    if request.method == 'POST':
        form = ProfileForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = ProfileForm()

    return render(request, 'registration/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


# def password_change(self, request, *args, **kwargs):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user) 
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('registration/password_change_done.html')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'registration/password_change.html', {'form': form})


class PasswordChangeView(FormView):
    form_class = PasswordChangeForm
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('password_change_done')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


# class AddOffer(UpdateView):
#     model = Offer
#     form_class = OfferForm
#     template_name = 'adverts/offer_form.html'
#     success_url = '/'

#     def form_valid(self, form):
#         form.save()
#         return super(AddOffer, self).form_valid(form)


class AddOffer(CreateView):
    template_name = 'adverts/offer_form.html'
    form_class = OfferForm
    success_url = "/"
    # form_class = OfferForm
    # template_name = 'adverts/offer_form.html'
    # success_url = '/'
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddOffer, self).dispatch(*args, **kwargs)    
    
    def form_valid(self, form):
        print("dupa")
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class OfferDetail(DetailView):
    model = Offer
    template_name = "adverts/offer_detail.html"


class OfferDelete(DeleteView):
    template_name = 'adverts/offer_delete.html'
    success_url = '/'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Offer, id=id_)

    # def get_queryset(self):
    #     if self.request.user.is_authenticated:
    #         return Offer.objects.filter(is_published=True, user=self.request.user)
    #     else:
    #         return Offer.objects.none()


class GetOffersByCategory(ListView):
    model = Offer
    template_name = 'adverts/offer_list.html'
    context_object_name = "offer_list"
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, name=self.kwargs['category'])
        isChild = self.category.id 
        return Offer.objects.filter(category__parent=isChild)

            
    # def get_queryset(self):
    #     self.category = get_object_or_404(Category, name=self.kwargs['category'])
        
    #     return Offer.objects.filter(category=self.category)


class HomeView(ListView):
    model = Category
    template_name = "accounts/home.html"
    context_object_name = "category_list"