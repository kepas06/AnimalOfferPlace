from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.urls import reverse

from django.views.generic import ListView,DetailView
from django.views.generic.edit import FormView, UpdateView, CreateView, DeleteView
from .forms import OfferForm, ProfileForm, QuestionForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Category, Offer,Question

from django.contrib.auth.decorators import login_required
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.core.paginator import Paginator

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


#CRUD Offers



class AddOffer(CreateView):
    template_name = 'adverts/offer_form.html'
    form_class = OfferForm
    success_url = "/"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddOffer, self).dispatch(*args, **kwargs)    
    
    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class OfferDetail(DetailView):
    model = Offer
    template_name = "adverts/offer_detail.html"


class OfferUpdate(UpdateView):
    model = Offer
    template_name = "adverts/offer_form.html"
    fields = ['title','content','category','price','contact','photo',]


    def get_absolute_url(self):
        return reverse('offers:offer_detail',args=[self.title, self.slug])

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)
        
    def __str__(self):
        return self.title


class OfferDelete(DeleteView):
    template_name = 'adverts/offer_delete.html'
    success_url = '/'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Offer, id=id_)


class GetOffersByCategory(ListView):
    model = Offer
    template_name = 'adverts/offer_list.html'
    #context_object_name = "offer_list"

    def get_context_data(self, **kwargs):
        self.category = get_object_or_404(Category, name=self.kwargs['category'])
        isChild = self.category.id 
        context = super(GetOffersByCategory, self).get_context_data(**kwargs)
        context['category'] = Category.objects.filter(parent_id=isChild)
        context['category_name'] = self.category.name
        context['offer_list'] = Offer.objects.filter(category__parent=isChild)
        return context
    

class GetOffersFromCategory(ListView):
    model = Offer
    template_name = 'adverts/offer_list_filtered.html'
    context_object_name = "offer_list"

    def get_context_data(self, **kwargs):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        isChild = self.category.id 
        context = super(GetOffersFromCategory, self).get_context_data(**kwargs)
        context['category'] = Category.objects.filter(parent_id=isChild)
        context['category_name'] = self.category.name
        return context

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        cat = self.category.slug 
        return Offer.objects.filter(category__slug=cat)




#CRUD Questions

class AddQuestion(CreateView):
    template_name = 'questions/question_form.html'
    form_class = QuestionForm
    success_url = "/"


class QuestionsByCategory(ListView):
    model = Question
    template_name = 'questions/question_list.html'
    context_object_name = "question_list"
    
    def get_context_data(self, **kwargs):
        self.category = get_object_or_404(Category, name=self.kwargs['category'])
        isChild = self.category.id 
        context = super(QuestionsByCategory, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(parent_id=isChild)
        context['category_name'] = self.category.name
        context['question_list'] = Question.objects.filter(category__parent=isChild)
        return context

    def get_queryset(self):
        self.category = get_object_or_404(Category, name=self.kwargs['category'])
        isChild = self.category.id 
        return Question.objects.filter(category__parent=isChild)


class QuestionsFromCategory(ListView):
    model = Question
    template_name = 'questions/question_list_filtered.html'
    context_object_name = "question_list"

    def get_context_data(self, **kwargs):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        isChild = self.category.id 
        context = super(QuestionsFromCategory, self).get_context_data(**kwargs)
        context['category'] = Category.objects.filter(parent_id=isChild)
        context['category_name'] = self.category.name
        return context


    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        cat = self.category.slug
        
        return Question.objects.filter(category__slug=cat)





class QuestionDetail(DetailView):
    model = Question
    template_name = "questions/question_detail.html"


class QuestionUpdate(UpdateView):
    model = Question
    template_name = 'questions/question_form.html'
    fields = ['title','content','category']


    def get_absolute_url(self):
        return reverse('questions:question_detail',args=[self.title, self.slug])

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)
        
    def __str__(self):
        return self.title


class QuestionDelete(DeleteView):
    model = Question
    template_name = 'questions/question_delete.html'
    success_url = reverse_lazy('/')

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Question, id=id_)


            


class HomeView(ListView):
    model = Category
    template_name = "accounts/home.html"
    context_object_name = "category_list"