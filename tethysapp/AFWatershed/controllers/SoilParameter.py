from tethysapp.AFWatershed.app import AFWatershed as app
from tethysapp.AFWatershed.model import GelogicalRockType, HydrologicalMajorBasin, HydrologicalMacroLevelWatershed, \
    Statistic, GelogicalGeologyTemplate, GelogicalMineralType, GelogicalFaultLine, SoilParametersSoilsDepth, \
    SoilParametersSoilsType
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

# Pie Chart
def SoilDepth(request):
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
                rockTypeData = QueryObj[0].soil_parameters_soil_depth
                if (rockTypeData != None):
                    session.close()
                    return JsonResponse(rockTypeData)

            worinkgModelObjectQuery = session.query(modelObject).filter(modelObject.gid == controlGid)
        else:
            aoiWKT = ast.literal_eval(request.POST.get('wkt'))
            worinkgModelObjectQuery = session.query(
                func.ST_Transform(func.ST_SetSRID(func.ST_GeomFromText(aoiWKT), 3857), 4326).label('geom'))
            # worinkgModelObjectQuery = copy.deepcopy(cc)
        SoilDepthData = []
        for kk in worinkgModelObjectQuery:
            # rock_type
            soil_properties_soil_depth = {
                "moderately deep to deep": {"color": "#0e91c9", "count": 0},
                "shallow": {"color": "#48ec1f", "count": 0},
                "very deep": {"color": "#a81dca", "count": 0}
            }

            soil_properties_soil_depth_detail = session.query(SoilParametersSoilsDepth).filter(
                SoilParametersSoilsDepth.geom.ST_Intersects(kk.geom))

            for soildepth in soil_properties_soil_depth_detail:
                soil__depth = session.query(
                    (cast(func.ST_Intersection(kk.geom, soildepth.geom), Geography).ST_Area()).label('area_final'))
                soil_properties_soil_depth[soildepth.depth]["count"] = soil_properties_soil_depth[soildepth.depth][
                                                                           "count"] + soil__depth[0][0]

            soilDepthkeyValueList = list(soil_properties_soil_depth.items())
            totalsoildepth = sum(vm["count"] for (km, vm) in soilDepthkeyValueList)
            SoilDepthData = list(
                map(lambda soil_kk: {"name": soil_kk[0], "y": round(soil_kk[1]["count"] * 100 / totalsoildepth, 2),
                                     "color": soil_kk[1]["color"]},
                    list(filter(lambda nm: round(nm[1]["count"] * 100 / totalsoildepth, 2) != 0,
                                soilDepthkeyValueList))))
            print("soil type")
            break
        allData = {"seriesData": SoilDepthData, "status": 200}
        if (not IsWKT):
            try:
                statObj = Statistic(layer_name=layerName, gid=controlGid, soil_parameters_soil_depth=allData)
                session.add(statObj)
                session.commit()
            except:
                session.rollback()
                updateObjectStatistic = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
                    Statistic.gid == controlGid).first()
                updateObjectStatistic.soil_parameters_soil_depth = allData
                session.commit()

        session.close()
        return JsonResponse(allData)
    else:
        allData = {"status": 500, "error": "Something went wrong"}
        return JsonResponse(allData)


# Column Chart
def SoilType(request):
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
                DBDataGeologicalTemplate = QueryObj[0].soil_parameters_soil_type
                if (DBDataGeologicalTemplate != None):
                    session.close()
                    return JsonResponse(DBDataGeologicalTemplate)

            worinkgModelObjectQuery = session.query(modelObject).filter(modelObject.gid == controlGid)
        else:
            aoiWKT = ast.literal_eval(request.POST.get('wkt'))
            worinkgModelObjectQuery = session.query(
                func.ST_Transform(func.ST_SetSRID(func.ST_GeomFromText(aoiWKT), 3857), 4326).label('geom'))
            # worinkgModelObjectQuery = copy.deepcopy(cc)
        SoilTypeChartData = []
        for kk in worinkgModelObjectQuery:

            # soil_type
            soil_properties_soil_type = {
                "fine grained soils: clay underlain by gravel and silty sand": {"color": "#2ce8c0",
                                                                                "count": 0},
                "fine grained & coarse grained soils: silt & clay underlain by silty sand": {"color": "#2acd50",
                                                                                             "count": 0},
                "fine grained & coarse grained soils: clay & silty sand with rock fragments and exposed bedrock": {
                    "color": "#8856ce",
                    "count": 0},
                "fine grained & coarse grained soils: gravel overlain by clay": {"color": "#7580cb",
                                                                                 "count": 0},
                "coarse grained soils:gravel overlain by caliche and silty sand": {"color": "#dd67e1",
                                                                                   "count": 0},
                "fine grained & coarse grained soils: clay & silty sand (shallow), silt & clay (moderately deep to deep)": {
                    "color": "#a7ed86",
                    "count": 0},
                "fine grained soils: sandy silt": {"color": "#d99124",
                                                   "count": 0},
                "coarse grained soils: poorly graded sand": {"color": "#ccea20",
                                                             "count": 0},
                "coarse grained: gravel overlain by silty sand and clayey sand": {"color": "#78b3ce",
                                                                                  "count": 0},
                "fine grained & coarse grained soils: clay, silt, & sand": {"color": "#dc3586",
                                                                            "count": 0}
            }
            soil_properties_soil_type_detail = session.query(SoilParametersSoilsType).filter(
                SoilParametersSoilsType.geom.ST_Intersects(kk.geom))

            for soiltype in soil_properties_soil_type_detail:
                soil__type = session.query(
                    (cast(func.ST_Intersection(kk.geom, soiltype.geom), Geography).ST_Area()).label('area_final'))
                soil_properties_soil_type[soiltype.soiltype]["count"] = soil_properties_soil_type[soiltype.soiltype]["count"] + \
                                                               soil__type[0][0]

            SoilTypeKey = list(
                map(lambda soilTy_kk: soilTy_kk[0],
                    filter(lambda nm_stype: round(nm_stype[1]["count"] / 1000000, 2) != 0, soil_properties_soil_type.items())))
            SoilTypeValues = list(map(lambda soilTy_kk: {"y": round(soilTy_kk[1]["count"] / 1000000, 2),
             "color": soilTy_kk[1]['color']},
                                      filter(lambda nm_stype: round(nm_stype[1]["count"] / 1000000, 2) != 0,
                                             soil_properties_soil_type.items())))

            SoilTypeChartData.append(SoilTypeKey)
            SoilTypeChartData.append(SoilTypeValues)

            break

        allData = {"seriesData": SoilTypeChartData, "status": 200}
        if (not IsWKT):
            try:
                statObj = Statistic(layer_name=layerName, gid=controlGid, soil_parameters_soil_type=allData)
                session.add(statObj)
                session.commit()
            except:
                session.rollback()
                updateObjectStatistic = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
                    Statistic.gid == controlGid).first()
                updateObjectStatistic.soil_parameters_soil_type = allData
                session.commit()

        session.close()
        return JsonResponse(allData)
    else:
        allData = {"status": 500, "error": "Something went wrong"}
        return JsonResponse(allData)
