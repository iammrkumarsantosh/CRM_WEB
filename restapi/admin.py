from django.contrib import admin

# Register your models here.
from . models import ChangeLog, DocType, Docs, PatientTreatment, Payment, PaymentType, UserType,Country,Disease,State,UserRole,HealthCardType,AppUser,Employee,Clinic,Attendance,UserRequest,Patient,Treatment,ClinicDoctor,MedicineSet,TherapySet,HealthCardTypeCategory,CareOf

# Register your models here.
@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
 list_display =['id','role_name','is_valid']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
 list_display =['id','name','is_valid']


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
 list_display =['id','name','is_valid']

@admin.register(CareOf)
class CareOfAdmin(admin.ModelAdmin):
 list_display =['id','name','is_valid'] 

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
 list_display =['id','name','is_valid']


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
 list_display =['id','create_emp','export_report','emp_pwd_update','emp_valid_mark','user_type']


@admin.register(HealthCardType)
class HealthCardTypeAdmin(admin.ModelAdmin):
 list_display =['id','name','is_valid']

@admin.register(HealthCardTypeCategory)
class HealthCardTypeCategoryAdmin(admin.ModelAdmin):
 list_display =['id','name','is_valid']

@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
 list_display =['id','username','password','pass_code','first_name','last_name','gender','dob','user_type','email','mobile','is_valid','join_datetime','last_login_datetime']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
 list_display =['id','first_name','last_name','gender','dob','user_type_id','email','mobile','is_valid','join_datetime','address','city','state','country', 'reporting_manager','app_user']

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
 list_display =['id','name','code','start_date','is_valid','phone','mobile','address','city','state','country','clinic_timing','latitude','longitude','app_user']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
 list_display =['id','employee','login_time','logout_time','date','latitude','longitude','out_latitude','out_longitude']


@admin.register(UserRequest)
class UserRequestAdmin(admin.ModelAdmin):
 list_display =['id','mobile','mobile_2','employee','datetime','first_name','last_name','care_of','care_of_type','gender','dob','age','address','city','state','country','clinic','disease','appointment_datetime','remark','is_clinic_visit','is_treatment_start','health_card_type','health_card_type_cat','health_card_number']


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
 list_display =['id','patient_uhid','old_uhid','date','mobile','alt_mobile','pin_code','user_request','first_name','last_name','care_of','care_of_type','gender','dob','age','address','city','state','country','clinic','disease','remark','total_service','health_card_type','health_card_number','patient_source','referral_number','referral_date','blood_group','occupation','religion','email','marital_status']


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
 list_display =['id','opd_no','ipd_no','disease','patient','datetime','doctor','remark','medicine','therapy','is_complete','bp','sugar','weight','referral_number','referral_date','health_card_type','health_card_category','health_card_number','referral_status']


@admin.register(ClinicDoctor)
class ClinicDoctorAdmin(admin.ModelAdmin):
 list_display =['id','clinic','doctor','is_valid','fee']


@admin.register(MedicineSet)
class MedicineSetAdmin(admin.ModelAdmin):
 list_display =['id','name','price','is_valid']


@admin.register(TherapySet)
class TherapySetAdmin(admin.ModelAdmin):
 list_display =['id','name','discription','duration','price','is_valid']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
 list_display =['id','clinic','patient','date','title','fee','payment_type','transaction_num']


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
 list_display =['id','name','is_valid'] 

@admin.register(DocType)
class DocTypeAdmin(admin.ModelAdmin):
 list_display =['id','name','is_valid']

@admin.register(Docs)
class DocsAdmin(admin.ModelAdmin):
 list_display =['id','patient','date','remark','file_name']

@admin.register(PatientTreatment)
class PatientTreatmentAdmin(admin.ModelAdmin):
 list_display =['id','patient','startdate','time','enddate','status','file_status','file_date','therapy','billing_status','billing_date','inserted_on'] 

@admin.register(ChangeLog)
class DocsAdmin(admin.ModelAdmin):
 list_display =['id','change_name','old_value','new_value','login_id','inserted_on'] 