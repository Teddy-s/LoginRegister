## 该项目教程根据刘江老师发布在www.liujiangblog.com的项目教程学习而来
##特在此感谢刘江老师提供的项目教程资源
## 这是一个用户登录和注册教学项目，实现一个可重用的登录和注册APP。

## 以下是该项目的简单的使用方法：


创建虚拟环境
使用pip安装第三方依赖
修改settings.example.py文件为settings.py
运行migrate命令，创建数据库和数据表
运行python manage.py runserver启动服务器


路由设置：


from django.contrib import admin
from django.urls import path, include
from login import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('confirm/', views.user_confirm),
    path('captcha/', include('captcha.urls'))   # 增加这一行
]
对于许可文件LICENSE，如果你暂时不想公开授权，或者不知道用哪种授权，可以暂时不提供。

下面是一个APACHE2.0授权的范例：

   mysite - User login and register system

   Copyright 2019- www.liujiangblog.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.