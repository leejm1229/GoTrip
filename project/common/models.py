from django.db import models
 
class User(models.Model):
    username = models.CharField(max_length=32, verbose_name='사용자명',null=True,default='')
    useremail = models.EmailField(max_length=128, verbose_name='emailID',default='')
    password = models.CharField(max_length=128,verbose_name='비밀번호')
    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
 
    def __str__(self):
        return self.email
 
    class Meta:
        db_table = 'django_user'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'



