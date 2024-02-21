from datetime import date, timedelta
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, logout, login as auth_login
from . models import *
from Company_Staff.views import company_dashboard
from Distributor.views import distributor_dashboard
from Admin.views import admindash
from Company_Staff.models import *
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.core.exceptions import ObjectDoesNotExist
import random
import string





# Create your views here.
def landing_page(request):
    return render(request,'landpage.html')


# ------------------Distributor registration and save---------------------


def distributor_register_page(request):
  terms = PaymentTerms.objects.all()
  return render(request, 'distributor_register.html',{'terms':terms})

def register(request):
  if request.method == 'POST':
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['eid']
    username = request.POST['uname']
    phone = request.POST['ph']
    password = request.POST['pass']
    confirm_pass = request.POST['cpass']
    pterm = request.POST['select']
    pic = request.FILES.get('image')

    terms=PaymentTerms.objects.get(id=pterm)
    start_date=date.today()
    days=int(terms.days)

    
    end= date.today() + timedelta(days=days)
    End_date=end

    code_length = 8  
    characters = string.ascii_letters + string.digits  # Letters and numbers
    while True:
      unique_code = ''.join(random.choice(characters) for _ in range(code_length))
        
      # Check if the code already exists in the table
      if not DistributorDetails.objects.filter(distributor_code=unique_code).exists():
        break
    
    if password == confirm_pass:
      if LoginDetails.objects.filter(username = username).exists():
        messages.warning(request, 'Sorry, Username already exists')
        return redirect('distributor_register_page')
      

      elif not LoginDetails.objects.filter(email = email).exists():
      
        login_data =LoginDetails(
          first_name = fname,
          last_name = lname,
          username = username,
          email = email,
          password = password,
          user_type = 'Distributor'
        )
        login_data.save()
        
        data = LoginDetails.objects.get(id = login_data.id)
        distributor_data = DistributorDetails(
          login_details=data,
          payment_term=terms,
          contact=phone,
          distributor_code=unique_code,
          image=pic,
          start_date=start_date,
          End_date=End_date,
        )
        distributor_data.save()

        pterm_update = PaymentTermsUpdates(
          distributor = distributor_data,
          payment_term = terms
        )
        pterm_update.save()
        
        return redirect('login_page')
      else:
        messages.info(request, 'Sorry, Email already exists')
        return redirect('distributor_register_page')
    return redirect('distributor_register_page')



# ------------------Company registration and save-------------------------

def company_register_page1(request):
  return render(request, 'company_register.html')



def company_registration_save1(request):
  if request.method == 'POST':
    # Get data from the form
    first_name = request.POST.get('fname')
    last_name = request.POST.get('lname')
    email = request.POST.get('eid')
    username = request.POST.get('uname')
    password = request.POST.get('pass')
    cpassword = request.POST.get('cpass')
    self_distributor=request.POST.get('self_distributor')
    distributor_id = request.POST.get('did', None)  # It will be none  if not provided
    user_type = 'Company'

    if distributor_id != '':
      if DistributorDetails.objects.filter(distributor_code=distributor_id).exists():
        distributor_id=distributor_id
      else :
        messages.success(request, 'Sorry, Distributor id does not exists')
        return redirect('company_register_page1')

    if password == cpassword:
      if LoginDetails.objects.filter(email=email).exists():
        messages.info(request,'Email id exists')
        return redirect('company_register_page1')
      elif LoginDetails.objects.filter(username=username).exists():
        messages.info(request,'Username exists')
        return redirect('company_register_page1')
      else:
        # Save data to the database
        user = LoginDetails(
          first_name=first_name,
          last_name=last_name,
          email=email,
          username=username,
          password=password,  # Note: Hash the password before saving in a real-world scenario
          user_type=user_type,
          self_distributor=self_distributor,
          distributor_id=distributor_id
        )
        user.save()
        # Redirect to a success page or home page
        return redirect('company_register_page2',user.id)  
    else:
      return redirect('company_register_page1')
  return render(request, 'company_register.html')  

def company_register_page2(request,pk):
  terms=PaymentTerms.objects.all()
  context={
    'terms':terms,
    'company_id':pk
  }
  return render(request,'company_register2.html', context) 

def company_registration_save2(request,pk):
  if request.method == 'POST':
    user=LoginDetails.objects.get(id=pk)
    register_action = 'distributor' if user.self_distributor == 'distributor' else 'self'
    distributor_approve = 0 if user.self_distributor == 'distributor' else 1

    distributor_details = DistributorDetails.objects.get(distributor_code=user.distributor_id) if user.self_distributor == 'distributor' else None


    # Retrieve data from the POST request
    company_name = request.POST.get('cname')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    city = request.POST.get('city')
    state = request.POST.get('state')
    country = request.POST.get('country')
    pincode = request.POST.get('pincode')
    pannumber = request.POST.get('pannumber')
    gsttype = request.POST.get('gsttype')
    gstno = request.POST.get('gstno')
    profile_pic=  request.FILES.get('image')
    s_date=date.today()
    days=int(30)
    end=date.today() + timedelta(days=days)
    e_date=end
    code_length = 8  
    characters = string.ascii_letters + string.digits  # Letters and numbers

    while True:
      unique_code = ''.join(random.choice(characters) for _ in range(code_length))
        
      # Check if the code already exists in the table
      if not CompanyDetails.objects.filter(company_code=unique_code).exists():
        break
       
  
    # Create a new CompanyDetails instance and populate it with form data
    company_details_instance = CompanyDetails(
      login_details=user,
      distributor=distributor_details,
      company_name=company_name,
      contact=phone,
      address=address,
      city=city,
      state=state,
      country=country,
      pincode=pincode,
      pan_number=pannumber,
      gst_type=gsttype,
      gst_no=gstno,
      profile_pic=profile_pic,
      start_date=s_date,
      End_date=e_date,
      company_code=unique_code,
      reg_action=register_action,
      Distributor_approval=distributor_approve
      # Add more fields as needed
    )

    company_details_instance.save()  # Save the instance to the database

    # Create a new paymentterm instance and populate it with form data
    active_plan=PaymentTermsUpdates(
      company=company_details_instance, 
    )
    active_plan.save() # Save the instance to the database

    # Create a Trial period instance and populate it with form data
    trial_period=TrialPeriod(
      company=company_details_instance,
      start_date=s_date,
      end_date=e_date
    )
    trial_period.save() # Save the instance to the database



    #sumayya-------- Adding default payment terms for company

    com = CompanyDetails.objects.get(id=company_details_instance.id)

    Company_Payment_Term.objects.create(company=com, term_name='Due on Receipt', days=0)
    Company_Payment_Term.objects.create(company=com, term_name='NET 30', days=30)
    Company_Payment_Term.objects.create(company=com, term_name='NET 60', days=60)


    #sumayya-------- Adding default repeat every values for company

    CompanyRepeatEvery.objects.create(company=com, repeat_every = '3 Month', repeat_type='Month',duration = 3, days=90)
    CompanyRepeatEvery.objects.create(company=com, repeat_every = '6 Month', repeat_type='Month',duration = 6, days=180)
    CompanyRepeatEvery.objects.create(company=com, repeat_every = '1 Year', repeat_type='Year',duration = 1, days=360)

    


    #Tinto-------- updated for items start
    com = CompanyDetails.objects.get(id=company_details_instance.id)
    data=com.login_details
    Unit.objects.create(company=com, unit_name='BOX')
    Unit.objects.create(company=com, unit_name='NUMBER')
    Unit.objects.create(company=com, unit_name='PACK')
    # Adding default accounts for companies

    #Tinto-------- updated for items end

    #Tinto-------- updated for chart of accounts  start
    created_date = date.today()

    account_info = [
      {"company_id": com, "login_details": data, "account_type": "Accounts Payable", "account_name": "Accounts Payable", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "This is an account of all the money which you owe to others like a pending bill payment to a vendor,etc.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Accounts Receivable", "account_name": "Accounts Receivable", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "The money that customers owe you becomes the accounts receivable. A good example of this is a payment expected from an invoice sent to your customer.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Other Current Asset", "account_name": "Advance Tax", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "Any tax which is paid in advance is recorded into the advance tax account. This advance tax payment could be a quarterly, half yearly or yearly payment", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Advertising and Marketing", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "Your expenses on promotional, marketing and advertising activities like banners, web-adds, trade shows, etc. are recorded in advertising and marketing account.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Automobile Expense", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "Transportation related expenses like fuel charges and maintenance charges for automobiles, are included to the automobile expense account.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Bad Debt", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "Any amount which is lost and is unrecoverable is recorded into the bad debt account.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Bank Fees and Charges", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": " Any bank fees levied is recorded into the bank fees and charges account. A bank account maintenance fee, transaction charges, a late payment fee are some examples.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},

      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Consultant Expense", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "Charges for availing the services of a consultant is recorded as a consultant expenses. The fees paid to a soft skills consultant to impart personality development training for your employees is a good example.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Cost Of Goods Sold", "account_name": "Cost of Goods Sold", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "An expense account which tracks the value of the goods sold.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Credit Card Charges", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": " Service fees for transactions , balance transfer fees, annual credit fees and other charges levied on a credit card are recorded into the credit card account.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Depreciation Expense", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "Any depreciation in value of your assets can be captured as a depreciation expense.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},

      {"company_id": com, "login_details": data, "account_type": "Income", "account_name": "Discount", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "Any reduction on your selling price as a discount can be recorded into the discount account.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Equity", "account_name": "Drawings", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "The money withdrawn from a business by its owner can be tracked with this account.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Other Current Asset", "account_name": "Employee Advance", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "Money paid out to an employee in advance can be tracked here till it's repaid or shown to be spent for company purposes", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Other Current Liability", "account_name": "Employee Reimbursements", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "This account can be used to track the reimbursements that are due to be paid out to employees.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Other Expense", "account_name": "Exchange Gain or Loss", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "Changing the conversion rate can result in a gain or a loss. You can record this into the exchange gain or loss account.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},

      {"company_id": com, "login_details": data, "account_type": "Fixed Asset", "account_name": "Furniture and Equipment", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "Purchases of furniture and equipment for your office that can be used for a long period of time usually exceeding one year can be tracked with this account.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Income", "account_name": "General Income", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "A general category of account where you can record any income which cannot be recorded into any other category", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Income", "account_name": "Interest Income", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "A percentage of your balances and deposits are given as interest to you by your banks and financial institutions. This interest is recorded into the interest income account.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Stock", "account_name": "Inventory Asset", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "An account which tracks the value of goods in your inventory.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "IT and Internet Expenses", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "Money spent on your IT infrastructure and usage like internet connection, purchasing computer equipment etc is recorded as an IT and Computer Expense", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},

      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Janitorial Expense", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "All your janitorial and cleaning expenses are recorded into the janitorial expenses account.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Income", "account_name": "Late Fee Income", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "Any late fee income is recorded into the late fee income account. The late fee is levied when the payment for an invoice is not received by the due date", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Lodging", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "Any expense related to putting up at motels etc while on business travel can be entered here.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Meals and Entertainment", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "Expenses on food and entertainment are recorded into this account.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "default", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Office Supplies", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "All expenses on purchasing office supplies like stationery are recorded into the office supplies account.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},

      {"company_id": com, "login_details": data, "account_type": "Other Current Liability", "account_name": "Opening Balance Adjustments", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "This account will hold the difference in the debits and credits entered during the opening balance.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Equity", "account_name": "Opening Balance Offset", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "This is an account where you can record the balance from your previous years earning or the amount set aside for some activities. It is like a buffer account for your funds.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Income", "account_name": "Other Charges", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "Miscellaneous charges like adjustments made to the invoice can be recorded in this account.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Other Expenses", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": " Any minor expense on activities unrelated to primary business operations is recorded under the other expense account.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Equity", "account_name": "Owner's Equity", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "The owners rights to the assets of a company can be quantified in the owner's equity account.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},

      {"company_id": com, "login_details": data, "account_type": "Cash", "account_name": "Petty Cash", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "It is a small amount of cash that is used to pay your minor or casual expenses rather than writing a check.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Postage", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "Your expenses on ground mails, shipping and air mails can be recorded under the postage account.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Other Current Asset", "account_name": "Prepaid Expenses", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "An asset account that reports amounts paid in advance while purchasing goods or services from a vendor.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Printing and Stationery", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": " Expenses incurred by the organization towards printing and stationery.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Rent Expense", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "The rent paid for your office or any space related to your business can be recorded as a rental expense.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},

      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Repairs and Maintenance", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "The costs involved in maintenance and repair of assets is recorded under this account.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Equity", "account_name": "Retained Earnings", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "The earnings of your company which are not distributed among the share holders is accounted as retained earnings.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Salaries and Employee Wages", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "Salaries for your employees and the wages paid to workers are recorded under the salaries and wages account.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Income", "account_name": "Sales", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": " The income from the sales in your business is recorded under the sales account.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Income", "account_name": "Shipping Charge", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "Shipping charges made to the invoice will be recorded in this account.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},

      {"company_id": com, "login_details": data, "account_type": "Other Liability", "account_name": "Tag Adjustments", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": " This adjustment account tracks the transfers between different reporting tags.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "active"},
      {"company_id": com, "login_details": data, "account_type": "Other Current Liability", "account_name": "Tax Payable", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "The amount of money which you owe to your tax authority is recorded under the tax payable account. This amount is a sum of your outstanding in taxes and the tax charged on sales.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Telephone Expense", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "The expenses on your telephone, mobile and fax usage are accounted as telephone expenses.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Travel Expense", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": " Expenses on business travels like hotel bookings, flight charges, etc. are recorded as travel expenses.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Uncategorized", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "This account can be used to temporarily track expenses that are yet to be identified and classified into a particular category.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},

      {"company_id": com, "login_details": data, "account_type": "Cash", "account_name": "Undeposited Funds", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "Record funds received by your company yet to be deposited in a bank as undeposited funds and group them as a current asset in your balance sheet.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Other Current Liability", "account_name": "Unearned Revenue", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "A liability account that reports amounts received in advance of providing goods or services. When the goods or services are provided, this account balance is decreased and a revenue account is increased.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Equity", "account_name": "Capital Stock", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": " An equity account that tracks the capital introduced when a business is operated through a company or corporation.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Long Term Liability", "account_name": "Construction Loans", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "An expense account that tracks the amount you repay for construction loans.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Contract Assets", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "An asset account to track the amount that you receive from your customers while you're yet to complete rendering the services.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},

      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Depreciation And Amortisation", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "An expense account that is used to track the depreciation of tangible assets and intangible assets, which is amortization.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Equity", "account_name": "Distributions", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "An equity account that tracks the payment of stock, cash or physical products to its shareholders.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Equity", "account_name": "Dividends Paid", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "An equity account to track the dividends paid when a corporation declares dividend on its common stock.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},

      {"company_id": com, "login_details": data, "account_type": "Other Current Liability", "account_name": "GST Payable", "credit_card_no": "", "sub_account": "on", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Other Current Liability", "account_name": "Output CGST", "credit_card_no": "", "sub_account": True, "parent_account": "GST Payable", "bank_account_no": None, "account_code": "", "description": "", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Other Current Liability", "account_name": "Output IGST", "credit_card_no": "", "sub_account": True, "parent_account": "GST Payable", "bank_account_no": None, "account_code": "", "description": "", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Other Current Liability", "account_name": "Output SGST", "credit_card_no": "", "sub_account": True, "parent_account": "GST Payable", "bank_account_no": None, "account_code": "", "description": "", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},

      {"company_id": com, "login_details": data, "account_type": "Other Current Asset", "account_name": "GST TCS Receivable", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Other Current Asset", "account_name": "GST TDS Receivable", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},

      {"company_id": com, "login_details": data, "account_type": "Other Current Asset", "account_name": "Input Tax Credits", "credit_card_no": "", "sub_account": "on", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Other Current Asset", "account_name": "Input CGST", "credit_card_no": "", "sub_account": True, "parent_account": "Input Tax Credits", "bank_account_no": None, "account_code": "", "description": "", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Other Current Asset", "account_name": "Input IGST", "credit_card_no": "", "sub_account": True, "parent_account": "Input Tax Credits", "bank_account_no": None, "account_code": "", "description": "", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Other Current Asset", "account_name": "Input SGST", "credit_card_no": "", "sub_account": True, "parent_account": "Input Tax Credits", "bank_account_no": None, "account_code": "", "description": "", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},

      {"company_id": com, "login_details": data, "account_type": "Equity", "account_name": "Investments", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "An equity account used to track the amount that you invest.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Cost Of Goods Sold", "account_name": "Job Costing", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "An expense account to track the costs that you incur in performing a job or a task.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Cost Of Goods Sold", "account_name": "Labor", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "An expense account that tracks the amount that you pay as labor.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "active"},
      {"company_id": com, "login_details": data, "account_type": "Cost Of Goods Sold", "account_name": "Materials", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "An expense account that tracks the amount you use in purchasing materials.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Merchandise", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "An expense account to track the amount spent on purchasing merchandise.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},

      {"company_id": com, "login_details": data, "account_type": "Long Term Liability", "account_name": "Mortgages", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "An expense account that tracks the amounts you pay for the mortgage loan.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Raw Materials And Consumables", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "An expense account to track the amount spent on purchasing raw materials and consumables.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Other Current Asset", "account_name": "Reverse Charge Tax Input but not due", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "The amount of tax payable for your reverse charge purchases can be tracked here.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Other Current Asset", "account_name": "Sales to Customers (Cash)", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Cost Of Goods Sold", "account_name": "Subcontractor", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": " An expense account to track the amount that you pay subcontractors who provide service to you.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},

      {"company_id": com, "login_details": data, "account_type": "Other Current Liability", "account_name": "TDS Payable", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Other Current Asset", "account_name": "TDS Receivable", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Expense", "account_name": "Transportation Expense", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "An expense account to track the amount spent on transporting goods or providing services.", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},

      {"company_id": com, "login_details": data, "account_type": "Bank", "account_name": "Bank Account", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Cash", "account_name": "Cash Account", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Credit Card", "account_name": "Credit Card Account", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
      {"company_id": com, "login_details": data, "account_type": "Payment Clearing Account", "account_name": "Payment Clearing Account", "credit_card_no": "", "sub_account": "", "parent_account": "", "bank_account_no": None, "account_code": "", "description": "", "balance":0.0, "balance_type" : "", "date" : created_date, "create_status": "Active", "status": "Active"},
    ]

    for account in account_info:
      if not Chart_of_Accounts.objects.filter(company = com,account_name=account['account_name']).exists():
        new_account = Chart_of_Accounts(company=account['company_id'],login_details=account['login_details'],account_name=account['account_name'],sub_account=account['sub_account'],parent_account=account['parent_account'],account_type=account['account_type'],account_code=account['account_code'],account_description=account['description'],Create_status=account['create_status'],status=account['status'])
        if account['account_type'] == 'Other Assets':
          new_account.description = 'Track special assets like goodwill and other intangible assets'
        if account['account_type'] == 'Other Current Assets':
          new_account.description = 'Any short term asset that can be converted into cash or cash equivalents easily Prepaid expenses Stocks and Mutual Funds'
        if account['account_type'] == 'Cash':
          new_account.description = 'To keep track of cash and other cash equivalents like petty cash, undeposited funds, etc., use an organized accounting system  financial software'
        if account['account_type'] == 'Bank':
          new_account.description = 'To keep track of bank accounts like Savings, Checking, and Money Market accounts.'
        if account['account_type'] == 'Fixed Asset':
          new_account.description = 'Any long-term investment or asset that cannot be easily converted into cash includes: Land and Buildings, Plant, Machinery, and Equipment, Computers, Furniture.'
        if account['account_type'] == 'Stock':
          new_account.description = 'To keep track of your inventory assets.'
        if account['account_type'] == 'Payment Clearing':
          new_account.description = 'To keep track of funds moving in and out via payment processors like Stripe, PayPal, etc.'
        if account['account_type'] == 'Other Liability':
          new_account.description = 'Obligation of an entity arising from past transactions or events which would require repayment.Tax to be paid Loan to be Repaid Accounts Payableetc.'
        if account['account_type'] == 'Other Current Liability':
          new_account.description = 'Any short term liability like: Customer Deposits Tax Payable'
        if account['account_type'] == 'Credit Card':
          new_account.description = 'Create a trail of all your credit card transactions by creating a credit card account.'
        if account['account_type'] == 'Long Term Liability':
          new_account.description = 'Liabilities that mature after a minimum period of one year like: Notes Payable Debentures Long Term Loans '
        if account['account_type'] == 'Overseas Tax Payable':
          new_account.description = 'Track your taxes in this account if your business sells digital services to foreign customers.'
        if account['account_type'] == 'Equity':
          new_account.description = 'Owners or stakeholders interest on the assets of the business after deducting all the liabilities.'
        if account['account_type'] == 'Income':
          new_account.description = 'Income or Revenue earned from normal business activities like sale of goods and services to customers.'
        if account['account_type'] == 'Other Income':
          new_account.description = 'Income or revenue earned from activities not directly related to your business like : Interest Earned Dividend Earned'
        if account['account_type'] == 'Expense':
          new_account.description = 'Reflects expenses incurred for running normal business operations, such as : Advertisements and Marketing Business Travel Expenses License Fees Utility Expenses'
        if account['account_type'] == 'Cost Of Goods Sold':
          new_account.description = 'This indicates the direct costs attributable to the production of the goods sold by a company such as: Material and Labor costs Cost of obtaining raw materials'
        if account['account_type'] == 'Other Expense':
          new_account.description = 'Track miscellaneous expenses incurred for activities other than primary business operations or create additional accounts to track default expenses like insurance or contribution towards charity.'
                  
        new_account.save()
    #Tinto-------- updated for chart of accounts  end
    # Re  # Save the instance to the database
 
    return redirect('modules_select_page', company_details_instance.id)

  return render(request,'company_register2.html')


#--------------- Staff registration and save-------------------------

def staff_register_page(request):
  return render(request, 'staff_register.html')


def staff_registration(request):
  if request.method == 'POST':
    # Get data from the form
    first_name = request.POST.get('fname')
    last_name = request.POST.get('lname')
    email = request.POST.get('eid')
    username = request.POST.get('uname')
    phone = request.POST.get('ph')
    password = request.POST.get('pass')
    cpassword = request.POST.get('cpass')
    user_type = 'Staff'
    profile_pic=  request.FILES.get('image')
    code = request.POST.get('code')

    if code != '':
      if CompanyDetails.objects.filter(company_code=code).exists():
        company=CompanyDetails.objects.get(company_code=code)
      else :
        messages.warning(request, 'Sorry, company id does not exists')
        return redirect('staff_register_page')

    # Check if the username is unique within the same company
    if StaffDetails.objects.filter(login_details__username=username, company=company).exists():
      messages.warning(request, 'Username already exists for staff in the same company')
      return redirect('staff_register_page')

    if password == cpassword:
      if LoginDetails.objects.filter(email=email).exists():
        messages.success(request,'Email id exists')
        return redirect('staff_register_page')
      if LoginDetails.objects.filter(password=password).exists():
        messages.error(request,'Use another password')
        return redirect('staff_register_page')
      else:
        # Save data to the database
        user = LoginDetails(
          first_name=first_name,
          last_name=last_name,
          email=email,
          username=username,
          password=password,  # Note: Hash the password before saving in a real-world scenario
          user_type=user_type,
        )
        user.save()

        staff_details_instance= StaffDetails(
          login_details=user,
          company=company,
          contact=phone,
          image=profile_pic,
          position='staff'
        )
        staff_details_instance.save()

        # Redirect to a success page or home page
        return redirect('login_page')  
    else:
      return redirect('staff_register_page')
  return render(request, 'staff_register.html')  


#------------------Company Modules Select Section-------------------------

def modules_select_page(request,pk):
  company_id=pk
  context={
    'company':company_id,
  }
  return render(request, 'modules.html',context)


def choose_modules(request, pk):
  if request.method == 'POST':

    # Get the company based on the id
    company = CompanyDetails.objects.get(id=pk)

    # Retrieve values
    items = request.POST.get('items', 0)
    price_list = request.POST.get('price_list', 0)
    stock_adjustment = request.POST.get('stock_adjustment', 0)
    godown = request.POST.get('godown', 0)

    cash_in_hand = request.POST.get('cash_in_hand', 0)
    offline_banking = request.POST.get('offline_banking', 0)
    upi = request.POST.get('upi', 0)
    bank_holders = request.POST.get('bank_holders', 0)
    cheque = request.POST.get('cheque', 0)
    loan_account = request.POST.get('loan_account', 0)

    customers = request.POST.get('customers', 0)
    invoice = request.POST.get('invoice', 0)
    estimate = request.POST.get('estimate', 0)
    sales_order = request.POST.get('sales_order', 0)
    recurring_invoice = request.POST.get('recurring_invoice', 0)
    retainer_invoice = request.POST.get('retainer_invoice', 0)
    credit_note = request.POST.get('credit_note', 0)
    payment_received = request.POST.get('payment_received', 0)
    delivery_challan = request.POST.get('delivery_challan', 0)

    vendors = request.POST.get('vendors', 0)
    bills = request.POST.get('bills', 0)
    recurring_bills = request.POST.get('recurring_bills', 0)
    vendor_credit = request.POST.get('vendor_credit', 0)
    purchase_order = request.POST.get('purchase_order', 0)
    expenses = request.POST.get('expenses', 0)
    recurring_expenses = request.POST.get('recurring_expenses', 0)
    payment_made = request.POST.get('payment_made', 0)

    projects = request.POST.get('projects', 0)

    chart_of_accounts = request.POST.get('chart_of_accounts', 0)
    manual_journal = request.POST.get('manual_journal', 0)

    eway_bill = request.POST.get('ewaybill', 0)

    employees = request.POST.get('employees', 0)
    employees_loan = request.POST.get('employees_loan', 0)
    holiday = request.POST.get('holiday', 0)
    attendance = request.POST.get('attendance', 0)
    salary_details = request.POST.get('salary_details', 0)

    reports = request.POST.get('reports', 0)


    # Create a new ZohoModules instance and save it to the database
    data = ZohoModules(
      company=company,
      items=items, price_list=price_list, stock_adjustment=stock_adjustment, godown=godown,
      cash_in_hand=cash_in_hand, offline_banking=offline_banking, upi=upi, bank_holders=bank_holders,
      cheque=cheque, loan_account=loan_account,
      customers=customers, invoice=invoice, estimate=estimate, sales_order=sales_order,
      recurring_invoice=recurring_invoice, retainer_invoice=retainer_invoice, credit_note=credit_note,
      payment_received=payment_received, delivery_challan=delivery_challan,
      vendors=vendors, bills=bills, recurring_bills=recurring_bills, vendor_credit=vendor_credit,
      purchase_order=purchase_order, expenses=expenses, recurring_expenses=recurring_expenses,
      payment_made=payment_made,
      projects=projects,
      chart_of_accounts=chart_of_accounts, manual_journal=manual_journal,
      eway_bill=eway_bill,
      employees=employees, employees_loan=employees_loan, holiday=holiday,
      attendance=attendance, salary_details=salary_details,
      reports=reports,    
    )
    data.save()
    return redirect('login_page')
  return render(request, 'modules.html.html')




#------------------ Login Section-------------------------

def login_page(request):
  return render(request, 'login.html')

def plan_expired(request):
  return render(request,'plan_inactive.html')

def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None and user.is_staff:
      auth_login(request, user)
      return redirect('admindash')

    try:
      log_user = LoginDetails.objects.get(username=username, password=password)
    except ObjectDoesNotExist:
      messages.error(request, 'Invalid Username or Password. Try Again.')
      return redirect('login_page')

    # Distributor login session
    if log_user.user_type == 'Distributor':
      request.session["login_id"] = log_user.id
      if 'login_id' in request.session:
        distributor_id = request.session['login_id']
      else:
        return redirect('login_page')

      try:
        distributor = LoginDetails.objects.get(id=distributor_id)
        current_date=date.today()
      except LoginDetails.DoesNotExist:
        return redirect('login_page')

      try:
        dash_details = DistributorDetails.objects.get(login_details=distributor, superadmin_approval=1)
        if current_date > dash_details.End_date:
          return redirect('plan_expired')
        else:
          return redirect('distributor_dashboard')
      except DistributorDetails.DoesNotExist:
        messages.info(request, 'Approval is Pending..')
        return redirect('login_page')

    # Company login session
    
    elif log_user.user_type == 'Company':
      request.session["login_id"] = log_user.id
      if 'login_id' in request.session:
        company_id = request.session['login_id']
      else:
        return redirect('login_page')

      try:
        company = LoginDetails.objects.get(id=company_id)
        current_date=date.today()
      except LoginDetails.DoesNotExist:
        return redirect('login_page')

      try:
        dash_details = CompanyDetails.objects.get(
          login_details=company,
          superadmin_approval=1,
          Distributor_approval=1,
        )
        if current_date > dash_details.End_date:
          return redirect('plan_expired')
        else:
          return redirect('company_dashboard')
      except CompanyDetails.DoesNotExist:
        messages.warning(request, 'Approval is Pending')
        return redirect('login_page')

    # Staff login session
    elif log_user.user_type == 'Staff':
      request.session["login_id"] = log_user.id
      if 'login_id' in request.session:
        staff_id = request.session['login_id']
      else:
        return redirect('login_page')

      try:
        staff = LoginDetails.objects.get(id=staff_id)
        current_date=date.today()
      except LoginDetails.DoesNotExist:
        return redirect('login_page')

      try:
        dash_details = StaffDetails.objects.get(login_details=staff, company_approval=1)
        if current_date > dash_details.company.End_date:
          return redirect('plan_expired')
        else:
          return redirect('staff_dashboard')
      except StaffDetails.DoesNotExist:
        messages.error(request, 'Approval is Pending..')
        return redirect('login_page')

    else:
      return render(request, 'error-404.html')

  # Handle GET requests
  else:
    return redirect('login_page')


#------------------ Logout Section-------------------------

def admin_logout(request):
  auth.logout(request)
  return redirect('login_page')

def logout(request):
  request.session.pop('login_id', None)
  return redirect('login_page')   