# Generated by Django 2.1.4 on 2018-12-28 18:58

from django.db import migrations

from django.utils import timezone

def populate(apps, schema_editor):
    Question = apps.get_model('polls', 'Question')
    Choice = apps.get_model('polls', 'Choice')

    Question.objects.bulk_create([
        Question(question_text='q1', pub_date=timezone.now()),
        Question(question_text='q2', pub_date=timezone.now()),
        Question(question_text='q3', pub_date=timezone.now()),
    ])

    questions = Question.objects.all()

    for question in questions:
        Choice.objects.create(question=question, choice_text='choice 1',votes=1)
        Choice.objects.create(question=question, choice_text='choice 2',votes=2)

def purge(apps, schema_editor):
    Question = apps.get_model('polls', 'Question')
    Choice = apps.get_model('polls', 'Choice')
    Question.objects.all().delete()
    Choice.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate, purge)
    ]