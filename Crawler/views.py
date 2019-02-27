# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
from django.contrib.staticfiles.views import serve
import json

sys.path.append(os.getcwd())
from util import GetImagesUtil, GetLinksUtil


# Create your views here.

@api_view(["POST"])
def GetLinks(siteData):
	try:
		res = GetLinksUtil(siteData)
		return JsonResponse({'links': res},safe=False)
	except ValueError as e:
		return Response(e.args[0],status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def GetImages(siteData):
	try:
		res = GetImagesUtil(siteData)
		return JsonResponse({'images': res},safe=False)
	except ValueError as e:
		return Response(e.args[0],status.HTTP_400_BAD_REQUEST)

def index(request):
	return serve(request, os.path.join(settings.BASE_DIR, 'Crawler/public/index.html'))

def serve_js(request, file_name):
	return serve(request, os.path.join(settings.BASE_DIR, 'Crawler/public/js/'+file_name))

def serve_css(request, file_name):
	return serve(request, os.path.join(settings.BASE_DIR, 'Crawler/public/css/'+file_name))