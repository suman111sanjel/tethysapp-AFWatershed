from django.shortcuts import render
import json

from django.http import JsonResponse, HttpResponse
import ast
from dateutil import parser
import os
# from osgeo import gdal, ogr

import uuid
# import rioxarray
import xarray as xr
import rasterio as rio
# import geopandas as gpd
import rasterstats as rstats
import numpy
import netCDF4
from datetime import datetime
import base64
import shapely.wkt


import httplib2
import urllib
# from urllib.request import urlopen
import urllib.request
from django.http import HttpResponse

def WMSProxy(request,url):
    completeURL = str(request.build_absolute_uri())
    url=completeURL.split('/apps/AFWatershed/WMSProxy/')[-1]
    url=url.replace('/wms/?Service','/wms?Service').replace('.ncml/?FORMAT','.ncml?FORMAT').replace('.ncml/?SERVICE','.ncml?SERVICE')
    request1 = urllib.request.Request(url)
    response = urllib.request.urlopen(request1).read()
    return HttpResponse(response ,content_type="image/png")

