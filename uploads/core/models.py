from __future__ import unicode_literals

from django.db import models
from django import forms
from django.contrib.auth.models import User
import urllib.parse as urlparse
from urllib.parse import parse_qs

class Json(models.Model):
    document = models.FileField(upload_to="documents/json")

class Yaml(models.Model):
    document = models.FileField(upload_to="documents/yml")

class Name(models.Model):
    your_name = models.CharField(max_length=100)



