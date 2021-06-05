from __future__ import unicode_literals

from django import forms
from django.forms import ModelMultipleChoiceField

from django.contrib.auth.models import User
from .models import Data, Announcement, Profile, UserInfo, Current
from django_summernote.widgets import SummernoteWidget

class ParticipatorModelChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.student_info.name

class DataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        self.is_mobile = kwargs.pop('is_mobile', None)

        super(DataForm, self).__init__(*args, **kwargs)

        if user and user.profile.group is not None:
            current = Current.objects.all().first()
            self.fields['participator'].queryset = UserInfo.objects.filter(group=user.profile.group, year=current.year, sem=current.sem)


    image = forms.ImageField(label='', widget=forms.ClearableFileInput(
        attrs={
            'id': 'ex_file',
            'name': 'ex_file',
            'onchange': "javascript:document.getElementById('fileName').value = this.value",
        }
    ))

    participator = ParticipatorModelChoiceField(
        widget = forms.CheckboxSelectMultiple,
        queryset = UserInfo.objects.none()
    )

    __hour_choice = (
        ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), 
        ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), 
        ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), 
        ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), 
    )
    __minute_choice = (
        ('00', '00'), ('05', '05'),
        ('10', '10'), ('15', '15'), 
        ('20', '20'), ('25', '25'), 
        ('30', '30'), ('35', '35'),
        ('40', '40'), ('45', '45'), 
        ('50', '50'), ('55', '55'), 
    )
    __minute_choice_2 = (
        ('00', '00'), ('05', '05'),
        ('10', '10'), ('15', '15'), 
        ('20', '20'), ('25', '25'), 
        ('30', '30'), ('35', '35'),
        ('40', '40'), ('45', '45'), 
        ('50', '50'), ('55', '55'), 
        ('60', '60'), ('65', '65'),
        ('70', '70'), ('75', '75'), 
        ('80', '80'), ('85', '85'), 
        ('90', '90'), ('95', '95'),
        ('100', '100'), ('105', '105'), 
        ('110', '110'), ('115', '115'), 
        ('120', '120'), ('125', '125'), 
        ('130', '130'), ('135', '135'), 
        ('140', '140'), ('145', '145'), 
        ('150', '150'), ('155', '155'), 
        ('160', '160'), ('165', '165'), 
        ('170', '170'), ('175', '175'), 
        ('180', '180'), 
    )
    study_start_time = forms.CharField(label='', widget=forms.Select(choices=__hour_choice))
    study_start_time_minute = forms.CharField(label='', widget=forms.Select(choices=__minute_choice))
    
    study_total_duration = forms.IntegerField(label='', widget=forms.Select(choices=__minute_choice_2))

    title = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '제목을 입력해주세요.',
            }
        ))


    text = forms.CharField(widget=SummernoteWidget())



    class Meta:
        model = Data
        fields = ('text', 'participator', 'image', 'title', 'study_start_time', 'study_total_duration')

    def set_is_mobile(self):
        if self.is_mobile:
            self.fields['text'].widget = forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': '공부한 내용을 써주세요 ʕ•ﻌ•ʔ ♡',
                    }
            )

'''
class ProfileForm(forms.ModelForm):
    student_id = forms.IntegerField(label='', widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '학번을 입력해주세요.'
            }
        ))

    name = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '이름을 입력해주세요.',
            }
        ))

    email = forms.EmailField(label='', widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Email 주소를 입력해주세요',
            }
        ))
    class Meta:
        model = Member
        fields = ('student_id', 'name', 'email')
'''

class AnnouncementForm(forms.ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '제목',
        }
    ))

    content = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = Announcement
        fields = ('title' , 'content')
