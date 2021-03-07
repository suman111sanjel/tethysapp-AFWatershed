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

from tethysapp.AFWatershed.config import TifDir
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker

slope_raster = TifDir + '/Slope.tif'
elevation_raster = TifDir + '/DEM.tif'
aspect_raster = TifDir + '/Aspect.tif'
plan_Curvature = TifDir + '/planCurvature.tif'
profile_Curvature = TifDir + '/profileCurvature.tif'


# Pie Chart
def Slope(request):
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
                rockTypeData = QueryObj[0].topographical_slope_degree
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
            slope_stats = zonal_stats(poly, slope_raster, copy_properties=True, nodata_value=0, categorical=True)
            classifiedData = classifySlope_New(slope_stats[0])

            break
        allData = {"seriesData": classifiedData, "status": 200}
        if (not IsWKT):
            try:
                statObj = Statistic(layer_name=layerName, gid=controlGid, topographical_slope_degree=allData)
                session.add(statObj)
                session.commit()
            except:
                session.rollback()
                updateObjectStatistic = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
                    Statistic.gid == controlGid).first()
                updateObjectStatistic.topographical_slope_degree = allData
                session.commit()

        session.close()
        return JsonResponse(allData)
    else:
        allData = {"status": 500, "error": "Something went wrong"}
        return JsonResponse(allData)


def classifySlope_New(data):
    mappingDict = {'0-5': {"name": '',
                           "color": '#058DC7',
                           "count": 0},
                   '5-10': {"name": '',
                            "color": "#5e66cf",
                            "count": 0},
                   '10-15': {"name": '',
                             "color": '#ED561B',
                             "count": 0},
                   '15-20': {"name": '',
                             "color": '#DDDF00',
                             "count": 0},
                   '20-25': {"name": '',
                             "color": '#24CBE5',
                             "count": 0},
                   '25-30': {"name": '',
                             "color": '#64E572',
                             "count": 0},
                   '30-35': {"name": '',
                             "color": '#FF9655',
                             "count": 0},
                   '35-40': {"name": '',
                             "color":  '#FFF263',
                             "count": 0},
                   '40-45': {"name": '',
                             "color": '#6AF9C4',
                             "count": 0},
                   '45-50': {"name": '',
                             "color": '#8000ff',
                             "count": 0},
                   '50 and Above': {"name": '',
                                    "color": "#5e66cf",
                                    "count": 0},
                   }
    
    slope = data.keys()
    for i in slope:
        a = float(i)
        if a >= 0 and a < 5:
            mappingDict['0-5']["count"] = mappingDict['0-5']["count"] + data[i]
        elif a >= 5 and a < 10:
            mappingDict['5-10']["count"] = mappingDict['5-10']["count"] + data[i]
        elif a >= 10 and a < 15:
            mappingDict['10-15']["count"] = mappingDict['10-15']["count"] + data[i]
        elif a >= 15 and a < 20:
            mappingDict['15-20']["count"] = mappingDict['15-20']["count"] + data[i]
        elif a >= 20 and a < 25:
            mappingDict['20-25']["count"] = mappingDict['20-25']["count"] + data[i]
        elif a >= 25 and a < 30:
            mappingDict['25-30']["count"] = mappingDict['25-30']["count"] + data[i]
        elif a >= 30 and a < 35:
            mappingDict['30-35']["count"] = mappingDict['30-35']["count"] + data[i]
        elif a >= 35 and a < 40:
            mappingDict['35-40']["count"] = mappingDict['35-40']["count"] + data[i]
        elif a >= 40 and a < 45:
            mappingDict['40-45']["count"] = mappingDict['40-45']["count"] + data[i]
        elif a >= 45 and a < 50:
            mappingDict['45-50']["count"] = mappingDict['45-50']["count"] + data[i]
        elif a >= 50:
            mappingDict['50 and Above']["count"] = mappingDict['50 and Above']["count"] + data[i]

        SlopeKeyValueList = list(mappingDict.items())
        totalSlope = sum(v["count"] for (k, v) in mappingDict.items())
        SlopeChartData = list(map(lambda kk: {"name": kk[0], "y": round(kk[1]["count"] * 100 / totalSlope, 2),
                                              "color": kk[1]["color"]},
                                  SlopeKeyValueList))
    return SlopeChartData


# Column Chart
def Aspect(request):
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
                rockTypeData = QueryObj[0].topographical_aspect
                if (rockTypeData != None):
                    session.close()
                    return JsonResponse(rockTypeData)

            worinkgModelObjectQuery = session.query(modelObject).filter(modelObject.gid == controlGid)
        else:
            aoiWKT = ast.literal_eval(request.POST.get('wkt'))
            worinkgModelObjectQuery = session.query(
                func.ST_Transform(func.ST_SetSRID(func.ST_GeomFromText(aoiWKT), 3857), 4326).label('geom'))
            # worinkgModelObjectQuery = copy.deepcopy(cc)
        AspectChartdata = []
        for kk in worinkgModelObjectQuery:
            # aspect
            # 2="North(0-22.5)" 10: "North(337.5-360)"
            poly = session.query(kk.geom.ST_AsText())[0]
            aspect_referenceKeyValues = {
                1: {"name":"Flat","color":"#6ee16e"},
                2: {"name":"North","color":"#dc0f0f"},
                3: {"name":"Northeast","color":"#44cea0"},
                4: {"name":"East","color":"#3fb1ea"},
                5: {"name":"Southeast","color":"#de9a13"},
                6: {"name":"South","color":"#6464ef"},
                7: {"name":"Southwest","color":"#e633ab"},
                8: {"name":"West","color":"#b9ef4d"},
                9: {"name":"Northwest","color":"#9e45ca"},
                10:{"name": "North(337.5-360)","color":"#ffffff"},
            }

            aspect_stats = zonal_stats(poly, aspect_raster, copy_properties=True, nodata_value=0, categorical=True)
            print('test')
            sumTwoItem = 0
            if 10 in aspect_stats[0]:
                sumTwoItem = sumTwoItem +  aspect_stats[0][10]
                del aspect_stats[0][10]

            if 2 in aspect_stats[0]:
                sumTwoItem = sumTwoItem + aspect_stats[0][2]

            aspect_stats[0][2] = sumTwoItem

            aspectStatItemsList = list(aspect_stats[0].items())
            AspectKeys = list(map(lambda kk: aspect_referenceKeyValues[kk[0]]["name"], aspectStatItemsList))
            AspectValues = list(map(lambda kk: {"y": round(kk[1] * 0.001156, 2), "color": aspect_referenceKeyValues[kk[0]]["color"]}, aspectStatItemsList))
            AspectChartdata.append(AspectKeys)
            AspectChartdata.append(AspectValues)
            break
        allData = {"seriesData": AspectChartdata, "status": 200}
        if (not IsWKT):
            try:
                statObj = Statistic(layer_name=layerName, gid=controlGid, topographical_aspect=allData)
                session.add(statObj)
                session.commit()
            except:
                session.rollback()
                updateObjectStatistic = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
                    Statistic.gid == controlGid).first()
                updateObjectStatistic.topographical_aspect = allData
                session.commit()

        session.close()
        return JsonResponse(allData)
    else:
        allData = {"status": 500, "error": "Something went wrong"}
        return JsonResponse(allData)


# Column Chart
def Elevation(request):
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
                rockTypeData = QueryObj[0].topographical_elevation
                if (rockTypeData != None):
                    session.close()
                    return JsonResponse(rockTypeData)

            worinkgModelObjectQuery = session.query(modelObject).filter(modelObject.gid == controlGid)
        else:
            aoiWKT = ast.literal_eval(request.POST.get('wkt'))
            worinkgModelObjectQuery = session.query(
                func.ST_Transform(func.ST_SetSRID(func.ST_GeomFromText(aoiWKT), 3857), 4326).label('geom'))
            # worinkgModelObjectQuery = copy.deepcopy(cc)
        ElevationChartData = []
        for kk in worinkgModelObjectQuery:
            # aspect
            # 2="North(0-22.5)" 10: "North(337.5-360)"
            poly = session.query(kk.geom.ST_AsText())[0]

            print("elevation")
            # elevation
            elevation_stats = zonal_stats(poly, elevation_raster, stats="min max")
            elevationStatTest = zonal_stats(poly, elevation_raster, copy_properties=True, nodata_value=0,
                                            categorical=True)
            elevationStatKeyValue = list(elevationStatTest[0].items())

            elevMin = elevation_stats[0]['min']
            elevMax = elevation_stats[0]['max']

            diff = elevMax - elevMin
            elevA = str(int(diff / 10))
            elevB = len(elevA)
            ElevInterval = int(elevA[:elevB - 1] + '0')
            AllElevationInterval = []
            initialInterval = 0
            FinalInterval = 0
            ElevationCounter = 0
            while True:
                if (ElevationCounter <= elevMin):
                    initialInterval = ElevationCounter
                elif (ElevationCounter > elevMin and ElevationCounter < elevMax):
                    currentIntervalCount = len(AllElevationInterval)
                    if (currentIntervalCount == 0):
                        AllElevationInterval.append(initialInterval)
                        AllElevationInterval.append(ElevationCounter)
                    else:
                        AllElevationInterval.append(ElevationCounter)
                elif (ElevationCounter >= elevMax):
                    AllElevationInterval.append(ElevationCounter)
                    break
                ElevationCounter += ElevInterval

            ElevationNewDict = {}
            initialValDict = ''
            for imp in range(len(AllElevationInterval)):
                if (initialValDict):
                    ElevationNewDict[str(initialValDict) + "-" + str(AllElevationInterval[imp])] = 0
                initialValDict = str(AllElevationInterval[imp])

            for (mk, mv) in elevationStatKeyValue:
                for elevKey in ElevationNewDict.keys():
                    myKeyList = elevKey.split("-")
                    if (mk >= int(myKeyList[0]) and mk < int(myKeyList[1])):
                        ElevationNewDict[elevKey] = ElevationNewDict[elevKey] + mv
                        break

            ElevationKey = list(map(lambda kkK: kkK[0], ElevationNewDict.items()))
            ElevationValues = list(map(lambda kkK: round(kkK[1] * 0.001156, 2), ElevationNewDict.items()))
            ElevationChartData.append(ElevationKey)
            ElevationChartData.append(ElevationValues)

            break
        allData = {"seriesData": ElevationChartData, "status": 200}
        if (not IsWKT):
            try:
                statObj = Statistic(layer_name=layerName, gid=controlGid, topographical_elevation=allData)
                session.add(statObj)
                session.commit()
            except:
                session.rollback()
                updateObjectStatistic = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
                    Statistic.gid == controlGid).first()
                updateObjectStatistic.topographical_elevation = allData
                session.commit()

        session.close()
        return JsonResponse(allData)
    else:
        allData = {"status": 500, "error": "Something went wrong"}
        return JsonResponse(allData)



# Pie Chart
def PlanCurvature(request):
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
                rockTypeData = QueryObj[0].topographical_plan_curvature
                if (rockTypeData != None):
                    session.close()
                    return JsonResponse(rockTypeData)

            worinkgModelObjectQuery = session.query(modelObject).filter(modelObject.gid == controlGid)
        else:
            aoiWKT = ast.literal_eval(request.POST.get('wkt'))
            worinkgModelObjectQuery = session.query(
                func.ST_Transform(func.ST_SetSRID(func.ST_GeomFromText(aoiWKT), 3857), 4326).label('geom'))
            # worinkgModelObjectQuery = copy.deepcopy(cc)
        PlanCurvatureData = []
        for kk in worinkgModelObjectQuery:
            # slope
            PlanCurvature = {
                0: {"name": "Linear Surface", "color": "#d9e0bf"},
                1: {"name": "Laterally Concave surface", "color": "#2a33b0"},
                2: {"name": "Laterally Convex Surface", "color": "#f20246"}
            }
            poly = session.query(kk.geom.ST_AsText())[0]
            planCurvateure_stats = zonal_stats(poly, plan_Curvature, copy_properties=True, nodata_value=0, categorical=True)
            planCurvateureItemsList = list(planCurvateure_stats[0].items())
            totalPlanCurvature = sum(v for (k, v) in planCurvateure_stats[0].items())
            ChartData = list(map(lambda kk: {"name": PlanCurvature[kk[0]]["name"], "y": round(kk[1]* 100 / totalPlanCurvature, 2),
                                                  "color": PlanCurvature[kk[0]]["color"]},
                                      planCurvateureItemsList))
            PlanCurvatureData=ChartData

            break
        allData = {"seriesData": PlanCurvatureData, "status": 200}
        if (not IsWKT):
            try:
                statObj = Statistic(layer_name=layerName, gid=controlGid, topographical_plan_curvature=allData)
                session.add(statObj)
                session.commit()
            except:
                session.rollback()
                updateObjectStatistic = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
                    Statistic.gid == controlGid).first()
                updateObjectStatistic.topographical_plan_curvature = allData
                session.commit()

        session.close()
        return JsonResponse(allData)
    else:
        allData = {"status": 500, "error": "Something went wrong"}
        return JsonResponse(allData)



# Pie Chart
def ProfileCurvature(request):
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
                rockTypeData = QueryObj[0].topographical_profile_curvature
                if (rockTypeData != None):
                    session.close()
                    return JsonResponse(rockTypeData)

            worinkgModelObjectQuery = session.query(modelObject).filter(modelObject.gid == controlGid)
        else:
            aoiWKT = ast.literal_eval(request.POST.get('wkt'))
            worinkgModelObjectQuery = session.query(
                func.ST_Transform(func.ST_SetSRID(func.ST_GeomFromText(aoiWKT), 3857), 4326).label('geom'))
            # worinkgModelObjectQuery = copy.deepcopy(cc)
        ProfileCurvatureData = []
        for kk in worinkgModelObjectQuery:
            # slope
            ProfileCurvature = {
                0: {"name": "Linear Surface", "color": "#e4d5a0"},
                1: {"name": "Upwardly Convex Surface", "color": "#fc2007"},
                2: {"name": "Upwardly Concave Surface", "color": "#5023f0"}
            }
            poly = session.query(kk.geom.ST_AsText())[0]
            ProfileCurvateure_stats = zonal_stats(poly, profile_Curvature, copy_properties=True, nodata_value=0, categorical=True)
            ProfileCurvateureItemsList = list(ProfileCurvateure_stats[0].items())
            totalProfileCurvature = sum(v for (k, v) in ProfileCurvateure_stats[0].items())
            ChartData = list(map(lambda kk: {"name": ProfileCurvature[kk[0]]["name"], "y": round(kk[1]* 100 / totalProfileCurvature, 2),
                                                  "color": ProfileCurvature[kk[0]]["color"]},
                                      ProfileCurvateureItemsList))
            ProfileCurvatureData=ChartData

            break
        allData = {"seriesData": ProfileCurvatureData, "status": 200}
        if (not IsWKT):
            try:
                statObj = Statistic(layer_name=layerName, gid=controlGid, topographical_profile_curvature=allData)
                session.add(statObj)
                session.commit()
            except:
                session.rollback()
                updateObjectStatistic = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
                    Statistic.gid == controlGid).first()
                updateObjectStatistic.topographical_profile_curvature = allData
                session.commit()

        session.close()
        return JsonResponse(allData)
    else:
        allData = {"status": 500, "error": "Something went wrong"}
        return JsonResponse(allData)

