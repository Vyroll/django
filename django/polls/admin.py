from django.contrib import admin

from .models import Question, Choice, Person, Task

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

class TaskInline(admin.TabularInline):
    model = Task
    extra = 3

class PersonAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
    ]
    inlines = [TaskInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)

admin.site.register(Task)
admin.site.register(Person, PersonAdmin)