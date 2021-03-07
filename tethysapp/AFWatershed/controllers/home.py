from django.shortcuts import render
from tethysapp.AFWatershed.app import AFWatershed as app
from tethysapp.AFWatershed.model import HydrologicalMajorBasin, HydrologicalMacroLevelWatershed, \
    AdminDistrictBoundry, AdminProvienceBoundary, AdminVillages45533, Statistic

from ..utilities import alldata, detailDataWatershed, detailDataWatershedAll, detailDataWatershedAll_new, StoringStats, \
    getStatistics
import ast
from django.http import JsonResponse, HttpResponse
import copy
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy import cast
from geoalchemy2 import Geography, Geometry
def Home(request):
    """
    Controller for the app home page.
    """
    allinformations = alldata()

    context = {
        'layerlist': allinformations['layerlist'],
    }

    return render(request, 'AFWatershed/watershed_home.html', context)

def GetGeoJson(request):
    engine = app.get_persistent_store_database('watershed_afganistan', as_sessionmaker=False)
    engineURL=engine.url
    NewEngine = create_engine(engineURL, poolclass=NullPool)
    session = sessionmaker(bind=NewEngine)()
    data_quick_introduction = {}


    layerName = ast.literal_eval(request.POST.get('layerName'))
    controlGid = ast.literal_eval(request.POST.get('controlGid'))
    worinkgModelObjectQuery = None
    modelObject = None
    if layerName == "basin":
        modelObject = copy.deepcopy(HydrologicalMajorBasin)
    elif layerName == "watershed":
        modelObject = copy.deepcopy(HydrologicalMacroLevelWatershed)


    centroid = None
    GeojsonObject = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {'name': 'EPSG:4326'}
        },
        'features': [
            {
                'type': 'Feature',
                'geometry': {},
                'properties': {
                    'layerName': layerName,
                    'gid': controlGid,
                }
            }
        ]
    }

    worinkgModelObjectQuery = session.query(modelObject).filter(modelObject.gid == controlGid)
    for kk in worinkgModelObjectQuery:

        geoJSONstr = session.query(func.ST_AsGeoJSON(func.ST_Transform(kk.geom, 3857)))[0][0]
        geoJSON = ast.literal_eval(str(geoJSONstr))
        GeojsonObject['features'][0]['geometry'] = geoJSON

        centroidStr = session.query(func.ST_AsGeoJSON(kk.geom.ST_Centroid()))[0][0]
        centroid = ast.literal_eval(str(centroidStr))['coordinates']

        ext = session.query(func.ST_Extent(func.ST_Transform(kk.geom, 3857))).group_by(kk.geom)[0][0]
        strExt = str(ext).replace('BOX(', '[').replace(')', ']').replace(' ', ',')
        mapExtent = ast.literal_eval(strExt)


    # Quick information Macro Watershed
    qiMicroLevelWatershed = session.query(HydrologicalMacroLevelWatershed).filter(
        HydrologicalMacroLevelWatershed.geom.ST_Intersects(kk.geom))
    totalarea = 0
    for qi in qiMicroLevelWatershed:
        area = session.query(
            (cast(func.ST_Intersection(kk.geom, qi.geom), Geography).ST_Area()).label('area_final'))
        if area[0][0] != 0:
            totalarea = totalarea + area[0][0]

    # Quick information Province Extent
    qiProvince = session.query(AdminProvienceBoundary).filter(AdminProvienceBoundary.geom.ST_Intersects(kk.geom))
    provinceExt = ''
    for qi in qiProvince:
        area = session.query(
            (cast(func.ST_Intersection(kk.geom, qi.geom), Geography).ST_Area()).label('area_final'))
        if area[0][0] != 0:
            provinceExt = provinceExt + '<li>' + qi.prov_34_na + '</li>'

    # Quick information Village Count
    villageCount = session.query(AdminVillages45533).filter(AdminVillages45533.geom.ST_Intersects(kk.geom)).count()


    data_quick_introduction['qi_total_area'] = str(round(totalarea / 1000000, 2)) + ' sq.km'
    data_quick_introduction['qi_num_of_village'] = villageCount
    data_quick_introduction['qi_provence'] = provinceExt

    data={"geojson":GeojsonObject,"centroid":centroid,"extent":mapExtent,'data_quick_introduction':data_quick_introduction}
    session.close()
    return JsonResponse(data)



# Pie Chart
def QuickIntroduction(request):
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
                rockTypeData = QueryObj[0].quick_introduction
                if (rockTypeData != None):
                    session.close()
                    return JsonResponse(rockTypeData)

            worinkgModelObjectQuery = session.query(modelObject).filter(modelObject.gid == controlGid)
        else:
            aoiWKT = ast.literal_eval(request.POST.get('wkt'))
            worinkgModelObjectQuery = session.query(
                func.ST_Transform(func.ST_SetSRID(func.ST_GeomFromText(aoiWKT), 3857), 4326).label('geom'))
            # worinkgModelObjectQuery = copy.deepcopy(cc)
        data_quick_introduction = {}
        for kk in worinkgModelObjectQuery:
            # slope
            # Quick information Macro Watershed
            qiMicroLevelWatershed = session.query(HydrologicalMacroLevelWatershed).filter(
                HydrologicalMacroLevelWatershed.geom.ST_Intersects(kk.geom))
            totalarea = 0
            for qi in qiMicroLevelWatershed:
                area = session.query(
                    (cast(func.ST_Intersection(kk.geom, qi.geom), Geography).ST_Area()).label('area_final'))
                if area[0][0] != 0:
                    totalarea = totalarea + area[0][0]

            # Quick information Province Extent
            qiProvince = session.query(AdminProvienceBoundary).filter(
                AdminProvienceBoundary.geom.ST_Intersects(kk.geom))
            provinceExt = ''
            for qi in qiProvince:
                area = session.query(
                    (cast(func.ST_Intersection(kk.geom, qi.geom), Geography).ST_Area()).label('area_final'))
                if area[0][0] != 0:
                    provinceExt = provinceExt + '<li>' + qi.prov_34_na + '</li>'

            # Quick information Village Count
            villageCount = session.query(AdminVillages45533).filter(
                AdminVillages45533.geom.ST_Intersects(kk.geom)).count()

            data_quick_introduction['qi_total_area'] = str(round(totalarea / 1000000, 2)) + ' sq.km'
            data_quick_introduction['qi_num_of_village'] = villageCount
            data_quick_introduction['qi_provence'] = provinceExt

            break
        allData = {"data_quick_introduction": data_quick_introduction, "status": 200}
        if (not IsWKT):
            try:
                statObj = Statistic(layer_name=layerName, gid=controlGid, quick_introduction=allData)
                session.add(statObj)
                session.commit()
            except:
                session.rollback()
                updateObjectStatistic = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
                    Statistic.gid == controlGid).first()
                updateObjectStatistic.quick_introduction = allData
                session.commit()

        session.close()
        return JsonResponse(allData)
    else:
        allData = {"status": 500, "error": "Something went wrong"}
        return JsonResponse(allData)



