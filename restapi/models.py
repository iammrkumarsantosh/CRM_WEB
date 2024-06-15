from pyexpat import model
from django.db import models
from datetime import date

# Create your models here.
class UserType(models.Model):
    role_name = models.CharField(max_length=100,null=False,blank=False,unique=True)
    is_valid = models.IntegerField()
    
    def __str__(self):
        return (self.role_name)


class Country(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)
    is_valid = models.IntegerField()

    def __str__(self):
        return (self.name)


class Disease(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)
    is_valid = models.IntegerField()
    
    def __str__(self):
        return (self.name)


class State(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)
    is_valid = models.IntegerField()
    
    def __str__(self):
        return (self.name)


class UserRole(models.Model):
    create_emp = models.IntegerField()
    export_report = models.IntegerField()
    emp_pwd_update = models.IntegerField()
    emp_valid_mark = models.IntegerField()
    user_type = models.ForeignKey(UserType,on_delete=models.CASCADE)


class HealthCardType(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)
    is_valid = models.IntegerField()
    
    def __str__(self):
        return (self.name)


class CareOf(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)
    is_valid = models.IntegerField()
    
    def __str__(self):
        return (self.name)


class HealthCardTypeCategory(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)
    is_valid = models.IntegerField()
    
    def __str__(self):
        return (self.name)


class AppUser(models.Model):
    username = models.CharField(max_length=200,null=False,blank=False,unique=True)
    password = models.CharField(max_length=500,null=False,blank=False)
    pass_code = models.CharField(max_length=500,null=False,blank=False)
    first_name = models.CharField(max_length=200,null=False,blank=False)
    last_name = models.CharField(max_length=200,null=False,blank=False)
    gender = models.CharField(max_length=50,null=False,blank=False)
    dob = models.DateField()
    user_type = models.ForeignKey(UserType,on_delete=models.CASCADE)
    email = models.EmailField()
    mobile = models.CharField(max_length=50)
    is_valid = models.IntegerField()
    join_datetime = models.DateTimeField(auto_now_add=True)
    last_login_datetime = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return (self.username)


class Employee(models.Model):    
    first_name = models.CharField(max_length=200,null=False,blank=False)
    last_name = models.CharField(max_length=200,null=False,blank=False)
    gender = models.CharField(max_length=50,null=False,blank=False)
    dob = models.DateField()
    user_type = models.ForeignKey(UserType,on_delete=models.CASCADE)
    email = models.EmailField()
    mobile = models.CharField(max_length=50)
    is_valid = models.IntegerField()
    join_datetime = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    reporting_manager = models.IntegerField()
    app_user = models.ForeignKey(AppUser,on_delete=models.CASCADE)
    
    def __str__(self):
        return (self.first_name)


class Clinic(models.Model):    
    name = models.CharField(max_length=200,null=False,blank=False)
    start_date = models.DateField()
    is_valid = models.IntegerField()
    phone = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    clinic_timing = models.CharField(max_length=500)
    latitude = models.CharField(max_length=250)
    longitude = models.CharField(max_length=250)
    app_user = models.ForeignKey(AppUser,on_delete=models.CASCADE)
    code = models.CharField(max_length=5, default='JS')
    
    def __str__(self):
        return (self.name)


class Attendance(models.Model):    
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    login_time = models.TimeField()
    logout_time = models.TimeField()
    date = models.DateField()
    latitude = models.CharField(max_length=250)
    longitude = models.CharField(max_length=250)
    out_latitude = models.CharField(max_length=250,default=0)
    out_longitude = models.CharField(max_length=250,default=0)


class UserRequest(models.Model):    
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=200,null=False,blank=False,default=0)
    mobile_2 = models.CharField(max_length=200,null=False,blank=False,default=0)
    datetime = models.DateTimeField()
    first_name = models.CharField(max_length=200,null=False,blank=False)
    last_name = models.CharField(max_length=200,null=False,blank=False)
    care_of = models.CharField(max_length=250,default=0)
    care_of_type = models.IntegerField(default=0)
    gender = models.CharField(max_length=50,null=False,blank=False)
    dob = models.DateField()
    age = models.IntegerField()
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    state = models.IntegerField(default=0)
    country = models.IntegerField(default=0)
    clinic = models.IntegerField(default=0)
    disease = models.IntegerField(default=0)
    appointment_datetime = models.DateTimeField()
    remark = models.CharField(max_length=500)
    is_clinic_visit = models.IntegerField()
    is_treatment_start = models.IntegerField()
    health_card_type = models.IntegerField(default=0)
    health_card_type_cat = models.IntegerField(default=0)
    health_card_number = models.CharField(max_length=250)

class Patient(models.Model):    
    patient_uhid = models.CharField(max_length=250,unique=True)
    old_uhid = models.CharField(max_length=250,default=0)
    user_request = models.IntegerField(default=0)
    first_name = models.CharField(max_length=200,null=False,blank=False)
    last_name = models.CharField(max_length=200,null=False,blank=False)
    care_of_type = models.IntegerField(default=0)
    care_of = models.CharField(max_length=250,default=0)
    gender = models.CharField(max_length=50,null=False,blank=False)
    dob = models.DateField()
    age = models.IntegerField()
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    state = models.IntegerField(default=0)
    country = models.IntegerField(default=0)
    clinic = models.IntegerField(default=0)
    disease = models.IntegerField(default=0)
    remark = models.CharField(max_length=500)
    total_service = models.IntegerField()
    health_card_type = models.IntegerField(default=0)
    health_card_category = models.IntegerField(default=0)
    health_card_number = models.CharField(max_length=250)
    patient_source = models.CharField(max_length=250)
    referral_number = models.CharField(max_length=250,default=0)
    referral_date = models.DateField()
    date = models.DateField(default=date.today().isoformat())
    mobile = models.CharField(max_length=50,default='-')
    alt_mobile = models.CharField(max_length=50,default='-')
    pin_code = models.CharField(max_length=50,default='-')
    blood_group = models.CharField(max_length=50,default='-')
    occupation = models.CharField(max_length=500,default='-')
    religion = models.CharField(max_length=500,default='-')
    email = models.CharField(max_length=500,default='-')
    marital_status = models.CharField(max_length=500,default='-')

    def __str__(self):
        return (self.patient_uhid)



class MedicineSet(models.Model):
    name =  models.CharField(max_length=250,null=False,blank=False)    
    price = models.IntegerField()
    is_valid =  models.IntegerField()
    
    def __str__(self):
        return (self.name)


class TherapySet(models.Model):
    name =  models.CharField(max_length=250,null=False,blank=False)
    discription = models.CharField(max_length=250,default=0)
    duration =  models.CharField(max_length=250,default=0)
    price = models.IntegerField()
    is_valid =  models.IntegerField()
    
    def __str__(self):
        return (self.name)


class Treatment(models.Model):
    patient =  models.ForeignKey(Patient,on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    doctor = models.IntegerField(default=0)
    opd_no = models.CharField(max_length=10,default=0)
    ipd_no = models.CharField(max_length=10,default=0)
    disease = models.IntegerField(default=0)
    remark =  models.CharField(max_length=2000)
    medicine = models.IntegerField(default=0)
    therapy = models.IntegerField(default=0)
    is_complete = models.IntegerField(default=0)
    bp = models.CharField(max_length=500,default=0)
    sugar = models.CharField(max_length=500,default=0)
    weight = models.CharField(max_length=500,default=0)
    referral_number = models.CharField(max_length=250,default=0)
    referral_date = models.CharField(max_length=250,default='-')
    health_card_type = models.IntegerField(default=0)
    health_card_category = models.IntegerField(default=0)
    health_card_number = models.CharField(max_length=250,default='-')
    referral_status = models.CharField(max_length=250,default='-')


class PatientTreatment(models.Model):
    patient =  models.ForeignKey(Patient,on_delete=models.CASCADE)
    startdate = models.DateField()
    enddate = models.DateField(default=date.today().isoformat())
    status = models.IntegerField(default=0)
    file_status = models.IntegerField(default=0)
    file_date = models.DateField(default=date.today().isoformat())
    therapy = models.IntegerField(default=0)
    billing_status = models.IntegerField(default=0)
    billing_date = models.DateField(default=date.today().isoformat())
    inserted_on = models.DateTimeField(auto_now_add=True)
    time = models.TimeField(default='01:00')

class ClinicDoctor(models.Model):
    clinic =  models.ForeignKey(Clinic,on_delete=models.CASCADE)
    doctor = models.ForeignKey(Employee,on_delete=models.CASCADE)
    is_valid =  models.IntegerField()
    fee = models.IntegerField(default=500)

class Payment(models.Model):
    clinic =  models.ForeignKey(Clinic,on_delete=models.CASCADE)
    patient =  models.ForeignKey(Patient,on_delete=models.CASCADE)
    date = models.DateField(default=date.today().isoformat())
    fee = models.IntegerField()
    title = models.CharField(max_length=500,default='Fee')
    payment_type = models.CharField(max_length=500)
    transaction_num = models.CharField(max_length=500)

class PaymentType(models.Model):
    name =  models.CharField(max_length=500)
    is_valid =  models.IntegerField()

class DocType(models.Model):
    name =  models.CharField(max_length=500)
    is_valid =  models.IntegerField()

class Docs(models.Model):
    patient =  models.ForeignKey(Patient,on_delete=models.CASCADE)
    date = models.DateField(default=date.today().isoformat())
    remark = models.CharField(max_length=1000,default='-')
    file_name = models.CharField(max_length=1000,default='-')

class ChangeLog(models.Model):
    change_name = models.CharField(max_length=500,default='-')
    old_value = models.CharField(max_length=4000,default='-')
    new_value = models.CharField(max_length=4000,default='-')
    login_id = models.IntegerField()    
    inserted_on = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return (self.change_name)  