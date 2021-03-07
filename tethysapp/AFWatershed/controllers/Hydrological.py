from tethysapp.AFWatershed.app import AFWatershed as app
from tethysapp.AFWatershed.model import GelogicalRockType, HydrologicalMajorBasin, HydrologicalMacroLevelWatershed, \
    Statistic, GelogicalGeologyTemplate, GelogicalMineralType, GelogicalFaultLine, HydrologicalWellsDepth, \
    HydrologicalGwDepthFlow2010, FloodAllFlood, HydrologicalMarshland, HydrologicalLake, HydrologicalAfgAllRiver
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

growndWaterPotentialZone = TifDir + '/growndWaterPotentialZone.tif'
drainageDensity = TifDir + '/drainageDensity.tif'


# line graph
def YearlyWellDepthTrend(request):
    """
    Get all persisted dams.
    """
    # Get connection/session to database
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
                rockTypeData = QueryObj[0].hydrological_yearly_well_depth_trend
                if (rockTypeData != None):
                    session.close()
                    return JsonResponse(rockTypeData)

            worinkgModelObjectQuery = session.query(modelObject).filter(modelObject.gid == controlGid)
        else:
            aoiWKT = ast.literal_eval(request.POST.get('wkt'))
            worinkgModelObjectQuery = session.query(
                func.ST_Transform(func.ST_SetSRID(func.ST_GeomFromText(aoiWKT), 3857), 4326).label('geom'))
            # worinkgModelObjectQuery = copy.deepcopy(cc)
        data_well_depth = [{
            "name": "Max",
            "data": []}, {
            "name": "Mean",
            "data": []}, {
            "name": "Min",
            "data": []}]
        for kk in worinkgModelObjectQuery:
            # rock_type
            # welldepth
            well_depth_detail = session.query(HydrologicalWellsDepth).filter(
                HydrologicalWellsDepth.geom.ST_Intersects(kk.geom)).filter(HydrologicalWellsDepth.year != 0).filter(
                HydrologicalWellsDepth.well_depth != 0)

            well_depth_detail_distinct = well_depth_detail.distinct(HydrologicalWellsDepth.year)

            for ik in well_depth_detail_distinct:
                dataYearList = []
                datathisyear = well_depth_detail.filter(HydrologicalWellsDepth.year == ik.year)
                for jj in datathisyear:
                    dataYearList.append(float(jj.well_depth))
                year_c = ik.year
                mini = min(dataYearList)
                maxi = max(dataYearList)
                mean = round(sum(dataYearList) / len(dataYearList), 2)
                date_str = str(year_c)
                dt = int(datetime.strptime(date_str, '%Y').timestamp() * 1000)
                data_well_depth[0]['data'].append([dt, maxi])
                data_well_depth[1]['data'].append([dt, mean])
                data_well_depth[2]['data'].append([dt, mini])

            break
        allData = {"seriesData": data_well_depth, "status": 200}
        if (not IsWKT):
            try:
                statObj = Statistic(layer_name=layerName, gid=controlGid, hydrological_yearly_well_depth_trend=allData)
                session.add(statObj)
                session.commit()
            except:
                session.rollback()
                updateObjectStatistic = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
                    Statistic.gid == controlGid).first()
                updateObjectStatistic.hydrological_yearly_well_depth_trend = allData
                session.commit()

        session.close()
        return JsonResponse(allData)
    else:
        allData = {"status": 500, "error": "Something went wrong"}
        return JsonResponse(allData)


# column Graph
def GroundWaterDepthFlow(request):
    """
    Get all persisted dams.
    """
    # Get connection/session to database
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
                rockTypeData = QueryObj[0].hydrological_ground_water_depth_flow
                if (rockTypeData != None):
                    session.close()
                    return JsonResponse(rockTypeData)

            worinkgModelObjectQuery = session.query(modelObject).filter(modelObject.gid == controlGid)
        else:
            aoiWKT = ast.literal_eval(request.POST.get('wkt'))
            worinkgModelObjectQuery = session.query(
                func.ST_Transform(func.ST_SetSRID(func.ST_GeomFromText(aoiWKT), 3857), 4326).label('geom'))
            # worinkgModelObjectQuery = copy.deepcopy(cc)
        GwDepthFlowChartData = []
        for kk in worinkgModelObjectQuery:
            # GwDepthFlow
            gw_depth_flow = {
                "Fresh water locally plentiful": {"name": '',
                                                  "color": "#5e66cf",
                                                  "count": 0},
                "Fresh water scarce or lacking": {"name": '',
                                                  "color": "#5e66cf",
                                                  "count": 0},
                "Fresh water generally plentiful": {"name": '',
                                                    "color": "#5e66cf",
                                                    "count": 0}
            }
            GwDepthFlow_detail = session.query(HydrologicalGwDepthFlow2010).filter(
                HydrologicalGwDepthFlow2010.geom.ST_Intersects(kk.geom))

            for gwdf in GwDepthFlow_detail:
                groundwater__depthflow = session.query(
                    (cast(func.ST_Intersection(kk.geom, gwdf.geom), Geography).ST_Area()).label('area_final'))
                gw_depth_flow[gwdf.descrip1]["count"] = gw_depth_flow[gwdf.descrip1]["count"] + \
                                                        groundwater__depthflow[0][0]

            GwDepthFlowKey = list(
                map(lambda gwk: gwk[0],
                    filter(lambda nm: round(nm[1]["count"] / 1000000, 2) != 0, gw_depth_flow.items())))

            GwDepthFlowValues = list(map(lambda gwk: {"y": round(gwk[1]["count"] / 1000000, 2),
                                                      "color": gwk[1]['color']},
                                         filter(lambda nm: round(nm[1]["count"] / 1000000, 2) != 0,
                                                gw_depth_flow.items())))

            GwDepthFlowChartData.append(GwDepthFlowKey)
            GwDepthFlowChartData.append(GwDepthFlowValues)

            break

        allData = {"seriesData": GwDepthFlowChartData, "status": 200}
        if (not IsWKT):
            try:
                statObj = Statistic(layer_name=layerName, gid=controlGid, hydrological_ground_water_depth_flow=allData)
                session.add(statObj)
                session.commit()
            except:
                session.rollback()
                updateObjectStatistic = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
                    Statistic.gid == controlGid).first()
                updateObjectStatistic.hydrological_ground_water_depth_flow = allData
                session.commit()

        session.close()
        return JsonResponse(allData)
    else:
        allData = {"status": 500, "error": "Something went wrong"}
        return JsonResponse(allData)


# column Graph
def FloodRisk(request):
    """
    Get all persisted dams.
    """
    # Get connection/session to database
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
                rockTypeData = QueryObj[0].hydrological_flood_risk
                if (rockTypeData != None):
                    session.close()
                    return JsonResponse(rockTypeData)

            worinkgModelObjectQuery = session.query(modelObject).filter(modelObject.gid == controlGid)
        else:
            aoiWKT = ast.literal_eval(request.POST.get('wkt'))
            worinkgModelObjectQuery = session.query(
                func.ST_Transform(func.ST_SetSRID(func.ST_GeomFromText(aoiWKT), 3857), 4326).label('geom'))
            # worinkgModelObjectQuery = copy.deepcopy(cc)
        floodChartData = []
        for kk in worinkgModelObjectQuery:

            hydrological_flood = {"High Severity": {"name": '',
                                                    "color": "#feba6e",
                                                    "count": 0},
                                  "Moderate Severity": {"name": '',
                                                        "color": "#ffe8a4",
                                                        "count": 0},
                                  "Severe Event": {"name": '',
                                                   "color": "#ed6e43",
                                                   "count": 0},
                                  "Moderately Low Severity": {"name": '',
                                                              "color": "#e7f6b8",
                                                              "count": 0},
                                  "Very Low Severity": {"name": '',
                                                        "color": "#74b7ae",
                                                        "count": 0},
                                  "Most Severe Event": {"name": '',
                                                        "color": "#d7191c",
                                                        "count": 0},
                                  "Low Severity": {"name": '',
                                                   "color": "#b7e2a8",
                                                   "count": 0}}
            hydrological_flood_detail = session.query(FloodAllFlood.gid, FloodAllFlood.flood, (
                cast(func.ST_Intersection(kk.geom, FloodAllFlood.geom), Geography).ST_Area()).label(
                'area_final')).filter(
                FloodAllFlood.geom.ST_Intersects(kk.geom))
            print(hydrological_flood_detail.count())
            print(hydrological_flood_detail)
            cc = hydrological_flood_detail.count()
            floodCount = 0
            printInterval = 0
            for floodItem in hydrological_flood_detail:
                if (floodCount == printInterval):
                    print(floodCount)
                    printInterval += 1000
                # hydro__flood = session.query(
                #     (cast(func.ST_Intersection(kk.geom, floodItem.geom), Geography).ST_Area()).label('area_final'))
                hydrological_flood[floodItem.flood]["count"] = hydrological_flood[floodItem.flood][
                                                                   "count"] + floodItem.area_final
                floodCount += 1

            hydroFloodkeyValueList = list(hydrological_flood.items())
            totalfloodItem = sum(vm["count"] for (km, vm) in hydroFloodkeyValueList)
            floodChartData = list(
                map(lambda flood_kk: {"name": flood_kk[0], "y": round(flood_kk[1]["count"] * 100 / totalfloodItem, 2),
                                      "color": flood_kk[1]["color"]},
                    list(filter(lambda nm: round(nm[1]["count"] * 100 / totalfloodItem, 2) != 0,
                                hydroFloodkeyValueList))))

            break

        allData = {"seriesData": floodChartData, "status": 200}
        if (not IsWKT):
            try:
                statObj = Statistic(layer_name=layerName, gid=controlGid, hydrological_flood_risk=allData)
                session.add(statObj)
                session.commit()
            except:
                session.rollback()
                updateObjectStatistic = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
                    Statistic.gid == controlGid).first()
                updateObjectStatistic.hydrological_flood_risk = allData
                session.commit()

        session.close()
        return JsonResponse(allData)
    else:
        allData = {"status": 500, "error": "Something went wrong"}
        return JsonResponse(allData)


# column Graph
def WaterBodies(request):
    """
    Get all persisted dams.
    """
    # Get connection/session to database
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
                rockTypeData = QueryObj[0].hydrological_water_bodies
                if (rockTypeData != None):
                    session.close()
                    return JsonResponse(rockTypeData)

            worinkgModelObjectQuery = session.query(modelObject).filter(modelObject.gid == controlGid)
        else:
            aoiWKT = ast.literal_eval(request.POST.get('wkt'))
            worinkgModelObjectQuery = session.query(
                func.ST_Transform(func.ST_SetSRID(func.ST_GeomFromText(aoiWKT), 3857), 4326).label('geom'))
            # worinkgModelObjectQuery = copy.deepcopy(cc)

        DatawaterBodiesAndMarshland = []
        for kk in worinkgModelObjectQuery:

            DatawaterBodiesAndMarshlandDictionary = {}

            print("marshland")
            # marshland
            marshland = {
                "Seasonally Inundated Vegetation": 0,
                "Permanent Marsh": 0,
            }
            marshland_detail = session.query(HydrologicalMarshland).filter(
                HydrologicalMarshland.geom.ST_Intersects(kk.geom))

            for mrlnd in marshland_detail:
                marsh__land = session.query(
                    (cast(func.ST_Intersection(kk.geom, mrlnd.geom), Geography).ST_Area()).label('area_final'))
                marshland[mrlnd.lc_class] = marshland[mrlnd.lc_class] + \
                                            marsh__land[0][0]

            totalmarshland = sum(vm for (km, vm) in marshland.items())
            DatawaterBodiesAndMarshlandDictionary['marshland'] = str(round(totalmarshland / 1000000, 2)) + ' sq.km'

            print("lanke")
            # lake
            lake_detail = session.query(HydrologicalLake).filter(HydrologicalLake.geom.ST_Intersects(kk.geom))
            lakeall = 0
            for lk in lake_detail:
                l_k = session.query(
                    (cast(func.ST_Intersection(kk.geom, lk.geom), Geography).ST_Area()).label('area_final'))
                lakeall = lakeall + l_k[0][0]

            DatawaterBodiesAndMarshlandDictionary['lake'] = str(round(lakeall / 1000000, 2)) + ' sq.km'

            print("rivers")
            # rivers
            rivers = {
                "River": 0,
                "Main River": 0,
                "Major River": 0
            }
            rivers_detail = session.query(HydrologicalAfgAllRiver).filter(
                HydrologicalAfgAllRiver.geom.ST_Intersects(kk.geom))

            for rive in rivers_detail:
                ri__vers = session.query(
                    (cast(func.ST_Intersection(kk.geom, rive.geom), Geography).ST_Length()).label('length_final'))
                rivers[rive.river_type] = rivers[rive.river_type] + ri__vers[0][0]

            DatawaterBodiesAndMarshlandDictionary['majorRiver'] = str(round(rivers["Main River"] / 1000, 2)) + ' km'
            DatawaterBodiesAndMarshlandDictionary['MinroRiver'] = str(round(rivers["Major River"] / 1000, 2)) + ' km'

            DatawaterBodiesAndMarshland.append(DatawaterBodiesAndMarshlandDictionary)

            break

        allData = {"seriesData": DatawaterBodiesAndMarshland, "status": 200}
        if (not IsWKT):
            try:
                statObj = Statistic(layer_name=layerName, gid=controlGid, hydrological_water_bodies=allData)
                session.add(statObj)
                session.commit()
            except:
                session.rollback()
                updateObjectStatistic = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
                    Statistic.gid == controlGid).first()
                updateObjectStatistic.hydrological_water_bodies = allData
                session.commit()

        session.close()
        return JsonResponse(allData)
    else:
        allData = {"status": 500, "error": "Something went wrong"}
        return JsonResponse(allData)


def DrainageDensity(request):
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
                rockTypeData = QueryObj[0].hydrological_drainage_density
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
            slope_stats = zonal_stats(poly, drainageDensity, copy_properties=True, nodata_value=0, categorical=True)
            classifiedData = classifyDrainageDensity(slope_stats[0])

            break
        allData = {"seriesData": classifiedData, "status": 200}
        if (not IsWKT):
            try:
                statObj = Statistic(layer_name=layerName, gid=controlGid, hydrological_drainage_density=allData)
                session.add(statObj)
                session.commit()
            except:
                session.rollback()
                updateObjectStatistic = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
                    Statistic.gid == controlGid).first()
                updateObjectStatistic.hydrological_drainage_density = allData
                session.commit()

        session.close()
        return JsonResponse(allData)
    else:
        allData = {"status": 500, "error": "Something went wrong"}
        return JsonResponse(allData)


def classifyDrainageDensity(data):
    mappingDict = {
        '0.01-1': {"name": "Less (0.01 -1)", "color": "#feffdf", "count": 0},
        '1.1-2': {"name": "Moderate (1.1 - 2)", "color": "#fcd681", "count": 0},
        '2.1-2.5': {"name": "High (2.1 - 2.5)", "color": "#f66211", "count": 0},
        '2.6 and Above': {"name": "Very High (2.6 - 3.3)", "color": "#71120b", "count": 0}
    }

    drainageDensity = data.keys()
    for i in drainageDensity:
        a = float(i)
        if a >= 0 and a < 1:
            mappingDict['0.01-1']["count"] = mappingDict['0.01-1']["count"] + data[i]
        elif a >= 1 and a < 2:
            mappingDict['1.1-2']["count"] = mappingDict['1.1-2']["count"] + data[i]
        elif a >= 2 and a < 2.5:
            mappingDict['2.1-2.5']["count"] = mappingDict['2.1-2.5']["count"] + data[i]
        elif a >= 2.6:
            mappingDict['2.6 and Above']["count"] = mappingDict['2.6 and Above']["count"] + data[i]

        KeyValueList = list(mappingDict.items())
        total = sum(v["count"] for (k, v) in mappingDict.items())
        ChartData = list(map(lambda kk: {"name": kk[1]["name"], "y": round(kk[1]["count"] * 100 / total, 2),
                                         "color": kk[1]["color"]},
                             KeyValueList))
    return ChartData


def GroundWaterPotentialZone(request):
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
                rockTypeData = QueryObj[0].hydrological_ground_water_potential_zone
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
            groundWaterPZ_stats = zonal_stats(poly, growndWaterPotentialZone, copy_properties=True, nodata_value=0, categorical=True)
            classifiedData = classifyGroundWaterPotentialZone(groundWaterPZ_stats[0])

            break
        allData = {"seriesData": classifiedData, "status": 200}
        if (not IsWKT):
            try:
                statObj = Statistic(layer_name=layerName, gid=controlGid,
                                    hydrological_ground_water_potential_zone=allData)
                session.add(statObj)
                session.commit()
            except:
                session.rollback()
                updateObjectStatistic = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
                    Statistic.gid == controlGid).first()
                updateObjectStatistic.hydrological_ground_water_potential_zone = allData
                session.commit()

        session.close()
        return JsonResponse(allData)
    else:
        allData = {"status": 500, "error": "Something went wrong"}
        return JsonResponse(allData)


def classifyGroundWaterPotentialZone(data):
    mappingDict = {
        '0-0.2': {"name": "0 - 0.2", "color": "#f5aeb4", "count": 0},
        '0.2-0.4': {"name": "0.2 - 0.4", "color": "#ffda5b", "count": 0},
        '0.4-0.6': {"name": "0.4 - 0.6", "color": "#cdffad", "count": 0},
        '0.6-0.8': {"name": "0.6 - 0.8", "color": "#74cef7", "count": 0},
        '0.8-1': {"name": "0.8 - 1", "color": "#4d4dff", "count": 0}
    }

    groundWaterPotentialzo = data.keys()
    for i in groundWaterPotentialzo:
        a = float(i)
        if a >= 0 and a < 0.2:
            mappingDict['0-0.2']["count"] = mappingDict['0-0.2']["count"] + data[i]
        elif a >= 0.2 and a < 0.4:
            mappingDict['0.2-0.4']["count"] = mappingDict['0.2-0.4']["count"] + data[i]
        elif a >= 0.4 and a < 0.6:
            mappingDict['0.4-0.6']["count"] = mappingDict['0.4-0.6']["count"] + data[i]
        elif a >= 0.6 and a < 0.8:
            mappingDict['0.6-0.8']["count"] = mappingDict['0.6-0.8']["count"] + data[i]
        elif a >= 0.8:
            mappingDict['0.8-1']["count"] = mappingDict['0.8-1']["count"] + data[i]

        ChartData = []
        KeyValueList = list(mappingDict.items())
        KeyValue = list(map(lambda kkK: kkK[1]["name"], KeyValueList))
        dataWithColor = list(map(lambda kkK: {"y": round(kkK[1]["count"] * 0.007225, 2),
                                                              "color": kkK[1]["color"]}, KeyValueList))
        ChartData.append(KeyValue)
        ChartData.append(dataWithColor)

    return ChartData

