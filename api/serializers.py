from rest_framework import serializers
from .models import User, Task
#serializers are used to transform data into JSON format so we can send it over the web

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #these are the fields that we are going to send
        fields = ['id','name','email','password']
        #this means we cannot read but only right passwords
        extra_kwargs = {
            'password': {'write_only':True}
        }

    #this is used to hash the password using django native hashing
    #this function sits between the view and model creation
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        # the **validated data is data without the password
        instance = self.Meta.model(**validated_data)
        if password is not None:
            #set_password is provided by django and will hash the password
            instance.set_password(password)
        instance.save()
        return instance
    
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
