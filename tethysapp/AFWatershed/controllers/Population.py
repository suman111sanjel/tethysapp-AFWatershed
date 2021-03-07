from tethysapp.AFWatershed.app import AFWatershed as app
from tethysapp.AFWatershed.model import GelogicalRockType, HydrologicalMajorBasin, HydrologicalMacroLevelWatershed, \
    Statistic, GelogicalGeologyTemplate, GelogicalMineralType, GelogicalFaultLine
from rasterstats import zonal_stats
from datetime import datetime

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
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker
from tethysapp.AFWatershed.config import TifDir

populationDensity = TifDir + '/populationDensity.tif'
villageDensity = TifDir + '/villageDensity.tif'


# Pie Chart
def PopulationDensity(request):
    engine = app.get_persistent_store_database('watershed_afganistan', as_sessionmaker=False)
    engineURL=engine.url
    NewEngine = create_engine(engineURL, poolclass=NullPool)
    session = sessionmaker(bind=NewEngine)()

    if (session):
        layerName = ast.literal_eval(request.POST.get('layerName'))
        controlGid = ast.literal_eval(request.POST.get('controlGid'))
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
            QueryObj = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
                Statistic.gid == controlGid)

            countObject = QueryObj.count()
            if (countObject):
                print("From Database")
                rockTypeData = QueryObj[0].population_population_density
                if (rockTypeData != None):
                    session.close()
                    return JsonResponse(rockTypeData)

            worinkgModelObjectQuery = session.query(modelObject).filter(modelObject.gid == controlGid)
        else:
            aoiWKT = ast.literal_eval(request.POST.get('wkt'))
            worinkgModelObjectQuery = session.query(
                func.ST_Transform(func.ST_SetSRID(func.ST_GeomFromText(aoiWKT), 3857), 4326).label('geom'))
            # worinkgModelObjectQuery = copy.deepcopy(cc)
        classifiedData = []
        for kk in worinkgModelObjectQuery:
            # slope
            poly = session.query(kk.geom.ST_AsText())[0]

            stats = zonal_stats(poly, populationDensity, copy_properties=True, nodata_value=0, categorical=True)
            classifiedData = classifyPopulationDensity(stats[0])

            break
        allData = {"seriesData": classifiedData, "status": 200}
        if (not IsWKT):
            try:
                statObj = Statistic(layer_name=layerName, gid=controlGid, population_population_density=allData)
                session.add(statObj)
                session.commit()
            except:
                session.rollback()
                updateObjectStatistic = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
                    Statistic.gid == controlGid).first()
                updateObjectStatistic.population_population_density = allData
                session.commit()

        session.close()
        return JsonResponse(allData)
    else:
        allData = {"status": 500, "error": "Something went wrong"}
        return JsonResponse(allData)


def classifyPopulationDensity(data):
    mappingDict = {
        '1 - 3': {"name": "0 - 30", "color": "#f0f0f0", "count": 0},
        '4 - 6': {"name": "31 - 100", "color": "#79ad00", "count": 0},
        '7 - 9': {"name": "101 - 400", "color": "#fffc06", "count": 0},
        '10 - 12': {"name": "401 - 1000", "color": "#ff9900", "count": 0},
        '13 - 15': {"name": "1001 - 1500", "color": "#fb2402", "count": 0}
    }

    populationD = data.keys()
    for i in populationD:
        a = float(i)
        if a >= 1 and a < 4:
            mappingDict['1 - 3']["count"] = mappingDict['1 - 3']["count"] + data[i]
        elif a >= 4 and a < 7:
            mappingDict['4 - 6']["count"] = mappingDict['4 - 6']["count"] + data[i]
        elif a >= 7 and a < 10:
            mappingDict['7 - 9']["count"] = mappingDict['7 - 9']["count"] + data[i]
        elif a >= 10 and a < 13:
            mappingDict['10 - 12']["count"] = mappingDict['10 - 12']["count"] + data[i]
        elif a >= 13:
            mappingDict['13 - 15']["count"] = mappingDict['13 - 15']["count"] + data[i]

        KeyValueList = list(mappingDict.items())
        total = sum(v["count"] for (k, v) in mappingDict.items())
        ChartData = list(map(lambda kk: {"name": kk[1]["name"], "y": round(kk[1]["count"] * 100 / total, 2),
                                         "color": kk[1]["color"]},
                             KeyValueList))
    return ChartData


# Column Chart
def VillageDensity(request):
    engine = app.get_persistent_store_database('watershed_afganistan', as_sessionmaker=False)
    engineURL=engine.url
    NewEngine = create_engine(engineURL, poolclass=NullPool)
    session = sessionmaker(bind=NewEngine)()

    if (session):
        layerName = ast.literal_eval(request.POST.get('layerName'))
        controlGid = ast.literal_eval(request.POST.get('controlGid'))
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
            QueryObj = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
                Statistic.gid == controlGid)

            countObject = QueryObj.count()
            if (countObject):
                print("From Database")
                rockTypeData = QueryObj[0].population_village_density
                if (rockTypeData != None):
                    session.close()
                    return JsonResponse(rockTypeData)

            worinkgModelObjectQuery = session.query(modelObject).filter(modelObject.gid == controlGid)
        else:
            aoiWKT = ast.literal_eval(request.POST.get('wkt'))
            worinkgModelObjectQuery = session.query(
                func.ST_Transform(func.ST_SetSRID(func.ST_GeomFromText(aoiWKT), 3857), 4326).label('geom'))
            # worinkgModelObjectQuery = copy.deepcopy(cc)
        ChartData = []
        for kk in worinkgModelObjectQuery:
            # aspect
            # 2="North(0-22.5)" 10: "North(337.5-360)"
            poly = session.query(kk.geom.ST_AsText())[0]

            referenceKeyValues = {
                1: {"name": "Low Village Density", "color": "#caa3d1", "count": 0},
                2: {"name": "Low - Moderat Village Density", "color": "#0ffa02", "count": 0},
                3: {"name": "High - Moderat Village Density", "color": "#f7490a", "count": 0},
                4: {"name": "High Village Density", "color": "#1a21f0", "count": 0},
                5: {"name": "Very High Village Density", "color": "#0d6127", "count": 0},
                6: {"name": "Very High Village Density", "color": "#faf734", "count": 0}
            }
            
            stats = zonal_stats(poly, villageDensity, copy_properties=True, nodata_value=0, categorical=True)

            StatItemsList = list(stats[0].items())

            total = sum(v for (k, v) in StatItemsList)
            ChartData = list(map(lambda kk: {"name": referenceKeyValues[kk[0]]["name"], "y": round(kk[1]* 100 / total, 2),
                                             "color": referenceKeyValues[kk[0]]["color"]},
                                 StatItemsList))
            break
        allData = {"seriesData": ChartData, "status": 200}
        if (not IsWKT):
            try:
                statObj = Statistic(layer_name=layerName, gid=controlGid, population_village_density=allData)
                session.add(statObj)
                session.commit()
            except:
                session.rollback()
                updateObjectStatistic = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
                    Statistic.gid == controlGid).first()
                updateObjectStatistic.population_village_density = allData
                session.commit()

        session.close()
        return JsonResponse(allData)
    else:
        allData = {"status": 500, "error": "Something went wrong"}
        return JsonResponse(allData)
