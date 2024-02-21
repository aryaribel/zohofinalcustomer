from django.urls import path,re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve


urlpatterns = [


    # Payment term section----------------------------
    path('Payment_Terms',views.payment_terms,name='payment_terms'),
    path('Add/Payment_Terms',views.add_payment_terms,name='add_payment_terms'),
    path('Remove/Payment_Terms<int:pk>',views.remove_payment_terms,name='remove_payment_terms'),

    # distributor approval section----------------------------

    path('Admin/Dashboard',views.admindash,name='admindash'),
    path('Admin_Distributors',views.admin_distributors,name='admin_distributors'),
    path('Distributor_Requests',views.distributor_requests,name='distributor_requests'),
    path('Admin/Distributor_Accept/<int:id>',views.admin_distributor_accept,name='admin_distributor_accept'),
    path('Admin/Distributor_Reject/<int:id>',views.admin_distributor_reject,name='admin_distributor_reject'),
    path('Distributor_Request_Overview/<int:id>',views.distributor_request_overview,name='distributor_request_overview'),
    path('All_Distributors',views.all_distributors,name='all_distributors'),
    path('Distributor_Details/<int:id>',views.distributor_details,name='distributor_details'),
    path('Admin/Distributor_Cancel/<int:id>',views.admin_distributor_cancel,name='admin_distributor_cancel'),
    path('Clients_Under_Distributor',views.clients_under_distributor,name='clients_under_distributor'),
    path('getClients_Under_Distributor',views.get_clients_under_distributor,name='get_clients_under_distributor'),
    path('Distributor/client/profile_details/<int:pk>',views.distributor_client_profile_details,name='distributor_client_profile_details'),



    # client approval section----------------------------

    path('Admin/clients',views.admin_clients,name='admin_clients'),
    path('Client_Requests',views.client_requests,name='client_requests'),
    path('Admin/Client_Accept/<int:id>',views.admin_client_accept,name='admin_client_accept'),
    path('Admin/Client_Reject/<int:id>',views.admin_client_reject,name='admin_client_reject'),
    path('Client_Request_Overview/<int:id>',views.client_request_overview,name='client_request_overview'),
    path('All_Clients',views.all_clients,name='all_clients'),
    path('Client_Details/<int:id>',views.client_details,name='client_details'),
    path('Admin/Client_Cancel/<int:id>',views.admin_client_cancel,name='admin_client_cancel'),

    # Admin notifications------------------------------------

    path('Admin/Notification',views.admin_notification,name='admin_notification'),
    path('Module/Updation_Details/<int:mid>',views.module_updation_details,name='module_updation_details'),
    path('Module/Updation_Ok/<int:mid>',views.module_updation_ok,name='module_updation_ok'),

    path('clients/Paymentterm/Updation_Details/<int:pk>',views.client_paymentterm_updation_details,name='client_paymentterm_updation_details'),
    path('Client/Paymentterm/Updation_Ok/<int:cid>',views.client_paymentterm_updation_ok,name='client_paymentterm_updation_ok'),

    path('Distributor/Paymentterm_Updation/Details/<int:pk>',views.distribtor_paymentterm_updation_details,name='distribtor_paymentterm_updation_details'),
    path('Dist/Paymentterm_Updation_Ok/<int:cid>',views.distributor_paymentterm_updation_ok,name='distributor_paymentterm_updation_ok'),
   
    # Trial period sections------------------------------------
    path('Admin/Trial_Period/Section',views.trial_period_section,name='trial_period_section'),
    path('Admin/Trial_Period/Clients',views.trial_period_clients,name='trial_period_clients'),
    path('Admin/Trial_Period/Distributor-Clients',views.trial_period_distributor_clients,name='trial_period_distributor_clients'),

    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
   
    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)