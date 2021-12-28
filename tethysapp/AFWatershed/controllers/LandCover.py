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

LandCover2018 = TifDir + '/landcover-2018.tif'


# Column Chart
def LandCover(request):
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
                rockTypeData = QueryObj[0].landcover_landcover
                if (rockTypeData != None):
                    session.close()
                    return JsonResponse(rockTypeData)

            worinkgModelObjectQuery = session.query(modelObject).filter(modelObject.gid == controlGid)
        else:
            aoiWKT = ast.literal_eval(request.POST.get('wkt'))
            worinkgModelObjectQuery = session.query(
                func.ST_Transform(func.ST_SetSRID(func.ST_GeomFromText(aoiWKT), 3857), 4326).label('geom'))
            # worinkgModelObjectQuery = copy.deepcopy(cc)
        LCChartdata = []
        for kk in worinkgModelObjectQuery:
            # aspect
            # 2="North(0-22.5)" 10: "North(337.5-360)"
            poly = session.query(kk.geom.ST_AsText())[0]

            referenceKeyValues = {
                1: {"name": "Snow", "color": "#7fffdf", "count": 0},
                2: {"name": "Builtup", "color": "#ff3d44", "count": 0},
                3: {"name": "Water", "color": "#142beb", "count": 0},
                4: {"name": "Forest", "color": "#005c4c", "count": 0},
                5: {"name": "Irrigated Agri", "color": "#ffff00", "count": 0},
                6: {"name": "Rainfed Agri", "color": "#e6e600", "count": 0},
                7: {"name": "Fruit trees", "color": "#44ad70", "count": 0},
                8: {"name": "Vineyards", "color": "#32d69e", "count": 0},
                9: {"name": "Marshland", "color": "#00c5ff", "count": 0},
                10: {"name": "Bare Land", "color": "#f2ebaf", "count": 0},
                11: {"name": "Rangeland", "color": "#c4d766", "count": 0},
                12: {"name": "Sand Cover", "color": "#d7c29e", "count": 0},
                13: {"name": "Streams", "color": "#005ce6", "count": 0}
            }

            stats = zonal_stats(poly, LandCover2018, copy_properties=True, nodata_value=0, categorical=True)

            StatItemsList = list(stats[0].items())
            LandCoverKeys = list(map(lambda kk: referenceKeyValues[kk[0]]["name"], StatItemsList))
            LandcoverValues = list(
                map(lambda kk: {"y": round(kk[1] * 0.000676, 2), "color": referenceKeyValues[kk[0]]["color"]},
                    StatItemsList))
            LCChartdata.append(LandCoverKeys)
            LCChartdata.append(LandcoverValues)
            break
        allData = {"seriesData": LCChartdata, "status": 200}
        if (not IsWKT):
            try:
                statObj = Statistic(layer_name=layerName, gid=controlGid, landcover_landcover=allData)
                session.add(statObj)
                session.commit()
            except:
                session.rollback()
                updateObjectStatistic = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
                    Statistic.gid == controlGid).first()
                updateObjectStatistic.landcover_landcover = allData
                session.commit()

        session.close()
        return JsonResponse(allData)
    else:
        allData = {"status": 500, "error": "Something went wrong"}
        return JsonResponse(allData)
