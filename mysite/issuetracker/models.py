# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class User(models.Model):
    uid = models.AutoField(primary_key=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    uname = models.CharField(max_length=40, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)
    disname = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class Project(models.Model):
    pid = models.IntegerField(primary_key=True)
    pname = models.CharField(max_length=40, blank=True, null=True)
    pdescription = models.CharField(max_length=500, blank=True, null=True)
    puid = models.ForeignKey('User', models.CASCADE, db_column='puid', blank=True, null=True)
    ptime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project'


class Issue(models.Model):
    iid = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=40, blank=True, null=True)
    idescription = models.CharField(max_length=500, blank=True, null=True)
    currentstatus = models.ForeignKey('Status', models.CASCADE, db_column='currentstatus', blank=True, null=True)
    iuid = models.ForeignKey('User', models.CASCADE, db_column='iuid', blank=True, null=True)
    itime = models.DateTimeField(blank=True, null=True)
    ipid = models.ForeignKey('Project', models.CASCADE, db_column='ipid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'issue'




class Status(models.Model):
    sid = models.IntegerField(primary_key=True)
    sname = models.CharField(max_length=40, blank=True, null=True)
    sdescription = models.CharField(max_length=500, blank=True, null=True)
    spid = models.ForeignKey(Project, models.CASCADE, db_column='spid')

    class Meta:
        managed = False
        db_table = 'status'



