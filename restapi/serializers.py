from rest_framework import serializers
from . models import ChangeLog, DocType, Docs, PatientTreatment, Payment, PaymentType, UserType,Country,Disease,State,UserRole,HealthCardType,AppUser,Employee,Clinic,Attendance,UserRequest,Patient,Treatment,ClinicDoctor,TherapySet,MedicineSet,HealthCardTypeCategory,CareOf

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'


class HealthCardTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthCardType
        fields = '__all__'

class CareOfSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareOf
        fields = '__all__'

class HealthCardTypeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthCardTypeCategory
        fields = '__all__'


class AppUserSerializer(serializers.ModelSerializer):
    def validate_username(self,value):
        AppUser = self.Meta.model
        if AppUser.objects.filter(username = value).exists():
            raise serializers.ValidationError('Already Exist')
        return value

    class Meta:
        model = AppUser
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class UserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequest
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = '__all__'


class ClinicDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicDoctor
        fields = '__all__'
        

class MedicineSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineSet
        fields = '__all__'


class TherapySetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TherapySet
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = '__all__'

class DocTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocType
        fields = '__all__'

class DocsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docs
        fields = '__all__'

class PatientTreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientTreatment
        fields = '__all__'

class ChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeLog
        fields = '__all__'