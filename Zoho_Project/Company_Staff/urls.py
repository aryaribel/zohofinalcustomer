#zoho Final
from django.urls import path,re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

urlpatterns = [
    # -------------------------------Company section--------------------------------
    path('Company/Dashboard',views.company_dashboard,name='company_dashboard'),
    path('Company/Staff-Request',views.company_staff_request,name='company_staff_request'),
    path('Company/Staff-Request/Accept/<int:pk>',views.staff_request_accept,name='staff_request_accept'),
    path('Company/Staff-Request/Reject/<int:pk>',views.staff_request_reject,name='staff_request_reject'),
    path('Company/All-Staffs',views.company_all_staff,name='company_all_staff'),
    path('Company/Staff-Approval/Cancel/<int:pk>',views.staff_approval_cancel,name='staff_approval_cancel'),
    path('Company/Profile',views.company_profile,name='company_profile'),
    path('Company/Profile-Editpage',views.company_profile_editpage,name='company_profile_editpage'),
    path('Company/Profile/Edit/Basicdetails',views.company_profile_basicdetails_edit,name='company_profile_basicdetails_edit'),
    path('Company/Password_Change',views.company_password_change,name='company_password_change'),
    path('Company/Profile/Edit/Companydetails',views.company_profile_companydetails_edit,name='company_profile_companydetails_edit'),
    path('Company/Module-Editpage',views.company_module_editpage,name='company_module_editpage'),
    path('Company/Module-Edit',views.company_module_edit,name='company_module_edit'),
    path('Company/Renew/Payment_terms',views.company_renew_terms,name='company_renew_terms'),
    path('Company/Notifications',views.company_notifications,name='company_notifications'),
    path('company/messages/read/<int:pk>',views.company_message_read,name='company_message_read'),
    path('Company/Payment_History',views.company_payment_history,name='company_payment_history'),
    path('Company/Trial/Review',views.company_trial_feedback,name='company_trial_feedback'),
    path('Company/Profile/Edit/gsttype',views.company_gsttype_change,name='company_gsttype_change'),


    # -------------------------------Staff section--------------------------------
    path('Staff/Dashboard',views.staff_dashboard,name='staff_dashboard'),
    path('Staff/Profile',views.staff_profile,name='staff_profile'),
    path('Staff/Profile-Editpage',views.staff_profile_editpage,name='staff_profile_editpage'),
    path('Staff/Profile/Edit/details',views.staff_profile_details_edit,name='staff_profile_details_edit'),
    path('Staff/Password_Change',views.staff_password_change,name='staff_password_change'),
    
    # -------------------------------Zoho Modules section--------------------------------
    
    #-----------------------Customer---------------------------#
    #------------Arya E.R---------------#

    path('customer',views.customer,name='customer'),
    path('view_customer_list',views.view_customer_list,name='view_customer_list'),
    path('check_customer_phonenumber_exist',views.check_customer_phonenumber_exist,name='check_customer_phonenumber_exist'),
    path('check_customer_work_phone_exist',views.check_customer_work_phone_exist,name='check_customer_work_phone_exist'),
    path('check_customer_email_exist',views.check_customer_email_exist,name='check_customer_email_exist'),
    path('check_customer_term_exist',views.check_customer_term_exist,name='check_customer_term_exist'),
    path('customer_payment_terms_add',views.customer_payment_terms_add,name='customer_payment_terms_add'),
    path('customer_check_pan',views.customer_check_pan,name='customer_check_pan'),
    path('add_customer/',views.add_customer,name='add_customer'),
    path('customer_check_gst',views.customer_check_gst,name='customer_check_gst'),
    path('sort_customer_by_name',views.sort_customer_by_name,name='sort_customer_by_name'),
    path('sort_customer_by_amount',views.sort_customer_by_amount,name='sort_customer_by_amount'),
    path('view_customer_active',views.view_customer_active,name='view_customer_active'),
    path('view_customer_inactive',views.view_customer_inactive,name='view_customer_inactive'),
    path('import_customer_excel',views.import_customer_excel,name='import_customer_excel'),
    path('view_customer_details/<int:pk>',views.view_customer_details,name='view_customer_details'),
    path('sort_customer/<int:selectId>/<int:pk>',views.sort_customer,name='sort_customer'),
    path('customer_status_change/<int:statusId>/<int:pk>',views.customer_status_change,name='customer_status_change'),
    path('delete_customers/<int:pk>',views.delete_customers,name='delete_customers'),
    path('customer_status/<int:pk>',views.customer_status,name='customer_status'),
    path('customer_add_comment/<int:pk>',views.customer_add_comment,name='customer_add_comment'),
    path('customer_delete_comment/<int:pk>',views.customer_delete_comment,name='customer_delete_comment'), 
    path('add_customer_file/<int:pk>',views.add_customer_file,name='add_customer_file'),
    path('customer_shareemail/<int:pk>',views.customer_shareemail,name='customer_shareemail'),
    path('Customer_edit/<int:pk>',views.Customer_edit,name='Customer_edit'),
    path('do_customer_edit/<int:pk>',views.do_customer_edit,name='do_customer_edit'),


  
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)