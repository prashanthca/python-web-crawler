# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Links(models.Model):
	url = models.TextField()
	json = models.TextField()

	def __unicode__(self):
		return self.url

class Images(models.Model):
	url = models.TextField()
	json = models.TextField()

	def __unicode__(self):
		return self.url