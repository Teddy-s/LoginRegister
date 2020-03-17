from django.db import models

# Create your models here.

class User(models.Model):
    gender = (
        ('male',"男"),
        ('female',"女"),
              )
    '''
    各字段含义：

name: 必填，最长不超过128个字符，并且唯一，也就是不能有相同姓名；
password: 必填，最长不超过256个字符（实际可能不需要这么长）；
email: 使用Django内置的邮箱类型，并且唯一；
sex: 性别，使用了一个choice，只能选择男或者女，默认为男；
使用__str__方法帮助人性化显示对象信息；
元数据里定义用户按创建时间的反序排列，也就是最近的最先显示
    '''
    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32,choices=gender,default="男")
    c_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)
#新增了has_confirmed字段，这是个布尔值，默认为False，也就是未进行邮件注册

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"

class ConfirmString(models.Model):
    #ConfirmString模型保存了用户和注册码之间的关系，一对一的形式
    code = models.CharField(max_length=256)#code字段是哈希后的注册码
    user = models.OneToOneField('User', on_delete=models.CASCADE)#user是关联的一对一用户
    c_time = models.DateTimeField(auto_now_add=True)#c_time是注册的提交时间

    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:

        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"