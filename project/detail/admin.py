from django.contrib import admin
from .models import Board, Img, Kakao
# Register your models here.

class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'contents', 'scope')

class ImgAdmin(admin.ModelAdmin):
    list_display = ('address',)

class KakaoAdmin(admin.ModelAdmin):
    list_display = ('x','y')

admin.site.register(Board, BoardAdmin)
admin.site.register(Img, ImgAdmin)
admin.site.register(Kakao, KakaoAdmin)