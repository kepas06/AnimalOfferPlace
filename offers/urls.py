from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),  
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('password/', views.PasswordChangeView.as_view(), name='password_change'),
    path('settings/', TemplateView.as_view(template_name="accounts/settings.html"), name='settings'),
    
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name = 'registration/password_change_d.html'),name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'registration/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'registration/password_reset_d.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'registration/password_reset_conf.html'),name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name = 'registration/password_reset_cpl.html'),name='password_reset_complete'),
 

    path('add_offer/', views.AddOffer.as_view(), name='add_offer'),

    path('', views.HomeView.as_view(), name='home'),
    path('offer/<int:id>/delete/', views.OfferDelete.as_view(), name = 'offer_delete'),
    path('offer/<str:category>/', views.GetOffersByCategory.as_view(), name = 'offers'),
    path('offer/list/<slug:slug>/', views.GetOffersFromCategory.as_view(), name = 'offers_filtered'),

    path('offer/detail/<int:pk>/', views.OfferDetail.as_view(template_name='adverts/offer_detail.html'), name='detail'),
    path('offer/update/<int:pk>/', views.OfferUpdate.as_view(), name='updateOffer'),


    path('add_question/', views.AddQuestion.as_view(), name='add_question'),

    path('offer/<str:category>/', views.GetOffersByCategory.as_view(), name = 'offers'),
    path('offer/list/<str:category>/', views.GetOffersFromCategory.as_view(), name = 'offers_filtered'),
    
    path('question/<str:category>/', views.QuestionsByCategory.as_view(), name = 'questions'),
    path('question/list/<slug:slug>/', views.QuestionsFromCategory.as_view(), name = 'questions_filtered'),
    
    


    path('question/detail/<int:pk>/', views.QuestionDetail.as_view(template_name='questions/question_detail.html'), name='questions_detail'),
    path('question/<int:id>/delete/', views.QuestionDelete.as_view(), name = 'question_delete'),
    path('question/update/<int:pk>/', views.QuestionUpdate.as_view(), name='updateQuestion'),



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)