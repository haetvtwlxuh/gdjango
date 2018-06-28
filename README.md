# django中使用markdown实现代码高亮


## 注意： 请使用django2.0+，安装依赖
 
	pip install django 
	pip install markdown

## 一.新建一个项目gwbblog

	django-admin startproject gwbblog
	cd gwbblog

## 二.新建一个app叫blog

	python manage.py startapp blog

## 三.把app加入配置文件settings.py文件，并修改语言和时区
	gwbblog/gwbblog/settings.py
	
	INSTALLED_APPS = [
    # 加入blog
    'blog.apps.BlogConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	]

	#时区和语言
	LANGUAGE_CODE = 'zh-hans'

	TIME_ZONE = 'Asia/Shanghai'

## 四.和manage.py文件同文件夹，新建一个文件夹static，里面用来存放静态文件，再建一个templates，用来存放html，全部加入setting.py文件，如下：

	STATIC_URL = '/static/'
	STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
	
	
	
	TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,

## 五.打开models.py,添加一下代码，并执行三个操作，完成数据库新建

	from django.db import models

	# 注意每次更改后执行加载模型
	# 1. python manage.py makemigrations
	# 加载数据库
	# 2. python manage.py migrate
	# 创建管理员
	# 3.python manage.py createsuperuser
	
	
	class Post(models.Model):
	    blog_title = models.CharField('标题',max_length=200)
	    blog_body = models.TextField("正文")
	    blog_time = models.DateTimeField('更新时间')
	
	    def __str__(self):
	        return self.blog_title
	
	    class Meta:
	        verbose_name = '博文'
	        verbose_name_plural = '博文'

## 六.打开admin.py文件，添加以下代码

	from django.contrib import admin
	from .models import Post
	
	admin.site.register(Post)


## 七.打开views.py,输入以下代码

	from django.shortcuts import render, get_object_or_404
	import markdown
	from .models import Post
	
	
	def index(request):
	    context = Post.objects.all()
	    return render(request, 'index.html', {'context': context})
	
	
	def deta(request, blog_id):
	    context = get_object_or_404(Post, pk=blog_id)
	    config = {
	        'codehilite': {
	            'use_pygments': False,
	            'css_class': 'prettyprint linenums',
	        }
	    }
	    context.blog_body = markdown.markdown(context.blog_body, extensions=['codehilite'], extension_configs=config)
	    return render(request, 'deta.html', {'context': context})


## 八.在views.py所在目录新建一个urls.py文件，输入以下代码
	#!/usr/bin/env python
	# -*- coding: utf-8 -*-
	from django.urls import path
	from . import views
	
	urlpatterns = [
	    path('',views.index,name='index'),
	    path('blog/<int:blog_id>',views.deta,name='deta'),
	]

## 九.修改gwbblog/gwbblog/urls.py

	from django.contrib import admin
	from django.urls import path,include
	
	urlpatterns = [
	    path('admin/', admin.site.urls),
	    path('',include('blog.urls')),
	]



## 十.deta.html我们用来放置博文详情页

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>ZLOE</title>
	    <link href="/static/css/github.css" rel="stylesheet"/>
	    <script src="/static/js/run_prettify.js"></script>
	    <link href="https://cdn.rawgit.com/google/code-prettify/master/loader/skins/desert.css" rel="stylesheet">
	    <link rel="stylesheet" href="http://picturebag.qiniudn.com/monokai.css">
	
	
	</head>
	<body>
	<hr>
	    <div class="head">
	        <h1>{{ context.blog_title }}</h1>
	        <p>{{ context.blog_time }}</p>
	    </div>
	<hr>
	    <div class="text">
	        {{ context.blog_body | safe }}
	    </div>
	</body>
	</html>

{{ context.blog_body | safe }}，safe提示这个是安全的html，允许前端执行渲染，千万不要忘记加

> 项目地址：https://github.com/msterzhang/gdjango，如有错误，还请评论区指出