from django.db import models

# Create your models here.
class SSHConnection(models.Model):
    ssh_name = models.CharField(max_length=50)
    ssh_host = models.CharField(max_length=50)
    ssh_port = models.CharField(max_length=50)
    ssh_username = models.CharField(max_length=50)
    ssh_private_key = models.FileField(upload_to='sshkeys/', max_length=255)

    class Meta:
        verbose_name = 'SSH Connection'
        verbose_name_plural = 'SSH Connections'
        db_table = 'ssh_connection'
        ordering = ['-id']

    def __str__(self):
        return self.ssh_host

class GHConnection(models.Model):
    access_token = models.CharField(max_length=255)
    repo_owner = models.CharField(max_length=255)
    repo_name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Github Connection'
        verbose_name_plural = 'Github Connections'
        db_table = 'gh_connection'
        ordering = ['-id']

    def __str__(self):
        return self.repo_name

class Project(models.Model):
    project_name = models.CharField(max_length=50)
    project_path = models.CharField(max_length=255)
    ssh_connection = models.ForeignKey(SSHConnection, on_delete=models.DO_NOTHING)
    gh_connection = models.ForeignKey(GHConnection, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        db_table = 'project'
        ordering = ['-id']

    def __str__(self):
        return self.project_name