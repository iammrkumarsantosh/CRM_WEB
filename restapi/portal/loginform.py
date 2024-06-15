from django import forms

class LoginForm(forms.Form):
   username = forms.CharField(max_length = 500)
   password = forms.CharField(widget = forms.PasswordInput())

class ProfileForm(forms.Form):
   employee_id = forms.CharField(max_length = 500)
   first_name = forms.CharField(max_length = 500)
   last_name = forms.CharField(max_length = 500)
   gender = forms.CharField(max_length = 500)
   password = forms.CharField(widget = forms.PasswordInput())
   confirm_password = forms.CharField(widget = forms.PasswordInput())

class AddNewUserForm(forms.Form):  
   employee_id = forms.CharField(max_length = 500)
   rid = forms.IntegerField()
   mobile = forms.CharField(max_length = 500)
   mobile_2 = forms.CharField(max_length = 500)
   first_name = forms.CharField(max_length = 500)
   last_name = forms.CharField(max_length = 500)
   gender = forms.CharField(max_length = 500)
   age = forms.CharField(max_length = 500)
   care_of_type = forms.IntegerField()
   care_of = forms.CharField(max_length = 500)
   address = forms.CharField(max_length = 500)
   city = forms.CharField(max_length = 500)
   state = forms.IntegerField()
   country = forms.IntegerField()
   clinic = forms.IntegerField()
   symptoms = forms.IntegerField()
   hctype = forms.IntegerField()
   hctypeCat = forms.IntegerField()
   hcnumber = forms.CharField(max_length = 500)
   date = forms.CharField(max_length = 500)
   remark = forms.CharField(max_length = 500)


class AddNewPatientForm(forms.Form):
   employee_id = forms.CharField(max_length = 500)
   request_id = forms.IntegerField()
   mobile = forms.CharField(max_length = 500)
   first_name = forms.CharField(max_length = 500)
   last_name = forms.CharField(max_length = 500)
   gender = forms.CharField(max_length = 500)
   age = forms.CharField(max_length = 500)
   care_of_type = forms.IntegerField()
   care_of = forms.CharField(max_length = 500)
   address = forms.CharField(max_length = 500)
   city = forms.CharField(max_length = 500)
   pincode = forms.CharField(max_length = 500)
   state = forms.IntegerField()
   country = forms.IntegerField()
   clinic = forms.IntegerField()
   patient_source = forms.CharField(max_length = 500)
   symptoms = forms.IntegerField()
   hctype = forms.IntegerField()
   hctypeCat = forms.IntegerField()
   hcnumber = forms.CharField(max_length = 500)      
   referral_number = forms.CharField(max_length = 500)
   referral_date = forms.CharField(max_length = 500)
   total_service = forms.IntegerField()
   remark = forms.CharField(max_length = 500)  
   doctor_id = forms.IntegerField() 
   fee = forms.IntegerField()
   payment_type = forms.CharField(max_length = 500)  
   transaction_num = forms.CharField(max_length = 500)  


class PatientSearchForm(forms.Form):  
   start_date = forms.CharField(max_length = 500)
   end_date = forms.CharField(max_length = 500)

class BookDoctorForm(forms.Form):
   doctor_id = forms.CharField(max_length = 500)
   puid = forms.CharField(max_length = 500)
   employee_id = forms.CharField(max_length = 500)
   symptoms = forms.IntegerField()

class AddEmployeeForm(forms.Form):
   employee_id = forms.CharField(max_length = 500)
   edit_id = forms.CharField(max_length = 500)
   emp_type = forms.IntegerField()
   username = forms.CharField(max_length = 500)
   password = forms.CharField(max_length = 500)
   first_name = forms.CharField(max_length = 500)
   last_name = forms.CharField(max_length = 500)
   gender = forms.CharField(max_length = 500)
   mobile = forms.CharField(max_length = 500)
