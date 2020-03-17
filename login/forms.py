#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/15 15:37
# @Author  : Xuan
# @File    : forms.py

from django import forms
from captcha.fields import CaptchaField

#登录界面的form表单类
class UserForm(forms.Form):
    username = forms.CharField(label="用户名",max_length=128,
                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Username",'autofocus':''}))
    password = forms.CharField(label="密码",max_length=256,
                               widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':"Password"}))
    captcha = CaptchaField(label='验证码')

#注册界面的form表单类
class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')
'''
说明：

gender字典和User模型中的一样，其实可以拉出来作为常量共用，为了直观，特意重写一遍；
password1和password2，用于输入两遍密码，并进行比较，防止误输密码；
email是一个邮箱输入框；
sex是一个select下拉框；
没有添加更多的input属性
'''