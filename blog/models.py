from django.db import models

# 注意:每次更改后执行加载模型
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
