from django.shortcuts import render,redirect
from django.conf import settings
from .import models,forms
import hashlib,datetime
from django.core.mail import EmailMultiAlternatives
# Create your views here.

#使用哈希值的方式加密密码
def hash_code(s,salt='LoginWeb'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())#update方法只接收bytes类型
    return h.hexdigest()

def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user)
    return code

def send_email(email, code):

    subject = '来自www.xxx.com的注册确认邮件'

    text_content = '''感谢注册www.xxx.com，这里是专注于Python、Django和机器学习技术的分享！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.liujiangblog.com</a>，\
                    这里是专注于Python、Django和机器学习技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def index(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')
    return render(request,'login/index.html')

def login(request):
    if request.session.get('is_login',None): #不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid(): #数据验证工作
            username = login_form.cleaned_data.get('username')#验证成功后可以从表单对象的cleaned_data数据字典中获取表单的具体值
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用户不存在！'
                return render(request, 'login/login.html',locals())

            if not user.has_confirmed:
                message = '该用户还未经过邮件确认'
                return render(request,'login/login.html',locals())

            if user.password == hash_code(password):
                # 往session字典内写入用户状态和数据
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request,'login/login.html',locals())
        else:
            return render(request,'login/login.html',locals())

    login_form = forms.UserForm()
    return render(request,'login/login.html',locals())

def register(request):
    if request.session.get('is_login',None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)#实例化一个RegisterForm的对象
        message = "请检查填写的内容！"
        if register_form.is_valid():#使用is_valide()进行数据验证
            username = register_form.cleaned_data.get('username')#从cleaned_data中获取数据
            password1 = register_form.cleaned_data.get('password1')#两次输入的密码必须相同
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不一致！'
                return render(request,'login/register.html',locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已存在！'
                    return render(request,'login/register.html',locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已被注册！'
                    return render(request,'login/register.html',locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code = make_confirm_string(new_user)#make_confirm_string()是创建确认码对象的方法
                send_email(email,code)

                message = '请前往邮箱进行确认！'
                return render(request,'login/confirm.html',locals())
        else:
            return render(request,'login/register.html',locals())
    register_form = forms.RegisterForm()
    return render(request,'login/register.html',locals())

def logout(request):
    if not request.session.get('is_login',None):
        # 如果本来就未登录，也就没有登出一说
        return redirect('/login/')
    request.session.flush()

    # flush()方法是比较安全的一种做法，而且一次性将session中的所有内容全部清空，确保不留后患。
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login")

def user_confirm(request):
    code = request.GET.get('code', None)
    message = ' '
    try:
        #通过request.GET.get('code', None)从请求的url地址中获取确认码
        #先去数据库内查询是否有对应的确认码
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        #如果没有，返回confirm.html页面，并提示
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())
        #如果有，获取注册的时间c_time，加上设置的过期天数，这里是7天，然后与现在时间点进行对比
    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        # 如果时间已经超期，删除注册的用户，同时注册码也会一并删除，然后返回confirm.html页面，并提示
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        # 如果未超期，修改用户的has_confirmed字段为True，并保存，表示通过确认了。
        # 然后删除注册码，但不删除用户本身。最后返回confirm.html页面，并提示
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())