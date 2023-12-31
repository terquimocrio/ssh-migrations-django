# Generated by Django 4.1.1 on 2023-09-10 21:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GHConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=255)),
                ('repo_owner', models.CharField(max_length=255)),
                ('repo_name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Github Connection',
                'verbose_name_plural': 'Github Connections',
                'db_table': 'gh_connection',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='SSHConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ssh_name', models.CharField(max_length=50)),
                ('ssh_host', models.CharField(max_length=50)),
                ('ssh_port', models.CharField(max_length=50)),
                ('ssh_username', models.CharField(max_length=50)),
                ('ssh_private_key', models.FileField(max_length=255, upload_to='sshkeys/')),
            ],
            options={
                'verbose_name': 'SSH Connection',
                'verbose_name_plural': 'SSH Connections',
                'db_table': 'ssh_connection',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=50)),
                ('project_path', models.CharField(max_length=255)),
                ('gh_connection', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='sshmigrations.ghconnection')),
                ('ssh_connection', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='sshmigrations.sshconnection')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
                'db_table': 'project',
                'ordering': ['-id'],
            },
        ),
    ]
