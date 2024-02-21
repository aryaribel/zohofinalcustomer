from datetime import date, timedelta
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string
from Register_Login.models import *

# Create your views here.

def distributor_dashboard(request):
    if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/') 
        log_det = LoginDetails.objects.get(id=login_id)
        distributor_det = DistributorDetails.objects.get(login_details=log_det)

        # Calculate the date 20 days before the end date for payment term renew
        reminder_date = distributor_det.End_date - timedelta(days=20)
        current_date = date.today()
        alert_message = current_date >= reminder_date

        # Calculate the number of days between the reminder date and end date
        days_left = (distributor_det.End_date - current_date).days

        payment_request = True if PaymentTermsUpdates.objects.filter(distributor=distributor_det,update_action=1,status='Pending').exists() else False
   
        context = {
            'distributor_details': distributor_det,
            'alert_message':alert_message,
            'days_left':days_left,
            'payment_request':payment_request,
        }
        return render(request, 'distributor_dash.html', context)
    else:
        return redirect('/')

def dist_clients(request):
    if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/') 
        log_det = LoginDetails.objects.get(id=login_id)
        distributor_det = DistributorDetails.objects.get(login_details=log_det)
        return render(request,'dist_clients.html',{'distributor_details':distributor_det})
    else:
        return redirect('/')

def dist_client_requests(request):
    if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/') 
        log_det = LoginDetails.objects.get(id=login_id)
        distributor_det = DistributorDetails.objects.get(login_details=log_det)
        clients = CompanyDetails.objects.filter(Distributor_approval=0,distributor=distributor_det).order_by('-id')
        return render(request,'dist_client_requests.html',{'distributor_details':distributor_det,'clients':clients})
    else:
        return redirect('/')
def dist_client_accept(request,id):
  data=CompanyDetails.objects.filter(id=id).update(Distributor_approval=1,superadmin_approval=1)
  return redirect('dist_client_requests')

def dist_client_reject(request,id):
  data=CompanyDetails.objects.get(id=id)
  data.login_details.delete()
  data.delete()
  return redirect('dist_client_requests')

def dist_client_request_overview(request,id):
    if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/') 
        log_det = LoginDetails.objects.get(id=login_id)
        distributor_det = DistributorDetails.objects.get(login_details=log_det)
        data=CompanyDetails.objects.get(id=id)
        allmodules=ZohoModules.objects.get(company=data,status='New')
        return render(request,'dist_client_request_overview.html',{'company':data,'allmodules':allmodules,'distributor_details':distributor_det})
    else:
        return redirect('/')

def dist_all_clients(request):
    if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/') 
        log_det = LoginDetails.objects.get(id=login_id)
        distributor_det = DistributorDetails.objects.get(login_details=log_det)
        clients=CompanyDetails.objects.filter(Distributor_approval=1,distributor=distributor_det)
        
        return render(request,'dist_all_clients.html',{'clients':clients,'distributor_details':distributor_det})
    else:
        return redirect('/')

def dist_client_details(request,id):
    if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')   
        log_det = LoginDetails.objects.get(id=login_id)
        distributor_det = DistributorDetails.objects.get(login_details=log_det)
        data=CompanyDetails.objects.get(id=id)
        allmodules=ZohoModules.objects.get(company=data,status='New')
        return render(request,'dist_client_details.html',{'company':data,'allmodules':allmodules,'distributor_details':distributor_det})
    else:
        return redirect('/')

def distributor_profile(request):
    if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/') 
        log_det = LoginDetails.objects.get(id=login_id)
        distributor= DistributorDetails.objects.get(login_details=log_det)
        terms=PaymentTerms.objects.all()
        payment_history=distributor.previous_plans.all()
        # Calculate the date 20 days before the end date
        reminder_date = distributor.End_date - timedelta(days=20)
        current_date = date.today()
        renew_button = current_date >= reminder_date
        context={
            'distributor_details':distributor,
            'terms':terms,
            'renew_button':renew_button,
            'payment_history':payment_history
        }
  
        return render(request,'distributor_profile.html',context)
    else:
        return redirect('/')

def dist_edit_profilePage(request,id):
  
  distributor = DistributorDetails.objects.get(id=id)
  terms=PaymentTerms.objects.all()
 
  return render(request,'edit_distributor_profile.html',{'terms':terms,'distributor_details':distributor})

def update_distributor_profile(request,id):
    distributor = DistributorDetails.objects.get(id=id)

    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['eid']
        username = request.POST['uname']
        phone = request.POST['phone']
        pic = request.FILES.get('profile_pic')


        login_data = LoginDetails.objects.get(id=distributor.login_details_id)
        login_data.first_name = fname
        login_data.last_name = lname
        login_data.email = email
        login_data.username = username
        login_data.save()

        distributor.contact = phone
        if pic:
            distributor.image = pic
        distributor.save()
        messages.success(request,'Profile Updated')

    return redirect('distributor_profile')

def distributor_password_change(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')

        log_details= LoginDetails.objects.get(id=log_id)
        if request.method == 'POST':
            # Get data from the form
            password = request.POST.get('pass')
            cpassword = request.POST.get('cpass')
            if password == cpassword:
                if LoginDetails.objects.filter(password=password).exists():
                    messages.error(request,'Use another password')
                    return redirect('distributor_profile')
                else:
                    log_details.password=password
                    log_details.save()

            messages.success(request,'Password Changed')
            return redirect('distributor_profile') 
        else:
            return redirect('distributor_profile') 

    else:
        return redirect('/')



# notifications------------------------------------

def distributor_notification(request):
    if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/') 
        log_det = LoginDetails.objects.get(id=login_id)
        distributor_det = DistributorDetails.objects.get(login_details=log_det)
        notifications = distributor_det.notifications.filter(is_read=0).order_by('-date_created','-time')

        end_date = distributor_det.End_date
        dist_days_remaining = (end_date - date.today()).days
        payment_request = True if PaymentTermsUpdates.objects.filter(distributor=distributor_det,update_action=1,status='Pending').exists() else False
        
        companies = CompanyDetails.objects.filter(reg_action='distributor')

        for c in companies:
            c.days_remaining = (c.End_date - date.today()).days
            
        pterm_updation = PaymentTermsUpdates.objects.filter(update_action=1,status='Pending')
        data= ZohoModules.objects.filter(update_action=1,status='Pending')

        context ={'data':data,
                  'pterm_updation':pterm_updation,
                  'distributor_details':distributor_det,
                  'companies':companies,
                  'dist_days_remaining':dist_days_remaining,
                  'notifications':notifications,
                  'payment_request':payment_request,
                  }
        
        return render(request,'distributor_notification.html',context)
    else:
        return redirect('/')

def dist_module_updation_details(request,mid):
    if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/') 
        log_det = LoginDetails.objects.get(id=login_id)
        distributor_det = DistributorDetails.objects.get(login_details=log_det)
        data = ZohoModules.objects.get(id=mid)
        modules_pending = ZohoModules.objects.filter(company=data.company, status='Pending')
        current_modules = ZohoModules.objects.filter(company=data.company, status='New')

        # Extract the field names related to modules
        module_fields = [field.name for field in ZohoModules._meta.fields if field.name not in ['id', 'company', 'status', 'update_action']]

        # Get the previous and new values for the selected modules
        previous_values = current_modules.values(*module_fields).first()
        new_values = data.__dict__

        # Identify added and deducted modules
        added_modules = {}
        deducted_modules = {}

        for field in module_fields:
            if new_values[field] > previous_values[field]:
                added_modules[field] = new_values[field] - previous_values[field]
            elif new_values[field] < previous_values[field]:
                deducted_modules[field] = previous_values[field] - new_values[field]
        

        allmodules = ZohoModules.objects.get(company=data.company, status='Pending')
        old_modules = ZohoModules.objects.get(company=data.company, status='New')
        

        context = {
            'data': data,
            'current_modules': current_modules,
            'modules_pending': modules_pending,
            'previous_values': previous_values,
            'new_values': new_values,
            'added_modules': added_modules,
            'deducted_modules': deducted_modules,
            'newmodules':allmodules,
            'allmodules':old_modules,

        }

        return render(request,'dist_module_updation_details.html', context)
    else:
        return redirect('/')

def dist_module_updation_ok(request,mid):
  
  old=ZohoModules.objects.get(company=mid,status='New')
  old.delete()

  data=ZohoModules.objects.get(company=mid,status='Pending')  
  data.status='New'
  data.update_action=0
  data.save()

  # notification section
  company=CompanyDetails.objects.get(id=mid)
  title='Congratz..! Modules Updated'
  message='Your module update request is approved'
  notification=Notifications.objects.create(company=company,title=title,message=message)
  
  return redirect('distributor_notification')

def paymentterm_updation_details(request,pk):
    if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/') 
        log_det = LoginDetails.objects.get(id=login_id)
        distributor_det = DistributorDetails.objects.get(login_details=log_det)
        term= PaymentTermsUpdates.objects.get(id=pk)
        new_term= PaymentTermsUpdates.objects.get(company=term.company.id,update_action=1,status='Pending')
        old_term = PaymentTermsUpdates.objects.get(company=term.company.id,update_action=0,status='New')
        start_date = term.company.start_date
        end_date = term.company.End_date 
        current_date = date.today()
        difference_in_days = (end_date - current_date).days
        print(term)
        context = {
            'new_term':new_term,
            'old_term':old_term,
            'term':term,
            'difference_in_days':difference_in_days,
            'distributor_details':distributor_det
            }
        return render(request,'client_pterm_updation_details.html',context)
    else:
        return redirect('/')

def paymentterm_updation_ok(request,pk):
  company = CompanyDetails.objects.get(id=pk)
  
  old_term=PaymentTermsUpdates.objects.get(company=pk,update_action=0,status='New')
  if old_term.payment_term:
    plan= f"{old_term.payment_term.payment_terms_number} {old_term.payment_term.payment_terms_value}"
  else:
    plan="Trial Period"
  s_date=company.start_date
  e_date=company.End_date
  previous_plan=PreviousPaymentTerms.objects.create(company=company,payment_term=plan,start_date=s_date,end_date=e_date)
  old_term.delete()

  new_term=PaymentTermsUpdates.objects.get(company=pk,update_action=1,status='Pending')  
  new_term.status='New'
  new_term.update_action=0
  new_term.save()

  terms = new_term.payment_term
  start_date=company.End_date + timedelta(days=1)
  days=int(terms.days)  
  end= start_date + timedelta(days=days)
  End_date=end
  
  company.payment_term=terms
  company.start_date=start_date
  company.End_date=End_date
  company.save()

  # notification section
  title='Congratz..! New Plan Activated'
  message=f'Your new plan is activated and ends on {End_date}'
  notification=Notifications.objects.create(company=company,title=title,message=message)
  return redirect('distributor_notification')


def dist_term_update_request(request):
    if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/') 
        log_det = LoginDetails.objects.get(id=login_id)
        distributor_det = DistributorDetails.objects.get(login_details=log_det)

        # Check for any previous  extension request
        if PaymentTermsUpdates.objects.filter(distributor=distributor_det,update_action=1,status='Pending').exists():
            messages.warning(request,'You have a pending request, wait for approval or contact our support team for any help..?')
            return redirect('distributor_profile')
        if request.method == 'POST':
            select=request.POST['select']
            terms=PaymentTerms.objects.get(id=select)
            pterm_update = PaymentTermsUpdates(
                distributor = distributor_det,
                payment_term = terms,
                update_action = 1,
                status = 'Pending'
            )
            pterm_update.save()
        
        terms=PaymentTerms.objects.all()
        messages.success(request, 'Request has been sent successfully.')
        return redirect('distributor_profile')
    else:
        return redirect('/')

        
# ----Trial period section------

def trial_periodclients(request):

    if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/') 
        log_det = LoginDetails.objects.get(id=login_id)
        distributor_det = DistributorDetails.objects.get(login_details=log_det)

        clients=TrialPeriod.objects.filter(company__distributor=distributor_det).order_by('-id')
        context={
            'distributor_details': distributor_det,
            'clients':clients,

        }
        return render(request,'trial_period_client.html', context)
    else:
        return redirect('/')

def distributor_message_read(request,pk):
    '''
    message read functions set the is_read to 1, 
    by default it is 0 means not seen by user.

    '''
    notification=Notifications.objects.get(id=pk)
    notification.is_read=1
    notification.save()
    return redirect('distributor_notification')


def distributor_payment_history(request):
    if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/') 
        log_det = LoginDetails.objects.get(id=login_id)
        distributor_det = DistributorDetails.objects.get(login_details=log_det)

        payment_history=distributor_det.previous_plans.all()
        
        context={
            'distributor_details': distributor_det,
            'payment_history':payment_history,

        }
        return render(request,'distributor_payment_history.html', context)
    else:
        return redirect('/')
