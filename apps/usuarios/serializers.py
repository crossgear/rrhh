"""
Serializers para el modelo Usuario
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

Usuario = get_user_model()


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para lectura y escritura de Usuario.
    """
    nombre_completo = serializers.SerializerMethodField()
    ROL_display = serializers.CharField(source='get_ROL_display', read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'CI',
            'CARGO',
            'DIRECCION_INSTITUCIONAL',
            'TELEFONO_INTERNO',
            'ROL',
            'ROL_display',
            'is_active',
            'is_staff',
            'date_joined',
            'nombre_completo'
        ]
        read_only_fields = [
            'id',
            'date_joined',
            'last_login'
        ]

    def get_nombre_completo(self, obj):
        return obj.nombre_completo

    def validate_CI(self, value):
        """Validar que la cédula sea única si se proporciona."""
        if value:
            if Usuario.objects.filter(CI=value).exclude(id=self.instance.id if self.instance else None).exists():
                raise serializers.ValidationError('Esta cédula ya está registrada.')
        return value


class UsuarioCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear nuevos usuarios.
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    ROL = serializers.ChoiceField(choices=Usuario.Rol.choices, default=Usuario.Rol.CONSULTA)

    class Meta:
        model = Usuario
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'CI',
            'CARGO',
            'DIRECCION_INSTITUCIONAL',
            'TELEFONO_INTERNO',
            'ROL',
            'is_active',
            'is_staff',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        user = Usuario.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        user.CI = validated_data.get('CI', '')
        user.CARGO = validated_data.get('CARGO', '')
        user.DIRECCION_INSTITUCIONAL = validated_data.get('DIRECCION_INSTITUCIONAL', '')
        user.TELEFONO_INTERNO = validated_data.get('TELEFONO_INTERNO', '')
        user.ROL = validated_data.get('ROL', Usuario.Rol.CONSULTA)
        user.is_staff = validated_data.get('is_staff', False)
        user.is_active = validated_data.get('is_active', True)
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer para cambio de contraseña.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
