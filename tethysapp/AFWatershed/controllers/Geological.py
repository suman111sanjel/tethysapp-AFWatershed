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
# Pie Chart
def RockType(request):
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
                rockTypeData = QueryObj[0].gelogical__rock_type
                if (rockTypeData != None):
                    session.close()
                    return JsonResponse(rockTypeData)

            worinkgModelObjectQuery = session.query(modelObject).filter(modelObject.gid == controlGid)
        else:
            aoiWKT = ast.literal_eval(request.POST.get('wkt'))
            worinkgModelObjectQuery = session.query(
                func.ST_Transform(func.ST_SetSRID(func.ST_GeomFromText(aoiWKT), 3857), 4326).label('geom'))
            # worinkgModelObjectQuery = copy.deepcopy(cc)
        RockTypeChartData = []
        for kk in worinkgModelObjectQuery:
            # rock_type
            rock_type = {
                "Bedrock continuously covered by > 20 ft. of soil": {
                    "name": "Bedrock continuously covered by > 20 ft. of soil",
                    "color": "#6de834",
                    "count": 0},
                "Soft Rocks:  Sandstone, shale, conglomerate": {
                    "name": "Soft Rocks:  Sandstone, shale, conglomerate",
                    "color": "#e988de",
                    "count": 0},
                "Hard Rocks:  Limestone, dolomite": {
                    "name": "Hard Rocks:  Limestone, dolomite",
                    "color": "#41a7f0",
                    "count": 0},
                "Hard Rocks:  Granite, basalt, gabbro": {
                    "name": "Hard Rocks:  Granite, basalt, gabbro",
                    "color": "#e1cb5b",
                    "count": 0},
                "Hard & Soft Rocks:  Gneiss, quartzite, marble, schist, slate": {
                    "name": "Hard & Soft Rocks:  Gneiss, quartzite, marble, schist, slate",
                    "color": "#68f0b3",
                    "count": 0},
                "Hard & Soft Rocks:  Limestone, sandstone, shale, conglomerate": {
                    "name": "Hard & Soft Rocks:  Limestone, sandstone, shale, conglomerate",
                    "color": "#9f83ed",
                    "count": 0}}
            rock_type_detail = session.query(GelogicalRockType).filter(
                GelogicalRockType.geom.ST_Intersects(kk.geom))
            for georocktype in rock_type_detail:
                area_rock = session.query(
                    (cast(func.ST_Intersection(kk.geom, georocktype.geom), Geography).ST_Area()).label('area_final'))
                # area_test=session.query((cast(kk.geom,Geography).ST_Area()).label('area_final'))
                rock_type[georocktype.descrip]['count'] = rock_type[georocktype.descrip]['count'] + area_rock[0][0]

            rockTypekeyValueList = list(rock_type.items())
            totalrocktype = sum(vm['count'] for (km, vm) in rockTypekeyValueList) + 0.0000001
            RockTypeChartData = list(
                map(lambda rtype_kk: {"name": rtype_kk[0], "y": round(rtype_kk[1]['count'] * 100 / totalrocktype, 2),
                                      "color": rtype_kk[1]['color']},
                    list(filter(lambda nm: round(nm[1]['count'] * 100 / totalrocktype, 2) != 0,
                                rockTypekeyValueList))))
            print(RockTypeChartData)
            break
        allData = {"seriesData": RockTypeChartData, "status": 200}
        if (not IsWKT):
            try:
                statObj = Statistic(layer_name=layerName, gid=controlGid, gelogical__rock_type=allData)
                session.add(statObj)
                session.commit()
            except:
                session.rollback()
                updateObjectStatistic = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
                    Statistic.gid == controlGid).first()
                updateObjectStatistic.gelogical__rock_type = allData
                session.commit()

        session.close()
        return JsonResponse(allData)
    else:
        allData = {"status": 500, "error": "Something went wrong"}
        return JsonResponse(allData)


# Column Chart
def GeologicalTemplate(request):
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
                DBDataGeologicalTemplate = QueryObj[0].gelogical__geologica_template
                if (DBDataGeologicalTemplate != None):
                    session.close()
                    return JsonResponse(DBDataGeologicalTemplate)


            worinkgModelObjectQuery = session.query(modelObject).filter(modelObject.gid == controlGid)
        else:
            aoiWKT = ast.literal_eval(request.POST.get('wkt'))
            worinkgModelObjectQuery = session.query(
                func.ST_Transform(func.ST_SetSRID(func.ST_GeomFromText(aoiWKT), 3857), 4326).label('geom'))
            # worinkgModelObjectQuery = copy.deepcopy(cc)
        GeologicalTemplateChartData = []
        for kk in worinkgModelObjectQuery:
            # rock_type

            geological_template = {"limestone": {"name": '',
                                                 "color": "#d77624",
                                                 "count": 0},
                                   "granite": {"name": '',
                                               "color": "#d8b97a",
                                               "count": 0},
                                   "clastic rock": {"name": '',
                                                    "color": "#c4b9ab",
                                                    "count": 0},
                                   "aeolian sands": {"name": '',
                                                     "color": "#f6e4c5",
                                                     "count": 0},
                                   "ophiolites": {"name": '',
                                                  "color": "#4b1706",
                                                  "count": 0},
                                   "foliated": {"name": '',
                                                "color": "#bcbd84",
                                                "count": 0},
                                   "sand. gravel, unconsolidated seds.": {"name": '',
                                                                          "color": "#7d5e18",
                                                                          "count": 0},
                                   "crystalline": {"name": '',
                                                   "color": "#f1d6cc",
                                                   "count": 0},
                                   "volcanic": {"name": '',
                                                "color": "#674545",
                                                "count": 0}}

            geological_template_detail = session.query(GelogicalGeologyTemplate).filter(
                GelogicalGeologyTemplate.geom.ST_Intersects(kk.geom))

            for geotemp in geological_template_detail:
                geo__temp = session.query(
                    (cast(func.ST_Intersection(kk.geom, geotemp.geom), Geography).ST_Area()).label('area_final'))
                geological_template[geotemp.template]["count"] = geological_template[geotemp.template]["count"] + \
                                                                 geo__temp[0][0]

            geologicalTemplateKey = list(
                map(lambda geotemp_kk: geotemp_kk[0],
                    filter(lambda nm_geotype: round(nm_geotype[1]["count"] / 1000000, 2) != 0,
                           geological_template.items())))

            geologicalTemplateValues = list(map(lambda geotemp_kk: {"y": round(geotemp_kk[1]["count"] / 1000000, 2),
                                                                    "color": geotemp_kk[1]['color']},
                                                filter( lambda nm_geotype: round(nm_geotype[1]["count"] / 1000000, 2) != 0, geological_template.items())))

            GeologicalTemplateChartData.append(geologicalTemplateKey)
            GeologicalTemplateChartData.append(geologicalTemplateValues)
            break

        allData = {"seriesData": GeologicalTemplateChartData, "status": 200}
        if (not IsWKT):
            try:
                statObj = Statistic(layer_name=layerName, gid=controlGid, gelogical__geologica_template=allData)
                session.add(statObj)
                session.commit()
            except:
                session.rollback()
                updateObjectStatistic = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
                    Statistic.gid == controlGid).first()
                updateObjectStatistic.gelogical__geologica_template = allData
                session.commit()


        session.close()
        return JsonResponse(allData)
    else:
        allData = {"status": 500, "error": "Something went wrong"}
        return JsonResponse(allData)


# Column Chart
def MineralTypes(request):
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
                DBData__gelogical__mineral_type = QueryObj[0].gelogical__mineral_type
                if (DBData__gelogical__mineral_type != None):
                    session.close()
                    return JsonResponse(DBData__gelogical__mineral_type)

            worinkgModelObjectQuery = session.query(modelObject).filter(modelObject.gid == controlGid)
        else:
            aoiWKT = ast.literal_eval(request.POST.get('wkt'))
            worinkgModelObjectQuery = session.query(
                func.ST_Transform(func.ST_SetSRID(func.ST_GeomFromText(aoiWKT), 3857), 4326).label('geom'))
            # worinkgModelObjectQuery = copy.deepcopy(cc)
        MineralTypeChartData = []
        for kk in worinkgModelObjectQuery:
            # rock_type

            mineral_types = {
                "Barite": {"name": '',
                           "color": "#0deb6a",
                           "count": 0},
                "Iron Ore": {"name": '',
                             "color": "#7d5ad5",
                             "count": 0},
                "Gold": {"name": '',
                         "color": "#f0eb5a",
                         "count": 0},
                "Copper": {"name": '',
                           "color": "#79dc5e",
                           "count": 0},
                "Sands and Gravels": {"name": '',
                                      "color": "#a264e4",
                                      "count": 0},
                "Crude Oil": {"name": '',
                              "color": "#d7287d",
                              "count": 0},
                "Graphite": {"name": '',
                             "color": "#8deadb",
                             "count": 0},
                "Natural gas": {"name": '',
                                "color": "#0ed5df",
                                "count": 0},
                "Sulphuretted": {"name": '',
                                 "color": "#44c846",
                                 "count": 0},
                "Clays": {"name": '',
                          "color": "#84e042",
                          "count": 0},
                "Zinc and Lead": {"name": '',
                                  "color": "#5868cb",
                                  "count": 0},
                "Rock Salt": {"name": '',
                              "color": "#deaf22",
                              "count": 0},
                "Carbonated": {"name": '',
                               "color": "#cb1e29",
                               "count": 0},
                "Limestones,dolomites,marbles": {"name": '',
                                                 "color": "#cb513e",
                                                 "count": 0},
                "Gem Stones": {"name": '',
                               "color": "#cc7dd4",
                               "count": 0},
                "Beryllium": {"name": '',
                              "color": "#b1f04c",
                              "count": 0},
                "Asbestos": {"name": '',
                             "color": "#527ed5",
                             "count": 0},
                "Sulphur": {"name": '',
                            "color": "#ea36b1",
                            "count": 0},
                "Coal": {"name": '',
                         "color": "#42c897",
                         "count": 0},
                "Chromium": {"name": '',
                             "color": "#e4ad69",
                             "count": 0},
                "Fluorite": {"name": '',
                             "color": "#3d33d2",
                             "count": 0},
                "Lazurite": {"name": '',
                             "color": "#ed6f90",
                             "count": 0},
                "Mica": {"name": '',
                         "color": "#74bbd3",
                         "count": 0},
                "Siliceous": {"name": '',
                              "color": "#c051ef",
                              "count": 0},
                "Nitric": {"name": '',
                           "color": "#37f05f",
                           "count": 0},
                "Bauxite": {"name": '',
                            "color": "#da5711",
                            "count": 0},
                "talc": {"name": '',
                         "color": "#ce42c0",
                         "count": 0},
                "Lithium": {"name": '',
                            "color": "#53a0df",
                            "count": 0}}

            minerals_detail = session.query(GelogicalMineralType).filter(
                GelogicalMineralType.geom.ST_Intersects(kk.geom))

            for mineral in minerals_detail:
                mineral_types[mineral.type]["count"] = mineral_types[mineral.type]["count"] + 1

            mineralTypeKey = list(
                map(lambda mineralType_kk: mineralType_kk[0],
                    filter(lambda nm_mineralType: nm_mineralType[1]["count"] != 0, mineral_types.items())))

            mineralTypeValues = list(map(lambda mineralType_kk: {"y": int(mineralType_kk[1]["count"]),
                                                                 "color": mineralType_kk[1]['color']},
                                         filter(lambda nm_mineralType: nm_mineralType[1]["count"] != 0,
                                                mineral_types.items())))

            MineralTypeChartData.append(mineralTypeKey)
            MineralTypeChartData.append(mineralTypeValues)
            break

        allData = {"seriesData": MineralTypeChartData, "status": 200}
        if (not IsWKT):
            try:
                statObj = Statistic(layer_name=layerName, gid=controlGid, gelogical__mineral_type=allData)
                session.add(statObj)
                session.commit()
            except:
                session.rollback()
                updateObjectStatistic = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
                    Statistic.gid == controlGid).first()
                updateObjectStatistic.gelogical__mineral_type = allData
                session.commit()


        session.close()
        return JsonResponse(allData)
    else:
        allData = {"status": 500, "error": "Something went wrong"}
        return JsonResponse(allData)


# Column Chart
def FaultLine(request):

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
                DBData__gelogical__fault_line = QueryObj[0].gelogical__fault_line
                if (DBData__gelogical__fault_line != None):
                    session.close()
                    return JsonResponse(DBData__gelogical__fault_line)
            worinkgModelObjectQuery = session.query(modelObject).filter(modelObject.gid == controlGid)
        else:
            aoiWKT = ast.literal_eval(request.POST.get('wkt'))
            worinkgModelObjectQuery = session.query(
                func.ST_Transform(func.ST_SetSRID(func.ST_GeomFromText(aoiWKT), 3857), 4326).label('geom'))
            # worinkgModelObjectQuery = copy.deepcopy(cc)
        FaultLinesChartData = []
        for kk in worinkgModelObjectQuery:
            # rock_type

            faultLines = {"Fault, trust, inferred": {"name": '',
                                                     "color": "#5e66cf",
                                                     "count": 0},
                          "Fault, normal, inferred": {"name": '',
                                                      "color": "#dfd23a",
                                                      "count": 0},
                          "Fault, normal, proven": {"name": '',
                                                    "color": "#d8b97a",
                                                    "count": 0},
                          "Fault, normal, buried": {"name": '',
                                                    "color": "#dd3fe8",
                                                    "count": 0},
                          "Fault, trust, proven": {"name": '',
                                                   "color": "#4b1706",
                                                   "count": 0}}
            faultLines_detail = session.query(GelogicalFaultLine).filter(
                GelogicalFaultLine.geom.ST_Intersects(kk.geom))

            for faultlin in faultLines_detail:
                fault__line = session.query(
                    (cast(func.ST_Intersection(kk.geom, faultlin.geom), Geography).ST_Length()).label('length_final'))
                faultLines[faultlin.name_type]["count"] = faultLines[faultlin.name_type]["count"] + fault__line[0][0]

            faultLinesKey = list(
                map(lambda faultLines_kk: faultLines_kk[0],
                    filter(lambda nm_faultLines: round(nm_faultLines[1]["count"] / 1000, 2) != 0, faultLines.items())))

            faultLinesValues = list(map(lambda faultLines_kk: {"y": round(faultLines_kk[1]["count"] / 1000, 2),
                                                                 "color": faultLines_kk[1]['color']},
                                        filter(lambda nm_faultLines: round(nm_faultLines[1]["count"] / 1000, 2) != 0,
                                               faultLines.items())))

            FaultLinesChartData.append(faultLinesKey)
            FaultLinesChartData.append(faultLinesValues)

            break

        allData = {"seriesData": FaultLinesChartData, "status": 200}
        if (not IsWKT):
            try:
                statObj = Statistic(layer_name=layerName, gid=controlGid, gelogical__fault_line=allData)
                session.add(statObj)
                session.commit()
            except:
                session.rollback()
                updateObjectStatistic = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
                    Statistic.gid == controlGid).first()
                updateObjectStatistic.gelogical__fault_line = allData
                session.commit()

        session.close()
        return JsonResponse(allData)
    else:
        allData = {"status": 500, "error": "Something went wrong"}
        return JsonResponse(allData)

