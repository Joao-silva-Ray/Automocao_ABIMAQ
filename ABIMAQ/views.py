import subprocess
import os
from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from django.conf import settings
from .models import PesquisaABIMAQ
from django.shortcuts import get_object_or_404

def 