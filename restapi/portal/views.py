from django.shortcuts import render
from cryptography.fernet import Fernet
from restapi.models import AppUser, Attendance, ClinicDoctor, Country, Docs, Employee, MedicineSet, Patient, PatientTreatment, Payment, PaymentType, TherapySet, Treatment, UserRequest, State, CareOf,Clinic,Disease,HealthCardType,HealthCardTypeCategory, UserType
from restapi.serializers import ChangeLogSerializer, ClinicDoctorSerializer, CountrySerializer, DocsSerializer, PatientSerializer, PatientTreatmentSerializer, PaymentSerializer, PaymentTypeSerializer, StateSerializer, CareOfSerializer,ClinicSerializer,DiseaseSerializer,HealthCardTypeSerializer,HealthCardTypeCategorySerializer, TherapySetSerializer, TreatmentSerializer,UserRequestSerializer,EmployeeSerializer,AppUserSerializer
from restapi.portal.loginform import LoginForm,AddNewUserForm,ProfileForm,PatientSearchForm,AddNewPatientForm,AddEmployeeForm
from datetime import date, datetime
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
import json
import xlwt

# Create your views here.
def PortalLoginPage(request):    
    if request.session.get('login_user', False):
        return dashboard_loading(request)

    return render(request,"auth-login-basic.html",{'error':'N'})

def Logout(request):
    try:
        del request.session['login_user']
    except KeyError:
        pass
    return render(request,"auth-login-basic.html",{'error':'N'})

def PortalLoginAction(request):  
    input_username = ""
    input_password = ""
    pwd_key = b'DRgiuOgIANXfB1j_BC9zFsjTfxA4GOCCSBc2iKz9mGw='
    fernet = Fernet(pwd_key)
    #ciphered_text = fernet.encrypt(bytes('crm@2024', 'utf-8'))
    #print(ciphered_text)
    user_found = False
    is_login = False
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            input_username = login_form.cleaned_data['username']
            input_password = login_form.cleaned_data['password']
            try:
                input_username = input_username.lower()
                appUser = AppUser.objects.get(username__iexact=input_username) 
                pwd = appUser.password
                pwd_code = appUser.pass_code
                d_pwd = fernet.decrypt(bytes(pwd,'utf-8')).decode()
                d_pwd_code = fernet.decrypt(bytes(pwd_code,'utf-8')).decode()
                if d_pwd == input_password:
                    user_found = True
                elif d_pwd_code == input_password:
                    user_found = True

                if user_found == True:
                    request.session['login_user'] = input_username
                    is_login = True

            except AppUser.DoesNotExist:
                user_found = False

    if is_login == False:
        return render(request,"auth-login-basic.html",{'error':'Y'})

    return dashboard_loading(request) 


def dashboard_loading(request):
    if request.session.get('login_user', False):
        input_username = request.session.get('login_user', False)
        return DashboardData(request,input_username) 

    return render(request,"auth-login-basic.html",{'error':'Y'})

def PortalDashboardAction(request):    
    return dashboard_loading(request)

def DashboardData(request,input_username):
    try:
        today = date.today().isoformat()
        mydate = datetime.now()
        monthname = mydate.strftime("%B")
        date_arr = today.split("-")
        appUser = AppUser.objects.get(username=input_username) 
        fullname = ""
        data_set_1 = 0
        data_set_1_all = 0
        data_set_1_title = ""
        data_set_2 = 0
        data_set_2_all = 0
        data_set_2_title = ""
        data_set_3 = 0
        data_set_3_all = 0
        data_set_3_title = ""
        data_set_4 = 0
        data_set_4_all = 0
        data_set_4_title = ""
        data_set_5_title = ""
        data_set_5 = 0
        data_set_5_all = 0
        data_set_6_title = ""
        data_set_6 = 0
        data_set_6_all = 0
        data_set_7_title = ""
        data_set_7 = 0
        data_set_7_all = 0
        employee_id = 0
        first_name = ""
        last_name = ""
        gender = ""
        viewdata = {}
        page = "DASH"
        view_type = 0
        state_name = ""
        state_id = 0
        error_str = request.GET.get('error')
        country = Country.objects.filter(is_valid=1)
        country_list = CountrySerializer(country,many=True).data
        state = State.objects.filter(is_valid=1)
        state_list = StateSerializer(state,many=True).data
        careof = CareOf.objects.filter(is_valid=1)
        careof_list = CareOfSerializer(careof,many=True).data
        disease = Disease.objects.filter(is_valid=1)
        disease_list = DiseaseSerializer(disease,many=True).data
        therapy_set = TherapySet.objects.filter(is_valid=1)
        therapy_set_list = TherapySetSerializer(therapy_set,many=True).data
        healthCardType = HealthCardType.objects.filter(is_valid=1)
        healthCardType_list = HealthCardTypeSerializer(healthCardType,many=True).data
        healthCardTypeCategory = HealthCardTypeCategory.objects.filter(is_valid=1)
        healthCardTypeCategory_list = HealthCardTypeCategorySerializer(healthCardTypeCategory,many=True).data
        clinic_all = Clinic.objects.filter(is_valid=1)
        clinic_list = ClinicSerializer(clinic_all,many=True).data
        doctor_list = Employee.objects.filter(user_type=3)
        paymentType = PaymentType.objects.filter(is_valid=1)        
        payment_type_list = PaymentTypeSerializer(paymentType,many=True).data
        if appUser.user_type.id == 2 or appUser.user_type.id == 7 or appUser.user_type.id == 8:
            try:
                if appUser.user_type.id == 2 :
                    clinic = Clinic.objects.get(app_user=appUser)
                elif appUser.user_type.id == 7 :
                    mngr = Employee.objects.get(app_user=appUser)
                    clinic = Clinic.objects.get(id=mngr.reporting_manager)
                
                if appUser.user_type.id != 8:
                    cld_list = ClinicDoctor.objects.filter(clinic=clinic,is_valid=1)
                    fullname = clinic.name                
                    employee_id = clinic.id
                elif appUser.user_type.id == 8:
                    cld_list = ClinicDoctor.objects.filter(is_valid=1)
                    fullname = "Hospital"
                    employee_id = 0
                didarr = []
                for d in cld_list:
                    didarr.append(d.doctor.id)

                doctor_list = doctor_list.filter(id__in=didarr)
                first_name = appUser.first_name
                last_name = appUser.last_name
                gender = appUser.gender
                data_set_1_title = "Today Appointment"        
                data_set_2_title = "Total Appointment"
                data_set_3_title = "New Patient"
                data_set_4_title = "Old Patient"
                data_set_5_title = "Male Patient"
                data_set_6_title = "Female Patient"
                data_set_7_title = "Total Patient"
                if appUser.user_type.id != 8:
                    userRequest = UserRequest.objects.filter(clinic=clinic.id,appointment_datetime__month=date_arr[1],appointment_datetime__year=date_arr[0])
                    ur_all = UserRequest.objects.filter(clinic=clinic.id)
                else:
                    userRequest = UserRequest.objects.filter(appointment_datetime__month=date_arr[1],appointment_datetime__year=date_arr[0])    
                    ur_all = UserRequest.objects.filter(appointment_datetime__year=date_arr[0])
                clinicVisited = userRequest.filter(is_clinic_visit=1,is_treatment_start=0)
                cv_all = ur_all.filter(is_clinic_visit=1,is_treatment_start=0)
                todayRequest = userRequest.filter(appointment_datetime__date = today,is_clinic_visit=0)                
                tr_all = ur_all.filter(appointment_datetime__date = today,is_clinic_visit=0)
                total_patient = 0
                if appUser.user_type.id != 8:
                    state_name = clinic.state.name
                    state_id = clinic.state.id
                else:
                    state_name = "Hospital"
                    state_id = 0
                
                try:
                    old_count = 0
                    new_count = 0
                    old_count_all = 0
                    new_count_all = 0
                    if appUser.user_type.id != 8:
                        patient = Patient.objects.filter(clinic=clinic.id,date__month=date_arr[1],date__year=date_arr[0])
                        pt_all = Patient.objects.filter(clinic=clinic.id)
                    else:
                        patient = Patient.objects.filter(date__month=date_arr[1],date__year=date_arr[0])    
                        pt_all = Patient.objects.filter(date__year=date_arr[0])    
                    for p in patient:
                        treatment_list = Treatment.objects.filter(patient=p)
                        if len(treatment_list) > 1:
                            old_count = old_count+1
                        elif len(treatment_list) == 1:
                            new_count = new_count+1
                    for p in pt_all:
                        treatment_list = Treatment.objects.filter(patient=p)
                        if len(treatment_list) > 1:
                            old_count_all = old_count_all+1
                        elif len(treatment_list) == 1:
                            new_count_all = new_count_all+1    
                    total_patient = len(patient)
                    male_patient = patient.filter(gender='Male')
                    female_patient = patient.filter(gender='Female')

                    total_patient_all = len(pt_all)
                    male_patient_all = pt_all.filter(gender='Male')
                    female_patient_all = pt_all.filter(gender='Female')
                except Patient.DoesNotExist:
                    None
                data_set_1 = len(todayRequest)
                data_set_1_all = data_set_1
                data_set_2 = len(userRequest)
                data_set_2_all = len(ur_all)
                data_set_3 = new_count
                data_set_3_all = new_count_all
                data_set_4 = old_count
                data_set_4_all = old_count_all
                data_set_5 = len(male_patient)
                data_set_5_all = len(male_patient_all)
                data_set_6 = len(female_patient)
                data_set_6_all = len(female_patient_all)
                data_set_7 = total_patient
                data_set_7_all = total_patient_all
            except Clinic.DoesNotExist:
                None  
        
        if appUser.user_type.id != 2:
            try:
                employee = Employee.objects.get(app_user=appUser)
                fullname = employee.first_name+" "+employee.last_name
                employee_id = employee.id
                first_name = employee.first_name
                last_name = employee.last_name
                gender = employee.gender                
                if appUser.user_type.id in [5,6]:
                    userRequest = UserRequest.objects.filter(employee=employee,datetime__month=date_arr[1],datetime__year=date_arr[0])
                    ur_all = UserRequest.objects.filter(employee=employee)
                    clinicVisited = userRequest.filter(is_clinic_visit=1,is_treatment_start=0)
                    treatmentStart = userRequest.filter(is_treatment_start=1)
                    todayRequest = userRequest.filter(datetime__date = today)
                    cv_all = ur_all.filter(is_clinic_visit=1,is_treatment_start=0)
                    ts_all = ur_all.filter(is_treatment_start=1)
                    tr_all = ur_all.filter(datetime__date = today)
                    data_set_1 = len(todayRequest)
                    data_set_1_all = len(tr_all)
                    data_set_1_title = "Today Request"
                    data_set_2 = len(userRequest)
                    data_set_2_all = len(ur_all)
                    data_set_2_title = monthname+" Request"
                    data_set_3 = len(clinicVisited)
                    data_set_3_all = len(cv_all)
                    data_set_3_title = "Clinic Visited"
                    data_set_4 = len(treatmentStart)
                    data_set_4_all = len(ts_all)
                    data_set_4_title = "Treatment Start"
                elif appUser.user_type.id == 4:
                    list_emp = Employee.objects.filter(reporting_manager = employee.id)                    
                    userRequest = UserRequest.objects.filter(employee__in=list_emp,datetime__month=date_arr[1],datetime__year=date_arr[0])
                    ur_all = UserRequest.objects.filter(employee__in=list_emp)
                    clinicVisited = userRequest.filter(is_clinic_visit=1,is_treatment_start=0)
                    treatmentStart = userRequest.filter(is_treatment_start=1)
                    todayRequest = userRequest.filter(datetime__date = today)
                    cv_all = ur_all.filter(is_clinic_visit=1,is_treatment_start=0)
                    ts_all = ur_all.filter(is_treatment_start=1)
                    tr_all = ur_all.filter(datetime__date = today)
                    data_set_1 = len(todayRequest)
                    data_set_1_all = len(tr_all)
                    data_set_1_title = "Today Request"
                    data_set_2 = len(userRequest)
                    data_set_2_all = len(ur_all)
                    data_set_2_title = monthname+" Request"
                    data_set_3 = len(clinicVisited)
                    data_set_3_all = len(cv_all)
                    data_set_3_title = "Clinic Visited"
                    data_set_4 = len(treatmentStart)
                    data_set_4_all = len(ts_all)
                    data_set_4_title = "Treatment Start"
            except Employee.DoesNotExist:
                None

        if appUser.user_type.id == 9:
            patientTreatment = PatientTreatment.objects.filter(startdate__month=date_arr[1],startdate__year=date_arr[0])
            pt_all = PatientTreatment.objects.filter(startdate__year=date_arr[0])
            pendingPT = patientTreatment.filter(billing_status=0)
            completePT = patientTreatment.filter(billing_status=1)
            pendingPT_all = pt_all.filter(billing_status=0)
            completePT_all = pt_all.filter(billing_status=1)
            data_set_1_title = "Pending Bill"
            data_set_2_title = "Complete Bill"
            data_set_1 = len(pendingPT)
            data_set_2 = len(completePT)
            data_set_1_all = len(pendingPT_all)
            data_set_2_all = len(completePT_all)
                
        param_page = request.GET.get('page')
        page = param_page                                
        if page == 'view':
            view_type = int(request.GET.get('type'))
            viewdata = ViewData(request)

        if page == 'patientdata':
            if request.method == "POST":
                viewdata = getPatientData(request)

        if page == 'export-data-emp':
            if request.method == "POST":
                viewdata = getEmpData(request)  

        if page == 'attendance':
            if request.method == "POST":    
                viewdata = getAttendanceData(request)      

        if page == 'bookdoctor':
            viewdata = getBookDoctorPage(request)

        if page == 'doctor':
            if request.GET.get('id') is not None:
                viewdata = getDoctorData(request)    

        if page == 'treatment':
            if request.GET.get('p') is not None:
                viewdata = getTreatmentData(request)    

        if page == 'employee-view':
            viewdata = getEmployeeViewData(request,employee_id)

        if page == 'clinic-doctor':
            viewdata = getClinicDoctor(request,employee_id)    

        if page == 'add-new-request':
            if request.GET.get('rid') is not None:
                viewdata = getURRequestData(request)   

        if page == 'add-new-employee':
            if request.GET.get('edit') is not None:
                viewdata = getEditEmpData(request)        

        if page == 'editinfo':
            if request.GET.get('uhid') is not None:
                viewdata = getEditPatientData(request)

        new_str = int(date_arr[0])
        old_str = new_str - 1
        old_1 = 0
        old_2 = 0
        old_3 = 0
        old_4 = 0
        old_5 = 0
        old_6 = 0
        old_7 = 0
        old_8 = 0
        old_9 = 0
        old_10 = 0
        old_11 = 0
        old_12 = 0
        new_1 = 0
        new_2 = 0
        new_3 = 0
        new_4 = 0
        new_5 = 0
        new_6 = 0
        new_7 = 0
        new_8 = 0
        new_9 = 0
        new_10 = 0
        new_11 = 0
        new_12 = 0
        if appUser.user_type.id == 2 or appUser.user_type.id == 7 or appUser.user_type.id == 8:
            c_emp_id = employee_id
            if appUser.user_type.id == 7:
                 mngr = Employee.objects.get(app_user=appUser)
                 c_emp_id = mngr.reporting_manager
            if appUser.user_type.id == 8:
                old_1 = len(Patient.objects.filter(date__month='01',date__year=old_str))
                old_2 = len(Patient.objects.filter(date__month='02',date__year=old_str))
                old_3 = len(Patient.objects.filter(date__month='03',date__year=old_str))
                old_4 = len(Patient.objects.filter(date__month='04',date__year=old_str))
                old_5 = len(Patient.objects.filter(date__month='05',date__year=old_str))
                old_6 = len(Patient.objects.filter(date__month='06',date__year=old_str))
                old_7 = len(Patient.objects.filter(date__month='07',date__year=old_str))
                old_8 = len(Patient.objects.filter(date__month='08',date__year=old_str))
                old_9 = len(Patient.objects.filter(date__month='09',date__year=old_str))
                old_10 = len(Patient.objects.filter(date__month='10',date__year=old_str))
                old_11 = len(Patient.objects.filter(date__month='11',date__year=old_str))
                old_12 = len(Patient.objects.filter(date__month='12',date__year=old_str))
                new_1 = len(Patient.objects.filter(date__month='01',date__year=new_str))
                new_2 = len(Patient.objects.filter(date__month='02',date__year=new_str))
                new_3 = len(Patient.objects.filter(date__month='03',date__year=new_str))
                new_4 = len(Patient.objects.filter(date__month='04',date__year=new_str))
                new_5 = len(Patient.objects.filter(date__month='05',date__year=new_str))
                new_6 = len(Patient.objects.filter(date__month='06',date__year=new_str))
                new_7 = len(Patient.objects.filter(date__month='07',date__year=new_str))
                new_8 = len(Patient.objects.filter(date__month='08',date__year=new_str))
                new_9 = len(Patient.objects.filter(date__month='09',date__year=new_str))
                new_10 = len(Patient.objects.filter(date__month='10',date__year=new_str))
                new_11 = len(Patient.objects.filter(date__month='11',date__year=new_str))
                new_12 = len(Patient.objects.filter(date__month='12',date__year=new_str))
            else:        
                old_1 = len(Patient.objects.filter(clinic=c_emp_id,date__month='01',date__year=old_str))
                old_2 = len(Patient.objects.filter(clinic=c_emp_id,date__month='02',date__year=old_str))
                old_3 = len(Patient.objects.filter(clinic=c_emp_id,date__month='03',date__year=old_str))
                old_4 = len(Patient.objects.filter(clinic=c_emp_id,date__month='04',date__year=old_str))
                old_5 = len(Patient.objects.filter(clinic=c_emp_id,date__month='05',date__year=old_str))
                old_6 = len(Patient.objects.filter(clinic=c_emp_id,date__month='06',date__year=old_str))
                old_7 = len(Patient.objects.filter(clinic=c_emp_id,date__month='07',date__year=old_str))
                old_8 = len(Patient.objects.filter(clinic=c_emp_id,date__month='08',date__year=old_str))
                old_9 = len(Patient.objects.filter(clinic=c_emp_id,date__month='09',date__year=old_str))
                old_10 = len(Patient.objects.filter(clinic=c_emp_id,date__month='10',date__year=old_str))
                old_11 = len(Patient.objects.filter(clinic=c_emp_id,date__month='11',date__year=old_str))
                old_12 = len(Patient.objects.filter(clinic=c_emp_id,date__month='12',date__year=old_str))
                new_1 = len(Patient.objects.filter(clinic=c_emp_id,date__month='01',date__year=new_str))
                new_2 = len(Patient.objects.filter(clinic=c_emp_id,date__month='02',date__year=new_str))
                new_3 = len(Patient.objects.filter(clinic=c_emp_id,date__month='03',date__year=new_str))
                new_4 = len(Patient.objects.filter(clinic=c_emp_id,date__month='04',date__year=new_str))
                new_5 = len(Patient.objects.filter(clinic=c_emp_id,date__month='05',date__year=new_str))
                new_6 = len(Patient.objects.filter(clinic=c_emp_id,date__month='06',date__year=new_str))
                new_7 = len(Patient.objects.filter(clinic=c_emp_id,date__month='07',date__year=new_str))
                new_8 = len(Patient.objects.filter(clinic=c_emp_id,date__month='08',date__year=new_str))
                new_9 = len(Patient.objects.filter(clinic=c_emp_id,date__month='09',date__year=new_str))
                new_10 = len(Patient.objects.filter(clinic=c_emp_id,date__month='10',date__year=new_str))
                new_11 = len(Patient.objects.filter(clinic=c_emp_id,date__month='11',date__year=new_str))
                new_12 = len(Patient.objects.filter(clinic=c_emp_id,date__month='12',date__year=new_str))

        chart_data = {
            'old_str':old_str,
            'old_1':old_1,
            'old_2':old_2,
            'old_3':old_3,
            'old_4':old_4,
            'old_5':old_5,
            'old_6':old_6,
            'old_7':old_7,
            'old_8':old_8,
            'old_9':old_9,
            'old_10':old_10,
            'old_11':old_11,
            'old_12':old_12,
            'new_str':new_str,
            'new_1':new_1,
            'new_2':new_2,
            'new_3':new_3,
            'new_4':new_4,
            'new_5':new_5,
            'new_6':new_6,
            'new_7':new_7,
            'new_8':new_8,
            'new_9':new_9,
            'new_10':new_10,
            'new_11':new_11,
            'new_12':new_12,
        }  
        emp_arr = []      
        if appUser.user_type.id == 4:
            emp_arr = GetDataOFEmployee(employee_id)

        data = {
            'payment_type' : payment_type_list,
            'monthname' : monthname,
            'emp_arr':emp_arr,
            'employee_id': employee_id,
            'user_type':appUser.user_type,
            'full_name' : fullname,
            'first_name' : first_name,
            'last_name' : last_name,
            'gender' : gender,
            'user_cat' : appUser.user_type.role_name,
            'data_set_1':data_set_1,
            'data_set_1_all' : data_set_1_all,
            'data_set_1_title':data_set_1_title,
            'data_set_2':data_set_2,
            'data_set_2_all' : data_set_2_all,
            'data_set_2_title':data_set_2_title,
            'data_set_3':data_set_3,
            'data_set_3_all' : data_set_3_all,
            'data_set_3_title':data_set_3_title,
            'data_set_4':data_set_4,
            'data_set_4_all' : data_set_4_all,
            'data_set_4_title':data_set_4_title,
            'data_set_5':data_set_5,
            'data_set_5_all' : data_set_5_all,
            'data_set_5_title':data_set_5_title,
            'data_set_6':data_set_6,
            'data_set_6_all' : data_set_6_all,
            'data_set_6_title':data_set_6_title,
            'data_set_7':data_set_7,
            'data_set_7_all' : data_set_7_all,
            'data_set_7_title':data_set_7_title,
            'page':page,
            'country':country_list,
            'state':state_list,
            'careof':careof_list,
            'disease':disease_list,
            'healthCardType':healthCardType_list,
            'healthCardTypeCategory':healthCardTypeCategory_list,
            'clinic':clinic_list,
            'view_data':viewdata,
            'view_type':view_type,
            'state_name':state_name,
            'state_id':state_id,
            'chart_data':chart_data,
            'doctor_list':doctor_list,
            'error':error_str,
            'therapy_set_list':therapy_set_list
        }
        return render(request,"index.html",data) 
    except AppUser.DoesNotExist:
        return render(request,"auth-login-basic.html",{'error':'Y'})

def UpdateReferralStatus(request):
    id = int(request.GET.get('id').strip())
    rn = request.GET.get('rn').strip()
    rd = request.GET.get('rd').strip()
    em = request.GET.get('em').strip()
    treatment=Treatment.objects.get(id=id)
    old_value = TreatmentSerializer(treatment,many=False).data
    treatment.referral_number = rn
    treatment.referral_date = rd
    treatment.referral_status = 'Approved'
    treatment.save()
    new_value = TreatmentSerializer(treatment,many=False).data
    json_obj = {
        'change_name' : 'Update Referral Status UHID = '+treatment.patient.patient_uhid,
        'old_value' : json.dumps(old_value),
        'new_value' : json.dumps(new_value),
        'login_id' : em            
    }        
    change_log_serializer = ChangeLogSerializer(data=json_obj)            
    if change_log_serializer.is_valid():
        change_log_serializer.save()
    return HttpResponse(0)

def UpdateTreatmentStatus(request):
    id = int(request.GET.get('id').strip())
    complete = int(request.GET.get('complete').strip())
    shift_ipd = int(request.GET.get('shift_ipd').strip())
    remark = request.GET.get('remark').strip()
    response = 0
    treatment=Treatment.objects.get(id=id)
    if shift_ipd == 1:
        patient_id = treatment.patient.id
        patient = Patient.objects.get(id=patient_id)
        clinic_id = patient.clinic
        pt_list = Patient.objects.filter(clinic=clinic_id)
        tr_list = Treatment.objects.filter(patient__in=pt_list)
        last_ipd = tr_list.latest('ipd_no')
        response = int(last_ipd.ipd_no)+1
        treatment.ipd_no=str(response)
    
    treatment.remark = remark
    treatment.is_complete = complete
    treatment.save()
    return HttpResponse(response)

def BillingAction(request):
    sl = request.GET.get('sl').strip()
    cl = request.GET.get('cl').strip()
    id = request.GET.get('id').strip()
    try:
        patientTrt = PatientTreatment.objects.get(id=id)
        if sl != '0':
            patientTrt.billing_status = sl
            patientTrt.billing_date = cl
            patientTrt.save()
    except PatientTreatment.DoesNotExist:
        None

    return HttpResponse({'error':'N'})

def UpdatePTStatusAction(request):
    pt = request.GET.get('pt').strip()
    st = request.GET.get('st').strip()
    ft = request.GET.get('ft').strip()
    dt = request.GET.get('dt').strip()
    employee_id = request.GET.get('em').strip()
    try:
        patientTrt = PatientTreatment.objects.get(id=pt)
        old_value = PatientTreatmentSerializer(patientTrt,many=False).data
        if st != '0':
            patientTrt.status = st
        if ft != '0':
            patientTrt.file_status = ft
        if ft == '3':
            if dt != '0':
                patientTrt.file_date = dt
        patientTrt.save()
        new_value = PatientTreatmentSerializer(patientTrt,many=False).data
        json_obj = {
            'change_name' : 'Update Treatment Status UHID = '+patientTrt.patient.patient_uhid,
            'old_value' : json.dumps(old_value),
            'new_value' : json.dumps(new_value),
            'login_id' : employee_id            
        }        
        change_log_serializer = ChangeLogSerializer(data=json_obj)            
        if change_log_serializer.is_valid():
            change_log_serializer.save()
    except PatientTreatment.DoesNotExist:
        None

    return HttpResponse({'error':'N'})

def AddTherapyAction(request):
    th = request.GET.get('th').strip()
    dt = request.GET.get('dt').strip()
    uhid = request.GET.get('uhid').strip()
    time = request.GET.get('time').strip()
    file_status = request.GET.get('file_status').strip()
    try:
        try:
            patient = Patient.objects.get(patient_uhid=uhid)
        except Patient.DoesNotExist:
            patient = Patient.objects.get(old_uhid=uhid)

        data = {
            'patient':patient.id,
            'startdate':dt,
            'enddate':dt,
            'status':1,
            'file_status':file_status,
            'file_date':dt,
            'therapy':th,
            'billing_status':0,
            'billing_date':dt,
            'time':time
        }
        patient_treatment_serializer = PatientTreatmentSerializer(data=data)
        if patient_treatment_serializer.is_valid():        
            patient_treatment_serializer.save()
            ur = UserRequest.objects.get(id=patient.user_request)
            ur.is_treatment_start = 1
            ur.save()
    except Patient.DoesNotExist:
        None
    return HttpResponse({'error':'N'})

def SearchPatient(request):
    key = request.GET.get('key').strip()
    cl = request.GET.get('cl').strip()
    urid = request.GET.get('urid').strip()
    response = ''
    is_found = False
    ur_list = []
    try:
        if key != '0':
            patient_list = Patient.objects.filter(mobile=key,clinic=cl).order_by('id')
            if len(patient_list) > 0:
                patient = patient_list[0]
                is_found = True
                response = patient.patient_uhid+' - '+patient.first_name+'##/portal/dashboard/?page=bookdoctor&uhid='+str(patient.id)+'##'+str(patient.id)
    except Patient.DoesNotExist:
        is_found = False

    if is_found == False:
        try:
            ur_list = UserRequest.objects.filter(mobile=key,clinic=cl).order_by('-datetime')
            if key == '0':
                ur_list = UserRequest.objects.filter(id=urid,clinic=cl).order_by('-datetime')

            if len(ur_list) > 0:
                ur = ur_list[0]
                response = '2##'+ur.first_name+'##'+ ur.last_name+'##'+ ur.care_of+'##'+ str(ur.care_of_type)+'##'+ ur.gender+'##'+ str(ur.age)+'##'+ ur.address+'##'+ ur.city+'##'+ str(ur.state)+'##'+ str(ur.country)+'##'+ str(ur.disease)+'##'+ ur.remark+'##'+ str(ur.health_card_type)+'##'+ str(ur.health_card_type_cat)+'##'+ ur.health_card_number+"##"+str(ur.id)+"##"+ur.mobile
                is_found = True
        except UserRequest.DoesNotExist:
            is_found = False
    
    return HttpResponse(response)

def GetDoctorFee(request):
    key = request.GET.get('key').strip()
    cl = request.GET.get('cl').strip()
    response = '500'
    try:
        cl_doc = ClinicDoctor.objects.filter(clinic=cl,doctor=key,is_valid=1)
        if len(cl_doc) > 0:
            response = cl_doc[0].fee
    except ClinicDoctor.DoesNotExist:
        None

    return HttpResponse(response)

def DuplicateRequestCheck(request):
    mobile = request.GET.get('mobile').strip()
    response = 'Y'
    list = UserRequest.objects.filter(mobile=mobile,is_clinic_visit=0)
    if len(list) > 0:
        response = 'N'

    return HttpResponse(response)

def SearchURequest(request,cl,ut,key):
    response = ''    
    emp = Employee.objects.get(id=cl)
    ur = UserRequest.objects.filter(mobile = key,employee=emp)
    if ut == '4':
        ur = UserRequest.objects.filter(mobile= key)

    if len(ur) == 0:
       ur = UserRequest.objects.filter(mobile_2 = key,employee=emp)  
       if ut == '4':
          ur = UserRequest.objects.filter(mobile_2= key)

    if len(ur) > 0:
       response = makeResponseTxt3(ur)
    
    return HttpResponse(response)   

def SearchBCRequest(request,cl,ut,key):
    response = ''
    is_found = False
    try:
       patient = Patient.objects.filter(patient_uhid=key)
       if len(patient) > 0:
           response = makeResponseTxt(patient)
           is_found = True
       
       patient = Patient.objects.filter(old_uhid=key)
       if len(patient) > 0:
           response = makeResponseTxt(patient)
           is_found = True

       if is_found == False:
           patient = Patient.objects.filter(mobile=key)
           if len(patient) > 0:
               response = makeResponseTxt(patient)
               is_found = True
       
       if is_found == False:
           patient = Patient.objects.filter(alt_mobile=key)
           if len(patient) > 0:
               response = makeResponseTxt(patient)
               is_found = True

       if is_found == False:
           patient = Patient.objects.filter(health_card_number=key)
           if len(patient) > 0:
               response = makeResponseTxt(patient)
               is_found = True
       
    except Patient.DoesNotExist:     
        is_found = False

    try:
       if is_found == False:
           user_request = UserRequest.objects.filter(mobile=key)
           if len(user_request) > 0:
               response = makeResponseTxt2(user_request)
               is_found = True

    except UserRequest.DoesNotExist:
        None
    return HttpResponse(response)

def SearchKey(request):
    key = request.GET.get('key').strip()
    cl = request.GET.get('cl').strip()
    ut = request.GET.get('ut').strip()
    response = ''
    is_found = False
    if key == '0' or key == '-' or len(key) == 0:
        return HttpResponse(response)

    if ut == '5' or ut == '6' or ut == '4':
        return SearchURequest(request,cl,ut,key)

    if ut == '8':
        return SearchBCRequest(request,cl,ut,key)

    try:
       if ut == '7':
           mngr = Employee.objects.get(id=cl)
           cl =  mngr.reporting_manager
       patient = Patient.objects.filter(patient_uhid=key,clinic=cl)
       if len(patient) > 0:
           response = makeResponseTxt(patient)
           is_found = True
       
       patient = Patient.objects.filter(old_uhid=key,clinic=cl)
       if len(patient) > 0:
           response = makeResponseTxt(patient)
           is_found = True

       if is_found == False:
           patient = Patient.objects.filter(mobile=key,clinic=cl)
           if len(patient) > 0:
               response = makeResponseTxt(patient)
               is_found = True
       
       if is_found == False:
           patient = Patient.objects.filter(alt_mobile=key,clinic=cl)
           if len(patient) > 0:
               response = makeResponseTxt(patient)
               is_found = True

       if is_found == False:
           patient = Patient.objects.filter(health_card_number=key,clinic=cl)
           if len(patient) > 0:
               response = makeResponseTxt(patient)
               is_found = True
       
    except Patient.DoesNotExist:     
        is_found = False

    try:
       if is_found == False:
           user_request = UserRequest.objects.filter(mobile=key,clinic=cl)
           if len(user_request) > 0:
               response = makeResponseTxt2(user_request)
               is_found = True

    except UserRequest.DoesNotExist:
        None


    return HttpResponse(response)

def makeResponseTxt2(userReq):
    text = ''
    for p in userReq:
        text = text + '<li><a class="dropdown-item" href="/portal/dashboard/?page=add-new-patient&urid='+str(p.id)+'"><i class="bx bx-user me-2"></i>'+'<span class="align-middle"><b>Appointment '+str(p.id) + "</b>, "+p.first_name+" "+p.last_name+", "+p.mobile+'</span></a></li>'+'<li><div class="dropdown-divider"></div></li>'

    return text

def makeResponseTxt3(userReq):
    text = ''
    for p in userReq:
        text = text + '<li><a class="dropdown-item" href="/portal/dashboard/?page=add-new-request&rid='+str(p.id)+'"><i class="bx bx-user me-2"></i>'+'<span class="align-middle"><b>Appointment '+str(p.id) + "</b>, "+p.first_name+" "+p.last_name+", "+p.mobile+'</span></a></li>'+'<li><div class="dropdown-divider"></div></li>'

    return text

def makeResponseTxt(patient):
    text = ''
    for p in patient:
        text = text + '<li><a class="dropdown-item" href="/portal/dashboard/?page=bookdoctor&uhid='+str(p.id)+'"><i class="bx bx-user me-2"></i>'+'<span class="align-middle"><b>Patient UHID '+p.patient_uhid + "</b>, "+p.first_name+" "+p.last_name+", "+p.mobile+'</span></a></li>'+'<li><div class="dropdown-divider"></div></li>'

    return text



def Filterclinic(request):
    state_id = request.GET.get('state')
    response = "<option value='0'>Select</option>"
    clinicList = Clinic.objects.filter(is_valid=1)
    try:
        state = State.objects.get(id=state_id,is_valid=1)    
        try: 
            clinicList = Clinic.objects.filter(state=state,is_valid=1)            
        except Clinic.DoesNotExist: 
            None           
    except State.DoesNotExist:
        None
    for cl in clinicList:
        response += "<option value='"+str(cl.id)+"'>"+cl.name+"</option>"
    return HttpResponse(response)

def EditpatientAction(request):
    old_value = {}    
    employee_id = 0
    if request.method == "POST":
        employee_id = request.POST.get('employee_id')
        patient_id = request.POST.get('patient_id')        
        pt = Patient.objects.get(id=patient_id)
        old_value = PatientSerializer(pt,many=False).data
        pt.alt_mobile = request.POST.get('alt_mobile')
        pt.old_uhid = request.POST.get('old_uhid').upper()
        pt.email = request.POST.get('email').upper()
        pt.occupation = request.POST.get('occupation').upper()
        pt.blood_group = request.POST.get('blood_group').upper()
        pt.first_name = request.POST.get('first_name').upper()
        pt.last_name = request.POST.get('last_name').upper()
        pt.gender = request.POST.get('gender').upper()
        pt.age = request.POST.get('age').upper()
        pt.marital_status = request.POST.get('marital_status').upper()
        pt.religion = request.POST.get('religion').upper()
        pt.care_of_type = request.POST.get('care_of_type').upper()
        pt.care_of = request.POST.get('care_of').upper()
        pt.address = request.POST.get('address').upper()
        pt.city = request.POST.get('city').upper()
        pt.pincode = request.POST.get('pincode').upper()
        pt.state = request.POST.get('state').upper()
        pt.country = request.POST.get('country').upper()
        pt.symptoms = request.POST.get('symptoms').upper()
        pt.health_card_type = request.POST.get('hctype').upper()
        pt.health_card_category = request.POST.get('hctypeCat').upper()
        pt.health_card_number = request.POST.get('hcnumber').upper()
        pt.referral_number = request.POST.get('referral_number').upper()
        pt.referral_date = request.POST.get('referral_date').upper()
        pt.remark = request.POST.get('remark').upper()
        pt.save()
        new_value = PatientSerializer(pt,many=False).data        
        json_obj = {
            'change_name' : 'Edit Patient '+pt.patient_uhid,
            'old_value' : json.dumps(old_value),
            'new_value' : json.dumps(new_value),
            'login_id' : employee_id            
        }
        change_log_serializer = ChangeLogSerializer(data=json_obj)            
        if change_log_serializer.is_valid():
            change_log_serializer.save() 
        return redirect('/portal/dashboard/?page=bookdoctor&uhid='+str(pt.id))    
    
    return dashboard_loading(request)
    

def AddNewPatientAction(request):
    if request.method == "POST":
        hct = request.POST.get('hctype')
        hctcat = request.POST.get('hctypeCat')
        clinic_id = request.POST.get('clinic')            
        request_id = request.POST.get('request_id')   
        if int(request_id) > 0:
            ur = UserRequest.objects.get(id=request_id)
            ur.is_clinic_visit = 1
            ur.save()

        clinic = Clinic.objects.get(id=clinic_id)
        patient_cl = Patient.objects.filter(clinic=clinic_id)
        uid = 1
        if len(patient_cl) > 0:
            latest_patient = patient_cl.latest('id')
            patient_uhid = latest_patient.patient_uhid
            patient_uhid = patient_uhid.replace('JS','').replace('-','').replace(' ','').replace(clinic.code,'')
            uid = int(patient_uhid)+1
        uidstr = str(uid)
        if len(uidstr) == 1:
            uidstr = "000"+uidstr
        elif len(uidstr) == 2:
            uidstr = "00"+uidstr 
        elif len(uidstr) == 3:
            uidstr = "0"+uidstr 

        patient_uhid = clinic.code+uidstr
        if hct == '0':
            hct = '1'

        if int(hct) < 2:
            hctcat = 0
        f_name = request.POST.get('first_name').upper()  
        m_mobile = request.POST.get('mobile')  
        json_data = {
            'patient_uhid':patient_uhid,
            'old_uhid':request.POST.get('old_uhid').upper(),
            'dob':'1999-01-01',                
            'date':datetime.now().strftime('%Y-%m-%d'),
            'alt_mobile':'0',
            'patient_source':'Self',
            'user_request':request.POST.get('request_id'),
            'first_name':f_name,
            'last_name':request.POST.get('last_name').upper(),
            'care_of_type':request.POST.get('care_of_type'),
            'care_of':request.POST.get('care_of').upper(),
            'gender':request.POST.get('gender').upper(),
            'age':request.POST.get('age'),
            'address':request.POST.get('address').upper(),
            'city':request.POST.get('city').upper(),
            'state':request.POST.get('state'),
            'country':request.POST.get('country'),
            'clinic':request.POST.get('clinic'),
            'disease':request.POST.get('symptoms'),
            'remark':request.POST.get('remark').upper(),
            'total_service':request.POST.get('total_service'),
            'health_card_type':request.POST.get('hctype'),
            'health_card_category':hctcat,
            'health_card_number':request.POST.get('hcnumber').upper(),
            'referral_number':request.POST.get('referral_number'),
            'referral_date':request.POST.get('referral_date'),
            'mobile':m_mobile,
            'pin_code':request.POST.get('pincode'),
            'marital_status':request.POST.get('marital_status').upper(),
            'alt_mobile':request.POST.get('alt_mobile'),
            'blood_group':request.POST.get('blood_group').upper(),
            'occupation':request.POST.get('occupation').upper(),
            'religion':request.POST.get('religion').upper(),
            'email':request.POST.get('email').upper(),

        }
        patient_serializer = PatientSerializer(data=json_data)            
        if patient_serializer.is_valid():
            lt_opd = 0
            try:
                ap = Patient.objects.get(first_name=f_name,mobile=m_mobile)
                return dashboard_loading(request)
            except Patient.DoesNotExist:
                newpatient = patient_serializer.save()
                            
            trt = Treatment.objects.filter(patient__in=patient_cl).exclude(opd_no='0')
            opd_num = 0
            if len(trt) > 0:
                last_opd = trt.latest('id')
                ar = last_opd.opd_no.split("/")
                lt_opd = int(ar[0])
                if ar[1] != datetime.now().strftime('%Y'):
                    lt_opd = 0
            opd_num = lt_opd+1
            opd_num_str = str(opd_num)
            if len(opd_num_str) == 1:
                opd_num_str = "000"+opd_num_str
            elif len(opd_num_str) == 2:
                opd_num_str = "00"+opd_num_str 
            elif len(opd_num_str) == 3:
                opd_num_str = "0"+opd_num_str

            ref_date = request.POST.get('referral_date')
            referral_status = 'Pending'
            if len(newpatient.referral_number) > 0:
                referral_status = 'Approved'

            if ref_date == '1999-01-01':
                ref_date = '-'    
            json = {
                'patient':newpatient.id,
                'datetime':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'doctor':request.POST.get('doctor_id'),
                'opd_no':opd_num_str+"/"+datetime.now().strftime('%Y'),
                'ipd_no':'0',
                'disease':request.POST.get('symptoms'),
                'remark':'-',
                'medicine':'0',
                'therapy':'0',
                'bp':request.POST.get('bp'),
                'sugar':request.POST.get('sugar'),
                'weight':request.POST.get('weight'),
                'referral_number':newpatient.referral_number,
                'referral_date':ref_date,
                'health_card_type':newpatient.health_card_type,
                'health_card_category':newpatient.health_card_category,
                'health_card_number':newpatient.health_card_number,
                'referral_status':referral_status,
            }
            treatment_serializer = TreatmentSerializer(data=json)
            if treatment_serializer.is_valid():
                treatment_serializer.save()

            payment_data = {
                'clinic':request.POST.get('clinic'),
                'patient':newpatient.id,
                'date':datetime.now().strftime('%Y-%m-%d'),
                'fee':request.POST.get('fee'),
                'payment_type':request.POST.get('payment_type'),
                'transaction_num':request.POST.get('transaction_num'),
            }
            payment_serializer = PaymentSerializer(data=payment_data)
            if payment_serializer.is_valid():
                payment_serializer.save()


    return redirect('/portal/dashboard/?page=bookdoctor&uhid='+str(newpatient.id))
    #return dashboard_loading(request)


def Adddoctoraction(request):
    cur_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if request.method == "POST":
        doctor_id = request.POST.get('doctor_id')     
        employee_id = request.POST.get('employee_id')
        clinic_doctor_id = request.POST.get('clinic_doctor_id')
        clinic_id = request.POST.get('clinic_id')
        first_name = request.POST.get('first_name')     
        last_name = request.POST.get('last_name')     
        status = request.POST.get('status')     
        fee = request.POST.get('fee')   
        mngr = Employee.objects.get(id=employee_id)
        cl_id = mngr.reporting_manager
        password = 'crm@2024'
        if doctor_id == '0':
            #add doctor
            username = datetime.now().strftime('%Y%m%d%H%M%S')+"."+employee_id+"."+str(cl_id)
            pwd_key = b'DRgiuOgIANXfB1j_BC9zFsjTfxA4GOCCSBc2iKz9mGw='
            #Fernet.generate_key()
            cipher_suite = Fernet(pwd_key)
            ciphered_text = cipher_suite.encrypt(bytes(password, 'utf-8'))
            password = ciphered_text.decode("utf-8")
            appuser_data = {
                "username":username,
                "password":password,
                "pass_code":password,
                "first_name":first_name,
                "last_name":last_name,
                "gender":'Select',
                "dob":'1999-01-01',
                "email":'hospitalappwork@gmail.com',
                "mobile":'0',
                "is_valid":1,
                "user_type":3
            }
            appuser_serializer = AppUserSerializer(data=appuser_data)
            if appuser_serializer.is_valid():        
                appuser_serializer.save()

            employee_data = {
                'first_name':first_name,
                'last_name':last_name,
                'gender':'Select',
                'dob':'1999-01-01',
                'user_type':3,
                'email':'hospitalappwork@gmail.com',
                'mobile':'0',
                'join_datetime':cur_date_time,
                'is_valid':1,
                'address':'-',
                'city':'-',
                'state':1,
                'country':1,
                'reporting_manager':0,
                'app_user':appuser_serializer.data.get('id'),
            }
            employee_serializer = EmployeeSerializer(data=employee_data)
            if employee_serializer.is_valid():        
                employee_serializer.save()

            cl_doctor = {
                'clinic' : cl_id,
                'doctor' : employee_serializer.data.get('id'),
                'is_valid':status,
                'fee':fee,
            }

            clinic_doctor_Serializer = ClinicDoctorSerializer(data=cl_doctor)
            if clinic_doctor_Serializer.is_valid():        
                clinic_doctor_Serializer.save()

        else:
            #update doctor
            doctor = Employee.objects.get(id=doctor_id)            
            doctor_clinic = ClinicDoctor.objects.get(id=clinic_doctor_id)
            doctor.first_name = first_name
            doctor.last_name = last_name
            doctor.save()
            doctor_clinic.is_valid=status
            doctor_clinic.fee = fee
            doctor_clinic.save()
            
    return dashboard_loading(request)    

def UpdateReqAction(request):
    cur_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    rid = request.POST.get('rid')
    eid = request.POST.get('employee_id')
    emp = Employee.objects.get(id=eid)
    hct = request.POST.get('hctype')
    hctcat = request.POST.get('hctypeCat')
    apt_datetime = request.POST.get('date')    
    if len(apt_datetime) == 0:
        apt_datetime = "1999-01-01"

    apt_datetime = apt_datetime + " 00:00:00"

    if int(hct) < 2:
        hctcat = 0

    ur = UserRequest.objects.get(id=rid,employee=emp)    
    #ur.mobile = request.POST.get('mobile')
    ur.mobile_2 = request.POST.get('mobile_2')
    ur.first_name = request.POST.get('first_name')
    ur.last_name = request.POST.get('last_name')
    ur.gender = request.POST.get('gender')
    ur.age = request.POST.get('age')
    ur.care_of_type = request.POST.get('care_of_type')
    ur.care_of = request.POST.get('care_of')
    ur.address = request.POST.get('address')
    ur.city = request.POST.get('city')
    ur.state = request.POST.get('state')
    ur.country = request.POST.get('country')
    ur.clinic = request.POST.get('clinic')
    ur.disease = request.POST.get('symptoms')
    ur.health_card_type = request.POST.get('hctype')
    ur.health_card_type_cat = hctcat
    ur.health_card_number = request.POST.get('hcnumber')
    ur.appointment_datetime = apt_datetime
    ur.remark = request.POST.get('remark')
    ur.datetime = cur_date_time
    ur.save()
    return dashboard_loading(request)

def AddNewReqAction(request):    
    cur_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if request.method == "POST":
        add_new_ur_form = AddNewUserForm(request.POST)
        if add_new_ur_form.is_valid():
            hct = add_new_ur_form.cleaned_data['hctype']
            hctcat = add_new_ur_form.cleaned_data['hctypeCat']
            apt_datetime = add_new_ur_form.cleaned_data['date']
            if len(apt_datetime) == 0:
                apt_datetime = "1999-01-01"

            apt_datetime = apt_datetime + " 00:00:00"

            if hct < 2:
                hctcat = 0

            m_mobile = add_new_ur_form.cleaned_data['mobile']
            json_data = {
                "mobile" : m_mobile,
                "mobile_2" : add_new_ur_form.cleaned_data['mobile_2'],
                "first_name" : add_new_ur_form.cleaned_data['first_name'],
                "last_name" : add_new_ur_form.cleaned_data['last_name'],
                "gender" : add_new_ur_form.cleaned_data['gender'],
                "age" : add_new_ur_form.cleaned_data['age'],
                "care_of_type" : add_new_ur_form.cleaned_data['care_of_type'],
                "care_of" : add_new_ur_form.cleaned_data['care_of'],
                "address" : add_new_ur_form.cleaned_data['address'],
                "city" : add_new_ur_form.cleaned_data['city'],
                "state" : add_new_ur_form.cleaned_data['state'],
                "country" : add_new_ur_form.cleaned_data['country'],
                "clinic" : add_new_ur_form.cleaned_data['clinic'],
                "disease" : add_new_ur_form.cleaned_data['symptoms'],
                "health_card_type" : add_new_ur_form.cleaned_data['hctype'],
                "health_card_type_cat" : hctcat,
                "health_card_number" : add_new_ur_form.cleaned_data['hcnumber'],
                "appointment_datetime" : apt_datetime,
                "remark" : add_new_ur_form.cleaned_data['remark'],
                "dob" : "1999-01-01",
                "datetime" :  cur_date_time,
                "is_clinic_visit" :  0,
                "is_treatment_start" : 0,
                "employee":add_new_ur_form.cleaned_data['employee_id'],
            }            
            user_request_serializer = UserRequestSerializer(data=json_data)
            if user_request_serializer.is_valid():
                try:
                    ur = UserRequest.objects.get(mobile=m_mobile)
                except UserRequest.DoesNotExist:
                    user_request_serializer.save()

    return dashboard_loading(request)

def UpdateProfileAction(request):
    if request.method == 'POST':        
        gender = request.POST.get('gender')
        employee_id = request.POST.get('employee_id')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        employee = Employee.objects.get(id=employee_id)        
        employee.gender = gender
        employee.save()
        if password != "0":
            app_user = AppUser.objects.get(id=employee.app_user.id)
            pwd_key = b'DRgiuOgIANXfB1j_BC9zFsjTfxA4GOCCSBc2iKz9mGw='
            fernet = Fernet(pwd_key)
            password_enct = fernet.encrypt(bytes(password, 'utf-8'))
            input_password = password_enct.decode("utf-8")
            app_user.password = input_password
            app_user.pass_code = input_password
            app_user.save()

    return dashboard_loading(request)

def GetDataOFEmployee(employee_id):
    today = date.today().isoformat()
    date_arr = today.split("-")
    employee_list = Employee.objects.filter(reporting_manager=employee_id,is_valid=1)
    arr = []
    for em in employee_list:
        userRequest = UserRequest.objects.filter(employee=em,datetime__month=date_arr[1],datetime__year=date_arr[0])
        ur_all = UserRequest.objects.filter(employee=em)
        clinicVisited = userRequest.filter(is_clinic_visit=1,is_treatment_start=0)
        treatmentStart = userRequest.filter(is_treatment_start=1)
        todayRequest = userRequest.filter(datetime__date = today)
        cv_all = ur_all.filter(is_clinic_visit=1,is_treatment_start=0)
        ts_all = ur_all.filter(is_treatment_start=1)
        tr_all = ur_all.filter(datetime__date = today)
        em_data = {
            'employee_name':em.first_name+" "+em.last_name+" ("+str(em.id)+")",
            'data_1':len(todayRequest),
            'data_2':len(userRequest),
            'data_3':len(clinicVisited),
            'data_4':len(treatmentStart),
            'data_1_all':len(tr_all),
            'data_2_all':len(ur_all),
            'data_3_all':len(cv_all),
            'data_4_all':len(ts_all),
        }
        arr.append(em_data)
    
    return arr


def ViewData(request):
    data_type = int(request.GET.get('type'))
    employee_id = int(request.GET.get('emp'))
    user_type = int(request.GET.get('ut'))
    today = date.today().isoformat()
    date_arr = today.split("-")    
    output = {}
    if user_type in [5,6,4] or ((user_type == 2 or user_type == 7 or user_type == 8) and (data_type == 1 or data_type == 2)):
        try:
            if user_type == 8:
                userRequest = UserRequest.objects.all().order_by('-id')
            else:    
                employee = Employee.objects.get(id=employee_id)
                userRequest = UserRequest.objects.filter(employee=employee).order_by('-id')
                if user_type == 4:
                    emp_list = Employee.objects.filter(reporting_manager = employee_id).order_by('-id')
                    userRequest = UserRequest.objects.filter(employee__in=emp_list).order_by('-id')
        except Employee.DoesNotExist:
            None
        if user_type == 2:
            clinic_o = Clinic.objects.get(id=employee_id)
            userRequest = UserRequest.objects.filter(clinic=clinic_o.id).order_by('-id')
        if user_type == 7:
            mngr = Employee.objects.get(id=employee_id)
            clinic_o = Clinic.objects.get(id=mngr.reporting_manager)
            userRequest = UserRequest.objects.filter(clinic=clinic_o.id).order_by('-id')
        if user_type == 8:
            userRequest = UserRequest.objects.all().order_by('-id')            
        clinicVisited = userRequest.filter(is_clinic_visit=1,is_treatment_start=0).order_by('-id')
        treatmentStart = userRequest.filter(is_treatment_start=1).order_by('-id')
        todayRequest = userRequest.filter(datetime__date = today).order_by('-id')
        if user_type == 2 or user_type == 7 or user_type == 8:
            todayRequest = userRequest.filter(appointment_datetime__date = today).order_by('-id')

        if data_type == 1:
            olist = UserRequestSerializer(todayRequest,many=True).data
            arr = []
            for o in olist:
                cl_name = ''
                try:
                    cl = Clinic.objects.get(id=o.get('clinic'))
                    cl_name = cl.name
                except Clinic.DoesNotExist:
                    cl_name = ''
                hct = HealthCardType.objects.get(id=o.get('health_card_type'))
                hstr = hct.name
                if o.get('health_card_type') > 1:
                    try:
                        hctc = HealthCardTypeCategory.objects.get(id=o.get('health_card_type_cat'))
                    except HealthCardTypeCategory.DoesNotExist:
                        hctc = HealthCardTypeCategory.objects.get(id='1')
                    hstr += " / "+hctc.name + " / " + o.get('health_card_number')
                o['clinic_name'] = cl_name
                o['health_card_type_str'] = hstr
                emp = Employee.objects.get(id=o.get('employee'))
                o['emp_name'] = emp.first_name+" "+emp.last_name
                o['datetime'] = o.get('appointment_datetime')
                o['old_uhid'] = o.get('old_uhid')
                if emp.user_type.id == 5:
                    o['emp_type'] = 'Call Center'
                elif emp.user_type.id == 6:
                    o['emp_type'] = 'Champion'
                arr.append(o)
            output = {
              'list' : arr
            }
        elif data_type == 2:
            olist = UserRequestSerializer(userRequest,many=True).data
            arr = []
            for o in olist:
                cl_name = ''
                try:
                    cl = Clinic.objects.get(id=o.get('clinic'))
                    cl_name = cl.name
                except Clinic.DoesNotExist:
                    cl_name = ''
                hct = HealthCardType.objects.get(id=o.get('health_card_type'))
                hstr = hct.name
                if o.get('health_card_type') > 1:
                    try:
                        hctc = HealthCardTypeCategory.objects.get(id=o.get('health_card_type_cat'))
                    except HealthCardTypeCategory.DoesNotExist:
                        hctc = HealthCardTypeCategory.objects.get(id='1')
                    hstr += " / "+hctc.name + " / " + o.get('health_card_number')
                o['clinic_name'] = cl_name
                o['health_card_type_str'] = hstr
                emp = Employee.objects.get(id=o.get('employee'))
                o['emp_name'] = emp.first_name+" "+emp.last_name
                o['datetime'] = o.get('appointment_datetime')
                o['old_uhid'] = o.get('old_uhid')
                if emp.user_type.id == 5:
                    o['emp_type'] = 'Call Center'
                elif emp.user_type.id == 6:
                    o['emp_type'] = 'Champion'
                arr.append(o)
            output = {
              'list' : arr
            }
        elif data_type == 3:
            olist = UserRequestSerializer(clinicVisited,many=True).data
            arr = []
            for o in olist:
                cl_name = ''
                try:
                    cl = Clinic.objects.get(id=o.get('clinic'))
                    cl_name = cl.name
                except Clinic.DoesNotExist:
                    cl_name = ''
                hct = HealthCardType.objects.get(id=o.get('health_card_type'))
                hstr = hct.name
                if o.get('health_card_type') > 1:
                    try:
                        hctc = HealthCardTypeCategory.objects.get(id=o.get('health_card_type_cat'))
                    except HealthCardTypeCategory.DoesNotExist:
                        hctc = HealthCardTypeCategory.objects.get(id='1')
                    hstr += " / "+hctc.name + " / " + o.get('health_card_number')
                o['clinic_name'] = cl_name
                o['health_card_type_str'] = hstr
                emp = Employee.objects.get(id=o.get('employee'))
                o['emp_name'] = emp.first_name+" "+emp.last_name
                o['datetime'] = o.get('appointment_datetime')
                o['old_uhid'] = o.get('old_uhid')
                if emp.user_type.id == 5:
                    o['emp_type'] = 'Call Center'
                elif emp.user_type.id == 6:
                    o['emp_type'] = 'Champion'
                arr.append(o)
            output = {
              'list' : arr
            }  
        elif data_type == 4:
            olist = UserRequestSerializer(treatmentStart,many=True).data
            arr = []
            for o in olist:
                cl_name = ''
                try:
                    cl = Clinic.objects.get(id=o.get('clinic'))
                    cl_name = cl.name
                except Clinic.DoesNotExist:
                    cl_name = ''
                hct = HealthCardType.objects.get(id=o.get('health_card_type'))
                hstr = hct.name
                if o.get('health_card_type') > 1:
                    try:
                        hctc = HealthCardTypeCategory.objects.get(id=o.get('health_card_type_cat'))
                    except HealthCardTypeCategory.DoesNotExist:
                        hctc = HealthCardTypeCategory.objects.get(id='1')
                    hstr += " / "+hctc.name + " / " + o.get('health_card_number')
                o['clinic_name'] = cl_name
                o['health_card_type_str'] = hstr
                emp = Employee.objects.get(id=o.get('employee'))
                o['emp_name'] = emp.first_name+" "+emp.last_name
                o['datetime'] = o.get('appointment_datetime')
                o['old_uhid'] = o.get('old_uhid')
                if emp.user_type.id == 5:
                    o['emp_type'] = 'Call Center'
                elif emp.user_type.id == 6:
                    o['emp_type'] = 'Champion'
                arr.append(o)
            output = {
              'list' : arr
            }                
    elif (user_type == 2 or user_type == 7 or user_type == 8) and data_type == 3:
        if user_type == 2:
            clinic = Clinic.objects.get(id=employee_id)
            patients = Patient.objects.filter(clinic=clinic.id).order_by('-date')
        elif user_type == 7:
            mngr = Employee.objects.get(id=employee_id)    
            clinic = Clinic.objects.get(id=mngr.reporting_manager)
            patients = Patient.objects.filter(clinic=clinic.id).order_by('-date')
        elif user_type == 8:
            patients = Patient.objects.all().order_by('-date')
        new_list = []
        for p in patients:
            treatment_list = Treatment.objects.filter(patient=p).order_by('-id')
            if len(treatment_list) == 1:
                new_list.append(p)
                
        arr = []
        for o in new_list:
            data = {}
            hstr = ''
            try:
                hct = HealthCardType.objects.get(id=o.health_card_type)
            except HealthCardType.DoesNotExist:
                hct = HealthCardType.objects.get(id=1)
            hstr = hct.name
            
            if o.health_card_type > 1:
                try:
                    hctc = HealthCardTypeCategory.objects.get(id=o.health_card_category)
                except HealthCardTypeCategory.DoesNotExist:
                    hctc = HealthCardTypeCategory.objects.get(id='1')
                hstr += " / "+hctc.name + " / " + o.health_card_number
            cl_name = ""
            try:
               clinic = Clinic.objects.get(id=o.clinic)
               cl_name = clinic.name
            except Clinic.DoesNotExist:
                cl_name = ""    
            data['clinic_name'] = cl_name
            data['health_card_type_str'] = hstr
            data['mobile'] = o.mobile
            data['first_name'] = o.first_name
            data['last_name'] = o.last_name
            data['patient_uhid'] = o.patient_uhid
            data['old_uhid'] = o.old_uhid
            data['id'] = o.id
            arr.append(data)

        output = {
            'list' : arr
        }
    
    elif (user_type == 2 or user_type == 7 or user_type == 8) and data_type == 4:
        if user_type == 2:
            clinic = Clinic.objects.get(id=employee_id)
            patients = Patient.objects.filter(clinic=clinic.id).order_by('-date')
        elif user_type == 7:
            mngr = Employee.objects.get(id=employee_id)    
            clinic = Clinic.objects.get(id=mngr.reporting_manager)
            patients = Patient.objects.filter(clinic=clinic.id).order_by('-date')
        elif user_type == 8:
            patients = Patient.objects.all().order_by('-date')
        new_list = []
        for p in patients:
            treatment_list = Treatment.objects.filter(patient=p).order_by('-id')
            if len(treatment_list) > 1:
                new_list.append(p)
                
        arr = []
        for o in new_list:
            data = {}
            try:
                hct = HealthCardType.objects.get(id=o.health_card_type)
            except HealthCardType.DoesNotExist:
                hct = HealthCardType.objects.get(id=1)
            hstr = hct.name            
            if o.health_card_type > 1:
                try:
                    hctc = HealthCardTypeCategory.objects.get(id=o.health_card_category)
                except HealthCardTypeCategory.DoesNotExist:
                    hctc = HealthCardTypeCategory.objects.get(id='1')
                hstr += " / "+hctc.name + " / " + o.health_card_number
            cl_name = ""
            try:
               clinic = Clinic.objects.get(id=o.clinic)
               cl_name = clinic.name
            except Clinic.DoesNotExist:
                cl_name = ""    
            data['clinic_name'] = cl_name
            data['health_card_type_str'] = hstr
            data['mobile'] = o.mobile
            data['first_name'] = o.first_name
            data['last_name'] = o.last_name
            data['patient_uhid'] = o.patient_uhid
            data['old_uhid'] = o.old_uhid
            data['id'] = o.id
            arr.append(data)

        output = {
            'list' : arr
        }
    
    elif (user_type == 2 or user_type == 7 or user_type == 8) and data_type == 5:
        if user_type == 2:
            clinic = Clinic.objects.get(id=employee_id)
            patients = Patient.objects.filter(clinic=clinic.id).order_by('-id')
        elif user_type == 7:
            mngr = Employee.objects.get(id=employee_id)    
            clinic = Clinic.objects.get(id=mngr.reporting_manager)
            patients = Patient.objects.filter(clinic=clinic.id).order_by('-id')
        elif user_type == 8:
            patients = Patient.objects.all().order_by('-id')
        patients = patients.filter(gender='Male').order_by('-date')                
        arr = []
        for o in patients:
            data = {}
            try:
                hct = HealthCardType.objects.get(id=o.health_card_type)
            except HealthCardType.DoesNotExist:
                hct = HealthCardType.objects.get(id=1)    
            hstr = hct.name            
            if o.health_card_type > 1:
                try:
                    hctc = HealthCardTypeCategory.objects.get(id=o.health_card_category)
                except HealthCardTypeCategory.DoesNotExist:
                    hctc = HealthCardTypeCategory.objects.get(id='1')
                hstr += " / "+hctc.name + " / " + o.health_card_number
            cl_name = ""
            try:
               clinic = Clinic.objects.get(id=o.clinic)
               cl_name = clinic.name
            except Clinic.DoesNotExist:
                cl_name = ""    
            data['clinic_name'] = cl_name
            data['health_card_type_str'] = hstr
            data['mobile'] = o.mobile
            data['first_name'] = o.first_name
            data['last_name'] = o.last_name
            data['patient_uhid'] = o.patient_uhid
            data['old_uhid'] = o.old_uhid
            data['id'] = o.id
            arr.append(data)

        output = {
            'list' : arr
        }

    elif (user_type == 2 or user_type == 7 or user_type == 8) and data_type == 6:
        if user_type == 2:
            clinic = Clinic.objects.get(id=employee_id)
            patients = Patient.objects.filter(clinic=clinic.id).order_by('-id')
        elif user_type == 7:
            mngr = Employee.objects.get(id=employee_id)    
            clinic = Clinic.objects.get(id=mngr.reporting_manager)
            patients = Patient.objects.filter(clinic=clinic.id).order_by('-id')
        elif user_type == 8:
            patients = Patient.objects.all().order_by('-id')    
        patients = patients.filter(gender='Female').order_by('-date')
                
        arr = []
        for o in patients:
            data = {}
            try:
                hct = HealthCardType.objects.get(id=o.health_card_type)
            except HealthCardType.DoesNotExist:
                hct = HealthCardType.objects.get(id=1)    
            hstr = hct.name
            if o.health_card_type > 1:
                try:
                    hctc = HealthCardTypeCategory.objects.get(id=o.health_card_category)
                except HealthCardTypeCategory.DoesNotExist:
                    hctc = HealthCardTypeCategory.objects.get(id='1')
                hstr += " / "+hctc.name + " / " + o.health_card_number
            cl_name = ""
            try:
               clinic = Clinic.objects.get(id=o.clinic)
               cl_name = clinic.name
            except Clinic.DoesNotExist:
                cl_name = ""    
            data['clinic_name'] = cl_name
            data['health_card_type_str'] = hstr
            data['mobile'] = o.mobile
            data['first_name'] = o.first_name
            data['last_name'] = o.last_name
            data['patient_uhid'] = o.patient_uhid
            data['old_uhid'] = o.old_uhid
            data['id'] = o.id
            arr.append(data)

        output = {
            'list' : arr
        }    

    elif (user_type == 2 or user_type == 7 or user_type == 8) and data_type == 7:
        if user_type == 2:
            clinic = Clinic.objects.get(id=employee_id)
            patients = Patient.objects.filter(clinic=clinic.id).order_by('-date')
        elif user_type == 7:
            mngr = Employee.objects.get(id=employee_id)    
            clinic = Clinic.objects.get(id=mngr.reporting_manager)
            patients = Patient.objects.filter(clinic=clinic.id).order_by('-date')
        elif user_type == 8:
            patients = Patient.objects.all().order_by('-date')
        arr = []
        for o in patients:
            data = {}
            try:
                hct = HealthCardType.objects.get(id=o.health_card_type)
            except HealthCardType.DoesNotExist:
                hct = HealthCardType.objects.get(id=1)    
            hstr = hct.name
            
            if o.health_card_type > 1:
                try:
                    hctc = HealthCardTypeCategory.objects.get(id=o.health_card_category)
                except HealthCardTypeCategory.DoesNotExist:
                    hctc = HealthCardTypeCategory.objects.get(id='1')
                hstr += " / "+hctc.name + " / " + o.health_card_number
            
            cl_name = ""
            try:
               clinic = Clinic.objects.get(id=o.clinic)
               cl_name = clinic.name
            except Clinic.DoesNotExist:
                cl_name = ""

            data['clinic_name'] = cl_name
            data['health_card_type_str'] = hstr
            data['mobile'] = o.mobile
            data['first_name'] = o.first_name
            data['last_name'] = o.last_name
            data['patient_uhid'] = o.patient_uhid
            data['old_uhid'] = o.old_uhid
            data['id'] = o.id
            arr.append(data)

        output = {
            'list' : arr
        }  
    elif user_type == 9 and data_type == 1:
        pendingPT = PatientTreatment.objects.filter(billing_status=0).order_by('-startdate')
        arr = []
        for o in pendingPT:
            data = {
                'uhid':o.patient.patient_uhid,
                'old_uhid':o.patient.old_uhid,
                'date':o.startdate.strftime('%Y-%m-%d'),
                'time':o.time,
                'status':'Pending'
            }
            arr.append(data)
        output = {
            'list' : arr
        }
    elif user_type == 9 and data_type == 2:
        pendingPT = PatientTreatment.objects.filter(billing_status=1).order_by('-startdate')
        arr = []
        for o in pendingPT:
            data = {
                'uhid':o.patient.patient_uhid,
                'old_uhid':o.patient.old_uhid,
                'date':o.startdate.strftime('%Y-%m-%d'),
                'time':o.time,
                'status':'Complete'
            }
            arr.append(data)
        output = {
            'list' : arr
        }    
    return output

def getTreatmentData(request):
    output = {}
    patient_id = request.GET.get('p')
    employee_id = request.GET.get('eid')
    user_type = request.GET.get('ut')
    try:        
        if user_type == '7':
            mngr = Employee.objects.get(id=employee_id)
            clinic = Clinic.objects.get(id=mngr.reporting_manager)
            try:
                patient = Patient.objects.get(patient_uhid=patient_id,clinic=clinic.id)
            except Patient.DoesNotExist:
                patient = Patient.objects.get(old_uhid=patient_id,clinic=clinic.id)
        else:
            try:
                patient = Patient.objects.get(patient_uhid=patient_id)
            except Patient.DoesNotExist:
                patient = Patient.objects.get(old_uhid=patient_id)    

        output['uhid']=patient_id
        output['patient_id']=patient.id
        hct = patient.health_card_type
        hct_name = 'Normal OPD'
        if hct > 0:
           hct_obj = HealthCardType.objects.get(id=hct)
           hct_name = hct_obj.name

        full_name = patient.first_name
        if patient.last_name != '-':
            full_name = full_name + " " +patient.last_name

        output['file_status']=1
        output['full_name']=full_name
        output['hct_name']=hct_name
        patient_treatment = PatientTreatment.objects.filter(patient=patient).order_by('startdate')
        output['ref_status']='Pending'
        if patient.referral_date.strftime('%Y-%m-%d') != '1999-01-01':
            output['ref_status']='Approved'

        if len(patient_treatment) > 0:
            last_pt = patient_treatment.latest('id')
            start_counter = 0
            first_pt = patient_treatment.first()
            startdate = first_pt.startdate
            check_file_status = 0
            for obj in patient_treatment:                
                if obj.status == 1 and start_counter == 0:
                    start_counter = 1
                    startdate = obj.startdate
                elif obj.status == 2 :
                    start_counter = 0
                    check_file_status = 1

            if check_file_status ==  1:  
                if last_pt.file_status == 1:
                    output['ref_status']= 'Pending'
                
                if last_pt.file_status == 2:
                    output['ref_status']= 'In Process'
                
                if last_pt.file_status == 3:
                    output['ref_status']= 'Approved'

            output['start_date']=startdate
            output['status']=last_pt.status
            output['pt_id']=last_pt.id
            output['file_status']=last_pt.file_status
            if last_pt.status != 2:
                output['complete_date']='N.A'
            else:
                output['complete_date']=last_pt.enddate

            if last_pt.file_status != 3:
                output['file_date']='N.A'
            else:
                output['file_date']=last_pt.file_date

            serializer = PatientTreatmentSerializer(patient_treatment, many=True)
            output['patient_treatment']=serializer.data
    except Patient.DoesNotExist:
        None 

    return output     

def getDoctorData(request):
    output = {}
    doc_id = int(request.GET.get('id'))
    emp_id = int(request.GET.get('eid'))
    doc_emp = Employee.objects.get(id=doc_id)
    mngr = Employee.objects.get(id=emp_id)
    cl_id = mngr.reporting_manager
    clinic = Clinic.objects.get(id=cl_id)
    cl_doc = ClinicDoctor.objects.get(clinic=clinic,doctor=doc_emp)
    output = {
        'first_name' : doc_emp.first_name,
        'last_name' : doc_emp.last_name,
        'is_valid':cl_doc.is_valid,
        'fee' : cl_doc.fee,
        'clinic_id' : cl_id,
        'clinic_doctor_id' : cl_doc.id,
    }
    return output

def getBookDoctorPage(request):
    output = {}
    final_list = []
    uhid = int(request.GET.get('uhid'))
    if uhid > 0:          
        patient_list = Patient.objects.filter(id=uhid)
        for o in patient_list:
            state_name = o.state
            country_name = o.country
            clinic_name = o.clinic
            disease_name = o.disease
            care_of_type_name = o.care_of_type
            health_card_type_name = o.health_card_type
            health_card_category =  o.health_card_category    
            if health_card_category > 0:
                try:
                    health_card_cat = HealthCardTypeCategory.objects.get(id=health_card_category)
                    health_card_category = health_card_cat.name
                except HealthCardTypeCategory.DoesNotExist:
                    None

            if health_card_type_name > 0:
                try:
                    health_card_type = HealthCardType.objects.get(id=health_card_type_name)
                    health_card_type_name = health_card_type.name
                except HealthCardType.DoesNotExist:
                    None

            if care_of_type_name > 0:
                try:
                    care_of_type = CareOf.objects.get(id=care_of_type_name)
                    care_of_type_name = care_of_type.name
                except CareOf.DoesNotExist:
                    None

            if disease_name > 0:
                try:
                    disease = Disease.objects.get(id=disease_name)
                    disease_name = disease.name
                except Disease.DoesNotExist:
                    None

            if clinic_name > 0:
                try:
                    clinic = Clinic.objects.get(id=clinic_name)
                    clinic_name = clinic.name
                except Clinic.DoesNotExist:
                    None

            if country_name > 0:
                try:
                    country = Country.objects.get(id=country_name)
                    country_name = country.name
                except Country.DoesNotExist:
                    None
            
            if state_name > 0:
                try:
                    state = State.objects.get(id=state_name)
                    state_name = state.name
                except State.DoesNotExist:
                    None

            p_obj = {
                'state' : state_name, 
                'country' : country_name, 
                'clinic' : clinic_name, 
                'disease' : disease_name, 
                'care_of_type' : care_of_type_name, 
                'health_card_type' : health_card_type_name, 
                'health_card_category' : health_card_category,
                'id' : o.id, 
                'patient_uhid' : o.patient_uhid, 
                'old_uhid' : o.old_uhid,
                'user_request' : o.user_request, 
                'first_name' : o.first_name, 
                'last_name' : o.last_name,                     
                'care_of' : o.care_of, 
                'gender' : o.gender, 
                'dob' : o.dob, 
                'age' : o.age, 
                'address' : o.address, 
                'city' : o.city, 
                'remark' : o.remark, 
                'total_service' : o.total_service,                     
                'health_card_number' : o.health_card_number, 
                'patient_source' : o.patient_source, 
                'referral_number' : o.referral_number, 
                'referral_date' : o.referral_date, 
                'date' : o.date, 
                'mobile' : o.mobile, 
                'alt_mobile' : o.alt_mobile, 
                'blood_group' : o.blood_group,
                'occupation' : o.occupation,
                'religion' : o.religion,
                'marital_status' : o.marital_status,
                'email' : o.email,
                'pin_code' : o.pin_code
            }
            treatment_list = Treatment.objects.filter(patient=o)
            tarr = []  
            t_count = 0    
            t_len = len(treatment_list)
            for t in treatment_list:
                t_count = t_count + 1
                is_shift_valid = 0
                if t_count == t_len and t.is_complete == 0 and t.ipd_no == '0' :
                    is_shift_valid = 1
                doctor_name = t.doctor
                medicine_name = t.medicine
                therapy_name = t.therapy
                if doctor_name > 0:
                    try:
                        doctor = Employee.objects.get(id=doctor_name)
                        doctor_name = "Dr. "+doctor.first_name 
                        if doctor.last_name != '-':
                            doctor_name = doctor_name + " " + doctor.last_name
                        
                    except Employee.DoesNotExist:
                        None

                if medicine_name > 0:
                    try:
                        medicine = MedicineSet.objects.get(id=medicine_name)
                        medicine_name = medicine.name
                    except MedicineSet.DoesNotExist:
                        None

                if therapy_name > 0:
                    try:
                        therapy = TherapySet.objects.get(id=therapy_name)
                        therapy_name = therapy.name
                    except TherapySet.DoesNotExist:
                        None
                disease_name = ''
                if t.disease > 0 :
                    dis = Disease.objects.get(id=t.disease)
                    disease_name = dis.name
                ref_date = t.referral_date    
                if ref_date == '1999-01-01':
                   ref_date = '-' 
                t_obj = {
                    'id':  t.id,
                    'datetime':  t.datetime.date(),
                    'doctor': doctor_name,
                    'opd_no': t.opd_no,
                    'ipd_no': t.ipd_no,
                    'disease_name': disease_name,
                    'remark': t.remark,
                    'medicine': medicine_name,
                    'therapy':therapy_name,
                    'bp':t.bp,
                    'sugar':t.sugar,
                    'weight':t.weight,
                    'is_complete' : t.is_complete,
                    'is_shift_valid':is_shift_valid,
                    'referral_number':t.referral_number,
                    'referral_date':ref_date
                }
                tarr.append(t_obj)
                
            payments = Payment.objects.filter(patient=o)    
            patient_trt = PatientTreatment.objects.filter(patient=o)
            p_trt_list = []
            for pt in patient_trt:
                if pt.status == 1:
                    status_name = 'Start'
                elif pt.status == 2:
                    status_name = 'Complete'

                if pt.billing_status == 0:
                    billing_status_name = 'Pending'
                elif pt.billing_status > 0:
                    billing_status_name = 'Complete'
                th = TherapySet.objects.get(id=pt.therapy)

                pt_obj = {
                    "id":pt.id,
                    "startdate":pt.startdate.strftime('%Y-%m-%d'),
                    "therapy_name":th.name,
                    "status_name":status_name,
                    "billing_status_name":billing_status_name,
                    "time":pt.time,
                    "uhid":pt.patient.patient_uhid
                }
                p_trt_list.append(pt_obj)
            p_obj['patient_trt_list'] = p_trt_list
            pay_list = PaymentSerializer(payments,many=True).data
            docs = Docs.objects.filter(patient=o)
            doc_list = DocsSerializer(docs,many=True).data
            p_obj['doc_list'] = doc_list
            p_obj['pay_list'] = pay_list
            p_obj['treatment'] = tarr
            final_list.append(p_obj)
        
        output['list']=final_list

    return output

def Booked(request):
    doctor_id =  request.GET.get('doctor_id').strip()
    puid =  request.GET.get('puid').strip()
    #employee_id =  request.GET.get('employee_id').strip()
    symptoms =  request.GET.get('symptoms').strip()
    bp =  request.GET.get('bp').strip()
    sugar =  request.GET.get('sugar').strip()
    weight =  request.GET.get('weight').strip()
    referral_number =  request.GET.get('referral_number').strip()
    referral_date =  request.GET.get('referral_date').strip()
    p = Patient.objects.get(id=puid)
    c = p.clinic
    patient_cl = Patient.objects.filter(clinic=c)
    lt_opd = 0
    trt = Treatment.objects.filter(patient__in=patient_cl).exclude(opd_no='0')
    last = trt.latest('id')
    ar = last.opd_no.split("/")
    lt_opd = int(ar[0])+1
    if ar[1] != datetime.now().strftime('%Y'):
        lt_opd = 1
    opd_num_str = str(lt_opd)
    if len(opd_num_str) == 1:
        opd_num_str = "000"+opd_num_str
    elif len(opd_num_str) == 2:
        opd_num_str = "00"+opd_num_str 
    elif len(opd_num_str) == 3:
        opd_num_str = "0"+opd_num_str
    json = {
        'patient':puid,
        'datetime':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'doctor':doctor_id,
        'opd_no':opd_num_str+"/"+datetime.now().strftime('%Y'),
        'ipd_no':'0',
        'disease':symptoms,
        'remark':'-',
        'medicine':'0',
        'therapy':'0',
        'bp':bp,
        'sugar':sugar,
        'weight':weight,
        'referral_number':referral_number,
        'referral_date':referral_date
    }
    treatment_serializer = TreatmentSerializer(data=json)
    if treatment_serializer.is_valid():
        treatment_serializer.save()
    return HttpResponse(1)

def getEmpData(request):
    output = {}
    final_list = []
    if request.method == "POST":
        patientSearchForm = PatientSearchForm(request.POST)
        if patientSearchForm.is_valid():
            start_date =  patientSearchForm.cleaned_data['start_date']
            end_date =  patientSearchForm.cleaned_data['end_date']
            mngr_id = request.POST.get('employee_id')
            output['start_date']=start_date
            output['end_date']=end_date            
            emp_list = Employee.objects.filter(reporting_manager=mngr_id,is_valid=1)
            user_req_list = UserRequest.objects.filter(employee__in=emp_list,datetime__gte=start_date+" 00:00:00", datetime__lte=end_date+" 00:00:00")
            for o in user_req_list:
                em = Employee.objects.get(id=o.employee.id)
                clinic_name = ''
                if o.clinic > 0:
                    clinic = Clinic.objects.get(id=o.clinic)
                    clinic_name = clinic.name
                
                data = {
                    'employee':em.first_name+" "+em.last_name+" ("+str(em.id)+")",
                    'mobile':o.mobile,
                    'first_name':o.first_name,
                    'last_name':o.last_name,
                    'gender':o.gender,
                    'is_clinic_visit':o.is_clinic_visit,
                    'is_treatment_start':o.is_treatment_start,
                    'clinic_name':clinic_name,
                    'date':o.datetime.strftime('%Y-%m-%d')
                }
                final_list.append(data)
            output['list']=final_list
    return output

def getAttendanceData(request):
    output = {}
    final_list = []
    if request.method == "POST":
        patientSearchForm = PatientSearchForm(request.POST)
        if patientSearchForm.is_valid():
            start_date =  patientSearchForm.cleaned_data['start_date']
            end_date =  patientSearchForm.cleaned_data['end_date']
            mngr_id = request.GET.get('emp')
            output['start_date']=start_date
            output['end_date']=end_date
            emp_list = Employee.objects.filter(reporting_manager=mngr_id,is_valid=1)
            attendance_list = Attendance.objects.filter(employee__in=emp_list,date__gte=start_date, date__lte=end_date)
            for o in attendance_list:
                em = Employee.objects.get(id=o.employee.id)
                
                data = {
                    'employee':em.first_name+" "+em.last_name+" ("+str(em.id)+")",
                    'date':o.date.strftime('%Y-%m-%d'),
                    'start_time':o.login_time.strftime('%H:%M:%S'),
                    'end_time':o.logout_time.strftime('%H:%M:%S'),
                }
                final_list.append(data)
            output['list']=final_list
    return output

def getPatientData(request):
    output = {}
    final_list = []
    if request.method == "POST":
        patientSearchForm = PatientSearchForm(request.POST)
        if patientSearchForm.is_valid():
            start_date =  patientSearchForm.cleaned_data['start_date']
            end_date =  patientSearchForm.cleaned_data['end_date']
            cl_id =  request.POST.get('employee_id')
            user_type_id = request.POST.get('user_type_id')
            if user_type_id == '7':
                mngr = Employee.objects.get(id=cl_id)
                cl_id = mngr.reporting_manager
            output['start_date']=start_date
            output['end_date']=end_date
            if user_type_id == '8':
                patient_list = Patient.objects.filter(date__gte=start_date, date__lte=end_date)    
            else:    
                patient_list = Patient.objects.filter(date__gte=start_date, date__lte=end_date,clinic=cl_id)
            for o in patient_list:
                state_name = o.state
                country_name = o.country
                clinic_name = o.clinic
                disease_name = o.disease
                care_of_type_name = o.care_of_type
                health_card_type_name = o.health_card_type
                health_card_category =  o.health_card_category    
                if health_card_category > 0:
                    try:
                        health_card_cat = HealthCardTypeCategory.objects.get(id=health_card_category)
                        health_card_category = health_card_cat.name
                    except HealthCardTypeCategory.DoesNotExist:
                        None

                if health_card_type_name > 0:
                    try:
                        health_card_type = HealthCardType.objects.get(id=health_card_type_name)
                        health_card_type_name = health_card_type.name
                    except HealthCardType.DoesNotExist:
                        None

                if care_of_type_name > 0:
                    try:
                        care_of_type = CareOf.objects.get(id=care_of_type_name)
                        care_of_type_name = care_of_type.name
                    except CareOf.DoesNotExist:
                        None

                if disease_name > 0:
                    try:
                        disease = Disease.objects.get(id=disease_name)
                        disease_name = disease.name
                    except Disease.DoesNotExist:
                        None

                if clinic_name > 0:
                    try:
                        clinic = Clinic.objects.get(id=clinic_name)
                        clinic_name = clinic.name
                    except Clinic.DoesNotExist:
                        None

                if country_name > 0:
                    try:
                        country = Country.objects.get(id=country_name)
                        country_name = country.name
                    except Country.DoesNotExist:
                        None
                
                if state_name > 0:
                    try:
                        state = State.objects.get(id=state_name)
                        state_name = state.name
                    except State.DoesNotExist:
                        None

                p_obj = {
                    'state' : state_name, 
                    'country' : country_name, 
                    'clinic' : clinic_name, 
                    'disease' : disease_name, 
                    'care_of_type' : care_of_type_name, 
                    'health_card_type' : health_card_type_name, 
                    'health_card_category' : health_card_category,
                    'id' : o.id, 
                    'patient_uhid' : o.patient_uhid,
                    'old_uhid' : o.old_uhid, 
                    'user_request' : o.user_request, 
                    'first_name' : o.first_name, 
                    'last_name' : o.last_name,                     
                    'care_of' : o.care_of, 
                    'gender' : o.gender, 
                    'dob' : o.dob, 
                    'age' : o.age, 
                    'address' : o.address.replace(',', ' '), 
                    'city' : o.city, 
                    'remark' : o.remark.replace(',', ' '), 
                    'total_service' : o.total_service,                     
                    'health_card_number' : o.health_card_number, 
                    'patient_source' : o.patient_source, 
                    'referral_number' : o.referral_number, 
                    'referral_date' : o.referral_date.strftime('%Y-%m-%d'), 
                    'date' : o.date.strftime('%Y-%m-%d'), 
                    'mobile' : o.mobile, 
                    'alt_mobile' : o.alt_mobile, 
                    'pin_code' : o.pin_code,
                    'marital_status' : o.marital_status,
                    'religion' : o.religion,
                    'blood_group' : o.blood_group,
                    'occupation' : o.occupation
                }
                treatment_list = Treatment.objects.filter(patient=o)
                tarr = []      
                for t in treatment_list:
                    doctor_name = t.doctor
                    medicine_name = t.medicine
                    therapy_name = t.therapy
                    if doctor_name > 0:
                        try:
                            doctor = Employee.objects.get(id=doctor_name)
                            doctor_name = "Dr. "+doctor.first_name 
                            if doctor.last_name != '-':
                                doctor_name = doctor_name + " " + doctor.last_name
                            
                        except Employee.DoesNotExist:
                            None

                    if medicine_name > 0:
                        try:
                            medicine = MedicineSet.objects.get(id=medicine_name)
                            medicine_name = medicine.name
                        except MedicineSet.DoesNotExist:
                            None

                    if therapy_name > 0:
                        try:
                            therapy = TherapySet.objects.get(id=therapy_name)
                            therapy_name = therapy.name
                        except TherapySet.DoesNotExist:
                            None
                    disease_name = ''
                    if t.disease > 0 :
                        dis = Disease.objects.get(id=t.disease)
                        disease_name = dis.name
                    t_obj = {
                        'id':  t.id,
                        'datetime':  t.datetime.date().strftime('%Y-%m-%d'),
                        'doctor': doctor_name,
                        'opd_no': t.opd_no,
                        'ipd_no': t.ipd_no,
                        'disease_name': disease_name,
                        'remark': t.remark.replace(',', ' '),
                        'medicine': medicine_name,
                        'therapy':therapy_name,
                        'is_complete':t.is_complete,
                        'bp':t.bp,
                        'sugar':t.sugar,
                        'weight':t.weight
                    }
                    tarr.append(t_obj)
                payments = Payment.objects.filter(patient=o)   
                patient_trt = PatientTreatment.objects.filter(patient=o)
                p_trt_list = []
                for pt in patient_trt:
                    if pt.status == 1:
                        status_name = 'Start'
                    elif pt.status == 2:
                        status_name = 'Complete'

                    if pt.billing_status == 0:
                        billing_status_name = 'Pending'
                    elif pt.billing_status > 0:
                        billing_status_name = 'Complete'
                    th = TherapySet.objects.get(id=pt.therapy)

                    pt_obj = {
                        "id":pt.id,
                        "startdate":pt.startdate.strftime('%Y-%m-%d'),
                        "therapy_name":th.name,
                        "status_name":status_name,
                        "billing_status_name":billing_status_name,
                        "time":pt.time,
                        "uhid":pt.patient.patient_uhid
                    }
                    p_trt_list.append(pt_obj)
                p_obj['patient_trt_list'] = p_trt_list
                pay_list = PaymentSerializer(payments,many=True).data
                p_obj['pay_list'] = pay_list
                p_obj['treatment'] = tarr
                final_list.append(p_obj)
            output['list']=final_list

    return output

def EditEmpAction(request,edit_id,emp_type,password,first_name,last_name,gender,mobile):
    pwd_key = b'DRgiuOgIANXfB1j_BC9zFsjTfxA4GOCCSBc2iKz9mGw='
    try:
        emp = Employee.objects.get(id=edit_id)
        emp.first_name = first_name
        emp.last_name = last_name
        emp.gender = gender
        emp.mobile = mobile
        ut = UserType.objects.get(id=emp_type)
        emp.user_type = ut
        emp.save()
        app_user_id = emp.app_user.id
        au = AppUser.objects.get(id=app_user_id)
        au.user_type = ut
        if len(password) > 0:
            cipher_suite = Fernet(pwd_key)
            ciphered_text = cipher_suite.encrypt(bytes(password, 'utf-8'))
            password = ciphered_text.decode("utf-8")
            au.password = password
            au.pass_code = password

        au.save()

    except Employee.DoesNotExist:
        None

    return dashboard_loading(request)

def AddNewEmpAction(request):
    cur_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if request.method == "POST":
        employee_id = request.POST.get('employee_id')
        emp_type = request.POST.get('emp_type')
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        mobile = request.POST.get('mobile')
        edit_id = request.POST.get('edit_id')
        if edit_id != '0':
            return EditEmpAction(request,edit_id,emp_type,password,first_name,last_name,gender,mobile)

        user_found = False
        try:
            appUser = AppUser.objects.get(username=username)
            return redirect('/portal/dashboard/?page=add-new-employee&error=y')
        except AppUser.DoesNotExist:
            user_found = False

        
        if user_found == False:
            pwd_key = b'DRgiuOgIANXfB1j_BC9zFsjTfxA4GOCCSBc2iKz9mGw='
            #Fernet.generate_key()
            cipher_suite = Fernet(pwd_key)
            ciphered_text = cipher_suite.encrypt(bytes(password, 'utf-8'))
            password = ciphered_text.decode("utf-8")
            appuser_data = {
                "username":username,
                "password":password,
                "pass_code":password,
                "first_name":first_name,
                "last_name":last_name,
                "gender":gender,
                "dob":'1999-01-01',
                "email":'hospitalappwork@gmail.com',
                "mobile":mobile,
                "is_valid":1,
                "user_type":emp_type
            }
            appuser_serializer = AppUserSerializer(data=appuser_data)
            if appuser_serializer.is_valid():        
                appuser_serializer.save()

            employee_data = {
                'first_name':first_name,
                'last_name':last_name,
                'gender':gender,
                'dob':'1999-01-01',
                'user_type':emp_type,
                'email':'hospitalappwork@gmail.com',
                'mobile':mobile,
                'join_datetime':cur_date_time,
                'is_valid':1,
                'address':'-',
                'city':'-',
                'state':1,
                'country':1,
                'reporting_manager':employee_id,
                'app_user':appuser_serializer.data.get('id'),
            }
            employee_serializer = EmployeeSerializer(data=employee_data)
            if employee_serializer.is_valid():        
                employee_serializer.save()

    return dashboard_loading(request)

def getEmployeeViewData(request,employee_id):
    inactive = request.GET.get('inactive')
    active = request.GET.get('active')
    if inactive is not None and len(inactive) > 0:
        try:
            emp = Employee.objects.get(id=inactive)
            emp.is_valid = 0
            emp.save()
        except Employee.DoesNotExist:
            None
    if active is not None and len(active) > 0:
        try:
            emp = Employee.objects.get(id=active)
            emp.is_valid = 1
            emp.save()
        except Employee.DoesNotExist:
            None        
    employee_active = Employee.objects.filter(reporting_manager=employee_id,is_valid=1)
    employee_inactive = Employee.objects.filter(reporting_manager=employee_id,is_valid=0)
    ac_arr = []
    inac_arr = []
    for em in employee_active:
        em_data = {
            'id':em.id,
            'employee_name':em.first_name+" "+em.last_name+" ("+str(em.id)+")",
            'mobile':em.mobile,
            'status':em.is_valid,
        }
        ac_arr.append(em_data)

    for em in employee_inactive:
        em_data = {
            'id':em.id,
            'employee_name':em.first_name+" "+em.last_name+" ("+str(em.id)+")",
            'mobile':em.mobile,
            'status':em.is_valid,
        }
        inac_arr.append(em_data)    
    
    return {'active':ac_arr,'inactive':inac_arr,'active_cnt':len(ac_arr),'inactive_cnt':len(inac_arr)}

def getClinicDoctor(request,employee_id):
    mngr = Employee.objects.get(id=employee_id)
    if mngr.user_type.id == 7: 
        clinic = Clinic.objects.get(id=mngr.reporting_manager)
        cl_doc = ClinicDoctor.objects.filter(clinic=clinic)
    elif mngr.user_type.id == 8: 
        cl_doc = ClinicDoctor.objects.all()
    output = {}
    #final_list = []    
    output['list']=cl_doc
    return output

def fileUpload(request):
    url = '/portal/dashboard/'
    if request.method == 'POST' and request.FILES['myfile']:
        pid = request.POST.get('pid')
        url = '/portal/dashboard/?page=bookdoctor&uhid='+pid
        p = Patient.objects.get(id=pid)        
        remark = request.POST.get('remark')
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(p.patient_uhid+'/'+myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        data={
            'patient':pid,
            'remark':remark,
            'file_name':uploaded_file_url
        }
        docs_serializer = DocsSerializer(data=data)
        if docs_serializer.is_valid():        
            docs_serializer.save()

    return redirect(url)

def getEditPatientData(request):
    uhid = request.GET.get('uhid')
    obj = {}
    try:
        pt = Patient.objects.get(id=uhid)
        serializer = PatientSerializer(pt, many=False)
        obj = serializer.data
        ref_date = pt.referral_date.strftime('%Y-%m-%d')
        if ref_date == '1999-01-01':
            ref_date = ''

        obj['referral_date'] = ref_date
    except Patient.DoesNotExist:
        None

    return obj 

def getEditEmpData(request):
    edit = request.GET.get('edit')
    obj = {}
    try:
        emp = Employee.objects.get(id=edit)
        obj['first_name']=emp.first_name
        obj['last_name']=emp.last_name
        obj['gender']=emp.gender
        obj['mobile']=emp.mobile
        obj['user_type']=emp.user_type.id
        obj['username']=emp.app_user.username

    except UserRequest.DoesNotExist:
        None

    return obj 

def getURRequestData(request):
    cur_date = datetime.now().strftime('%Y-%m-%d')
    rid = request.GET.get('rid')
    obj = {}
    try:
        ur = UserRequest.objects.get(id = rid)
        serializer = UserRequestSerializer(ur, many=False)
        obj = serializer.data
        apt_date = ur.appointment_datetime.strftime('%Y-%m-%d')
        if apt_date == '1999-01-01':
            apt_date = ''

        obj['date'] = apt_date
    except UserRequest.DoesNotExist:
        None

    return obj    

def ExportPatientDataAction(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Export_Patient_Data.xls"'
    wb = xlwt.Workbook(encoding='utf-8')    

    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    cl_id =  request.GET.get('em')
    user_type_id = request.GET.get('ut')

    if user_type_id == '7':
        mngr = Employee.objects.get(id=cl_id)
        cl_id = mngr.reporting_manager

    if user_type_id == '8':
        patient_list = Patient.objects.filter(date__gte=start_date, date__lte=end_date)    
    else:    
        patient_list = Patient.objects.filter(date__gte=start_date, date__lte=end_date,clinic=cl_id)

    # Sheet header
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['DATE','UHID','OLD_UHID','Mobile','Alt_Mobile','First_Name','Last_Name','Gender','Age','Care_Of','Address','City','State','Country','Pincode','Marital_Status','Religion','Clinic','Symptoms','Health_Card_Type','Health_Card_Category','Health_Card_Number','Referral_Date','Referral_Number','Blood_Group','Occupation','Remark']
    
    ws1 = wb.add_sheet('Patient_Data')

    for col_num in range(len(columns)):
        ws1.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body
    font_style = xlwt.XFStyle()
    font_style.font.bold = False

    for o in patient_list:
        row_num += 1
        state_name = o.state
        country_name = o.country
        clinic_name = o.clinic
        disease_name = o.disease
        care_of_type_name = 'C/O'
        health_card_type_name = o.health_card_type
        health_card_category =  o.health_card_category    
        if health_card_category > 0:
            try:
                health_card_cat = HealthCardTypeCategory.objects.get(id=health_card_category)
                health_card_category = health_card_cat.name
            except HealthCardTypeCategory.DoesNotExist:
                None

        if health_card_type_name > 0:
            try:
                health_card_type = HealthCardType.objects.get(id=health_card_type_name)
                health_card_type_name = health_card_type.name
            except HealthCardType.DoesNotExist:
                None

        if o.care_of_type > 0:
            try:
                care_of_type = CareOf.objects.get(id=o.care_of_type)
                care_of_type_name = care_of_type.name
            except CareOf.DoesNotExist:
                None

        if disease_name > 0:
            try:
                disease = Disease.objects.get(id=disease_name)
                disease_name = disease.name
            except Disease.DoesNotExist:
                None

        if clinic_name > 0:
            try:
                clinic = Clinic.objects.get(id=clinic_name)
                clinic_name = clinic.name
            except Clinic.DoesNotExist:
                None

        if country_name > 0:
            try:
                country = Country.objects.get(id=country_name)
                country_name = country.name
            except Country.DoesNotExist:
                None
        
        if state_name > 0:
            try:
                state = State.objects.get(id=state_name)
                state_name = state.name
            except State.DoesNotExist:
                None
        ref_date = o.referral_date.strftime('%Y-%m-%d')
        if ref_date == '1999-01-01':
            ref_date = '-'
            
        row = []
        row.append(o.date.strftime('%Y-%m-%d'))
        row.append(o.patient_uhid)
        row.append(o.old_uhid)
        row.append(o.mobile)
        row.append(o.alt_mobile)
        row.append(o.first_name)
        row.append(o.last_name)
        row.append(o.gender)
        row.append(o.age)
        row.append(care_of_type_name + " " + o.care_of)
        row.append(o.address)
        row.append(o.city)
        row.append(state_name)
        row.append(country_name)
        row.append(o.pin_code)
        row.append(o.marital_status)
        row.append(o.religion)
        row.append(clinic_name)
        row.append(disease_name)
        row.append(health_card_type_name)
        row.append(health_card_category)
        row.append(o.health_card_number)
        row.append(ref_date)
        row.append(o.referral_number)
        row.append(o.blood_group)
        row.append(o.occupation)
        row.append(o.remark)      
        for col_num in range(len(row)):
            ws1.write(row_num, col_num, row[col_num], font_style)

    columns = ['UHID','OPD_Date','OPD_Number','IPD_Number','BP','Sugar','Weight','Doctor','Disease','OPD_Remark','Referral_Date','Referral_Number']
    ws2 = wb.add_sheet('Patient_OPD')
    # Sheet head
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    col_num = 0
    for col_num in range(len(columns)):
        ws2.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body
    font_style = xlwt.XFStyle()
    font_style.font.bold = False
    
    for o in patient_list:        
        treatment_list = Treatment.objects.filter(patient=o)
        for t in treatment_list:
            row_num = row_num + 1
            doctor_name = t.doctor
            medicine_name = t.medicine
            therapy_name = t.therapy
            health_card_type_name = o.health_card_type
            health_card_category =  o.health_card_category    
            if health_card_category > 0:
                try:
                    health_card_cat = HealthCardTypeCategory.objects.get(id=health_card_category)
                    health_card_category = health_card_cat.name
                except HealthCardTypeCategory.DoesNotExist:
                    None

            if health_card_type_name > 0:
                try:
                    health_card_type = HealthCardType.objects.get(id=health_card_type_name)
                    health_card_type_name = health_card_type.name
                except HealthCardType.DoesNotExist:
                    None
            if doctor_name > 0:
                try:
                    doctor = Employee.objects.get(id=doctor_name)
                    doctor_name = "Dr. "+doctor.first_name 
                    if doctor.last_name != '-':
                        doctor_name = doctor_name + " " + doctor.last_name
                    
                except Employee.DoesNotExist:
                    None

            if medicine_name > 0:
                try:
                    medicine = MedicineSet.objects.get(id=medicine_name)
                    medicine_name = medicine.name
                except MedicineSet.DoesNotExist:
                    None

            if therapy_name > 0:
                try:
                    therapy = TherapySet.objects.get(id=therapy_name)
                    therapy_name = therapy.name
                except TherapySet.DoesNotExist:
                    None
            disease_name = ''
            if t.disease > 0 :
                dis = Disease.objects.get(id=t.disease)
                disease_name = dis.name                 
            
            row_opd = []
            row_opd.append(o.patient_uhid)
            row_opd.append(t.datetime.date().strftime('%Y-%m-%d'))
            row_opd.append(t.opd_no)
            row_opd.append(t.ipd_no)
            row_opd.append(t.bp)
            row_opd.append(t.sugar)
            row_opd.append(t.weight)
            row_opd.append(doctor_name)
            row_opd.append(disease_name)
            row_opd.append(t.remark)
            row_opd.append(t.referral_date)
            row_opd.append(t.referral_number) 
            for col_num in range(len(row_opd)):
                ws2.write(row_num, col_num, row_opd[col_num], font_style)

    columns = ['UHID','Date','Clinic','Payment_Title','Amount','Payment_Mode','Transaction_Number']
    ws3 = wb.add_sheet('Patient_Payment')
    # Sheet head
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    row_num = 0
    for col_num in range(len(columns)):
        ws3.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body
    font_style = xlwt.XFStyle()
    font_style.font.bold = False

    for o in patient_list:        
        payments = Payment.objects.filter(patient=o)
        for p in payments:
            row_num = row_num+1
            row = []
            row.append(o.patient_uhid)
            row.append(p.date.strftime('%Y-%m-%d'))
            row.append(p.clinic.name)
            row.append(p.title)
            row.append(p.fee)
            row.append(p.payment_type)
            row.append(p.transaction_num)
            for col_num in range(len(row)):
                ws3.write(row_num, col_num, row[col_num], font_style)


    columns = ['UHID','ID','DATE','Time','Therapy','Therapy_Status','Billing_Status','Referral_Status','Referral_Date']
    ws4 = wb.add_sheet('Patient_Therapy')
    # Sheet head
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    row_num = 0
    for col_num in range(len(columns)):
        ws4.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body
    font_style = xlwt.XFStyle()
    font_style.font.bold = False

    for o in patient_list:        
        patient_trt = PatientTreatment.objects.filter(patient=o)
        for pt in patient_trt:
            row_num = row_num + 1
            if pt.status == 1:
                status_name = 'Start'
            elif pt.status == 2:
                status_name = 'Complete'

            if pt.billing_status == 0:
                billing_status_name = 'Pending'
            elif pt.billing_status > 0:
                billing_status_name = 'Complete'

            therapy_name = '-'  
            try:
                tr = TherapySet.objects.get(id=pt.therapy)
                therapy_name = tr.name
            except TherapySet.DoesNotExist:
                therapy_name = '-'

            ref_status = 'Pending'    
            if pt.file_status == 2:
                ref_status = 'In Process'
            elif pt.file_status == 3:
                ref_status = 'Approved'

            row = []
            row.append(o.patient_uhid)
            row.append(pt.id)
            row.append(pt.startdate.strftime('%Y-%m-%d'))
            row.append(pt.time.strftime('%I:%M %p'))
            row.append(therapy_name)
            row.append(status_name)
            row.append(billing_status_name)
            row.append(ref_status)
            row.append(pt.file_date.strftime('%Y-%m-%d'))
            for col_num in range(len(row)):
                ws4.write(row_num, col_num, row[col_num], font_style)
                    
    wb.save(response)
    return response  

def ExportEmpDataAction(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Export_Employee_Data.xls"'
    wb = xlwt.Workbook(encoding='utf-8')    

    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    mngr_id =  request.GET.get('em')
    emp_list = Employee.objects.filter(reporting_manager=mngr_id,is_valid=1)
    user_req_list = UserRequest.objects.filter(employee__in=emp_list,datetime__gte=start_date+" 00:00:00", datetime__lte=end_date+" 00:00:00")
    
    columns = ['Date','Employee','Mobile','First_Name','Last_Name','Gender','Clinic_Name','Is_Clinic_Visit','Is_Treatment_Start']
    ws = wb.add_sheet('Employee_Data')
    # Sheet head
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    row_num = 0
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body
    font_style = xlwt.XFStyle()
    font_style.font.bold = False
    for o in user_req_list:
        em = Employee.objects.get(id=o.employee.id)
        clinic_name = ''
        row_num = row_num + 1
        if o.clinic > 0:
            clinic = Clinic.objects.get(id=o.clinic)
            clinic_name = clinic.name
        
        row = []
        row.append(o.datetime.strftime('%Y-%m-%d'))
        row.append(em.first_name+" "+em.last_name+" ("+str(em.id)+")")
        row.append(o.mobile)
        row.append(o.first_name)
        row.append(o.last_name)
        row.append(o.gender)
        row.append(clinic_name)
        row.append(o.is_clinic_visit)
        row.append(o.is_treatment_start)
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)        

    wb.save(response)
    return response     
