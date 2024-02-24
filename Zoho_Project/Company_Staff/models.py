#Zoho Final
from django.db import models
from Register_Login.models import *
from django.contrib.auth.models import User
from Register_Login.models import LoginDetails,CompanyDetails
# Create your models here.

#---------------- models for zoho modules--------------------
# TINTO -----ITEM ----START

class Unit(models.Model):
 
    unit_name=models.CharField(max_length=255)
    company=models.ForeignKey(CompanyDetails,on_delete=models.CASCADE)


class Company_Payment_Term(models.Model):
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE,null=True,blank=True)
    term_name =models.CharField(max_length=100,null=True,blank=True,default='')
    days =models.IntegerField(null=True,default=0)
    status =models.CharField(max_length=200,null=True,blank=True,default='')

class CompanyRepeatEvery(models.Model):
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE,null=True,blank=True)
    repeat_every =models.CharField(max_length=100,null=True,blank=True,default='')
    repeat_type =models.CharField(max_length=100,null=True,blank=True,default='')
    duration =models.IntegerField(null=True,default=0)
    days =models.IntegerField(null=True,default=0)
    



class Items(models.Model):
   
    item_type=models.CharField(max_length=255)
    item_name=models.CharField(max_length=255)
   
    unit=models.ForeignKey(Unit,on_delete=models.CASCADE)
    hsn_code=models.IntegerField(null=True,blank=True)
    tax_reference=models.CharField(max_length=255,null=True)
    intrastate_tax=models.IntegerField(null=True,blank=True)
    interstate_tax=models.IntegerField(null=True,blank=True)

    selling_price=models.IntegerField(null=True,blank=True)
    sales_account=models.CharField(max_length=255)
    sales_description=models.CharField(max_length=255)

    purchase_price=models.IntegerField(null=True,blank=True)
    purchase_account=models.CharField(max_length=255)
    purchase_description=models.CharField(max_length=255)
   
    minimum_stock_to_maintain=models.IntegerField(blank=True,null=True)  
    activation_tag=models.CharField(max_length=255,default='active')
    inventory_account=models.CharField(max_length=255,null=True)

    date=models.DateTimeField(auto_now_add=True)                                       

    opening_stock=models.IntegerField(blank=True,null=True,default=0)
    current_stock=models.IntegerField(blank=True,null=True,default=0)
    opening_stock_per_unit=models.IntegerField(blank=True,null=True,)
    company=models.ForeignKey(CompanyDetails,on_delete=models.CASCADE)
    login_details=models.ForeignKey(LoginDetails,on_delete=models.CASCADE)

    type=models.CharField(max_length=255,blank=True,null=True)

    track_inventory=models.IntegerField(blank=True,null=True)

class Item_Transaction_History(models.Model):
    company=models.ForeignKey(CompanyDetails,on_delete=models.CASCADE)
    logindetails=models.ForeignKey(LoginDetails,on_delete=models.CASCADE)
    items=models.ForeignKey(Items,on_delete=models.CASCADE)
    Date=models.DateField(null=True)
    action=models.CharField(max_length=255,default='Created')

class Items_comments(models.Model):                                              
    company=models.ForeignKey(CompanyDetails,on_delete=models.CASCADE)
    logindetails=models.ForeignKey(LoginDetails,on_delete=models.CASCADE)
    Items=models.ForeignKey(Items,on_delete=models.CASCADE)
    comments = models.CharField(max_length=255,null=True,blank=True)


# TINTO -----ITEM ----END
    
# TINTO -----CHART OF ACCOUNNTS ----START
    
class Chart_of_Accounts(models.Model):
  
    account_type = models.CharField(max_length=255,null=True,blank=True)
    account_name = models.CharField(max_length=255,null=True,blank=True)

    account_description = models.CharField(max_length=255,null=True,blank=True)

    account_number = models.CharField(max_length=255,null=True,blank=True)
    
    account_code = models.CharField(max_length=255,null=True,blank=True)
    description = models.CharField(max_length=255,null=True,blank=True)
    status=models.CharField(max_length=255,null=True,blank=True,default='Active')
    Create_status = models.CharField(max_length=255,null=True,blank=True,default='added')
    company=models.ForeignKey(CompanyDetails,on_delete=models.CASCADE)
    login_details=models.ForeignKey(LoginDetails,on_delete=models.CASCADE)
    sub_account = models.CharField(max_length=255,null=True,blank=True)
    parent_account = models.CharField(max_length=255,null=True,blank=True)

class Chart_of_Accounts_History(models.Model):
    company=models.ForeignKey(CompanyDetails,on_delete=models.CASCADE)
    logindetails=models.ForeignKey(LoginDetails,on_delete=models.CASCADE)
    chart_of_accounts=models.ForeignKey(Chart_of_Accounts,on_delete=models.CASCADE)
    Date=models.DateField(null=True)
    action=models.CharField(max_length=255,default='Created')



class chart_of_accounts_comments(models.Model):                                         
    company=models.ForeignKey(CompanyDetails,on_delete=models.CASCADE)
    logindetails=models.ForeignKey(LoginDetails,on_delete=models.CASCADE)
    chart_of_accounts=models.ForeignKey(Chart_of_Accounts,on_delete=models.CASCADE)
    comments = models.CharField(max_length=255,null=True,blank=True)
    
# TINTO -----CHART OF ACCOUNNTS ----END


#--------------------------GEORGE MATHEW____________
class payroll_employee(models.Model):
    title = models.CharField(max_length=100,null=True)
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100,null=True)
    alias = models.CharField(max_length=100,null=True)
    image=models.ImageField(upload_to="image/", null=True)
    joindate=models.DateField(null=True)
    salary_type = models.CharField(max_length=100, default='Fixed',null=True)
    salary = models.IntegerField(null=True,blank=True)
    emp_number = models.CharField(max_length=100,null=True)
    designation = models.CharField(max_length=100,null=True)
    location = models.CharField(max_length=100,null=True)
    gender = models.CharField(max_length=100,null=True)
    dob=models.DateField(null=True)
    age = models.PositiveIntegerField(default=0)
    blood = models.CharField(max_length=10,null=True)
    parent = models.CharField(max_length=100,null=True)
    spouse_name = models.CharField(max_length=100,null=True)
    address = models.CharField(max_length=250,null=True)
    permanent_address = models.CharField(max_length=250,null=True)
    Phone = models.BigIntegerField(null=True)
    emergency_phone = models.BigIntegerField(null=True ,blank=True,default=1)
    email = models.EmailField(max_length=255,null=True)
    Income_tax_no = models.CharField(max_length=255,null=True)
    Aadhar = models.CharField(max_length=250,default='',null=True)
    UAN = models.CharField(max_length=255,null=True)
    PFN = models.CharField(max_length=255,null=True)
    PRAN = models.CharField(max_length=255,null=True)
    status=models.CharField(max_length=200,default='Active',null=True)
    isTDS=models.CharField(max_length=200,null=True)
    TDS_percentage = models.IntegerField(null=True,default=0)
    salaryrange = models.CharField(max_length=10, choices=[('1-10', '1-10'), ('10-15', '10-15'), ('15-31', '15-31')], default='1-10',null=True)
    amountperhr = models.IntegerField(default=0,blank=True,null=True)
    workhr = models.IntegerField(default=0,blank=True,null=True)
    uploaded_file=models.FileField(upload_to="images/",null=True)
    company=models.ForeignKey(CompanyDetails,on_delete=models.CASCADE,null=True)
    login_details=models.ForeignKey(LoginDetails,on_delete=models.CASCADE,null=True)
    acc_no = models.CharField(null=True,max_length=255)  
    IFSC = models.CharField(max_length=100,null=True)
    bank_name = models.CharField(max_length=100,null=True)
    branch = models.CharField(max_length=100,null=True)
    transaction_type = models.CharField(max_length=100,null=True)
    
class employee_history(models.Model):
    company=models.ForeignKey(CompanyDetails,on_delete=models.CASCADE,null=True)
    login_details=models.ForeignKey(LoginDetails,on_delete=models.CASCADE,null=True)
    employee=models.ForeignKey(payroll_employee,on_delete=models.CASCADE,null=True)
    Date=models.DateField(null=True,auto_now=True)
    Action=models.CharField(null=True,max_length=255)
    
class Bloodgroup(models.Model):
    Blood_group=models.CharField(max_length=255,null=True)
    
class comment(models.Model):
    comment=models.CharField(null=True,max_length=255)
    login_details=models.ForeignKey(LoginDetails,on_delete=models.CASCADE,null=True)
    employee=models.ForeignKey(payroll_employee,on_delete=models.CASCADE,null=True)
#------------------------------------------------------------------end-------------------------------------------------------


class payroll_employee_comment(models.Model):
    comment=models.CharField(null=True,max_length=255)
    login_details=models.ForeignKey(LoginDetails,on_delete=models.CASCADE,null=True)
    employee=models.ForeignKey(payroll_employee,on_delete=models.CASCADE,null=True)
    
    
#----------------- Banking -----------------------------#

class Banking(models.Model):
    login_details = models.ForeignKey(LoginDetails, on_delete=models.CASCADE,null=True,blank=True)
    company=models.ForeignKey(CompanyDetails,on_delete=models.CASCADE)
    bnk_name = models.CharField(max_length=220,default='', null=True, blank=True)
    bnk_branch = models.CharField(max_length=220,default='', null=True, blank=True)
    bnk_acno = models.CharField(max_length=220,default='', null=True, blank=True)
    bnk_ifsc = models.CharField(max_length=220,default='', null=True, blank=True)
    BAL_TYPE = [
        ('Credit', 'Credit'),
        ('Debit', 'Debit'),
    ]
    bnk_bal_type = models.CharField(max_length=220,choices=BAL_TYPE, default='Debit')
    bnk_opnbal =models.FloatField(null=True, blank=True)
    bnk_bal =models.FloatField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    document=models.FileField(upload_to='bank/',null=True,blank=True)
    status= models.TextField(default='Active')

 
class BankTransaction(models.Model):
    login_details = models.ForeignKey(LoginDetails, on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(CompanyDetails,on_delete=models.CASCADE)
    banking = models.ForeignKey(Banking,on_delete=models.CASCADE)
    trans_cur_amount = models.FloatField(null=True, blank=True)
    trans_amount = models.FloatField(null=True, blank=True)
    trans_adj_amount = models.FloatField(null=True, blank=True)
    trans_adj_date = models.DateField(null=True, blank=True)

    TRANS_TYPE = [
        ('Opening Balance', 'Opening Balance'),
        ('Bank to Bank', 'Bank to Bank'),
        ('Bank to Cash', 'Bank to Cash'),
        ('Cash to Bank', 'Cash to Bank'),
        ('Bank Adjustment', 'Bank Adjustment'),
    ]
    trans_type = models.CharField(max_length=220,choices=TRANS_TYPE)

    ADJ_TYPE = [
        ('', ''),
        ('Balance Increase', 'Balance Increase'),
        ('Balance Decrease', 'Balance Decrease'),
    ]
    trans_adj_type = models.CharField(max_length=220,choices=ADJ_TYPE)
    trans_desc = models.CharField(max_length=220,null=True,blank=True)
    bank_to_bank_no = models.PositiveIntegerField(null=True,blank=True)


class BankingHistory(models.Model):
    login_details = models.ForeignKey(LoginDetails, on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(CompanyDetails,on_delete=models.CASCADE)
    banking = models.ForeignKey(Banking,on_delete=models.CASCADE)
    hist_adj_amount = models.FloatField(null=True, blank=True)
    hist_adj_date = models.DateField(auto_now_add=True, null=True, blank=True)
    ACTION_TYPE = [
        ('Created', 'Created'),
        ('Updated', 'Updated'),
    ]
    hist_action = models.CharField(max_length=220,choices=ACTION_TYPE)

class BankTransactionHistory(models.Model):
    login_details = models.ForeignKey(LoginDetails, on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(CompanyDetails,on_delete=models.CASCADE)
    transaction = models.ForeignKey(BankTransaction,on_delete=models.CASCADE,null=True,blank=True)
    hist_cur_amount = models.FloatField(null=True, blank=True)
    hist_amount = models.FloatField(null=True, blank=True)
    hist_adj_amount = models.FloatField(null=True, blank=True)
    hist_adj_date = models.DateField(auto_now_add=True, null=True, blank=True)
    ACTION_TYPE = [
        ('Created', 'Created'),
        ('Updated', 'Updated'),
    ]
    hist_action = models.CharField(max_length=220,choices=ACTION_TYPE)


class Customer(models.Model):
    login_details = models.ForeignKey(LoginDetails, on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(CompanyDetails,on_delete=models.CASCADE,null=True,blank=True)
    company_payment_terms = models.ForeignKey(Company_Payment_Term,on_delete=models.CASCADE,null=True,blank=True)

    customer_type = models.CharField(max_length=220,null=True,blank=True)
    title = models.CharField(max_length=220,null=True,blank=True)
    first_name = models.CharField(max_length=220,null=True,blank=True)
    last_name = models.CharField(max_length=220,null=True,blank=True)
    customer_display_name = models.CharField(max_length=220,null=True,blank=True)
    company_name = models.CharField(max_length=220,null=True,blank=True)
    customer_email = models.EmailField(max_length=255,null=True)
    customer_phone = models.CharField(max_length=220,null=True,blank=True)
    customer_mobile = models.CharField(max_length=220,null=True,blank=True)

    skype = models.CharField(max_length=220,null=True,blank=True)
    designation = models.CharField(max_length=220,null=True,blank=True)
    department = models.CharField(max_length=220,null=True,blank=True)
    website = models.CharField(max_length=220,null=True,blank=True)
    GST_treatement = models.CharField(max_length=220,null=True,blank=True)
    GST_number = models.CharField(max_length=220,null=True,blank=True)
    PAN_number = models.CharField(max_length=220,null=True,blank=True)
    place_of_supply = models.CharField(max_length=220,null=True,blank=True)
    tax_preference = models.CharField(max_length=220,null=True,blank=True)

    currency = models.CharField(max_length=220,null=True,blank=True)
    opening_balance_type = models.CharField(max_length=220,null=True,blank=True)
    opening_balance = models.FloatField(null=True, blank=True)
    credit_limit = models.FloatField(null=True, blank=True)
    price_list = models.CharField(max_length=220,null=True,blank=True)
    portal_language = models.CharField(max_length=220,null=True,blank=True)

    facebook = models.CharField(max_length=220,null=True,blank=True)
    twitter = models.CharField(max_length=220,null=True,blank=True)
    current_balance = models.FloatField(null=True, blank=True)

    billing_attention = models.CharField(max_length=220,null=True,blank=True)
    billing_address = models.CharField(max_length=220,null=True,blank=True)
    billing_city = models.CharField(max_length=220,null=True,blank=True)
    billing_state = models.CharField(max_length=220,null=True,blank=True)
    billing_country = models.CharField(max_length=220,null=True,blank=True)
    billing_pincode = models.CharField(max_length=220,null=True,blank=True)
    billing_mobile = models.CharField(max_length=220,null=True,blank=True)
    billing_fax = models.CharField(max_length=220,null=True,blank=True)

    shipping_attention = models.CharField(max_length=220,null=True,blank=True)
    shipping_address = models.CharField(max_length=220,null=True,blank=True)
    shipping_city = models.CharField(max_length=220,null=True,blank=True)
    shipping_state = models.CharField(max_length=220,null=True,blank=True)
    shipping_country = models.CharField(max_length=220,null=True,blank=True)
    shipping_pincode = models.CharField(max_length=220,null=True,blank=True)
    shipping_mobile = models.CharField(max_length=220,null=True,blank=True)
    shipping_fax = models.CharField(max_length=220,null=True,blank=True)

    remarks = models.CharField(max_length=220,null=True,blank=True)
    customer_status = models.CharField(max_length=220,null=True,blank=True)


class CustomerContactPersons(models.Model):
    login_details = models.ForeignKey(LoginDetails, on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(CompanyDetails,on_delete=models.CASCADE,null=True,blank=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True)

    title = models.CharField(max_length=220,null=True,blank=True)
    first_name = models.CharField(max_length=220,null=True,blank=True)
    last_name = models.CharField(max_length=220,null=True,blank=True)
    email = models.EmailField(max_length=220,null=True,blank=True)
    work_phone = models.CharField(max_length=220,null=True,blank=True)
    mobile = models.CharField(max_length=220,null=True,blank=True)
    skype = models.CharField(max_length=220,null=True,blank=True)
    designation = models.CharField(max_length=220,null=True,blank=True)
    department = models.CharField(max_length=220,null=True,blank=True)


class CustomerHistory(models.Model):
    login_details = models.ForeignKey(LoginDetails, on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(CompanyDetails,on_delete=models.CASCADE,null=True,blank=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True)

    action = models.CharField(max_length=220,null=True,blank=True)
    date = models.DateField(auto_now_add=True, null=True, blank=True)

class PriceList(models.Model):
    
    name = models.CharField(max_length=255, null=True)
    type_choices = [
        ('Sales', 'Sales'),('Purchase', 'Purchase'),]
    type = models.CharField(max_length=10, choices=type_choices, null=True)
    item_rate_choices = [('Percentage', 'Percentage'),('Each Item', 'Each Item'),]
    item_rate_type = models.CharField(max_length=15, choices=item_rate_choices, null=True)
    description = models.TextField(null=True)
    percentage_type_choices = [('Markup', 'Markup'),('Markdown', 'Markdown'),]
    percentage_type = models.CharField(max_length=10, choices=percentage_type_choices, null=True, blank=True)
    percentage_value = models.IntegerField(null=True, blank=True)
    round_off_choices = [
        ('Never Mind', 'Never Mind'),
        ('Nearest Whole Number', 'Nearest Whole Number'),
        ('0.99', '0.99'),
        ('0.50', '0.50'),
        ('0.49', '0.49'),
    ]
    round_off = models.CharField(max_length=20, choices=round_off_choices, null=True)
    currency_choices = [('Indian Rupee', 'Indian Rupee')]
    currency = models.CharField(max_length=20, choices=currency_choices, null=True)
    date = models.DateField(auto_now_add=True, null=True)
    STATUS_CHOICES = [('Active', 'Active'),('Inactive', 'Inactive'),]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    attachment = models.FileField(upload_to='price_list_attachment/', null=True, blank=True)

    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE)
    login_details = models.ForeignKey(LoginDetails, on_delete=models.CASCADE)

class PriceListItem(models.Model):
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE)
    login_details = models.ForeignKey(LoginDetails, on_delete=models.CASCADE)
    price_list = models.ForeignKey(PriceList, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)  
    standard_rate = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    custom_rate = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)


class Customer_remarks_table(models.Model):
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    remarks=models.CharField(max_length=500)   

class Customer_comments_table(models.Model):
    login_details=models.ForeignKey(LoginDetails,on_delete=models.CASCADE,null=True)
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    comment=models.TextField(max_length=500)  

class Customer_doc_upload_table(models.Model):
    login_details=models.ForeignKey(LoginDetails,on_delete=models.CASCADE,null=True)
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    title=models.TextField(max_length=200)
    document=models.FileField(upload_to='doc/')  


