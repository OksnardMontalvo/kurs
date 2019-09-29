from django.contrib import admin

# Register your models here.
from studykurs.models import Category, Course, Comments, UserAccount

class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category)
admin.site.register(Comments)
admin.site.register(Course, CourseAdmin)
admin.site.register(UserAccount)