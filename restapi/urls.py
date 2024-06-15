from django.urls import path
from . import views

urlpatterns = [
    path('usertype/', views.UserTypeAction, name='usertype'),
    path('disease/', views.DiseaseAction, name='disease'),
    path('healthcardtype/', views.HealthCardTypeAction, name='healthcardtype'),
    path('healthcardTypecategory/', views.HealthCardTypeCategoryAction, name='healthcardTypecategory'),
    path('careof/', views.CareofAction, name='careof'),
    path('country/', views.CountryAction, name='country'),
    path('state/', views.StateAction, name='state'),
    path('medicineset/', views.MedicineSetAction, name='medicineset'),
    path('therapyset/', views.TherapySetAction, name='therapyset'),
    path('usernamecheck/', views.UsernameCheck, name='usernamecheck'),
    path('addappuser/', views.AddAppUser, name='addappuser'),
    path('clinicdoctor/', views.ClinicDoctor, name='clinicdoctor'),
    path('attendance/', views.AttendanceAction, name='attendance'),
    path('login/', views.LoginAction, name='login'),
    path('clinic/', views.clinicAction, name='clinic'),
    path('registerrequest/', views.RegisterRequestAction, name='registerrequest'),
    path('viewuserrequest/', views.ViewUserRequestAction, name='viewuserrequest'),
    path('employee/', views.EmployeeAction, name='employee'),
    path('addClinic/', views.AddClinicAction, name='addClinic'),
    path('addpatientdata/', views.AddPatientData, name='addpatientdata'),
    path('ureqdata/', views.EditRequest, name='ureqdata'),
    path('searchbymobile/', views.Searchbymobile, name='searchbymobile'),
    path('deleteoldpataintdata/', views.DeleteOldPataintData, name='deleteoldpataintdata'),
    path('extrarun/', views.ExtraRun, name='extrarun'),
]

#handler404 = 'restapi.views.page_not_found_view'