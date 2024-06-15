import json
from rest_framework.parsers import JSONParser 
from django.http.response import JsonResponse
from rest_framework import status
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from restapi.serializers import AppUserSerializer, AttendanceSerializer, ClinicDoctorSerializer, ClinicSerializer, EmployeeSerializer, PatientSerializer, TreatmentSerializer, UserTypeSerializer, DiseaseSerializer, HealthCardTypeSerializer, CountrySerializer, StateSerializer, TherapySetSerializer, MedicineSetSerializer,UserRequestSerializer,HealthCardTypeCategorySerializer,CareOfSerializer
from restapi.models import AppUser, Attendance, Clinic, Employee, Patient, PatientTreatment, Treatment, UserRequest, UserType, Disease, HealthCardType, Country, State, TherapySet, MedicineSet,CareOf,HealthCardTypeCategory
from datetime import date    
from cryptography.fernet import Fernet
from datetime import date, datetime
#from django.shortcuts import redirect

#def page_not_found_view(request, exception):
#    print("Errororororo")
#    return redirect("/portal/login")

# Create your views here.
@api_view(['GET','POST','DELETE'])
def UserTypeAction(request):
    data_save = False
    if request.method == 'GET':
        userType = UserType.objects.all()
        serializer = UserTypeSerializer(userType, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':            
        json_data = JSONParser().parse(request)
        json_data = JSONParser().parse(request)
        for obj in json_data:
            usertype_serializer = UserTypeSerializer(data=obj)
            if usertype_serializer.is_valid():        
                usertype_serializer.save()    
                data_save = True
    elif request.method == 'DELETE':
        json_data = JSONParser().parse(request)
        userType = UserType.objects.get(id=json_data.get('id'))
        userType.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return JsonResponse({"save":data_save}, status=status.HTTP_201_CREATED)


@api_view(['GET','POST','DELETE'])
def CareofAction(request):
    data_save = False
    if request.method == 'GET':
        careOf = CareOf.objects.filter(is_valid=1)
        serializer = CareOfSerializer(careOf, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':            
        json_data = JSONParser().parse(request)
        for obj in json_data:
            careof_serializer = CareOfSerializer(data=obj)
            if careof_serializer.is_valid():        
                careof_serializer.save()    
                data_save = True        
    elif request.method == 'DELETE':
        json_data = JSONParser().parse(request)
        careOf = CareOf.objects.get(id=json_data.get('id'))
        careOf.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return JsonResponse({"save":data_save}, status=status.HTTP_201_CREATED)  

@api_view(['GET','POST','DELETE'])
def HealthCardTypeAction(request):
    data_save = False
    if request.method == 'GET':
        healthCardType = HealthCardType.objects.filter(is_valid=1)
        serializer = HealthCardTypeSerializer(healthCardType, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':            
        json_data = JSONParser().parse(request)
        for obj in json_data:
            healthcardtype_serializer = HealthCardTypeSerializer(data=obj)
            if healthcardtype_serializer.is_valid():        
                healthcardtype_serializer.save()    
                data_save = True
    elif request.method == 'DELETE':
        json_data = JSONParser().parse(request)
        healthCardType = HealthCardType.objects.get(id=json_data.get('id'))
        healthCardType.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return JsonResponse({"save":data_save}, status=status.HTTP_201_CREATED)

@api_view(['GET','POST','DELETE'])
def HealthCardTypeCategoryAction(request):
    data_save = False
    if request.method == 'GET':
        healthCardTypeCategory = HealthCardTypeCategory.objects.filter(is_valid=1)
        serializer = HealthCardTypeCategorySerializer(healthCardTypeCategory, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':            
        json_data = JSONParser().parse(request)
        for obj in json_data:
            healthcardtypecategory_serializer = HealthCardTypeCategorySerializer(data=obj)
            if healthcardtypecategory_serializer.is_valid():        
                healthcardtypecategory_serializer.save()    
                data_save = True        
    elif request.method == 'DELETE':
        json_data = JSONParser().parse(request)
        healthCardTypeCategory = HealthCardTypeCategory.objects.get(id=json_data.get('id'))
        healthCardTypeCategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return JsonResponse({"save":data_save}, status=status.HTTP_201_CREATED)  


@api_view(['GET','POST','DELETE'])
def CountryAction(request):
    data_save = False
    if request.method == 'GET':
        country = Country.objects.filter(is_valid=1)
        serializer = CountrySerializer(country, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':            
        json_data = JSONParser().parse(request)
        for obj in json_data:
            country_serializer = CountrySerializer(data=obj)
            if country_serializer.is_valid():        
                country_serializer.save()    
                data_save = True        
    elif request.method == 'DELETE':
        json_data = JSONParser().parse(request)
        country = Country.objects.get(id=json_data.get('id'))
        country.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return JsonResponse({"save":data_save}, status=status.HTTP_201_CREATED)


@api_view(['GET','POST','DELETE'])
def StateAction(request):
    data_save = False
    if request.method == 'GET':
        state = State.objects.filter(is_valid=1)
        serializer = StateSerializer(state, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':            
        json_data = JSONParser().parse(request)
        for obj in json_data:
            state_serializer = StateSerializer(data=obj)
            if state_serializer.is_valid():        
                state_serializer.save()    
                data_save = True        
    elif request.method == 'DELETE':
        json_data = JSONParser().parse(request)
        state = State.objects.get(id=json_data.get('id'))
        state.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return JsonResponse({"save":data_save}, status=status.HTTP_201_CREATED)  


@api_view(['GET','POST','DELETE'])
def MedicineSetAction(request):
    data_save = False
    if request.method == 'GET':
        medicineSet = MedicineSet.objects.filter(is_valid=1)
        serializer = MedicineSetSerializer(medicineSet, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':            
        json_data = JSONParser().parse(request)
        for obj in json_data:
            medicineSet_serializer = MedicineSetSerializer(data=obj)
            if medicineSet_serializer.is_valid():        
                medicineSet_serializer.save()    
                data_save = True
    elif request.method == 'DELETE':
        json_data = JSONParser().parse(request)
        medicineSet = MedicineSet.objects.get(id=json_data.get('id'))
        medicineSet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return JsonResponse({"save":data_save}, status=status.HTTP_201_CREATED)      

@api_view(['GET','POST','DELETE'])
def TherapySetAction(request):
    data_save = False
    if request.method == 'GET':
        therapySet = TherapySet.objects.filter(is_valid=1)
        serializer = TherapySetSerializer(therapySet, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':            
        json_data = JSONParser().parse(request)
        for obj in json_data:
            therapySet_serializer = TherapySetSerializer(data=obj)
            if therapySet_serializer.is_valid():        
                therapySet_serializer.save()    
                data_save = True        
    elif request.method == 'DELETE':
        json_data = JSONParser().parse(request)
        therapySet = TherapySet.objects.get(id=json_data.get('id'))
        therapySet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return JsonResponse({"save":data_save}, status=status.HTTP_201_CREATED)


@api_view(['GET','POST','DELETE'])
def DiseaseAction(request):
    data_save = False
    if request.method == 'GET':
        disease = Disease.objects.filter(is_valid=1)
        serializer = DiseaseSerializer(disease, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':            
        json_data = JSONParser().parse(request)
        for obj in json_data:
            disease_serializer = DiseaseSerializer(data=obj)
            if disease_serializer.is_valid():        
                disease_serializer.save()    
                data_save = True        
    elif request.method == 'DELETE':
        json_data = JSONParser().parse(request)
        disease = Disease.objects.get(id=json_data.get('id'))
        disease.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return JsonResponse({"save":data_save}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def UsernameCheck(request):
    json_data = JSONParser().parse(request)
    input_username = json_data.get('username')
    try:
        appUser = AppUser.objects.get(username__iexact=input_username,is_valid=1)
    except AppUser.DoesNotExist:
        return Response(data={'found':False})
    else:
        return Response(data={'found':True})


@api_view(['POST'])
def AddAppUser(request):
    json_data = JSONParser().parse(request)
    input_username = json_data.get('username')    
    user_found = False
    try:
        appUser = AppUser.objects.get(username__iexact=input_username)
    except AppUser.DoesNotExist:
        user_found = False
    else:
        user_found = True
        return Response(data={'found':True})
    
    if user_found == False:   
        pwd_key = b'DRgiuOgIANXfB1j_BC9zFsjTfxA4GOCCSBc2iKz9mGw='
        #Fernet.generate_key()
        cipher_suite = Fernet(pwd_key)
        ciphered_text = cipher_suite.encrypt(bytes(input_password, 'utf-8'))
        input_password = ciphered_text.decode("utf-8")
        ciphered_text_c = cipher_suite.encrypt(bytes(input_passcode, 'utf-8'))
        input_passcode = ciphered_text_c.decode("utf-8")
        appuser_data = {
            "username":json_data.get('username'),
            "password":input_password,
            "pass_code":input_passcode,
            "first_name":json_data.get('first_name'),
            "last_name":json_data.get('last_name'),
            "gender":json_data.get('gender'),
            "dob":json_data.get('dob'),
            "email":json_data.get('email'),
            "mobile":json_data.get('mobile'),
            "is_valid":json_data.get('is_valid'),
            "user_type":json_data.get('user_type')
        }
        appuser_serializer = AppUserSerializer(data=appuser_data)
        if appuser_serializer.is_valid():        
            appuser_serializer.save()
                
        if json_data.get('user_type') == 2:
            clinic_data = {
                "name":json_data.get('name'),
                "start_date":json_data.get('start_date'),
                "is_valid":json_data.get('is_valid'),
                "phone":json_data.get('phone'),
                "mobile":json_data.get('mobile'),
                "address":json_data.get('address'),
                "city":json_data.get('city'),
                "state":json_data.get('state'),
                "country":json_data.get('country'),
                "clinic_timing":json_data.get('clinic_timing'),
                "latitude":json_data.get('latitude'),
                "longitude":json_data.get('longitude'),
                "app_user":appuser_serializer.data.get('id')
            }
            clinic_serializer = ClinicSerializer(data=clinic_data)
            if clinic_serializer.is_valid():        
                clinic_serializer.save()
        elif json_data.get('user_type') != 1:
            employee_data = {
                "first_name":json_data.get('first_name'),
                "last_name":json_data.get('last_name'),
                "gender":json_data.get('gender'),
                "dob":json_data.get('dob'),
                "user_type":json_data.get('user_type'),
                "email":json_data.get('email'),
                "mobile":json_data.get('mobile'),
                "is_valid":json_data.get('is_valid'),
                "address":json_data.get('address'),
                "city":json_data.get('city'),
                "state":json_data.get('state'),
                "country":json_data.get('country'),
                "reporting_manager":json_data.get('reporting_manager'),
                "app_user":appuser_serializer.data.get('id')
            }
            employee_serializer = EmployeeSerializer(data=employee_data)
            if employee_serializer.is_valid():        
                employee_serializer.save()

        return JsonResponse(appuser_serializer.data, status=status.HTTP_201_CREATED) 
    return JsonResponse(appuser_serializer.errors, status=status.HTTP_400_BAD_REQUEST)     


@api_view(['POST'])
def ClinicDoctor(request):
    json_data = JSONParser().parse(request) 
    clinic_doctor_serializer = ClinicDoctorSerializer(data=json_data)
    if clinic_doctor_serializer.is_valid():
        clinic_doctor_serializer.save()
        return JsonResponse(clinic_doctor_serializer.data, status=status.HTTP_201_CREATED) 
    return JsonResponse(clinic_doctor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def AttendanceAction(request):
    json_data = JSONParser().parse(request)
    if json_data.get('type')==1:
        attendance_data = {
            "employee" : json_data.get('employee'),
            "login_time" : datetime.now().strftime('%H:%M:%S'),
            "logout_time" : datetime.now().strftime('%H:%M:%S'),
            "date" : datetime.now().strftime('%Y-%m-%d'),
            "latitude" : json_data.get('latitude'),
            "longitude" : json_data.get('longitude'),
            "out_latitude" : "0",
            "out_longitude" : "0",
        }
        attendance_serializer = AttendanceSerializer(data=attendance_data)
        if attendance_serializer.is_valid():
            attendance_serializer.save()
            return JsonResponse(attendance_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(attendance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif json_data.get('type')==2:
        attendance = Attendance.objects.get(employee=json_data.get('employee'),date=json_data.get('date'))
        attendance.logout_time = datetime.now().strftime('%H:%M:%S')
        attendance.out_latitude = json_data.get('latitude')
        attendance.out_longitude = json_data.get('longitude')
        attendance.save()        
        return JsonResponse({"out":True}, status=status.HTTP_201_CREATED)        


@api_view(['POST'])
def LoginAction(request):
    json_data = JSONParser().parse(request)
    input_username = json_data.get('username')
    input_password = json_data.get('password')
    pwd_key = b'DRgiuOgIANXfB1j_BC9zFsjTfxA4GOCCSBc2iKz9mGw='
    fernet = Fernet(pwd_key)
    user_found = False
    output = {}
    try:
        appUser = AppUser.objects.get(username__iexact=input_username,is_valid=1,user_type=6)        
        pwd = appUser.password
        pwd_code = appUser.pass_code
        d_pwd = fernet.decrypt(bytes(pwd,'utf-8')).decode()
        d_pwd_code = fernet.decrypt(bytes(pwd_code,'utf-8')).decode()
        if d_pwd == input_password:
            user_found = True
        elif d_pwd_code == input_password:
            user_found = True

        if user_found == True:
            today = date.today().isoformat()
            date_arr = today.split("-")
            data_set_1 = 0
            data_set_2 = 0
            data_set_3 = 0
            data_set_4 = 0  
            emp_id = 0
            app_user_id = 0
            login = "0"
            logout = "0"
            employee = Employee.objects.get(app_user=appUser,is_valid=1)
            emp_id = employee.id
            app_user_id = appUser.id
            if appUser.user_type.id in [5,6]:                
                userRequest = UserRequest.objects.filter(employee=employee,datetime__month__lte=date_arr[1],datetime__year__lte=date_arr[0])
                clinicVisited = userRequest.filter(is_clinic_visit=1)
                todayRequest = userRequest.filter(datetime__date = today)
                data_set_1 = len(userRequest)
                data_set_2 = len(clinicVisited)
                data_set_3 = len(todayRequest)
            elif appUser.user_type.id == 4:
                champian_usr = Employee.objects.filter(reporting_manager = employee.id, user_type=6, is_valid=1)
                office_usr = Employee.objects.filter(reporting_manager = employee.id, user_type=5, is_valid=1)
                ch_month_req = UserRequest.objects.filter(employee__in=champian_usr,datetime__month__lte=date_arr[1],datetime__year__lte=date_arr[0])
                of_month_req = UserRequest.objects.filter(employee__in=office_usr,datetime__month__lte=date_arr[1],datetime__year__lte=date_arr[0])
                ch_today_req = UserRequest.objects.filter(employee__in=champian_usr,datetime__date = today)
                of_today_req = UserRequest.objects.filter(employee__in=office_usr,datetime__date = today)
                data_set_1 = len(champian_usr)
                data_set_2 = len(office_usr)
                data_set_3 = len(ch_month_req)+len(of_month_req)
                data_set_4 = len(ch_today_req)+len(of_today_req)
            try:                    
                attendance = Attendance.objects.get(date=today,employee=employee)
                login = attendance.login_time.strftime('%H:%M:%S')
                logout = attendance.logout_time.strftime('%H:%M:%S')
                if login == logout:
                    logout = "0"
            except Attendance.DoesNotExist:
                login = "0"
                logout = "0"

            output = {
                    "username":input_username,
                    "fullname":"Hello, "+ appUser.first_name+" "+appUser.last_name,
                    "date":today,
                    "data_set_1":data_set_1,
                    "data_set_2":data_set_2,
                    "data_set_3":data_set_3,
                    "data_set_4":data_set_4,
                    "employee_id":emp_id,
                    "app_user_id":app_user_id,
                    "login":login,
                    "logout":logout,
                }    

    except AppUser.DoesNotExist:
       user_found = False 

    if user_found == False:
        output = {"error":"User Not Found"}

    return JsonResponse(output, status=status.HTTP_201_CREATED) 

@api_view(['POST'])
def clinicAction(request):
    json_data = JSONParser().parse(request)
    input_state_id = json_data.get('state')
    state = {}
    state_error = False
    try:
        state = State.objects.get(id=input_state_id,is_valid=1)        
    except State.DoesNotExist:
        state_error = True
        return JsonResponse({"error":True}, status=status.HTTP_201_CREATED)    

    if state_error == False:
        try:
            clinic = Clinic.objects.filter(state=state)
            serializer = ClinicSerializer(clinic, many=True)
            return Response(serializer.data)
        except Clinic.DoesNotExist:
            return JsonResponse({"error":True}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def RegisterRequestAction(request):
    rid = "0"
    json_data = JSONParser().parse(request)
    if json_data.get('rid') is not None:
        rid = json_data.get('rid')

    print(rid)
    if rid == "0":        
        user_request_serializer = UserRequestSerializer(data=json_data)
        if user_request_serializer.is_valid():
            user_request_serializer.save()
            return JsonResponse({"success":"Y"}, status=status.HTTP_201_CREATED) 
    else:
        ur = UserRequest.objects.get(id=rid)
        ur.mobile = json_data.get('mobile')
        ur.mobile_2 = json_data.get('mobile_2')
        ur.first_name = json_data.get('first_name')
        ur.last_name = json_data.get('last_name')
        ur.gender = json_data.get('gender')
        ur.age = json_data.get('age')
        ur.care_of_type = json_data.get('care_of_type')
        ur.care_of = json_data.get('care_of')
        ur.address = json_data.get('address')
        ur.city = json_data.get('city')
        ur.state = json_data.get('state')
        ur.country = json_data.get('country')
        ur.clinic = json_data.get('clinic')
        ur.disease = json_data.get('disease')
        ur.health_card_type = json_data.get('health_card_type')
        ur.health_card_type_cat = json_data.get('health_card_type_cat')
        ur.health_card_number = json_data.get('health_card_number')
        ur.appointment_datetime = json_data.get('appointment_datetime')
        ur.datetime = json_data.get('datetime')
        ur.remark = json_data.get('remark')
        ur.save()
        return JsonResponse({"success":"Y"}, status=status.HTTP_201_CREATED)

    return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def ViewUserRequestAction(request):
    json_data = JSONParser().parse(request)
    emp_id = json_data.get("employee")
    data_type = json_data.get("type")
    if data_type == '1':
        employee = Employee.objects.get(id=emp_id,is_valid=1)
        e_reg = UserRequest.objects.filter(employee=employee)
        e_serializer = UserRequestSerializer(e_reg, many=True)        
        return Response(e_serializer.data)
    elif data_type == '2':
        employee = Employee.objects.get(id=emp_id,is_valid=1)
        v_reg = UserRequest.objects.filter(employee=employee,is_clinic_visit=1)
        v_serializer = UserRequestSerializer(v_reg, many=True)
        return Response(v_serializer.data)
    elif data_type == '3':
        employee = Employee.objects.get(id=emp_id,is_valid=1)
        today = date.today().isoformat()
        v_reg = UserRequest.objects.filter(employee=employee,datetime__date=today)
        v_serializer = UserRequestSerializer(v_reg, many=True)
        return Response(v_serializer.data)    


@api_view(['GET','POST'])
def EmployeeAction(request):
    data_save = False
    if request.method == 'GET':
        json_data = JSONParser().parse(request)
        employee = Employee.objects.filter(reporting_manager=json_data.get('id'),is_valid=1)
        serializer = EmployeeSerializer(employee, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':            
        json_data = JSONParser().parse(request)
        for obj in json_data:
            employee_Serializer = EmployeeSerializer(data=obj)
            if employee_Serializer.is_valid():        
                employee_Serializer.save()    
                data_save = True    
    return JsonResponse({"save":data_save}, status=status.HTTP_201_CREATED) 

@api_view(['POST'])
def AddClinicAction(request):
    data_save = False
    json_data = JSONParser().parse(request)
    for obj in json_data:
        clinic_serializer = ClinicSerializer(data=obj)
        if clinic_serializer.is_valid():        
            clinic_serializer.save()    
            data_save = True    
    return JsonResponse({"save":data_save}, status=status.HTTP_201_CREATED)  

@api_view(['POST'])
def AddPatientData(request):
    json_data = JSONParser().parse(request)
    for obj in json_data:
        UHID = obj.get('UHID')        
        is_insert_patient = 0
        is_insert_trt = 0
        patient_id = 0
        try:
            if UHID == '0':
                UHID = 'SHUDDHI'
            patient = Patient.objects.get(patient_uhid=UHID)    
            is_insert_trt = 1
            patient_id = patient.id
        except Patient.DoesNotExist:
            is_insert_patient = 1

        if is_insert_patient == 1:
            patient_id = insertPatient(obj)
            insertTreatment(obj,patient_id)

        if is_insert_trt == 1:
            insertTreatment(obj,patient_id)    
    return JsonResponse({"save":True}, status=status.HTTP_201_CREATED)

def insertPatient(obj):
    p_id = 0
    UHID = obj.get('UHID')
    #Date = obj.get('Date').split("-")
    date_formatted = obj.get('Date')
    Health_Card_Type = int(obj.get('Health_Card_Type'))
    Patient_Type = obj.get('Patient_Type')
    GENDER = obj.get('GENDER')
    AGE = int(obj.get('AGE'))
    First_Name = obj.get('First_Name').strip()
    Last_Name = obj.get('Last_Name')
    Care_of_Type = int(obj.get('Care_of_Type'))
    Parent = obj.get('Parent')
    Address = obj.get('Address').strip()
    City = obj.get('City')
    PinCode = obj.get('PinCode')
    State = int(obj.get('State'))
    Mobile = obj.get('Mobile')
    Alternate_Mobile = obj.get('Alternate_Mobile')
    Clinic = int(obj.get('Clinic'))
    insert_data = {
        "patient_uhid":UHID,
        "user_request":"0",
        "first_name":First_Name,
        "last_name":Last_Name,
        "care_of_type":Care_of_Type,
        "care_of":Parent,
        "gender":GENDER,
        "dob":"1999-01-01",
        "age":AGE,
        "address":Address,
        "city":City,
        "state":State,
        "country":1,                
        "clinic":Clinic,
        "disease":0,
        "remark":"-",
        "total_service":0,
        "health_card_type":Health_Card_Type,
        "health_card_category":0,
        "health_card_number":"0",
        "patient_source":Patient_Type,
        "referral_number":"0",
        "referral_date":"1999-01-01",
        "date":date_formatted,
        "pin_code":PinCode,
        "mobile":Mobile,
        "alt_mobile":Alternate_Mobile
    }
    patient_serializer = PatientSerializer(data=insert_data)
    if patient_serializer.is_valid():
        patient = patient_serializer.save()
        p_id = patient.id
    
    return p_id



def insertTreatment(obj,pid):    
    Doctor = obj.get('Doctor')
    OPD_No = obj.get('OPD_No')
    IPD_No = obj.get('IPD_No')
    date_formatted = obj.get('Date')    
    date_time = date_formatted+" 00:00:00"
    insert_data = {
        "patient":pid,
        "datetime":date_time,
        "doctor":Doctor,
        "opd_no":OPD_No,
        "ipd_no":IPD_No,
        "day_care_no":"0",
        "remark":"-",
        "medicine":0,
        "therapy":0
    }
    treatment_serializer = TreatmentSerializer(data=insert_data)
    if treatment_serializer.is_valid():
        treatment_serializer.save()

@api_view(['POST'])
def EditRequest(request):    
    json_data = JSONParser().parse(request)
    rid = json_data.get('rid')
    obj = {}
    if rid is not None:
        ur = UserRequest.objects.get(id=rid)
        urs = UserRequestSerializer(ur,many=False)
        obj = urs.data
        apt_date = ur.appointment_datetime.strftime('%Y-%m-%d')
        if apt_date == '1999-01-01':
            apt_date = 'Select Date'
        obj['appointment_datetime'] = apt_date
    
    return JsonResponse(obj, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def Searchbymobile(request):    
    json_data = JSONParser().parse(request)
    mobile = json_data.get('mobile')
    employee_id = json_data.get('employee_id')
    obj = {'id':'0'}
    try:
        employee = Employee.objects.get(id=employee_id)
        ur = UserRequest.objects.filter(mobile=mobile,employee=employee)
        if len(ur) > 0:
            obj['id']=ur[0].id
        else:
            ur = UserRequest.objects.filter(mobile_2=mobile,employee=employee)
            if len(ur) > 0:
                obj['id']=ur[0].id
    except UserRequest.DoesNotExist:
        None
    return JsonResponse(obj, status=status.HTTP_201_CREATED)

@api_view(['GET','DELETE'])
def DeleteOldPataintData(request):
    delete_data = False
    if request.method == 'GET':
        p_list = Patient.objects.all()
        for obj in p_list:
            if obj.patient_uhid.startswith('JS'):
                try:
                    print(obj.patient_uhid)
                    t1_list = PatientTreatment.objects.filter(patient=obj)
                    for t1 in t1_list:
                        None
                        #t1.delete()
                        #print('deleting PatientTreatment')
                except PatientTreatment.DoesNotExist:
                    None  

                try:
                    t2_list = Treatment.objects.filter(patient=obj)
                    for t2 in t2_list:
                        None
                        #t2.delete()
                        #print('deleting Treatment')
                except Treatment.DoesNotExist:
                    None 
                #obj.delete()
                #print('deleting patient_uhid')
                #delete_data = True
        return Response(status=status.HTTP_204_NO_CONTENT)
    return JsonResponse({"delete_data":delete_data}, status=status.HTTP_201_CREATED)    

@api_view(['GET'])
def ExtraRun(request):
    run_status = False
    if request.method == 'GET':
        u_list = UserRequest.objects.all()
        for obj in u_list:
            #obj.is_treatment_start = 0
            if obj.mobile_2 != '0' and obj.first_name == '-':                 
                 obj.first_name = obj.mobile_2
                 obj.mobile_2 = '0'                 
            obj.save()
            run_status = True

        return Response(status=status.HTTP_204_NO_CONTENT)
    return JsonResponse({"run_status":run_status}, status=status.HTTP_201_CREATED)