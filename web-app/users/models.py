
from __future__ import unicode_literals
from django.db import  models

class UserInfo(models.Model):
    username = models.CharField(max_length=150, unique=True)
    pwd = models.CharField(max_length=30)

    #class Meta:
        #db_table = 't_user'



    #def __unicode__(self):
        #return u'UserInfo:%s'%self.username
