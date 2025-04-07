# Generated by Django 5.0.2 on 2025-02-15 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msys42app', '0003_alter_child_spc_sex'),
    ]

    operations = [
        migrations.RenameField(
            model_name='child',
            old_name='spc_birth',
            new_name='birth',
        ),
        migrations.RenameField(
            model_name='child',
            old_name='spc_code',
            new_name='code',
        ),
        migrations.RenameField(
            model_name='child',
            old_name='contact_number',
            new_name='contact',
        ),
        migrations.RemoveField(
            model_name='child',
            name='spc_name',
        ),
        migrations.RemoveField(
            model_name='child',
            name='spc_sex',
        ),
        migrations.AddField(
            model_name='child',
            name='firstname',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='child',
            name='lastname',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='child',
            name='middlename',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='child',
            name='sex',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='child',
            name='guardian_name',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='child',
            name='guardian_relationship',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='child',
            name='guardian_sex',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=10, null=True),
        ),
    ]
