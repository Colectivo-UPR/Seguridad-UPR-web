from rest_framework import serializers
from core.models import *

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ('id', 'email','first_name','last_name','password')
        write_only_fields = ('password',)
    def create(self, validated_data):
        user = AuthUser.objects.create_user(email= validated_data['email'], password=validated_data['password'])
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        return user

class AuthUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ('username','email','first_name','last_name')

        read_only_fields = ('email',)


class IncidentSerializer(serializers.ModelSerializer):

    owner = serializers.Field(source='owner.id')

    class Meta:
        model = Incident
        fields = ('id', 'owner','title','pub_date','incident_date', 'message','faculty','lat','lon')


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('id', 'title','pub_date','message','faculty','lat','lon')

class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ('id', 'place','description','lat','lon')

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'name','telephone')

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ('id', 'title','pub_date','incident_date', 'message','faculty','lat','lon')

class OfficialsPhonesSerializer(serializers.ModelSerializer):

    official = serializers.PrimaryKeyRelatedField(queryset=AuthUser.objects.all())

    class Meta:
        model = OfficialsPhones
        fields = ('id', 'official', 'phone_number')



"""
    Sancion arresto Serializer
"""

class SancionArrestoSerializer(serializers.ModelSerializer):

    class Meta:
        model = SancionArresto
        fields = ('id','tipo')

"""
    Tipo Incidente Serializer
"""

class TipoIncidenteSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoIncidente
        fields = ('id','tipo')

"""
    Medio Notificacion Serializer
"""

class MedioNotificacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedioNotificacion
        fields = ('id','tipo')

"""
    Forma se Refirio Serializer
"""

class FormaSeRefirioSerializer(serializers.ModelSerializer):

    class Meta:
        model = FormaSeRefirio
        fields = ('id','tipo')

"""
    Querellante Serializer
"""
class QuerellanteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Querellante
        fields = (
            'id',
            'id_querella',
            'nombre',
            'direccion_residencial',
            'direccion_postal',
            'lugar_trabajo',
            'tipo_identificacion',
            'numero_identificacion',
            'tel_trabajo',
            'tel_personal',
            'sector',
            'genero',
            'email'
            )

"""
    Sector Serializer
"""
class SectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sector
        fields = ('id', 'sector')

"""
    Oficiales Intervinieron Serializer
"""
class OficialesIntervinieronSerializer(serializers.ModelSerializer):

    class Meta:
        model = OficialesIntervinieron
        fields = (
            'id',
            'id_querella',
            'nombre',
            'turno',
            'numero_placa'
            )

"""
    Querellados Serializer
"""
class QuerelladoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Querellado
        fields = (
            'id',
            'id_querella',
            'nombre',
            'direccion_residencial',
            'direccion_postal',
            'telefono'
            )

"""
    Perjudicado Serializer
"""
class PerjudicadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Perjudicado
        fields = (
            'id',
            'id_querella',
            'nombre',
            'direccion_residencial',
            'direccion_postal',
            'telefono'
            )

"""
    Testigo Serializer
"""
class TestigoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Testigo
        fields = (
            'id',
            'id_querella',
            'direccion_residencial',
            'direccion_postal',
            'telefono'
            )

"""
    Area Geografica Serializer
"""
class AreaGeograficaSerializer(serializers.ModelSerializer):

    class Meta:
        model = AreaGeografica
        fields = ('id','tipo')

"""
    Querella Serializer
"""
class QuerellaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Querella
        fields = (
            'id',
            'numero_caso',
            'fecha_informada',
            'medio_notificacion',
            'hay_fotos',
            'official_atendio',
            'placa_official',
            'referido_a',
            'agente_se_notifico',
            'placa_agente',
            'numero_caso_policia',
            'forma_se_refirio',
            'accion_tomada',
            'fecha_incidente',
            'lugar_incidente',
            'area_incidente',
            'tipo_incidente',
            'crimen_odio',
            'descripcion_incidente',
            'sancion_arresto',
            'area_geografica'
            )


