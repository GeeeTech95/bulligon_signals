from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework.authtoken.models import Token




class UserSerializer(serializers.ModelSerializer) :
    password_comfirmation  = serializers.CharField(write_only = True)
    referral_id = serializers.CharField(write_only = True,required = False)


    class Meta() :
        extra_kwargs = {
            "password" : {"write_only" : True},
            
        }
        model = get_user_model()
        fields = [
            'email',
            'name',
            'phone_number',
            'password',
            'password_comfirmation',
            'country',
            'referral_id'
        ]




    def validate_referral_id(self,ref_id) :
        try : 
            ref_id = int(ref_id)
        except :
            return
        return ref_id
    
            

    def validate(self,data) :
        pwd = data.get("password")
        pwd_comfirm = data.get("password_comfirmation")
        if pwd != pwd_comfirm :
            raise serializers.ValidationError("The two passwords does not match")

        return data    


    def create(self,data) :
        #remove password comfirmation
        del data['password_comfirmation']
        model = get_user_model()
        user = model.objects.create_user(**data)
        #_token = Token.objects.create(user = user)
        return user




class LoginSerializer(serializers.Serializer) :
   
    email = serializers.EmailField(required = False)
    password = serializers.CharField()
        

    def validate_email(self,email) :
        if email :
            if not get_user_model().objects.filter(email = email).exists() :
                raise serializers.ValidationError("No user with this email was found")      
        return email          

    def validate(self,data) :
        username = data.get("username")
        email = data.get("email")
        #at least one must be supplied
        if not username and not email :
            raise serializers.ValidationError("Credentials are incomplete, email or username is expected")
        return data
            



class ProfileSerializer(serializers.ModelSerializer) :
    otp = serializers.CharField(max_length = 6,min_length=6,write_only=True)
    old_password = serializers.CharField(max_length = 10,write_only = True)
    
    class Meta() :
        model = get_user_model()
        fields = [
            'pk',
            'passport',
            'gender',
            'first_name',
            'last_name',
            'phone_number',
            'otp',
            'email',
            'old_password',
            ]


    def validate_new_password(self,password) :
        user = self.context['request'].user
        if check_password(password,user.password) :
            raise serializers.ValidationError("Your new password is the same as your old password. it is not allowed")
        return password


    def validate_phone_number(self,phone_number) :
        return phone_number

    def validate_email(self,email) :
        if email == self.context['request'].user.email :
            raise serializers.ValidationError("Yor old email cannot be the same as your new email")
        return email   


    def validate(self,data) :
        user = self.context['request'].user
        #check if secured credentials is about to change
        if data.get("email") or data.get("phone_number")  : 
            #make sure password was entered
            old_password =  data.get("old_password")
            if not old_password  : raise serializers.ValidationError("You need to enter your password in order to effect this change")
            
            if  not check_password(old_password,user.password) :
                raise serializers.ValidationError("The password you entered is not correct please crosscheck")
            
          
        return data   



    """def perform_update(self) :
        print("ss")
        _update_fields = self.data.keys() 
        user = self.context['request'].user
        for _field in _update_fields :
            setattr(user,self.data[_field])
        user.save()  """     




class SettingSerializer(serializers.ModelSerializer) :
    otp = serializers.CharField(max_length = 6)
    new_password = serializers.CharField(max_length = 10,write_only = True,validators=[validate_password])
    old_password = serializers.CharField(max_length = 10,write_only = True)
    
    class Meta() :
        model = get_user_model()
        fields = [
            'pk',
            'passport',
            'gender',
            'first_name',
            'last_name',
            'phone_number',
            'otp',
            'email',
            'old_password',
            'new_password'
            ]


    def validate_new_password(self,password) :
        user = self.context['request'].user
        if check_password(password,user.password) :
            raise serializers.ValidationError("Your new password is the same as your old password. it is not allowed")
        return password


    def validate_comfirm_password(self,phone_number) :
        return phone_number


    def validate(self,data) :
        user = self.context['request'].user
        #check if secured credentials is about to change
        if data.get("email") or data.get("phone_number") or data.get("password") : 
            #make sure password was entered
            old_password =  data.get("old_password")
            if not old_password  : raise serializers.ValidationError("You need to enter your password in order to effect this change")
            
            if  not check_password(old_password,user.password) :
                raise serializers.ValidationError("The password you entered is not correct please crosscheck")
            
            #if user is changing new password
            new_password = data.get("new_password")
            if  new_password :
                user.set_password(new_password)
        return data   



    """def perform_update(self) :
        print("ss")
        _update_fields = self.data.keys() 
        user = self.context['request'].user
        for _field in _update_fields :
            setattr(user,self.data[_field])
        user.save()  """     



class DetailVerificationSerializer(serializers.Serializer) :
    verification_type = serializers.CharField()
    verification_code = serializers.CharField()

    verification_types = ['email','phone_number'] 

    def validate_verification_code(self,verification_code) :
        user = self.context['request'].user
        from core.security import OTP
        otp = OTP(user) 
        validated,error = otp.validate_otp(verification_code)  
        if not validated :
            raise serializers.ValidationError(error)

        return verification_code   


    def validate_verification_type(self,verification_type) :
        if  verification_type not in self.verification_types :
            raise serializers.ValidationError("verification type is not valid")

        return verification_type    


    def validate(self,data) :
    
        user = self.context['request'].user
        
        ver_type = data.get("verification_type")

        if ver_type == "email" : 
            #never update the email, update should be done properly   
            #mark email as verified
            if user.email_verified :
                raise serializers.ValidationError("Your email is already verified")
            user.email_verified = True
            user.save()    
           
 

        elif ver_type == "phone_number" :
            if user.phone_number_verified :
                raise serializers.ValidationError("Your email is already verified")
            #mark phone number as verified
            user.phone_number_verified = True
            user.save() 
        
        
        return data