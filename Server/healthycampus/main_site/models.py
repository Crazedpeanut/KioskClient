from django.db import models

class Page(models.Model):
    header = models.CharField(max_length=200, default="Website Name")
    content = models.TextField(default="Website Name")
    footer = models.CharField(max_length=200, default="Copyright 2014")

    def __str__(self):             
        return self.header