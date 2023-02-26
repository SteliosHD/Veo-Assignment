# Generated by Django 4.1.7 on 2023-02-25 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('height', models.PositiveIntegerField()),
                ('node_type', models.CharField(choices=[('MANAGER', 'Manager'), ('DEVELOPER', 'Developer'), ('NONE', 'None')], default='NONE', max_length=50)),
                ('department_name', models.CharField(blank=True, max_length=50, null=True)),
                ('language_preference', models.CharField(blank=True, max_length=50, null=True)),
                ('parent_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='veo_company_structure.node')),
            ],
        ),
    ]