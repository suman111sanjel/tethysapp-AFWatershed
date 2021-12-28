
import xarray as xr
import netCDF4
import matplotlib
matplotlib.use('Agg')
import numpy as np
import datetime
import glob
import rasterio as rio
import numpy
import rasterstats as rstats
import shapely.wkt

from tethysapp.AFWatershed.app import AFWatershed as app
from tethysapp.AFWatershed.model import GelogicalRockType, HydrologicalMajorBasin, HydrologicalMacroLevelWatershed, \
    Statistic, GelogicalGeologyTemplate, GelogicalMineralType, GelogicalFaultLine
from rasterstats import zonal_stats
import datetime

import os
from sqlalchemy import func
from sqlalchemy.sql import select, insert
from sqlalchemy import cast
from geoalchemy2 import Geography, Geometry
import copy
import ast
import colorsys
from django.http import JsonResponse
from sqlalchemy import update
from tethysapp.AFWatershed.config import BaseDir
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker
# Column Chart
def ClimateTimeSeries(request):
    engine = app.get_persistent_store_database('watershed_afganistan', as_sessionmaker=False)
    engineURL=engine.url
    NewEngine = create_engine(engineURL, poolclass=NullPool)
    session = sessionmaker(bind=NewEngine)()
    if (session):
        layerName = ast.literal_eval(request.POST.get('layerName'))
        controlGid = ast.literal_eval(request.POST.get('controlGid'))
        DataDir = ast.literal_eval(request.POST.get('DATADIR'))
        LAYER = ast.literal_eval(request.POST.get('LAYER'))
        WKTType = ast.literal_eval(request.POST.get('type'))
        DataInterval = ast.literal_eval(request.POST.get('DataInterval'))
        ncFile = BaseDir + str(DataDir)
        collectionDir = None
        if '.ncml' in ncFile:
            collectionDir = ncFile.replace('.ncml', '')

        IsWKT = request.POST.get('is_wkt')
        if (IsWKT == "true"):
            IsWKT = True
        else:
            IsWKT = False

        worinkgModelObjectQuery = None
        modelObject = None
        if layerName == "basin":
            modelObject = copy.deepcopy(HydrologicalMajorBasin)
        elif layerName == "watershed":
            modelObject = copy.deepcopy(HydrologicalMacroLevelWatershed)
        if (not IsWKT):
            worinkgModelObjectQuery = session.query(modelObject).filter(modelObject.gid == controlGid)
        else:
            aoiWKT = ast.literal_eval(request.POST.get('wkt'))
            worinkgModelObjectQuery = session.query(
                func.ST_Transform(func.ST_SetSRID(func.ST_GeomFromText(aoiWKT), 3857), 4326).label('geom'))
        Data = None
        for kk in worinkgModelObjectQuery:
            # rock_type
            poly = session.query(kk.geom.ST_AsText())[0]
            Data = TimeSeriesModelDataCompute(collectionDir, LAYER, poly, WKTType,DataInterval)
            break

        allData = Data

        session.close()
        return JsonResponse(allData)
    else:
        allData = {"status": 500, "error": "Something went wrong"}
        return JsonResponse(allData)

def TimeSeriesModelDataCompute(collectionDir, parameterName, wkt,WKTType,DataInterval):

    AllNetCDFList=glob.glob(collectionDir+'/*.nc')
    seriesData=[]
    AllDates=[]
    AllNetCDFList.sort()
    for i in AllNetCDFList:
        nc_fid = netCDF4.Dataset(i, 'r')  # Reading the netCDF file
        lis_var = nc_fid.variables

        lats=None
        lons=None

        try:
            lats = nc_fid.variables['latitude'][:]  # Defining the latitude array
            lons = nc_fid.variables['longitude'][:]  # Defining the longitude array
        except:
            lats = nc_fid.variables['lat'][:]  # Defining the latitude array
            lons = nc_fid.variables['lon'][:]  # Defining the longitude array

        field = nc_fid.variables[parameterName][:]  # Defning the variable array
        time = nc_fid.variables['time'][:]

        deltaLats = lats[1] - lats[0]
        deltaLons = lons[1] - lons[0]

        deltaLatsAbs = numpy.abs(deltaLats)
        deltaLonsAbs = numpy.abs(deltaLons)

        if WKTType=='point':
            stn_lat=float(wkt.split("(")[1].split(")")[0].split(" ")[1])
            stn_lon=float(wkt.split("(")[1].split(")")[0].split(" ")[0])
            abslat = numpy.abs(lats - stn_lat)  # Finding the absolute latitude
            abslon = numpy.abs(lons - stn_lon)  # Finding the absolute longitude

            lat_idx = (abslat.argmin())
            lon_idx = (abslon.argmin())

        geotransform = rio.transform.from_origin(lons.min(), lats.max(), deltaLatsAbs, deltaLonsAbs)

        for timestep, v in enumerate(time):

            nc_arr = field[timestep]
            nc_arr[nc_arr < -9000] = numpy.nan  # use the comparator to drop nodata fills
            if deltaLats > 0:
                nc_arr = nc_arr[::-1]  # vertically flip array so tiff orientation is right (you just have to, try it)

            dt_str = netCDF4.num2date(lis_var['time'][timestep], units=lis_var['time'].units,
                                      calendar=lis_var['time'].calendar)
            strTime = str(dt_str)
            dt_str = datetime.datetime.strptime(strTime, '%Y-%m-%d %H:%M:%S')
            dateInmillisecond = dt_str.timestamp() * 1000
            AllDates.append(dt_str.date())

            interestedValue=None
            if WKTType == 'polygon':
                tt = rstats.zonal_stats(wkt, nc_arr, affine=geotransform, stats='mean')
                interestedValue=tt[0]['mean']
            else:
                a = field[timestep, lat_idx, lon_idx]
                if np.isnan(a):
                    interestedValue=False
                else:
                    b=str(a)
                    interestedValue=float(b)
            print("hello")

            if interestedValue:
                # strTime=str(dt_str)
                # print(strTime)
                # dt_str=datetime.datetime.strptime(strTime, '%Y-%m-%d %H:%M:%S')
                # dateInmillisecond = dt_str.timestamp() * 1000
                value = round(interestedValue, 3)
                seriesData.append([int(dateInmillisecond), value])
                # AllDates.append(dt_str.date())

        nc_fid.close()
    print(seriesData)
    DateRange=None
    try:
        if DataInterval=="annual":
            DateRange = '(' +str(AllDates[0].year) + "-" +  str(AllDates[-1].year)+')'
        else:
            DateRange = '(' + str(AllDates[0])[:7] + "  -  " + str(AllDates[-1])[:7] + ')'
    except:
        DateRange = ''
    return {"SeriesData":seriesData,"status":200,"DateRange":DateRange}
