from .app import AFWatershed as app
from .model import WatershedLayergrouptwo, WatershedLayergroupone, HydrologicalMacroLevelWatershed, \
    GelogicalMineralType, GelogicalRockType, SoilParametersSoilsDepth, SoilParametersSoilsType, HydrologicalWellsDepth, \
    HydrologicalLake, HydrologicalAfgAllRiver, HydrologicalMarshland, HydrologicalGwDepthFlow2010, \
    GelogicalGeologyTemplate, GelogicalFaultLine, HydrologicalMajorBasin, AdminDistrictBoundry, AdminProvienceBoundary, \
    AdminVillages45533, AdminCountryBndry, Statistic, FloodAllFlood
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
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker

# from .map_printer import PrintingAllMaps,PrintingAllMapsMain

myColorDictionary = {
    0: '#d1be0f',
    1: '#ffff00',
    2: '#80ff00',
    3: '#00ff00',  # Green
    4: '#00fd80',
    5: '#00ffff',
    6: '#0080ff',
    7: '#0000ff',  # Blue
    8: '#8000ff',
    9: '#ff00ff',
    10: '#ff007f',
    11: '#ff0000',  # red
}
slopeColors = ['#50B432', '#058DC7', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4',
               '#00ffff', '#8000ff']


def alldata():
    """
    Get all persisted dams.
    """
    # Get connection/session to database
    engine = app.get_persistent_store_database('watershed_afganistan', as_sessionmaker=False)
    engineURL=engine.url
    NewEngine = create_engine(engineURL, poolclass=NullPool)
    session = sessionmaker(bind=NewEngine)()

    all_layers_info = []
    layerGroup = session.query(WatershedLayergroupone).all()
    for i in layerGroup:
        LayerGroupInfo = {}
        LayerGroupInfo['name'] = str(i.htmlText)
        LayerGroupInfo['htmlid'] = str(i.htmlId)
        LayerGroupInfo['oder'] = i.order

        if (i.is_group_layer):
            LayerGroupInfo['is_group_layer'] = 1
        else:
            LayerGroupInfo['is_group_layer'] = 0

        LayersDetail = session.query(WatershedLayergrouptwo).filter(
            WatershedLayergrouptwo.LayerGroupOneId_id == i.id).order_by(WatershedLayergrouptwo.order.asc())
        # LayersDetail=LayerGroupTwo.objects.filter(LayerGroupOneId_id=i.id)
        layerDetailAll = []
        for j in LayersDetail:
            LayerDetailInfo = {}
            LayerDetailInfo['oder'] = j.order
            LayerDetailInfo['htmltext'] = str(j.htmlText)
            LayerDetailInfo['htmlid'] = str(j.htmlId)
            LayerDetailInfo['layernamegeoserver'] = str(j.layernamegeoserver)
            LayerDetailInfo['data_type'] = str(j.data_type)
            LayerDetailInfo['wmsTileType'] = str(j.wmsTileType)
            LayerDetailInfo['server_type'] = str(j.server_type)
            LayerDetailInfo['style'] = str(j.style)
            LayerDetailInfo['wms_url'] = str(j.wms_url)
            LayerDetailInfo['legend'] = str(j.legend)
            LayerDetailInfo['color_scale_range'] = str(j.color_scale_range)
            LayerDetailInfo['annual_monthly'] = str(j.annual_monthly)
            LayerDetailInfo['sld_body_thredds'] = str(j.sld_body_thredds)
            LayerDetailInfo['unit'] = str(j.unit)

            if (j.opacity_slider):
                LayerDetailInfo['opacity_slider'] = 1
            else:
                LayerDetailInfo['opacity_slider'] = 0

            if (j.isLayer):
                LayerDetailInfo['isLayer'] = 1
            else:
                LayerDetailInfo['isLayer'] = 0
            if (j.defaultLayerVisibility):
                LayerDetailInfo['layervisibility'] = 1
            else:
                LayerDetailInfo['layervisibility'] = 0
            if (j.mask):
                LayerDetailInfo['mask'] = 1
            else:
                LayerDetailInfo['mask'] = 0
            LayerDetailInfo['zindex'] = j.zIndex
            layerDetailAll.append(LayerDetailInfo)
        LayerGroupInfo["layers"] = layerDetailAll
        all_layers_info.append(LayerGroupInfo)

    BasinAll = session.query(HydrologicalMajorBasin).order_by(HydrologicalMajorBasin.mj_basin_f.asc())
    BasinAlData = []
    for bas in BasinAll:
        BasinAlData.append((bas.mj_basin_f, bas.gid))

    HydrologicalMacroLevelWatershedAll = session.query(HydrologicalMacroLevelWatershed).order_by(
        HydrologicalMacroLevelWatershed.ws_name_f_.asc())
    HydrologicalMacroLevelWatershedData = []
    for k in HydrologicalMacroLevelWatershedAll:
        HydrologicalMacroLevelWatershedData.append((k.ws_name_f_, k.gid))

    ProvinceAll = session.query(AdminProvienceBoundary).order_by(AdminProvienceBoundary.prov_34_na.asc())
    ProvinceData = []
    for provi in ProvinceAll:
        ProvinceData.append((provi.prov_34_na, provi.gid))

    DistrictAll = session.query(AdminDistrictBoundry).order_by(AdminDistrictBoundry.dist_34_na.asc())
    DistrictData = []
    for dist in DistrictAll:
        DistrictData.append((dist.dist_34_na, dist.gid))

    session.close()

    allData = {}
    allData['layerlist'] = all_layers_info
    allData['basindata'] = BasinAlData
    allData['watershedData'] = HydrologicalMacroLevelWatershedData
    allData['district'] = DistrictData
    allData['province'] = ProvinceData

    # poly=''
    # elevation_raster = 'mep/raster/dem.tif'
    # elevation = {}
    # elevation_stats = zonal_stats(poly, elevation_raster, stats="min max")
    # dirPath='/media/suman/New\ Volume/WTRSED/Topographical/'
    # #dirpath = os.getcwd()+'/tethysApplicationProject/tethysapp-AFWatershed/tethysapp/AFWatershed/raster/'

    return allData


def detailDataWatershed():
    """
    Get all persisted dams.
    """
    # Get connection/session to database
    engine = app.get_persistent_store_database('watershed_afganistan', as_sessionmaker=False)
    engineURL=engine.url
    NewEngine = create_engine(engineURL, poolclass=NullPool)
    session = sessionmaker(bind=NewEngine)()

    HydrologicalMacroLevelWatershedGEOJSON = session.query(HydrologicalMacroLevelWatershed).all()
    MacroGeoJSON = {}
    dirPath = os.getcwd() + "/SumanApp/tethysapp-AFWatershed/tethysapp/AFWatershed/raster/"
    elevation_raster = dirPath + 'topographical/DEM.tif'
    aspect_raster = dirPath + 'topographical/Aspect.tif'
    slope_raster = dirPath + 'topographical/Slope.tif'
    i = 1
    infographics_all = {}
    data_well_depth = [{
        "name": "Max",
        "data": []}, {
        "name": "Mean",
        "data": []}, {
        "name": "Min",
        "data": []}]
    data_quick_introduction = {}
    for kk in HydrologicalMacroLevelWatershedGEOJSON:

        # watershedId=kk.gid
        poly = session.query(kk.geom.ST_AsText())[0]

        # elevation
        elevation_stats = zonal_stats(poly, elevation_raster, stats="min max")
        elevMin = elevation_stats[0]['min']
        elevMax = elevation_stats[0]['max']

        ele_max = {'icon': ' <i class="fas fa-water"></i>', 'name': "Maximum", 'value': str(elevMax) + ' m'}
        ele_min = {'icon': ' <i class="fas fa-water"></i>', 'name': "minimum", 'value': str(elevMin) + ' m'}

        infographics_all['infographics_elevation'] = [ele_max, ele_min]

        # aspect
        infographics_aspect = []
        aspect_reference = {
            1: {"name": "Flat",
                "value": "",
                "nameandvalue": "Flat (-1)",
                'icon': ' <i class="fas fa-water"></i>'},
            2: {"name": "North",
                "value": "",
                "nameandvalue": "North (0-22.5)",
                'icon': ' <i class="fas fa-water"></i>'},
            3: {"name": "Northeast",
                "value": "",
                "nameandvalue": "Northeast (22.5-67.5)",
                'icon': ' <i class="fas fa-water"></i>'},
            4: {"name": "East",
                "value": "",
                "nameandvalue": "East (67.5-112.5)",
                'icon': ' <i class="fas fa-water"></i>'},
            5: {"name": "Southeast",
                "value": "",
                "nameandvalue": "Southeast (112.5-157.5)",
                'icon': ' <i class="fas fa-water"></i>'},
            6: {"name": "South",
                "value": "",
                "nameandvalue": "South (157.5-202.5)",
                'icon': ' <i class="fas fa-water"></i>'},
            7: {"name": "Southwest",
                "value": "",
                "nameandvalue": "Southwest (202.5-247.5)",
                'icon': ' <i class="fas fa-water"></i>'},
            8: {"name": "West",
                "value": "",
                "nameandvalue": "West (247.5-292.5)",
                'icon': ' <i class="fas fa-water"></i>'},
            9: {"name": "Northwest",
                "value": "",
                "nameandvalue": "Northwest (292.5-337.5)",
                'icon': ' <i class="fas fa-water"></i>'},
            10: {"name": "North",
                 "value": "",
                 "nameandvalue": "North (337.5-360)",
                 'icon': ' <i class="fas fa-water"></i>'}}

        aspect_stats = zonal_stats(poly, aspect_raster, copy_properties=True, nodata_value=0, categorical=True)
        aspectKeys = list(aspect_stats[0].keys())
        aspectKeys.sort()
        for jj in aspectKeys:
            temp = {'icon': ' <i class="fas fa-water"></i>', 'name': aspect_reference[jj]['name'],
                    'value': str(round(aspect_stats[0][jj] * 0.0081, 2)) + ' sq.km'}
            infographics_aspect.append(temp)

        infographics_all['infographics_aspect'] = infographics_aspect

        # slope
        infographics_slope = []
        slope_stats = zonal_stats(poly, slope_raster, copy_properties=True, nodata_value=0, categorical=True)
        classifiedData = classifySlope(slope_stats[0])

        for jj in classifiedData.keys():
            temp = {'icon': ' <i class="fas fa-water"></i>', 'name': str(jj) + ' %',
                    'value': str(round(classifiedData[jj] * 0.0081, 2)) + ' sq.km'}
            infographics_slope.append(temp)
        infographics_all['infographics_slope'] = infographics_slope

        # minerals type
        infographics_mineral_type = []
        mineral_types = {
            "Barite": 0,
            "Iron Ore": 0,
            "Gold": 0,
            "Copper": 0,
            "Sands and Gravels": 0,
            "Crude Oil": 0,
            "Graphite": 0,
            "Natural gas": 0,
            "Sulphuretted": 0,
            "Clays": 0,
            "Zinc and Lead": 0,
            "Rock Salt": 0,
            "Carbonated": 0,
            "Limestones, Dolomites, Marbles": 0,
            "Gem Stones": 0,
            "Beryllium": 0,
            "Asbestos": 0,
            "Sulphur": 0,
            "Coal": 0,
            "Chromium": 0,
            "Fluorite": 0,
            "Lazurite": 0,
            "Mica": 0,
            "Siliceous": 0,
            "Nitric": 0,
            "Bauxite": 0,
            "talc": 0,
            "Lithium": 0, }

        minerals_detail = session.query(GelogicalMineralType).filter(
            GelogicalMineralType.geom.ST_Intersects(kk.geom))

        # mineral_types={}
        # test_minerals_detail = session.query(GelogicalMineralType).filter(
        #     GelogicalMineralType.geom.ST_Intersects(kk.geom)).distinct(GelogicalMineralType.type)
        # for tt in test_minerals_detail:
        #     mineral_types[tt.type]=0

        for mineral in minerals_detail:
            mineral_types[mineral.type] = mineral_types[mineral.type] + 1

        for mine in mineral_types.keys():
            if mineral_types[mine] != 0:
                temp = {'icon': ' <i class="fas fa-water"></i>', 'name': mine,
                        'value': mineral_types[mine]}
                infographics_mineral_type.append(temp)

        infographics_all['infographics_mineral_type'] = infographics_mineral_type

        # rock_type
        infographics_rock_type = []
        rock_type = {"Bedrock continuously covered by > 20 ft. of soil": 0,
                     "Soft Rocks:  Sandstone, shale, conglomerate": 0,
                     "Hard Rocks:  Limestone, dolomite": 0,
                     "Hard Rocks:  Granite, basalt, gabbro": 0,
                     "Hard & Soft Rocks:  Gneiss, quartzite, marble, schist, slate": 0,
                     "Hard & Soft Rocks:  Limestone, sandstone, shale, conglomerate": 0}

        rock_type_detail = session.query(GelogicalRockType).filter(
            GelogicalRockType.geom.ST_Intersects(kk.geom))
        for georocktype in rock_type_detail:
            area_rock = session.query(
                (cast(func.ST_Intersection(kk.geom, georocktype.geom), Geography).ST_Area()).label('area_final'))
            # area_test=session.query((cast(kk.geom,Geography).ST_Area()).label('area_final'))
            rock_type[georocktype.descrip] = rock_type[georocktype.descrip] + area_rock[0][0]

        for rctype in rock_type.keys():
            if rock_type[rctype] != 0:
                temp = {'icon': ' <i class="fas fa-water"></i>', 'name': rctype,
                        'value': str(round(rock_type[rctype] / 1000000, 2)) + ' sq.km'}

                infographics_rock_type.append(temp)

        infographics_all['infographics_rock_type'] = infographics_rock_type

        # geological_templates
        infographics_geological_template = []
        geological_template = {"limestone": 0,
                               "granite": 0,
                               "clastic rock": 0,
                               "aeolian sands": 0,
                               "ophiolites": 0,
                               "foliated": 0,
                               "sand. gravel, unconsolidated seds.": 0,
                               "crystalline": 0,
                               "volcanic": 0}
        geological_template_detail = session.query(GelogicalGeologyTemplate).filter(
            GelogicalGeologyTemplate.geom.ST_Intersects(kk.geom))

        for geotemp in geological_template_detail:
            geo__temp = session.query(
                (cast(func.ST_Intersection(kk.geom, geotemp.geom), Geography).ST_Area()).label('area_final'))
            geological_template[geotemp.template] = geological_template[geotemp.template] + geo__temp[0][0]

        for gtemp in geological_template.keys():
            if geological_template[gtemp] != 0:
                temp = {'icon': ' <i class="fas fa-water"></i>', 'name': gtemp,
                        'value': str(round(geological_template[gtemp] / 1000000, 2)) + ' sq.km'}
                infographics_geological_template.append(temp)

        infographics_all['infographics_geological_template'] = infographics_geological_template

        # geological_fault_lines
        infographics_geological_fault_lines = []
        faultLines = {"Fault, trust, inferred": 0,
                      "Fault, normal, inferred": 0,
                      "Fault, normal, proven": 0,
                      "Fault, normal, buried": 0,
                      "Fault, trust, proven": 0}
        faultLines_detail = session.query(GelogicalFaultLine).filter(
            GelogicalFaultLine.geom.ST_Intersects(kk.geom))

        for faultlin in faultLines_detail:
            fault__line = session.query(
                (cast(func.ST_Intersection(kk.geom, faultlin.geom), Geography).ST_Length()).label('length_final'))
            faultLines[faultlin.name_type] = faultLines[faultlin.name_type] + fault__line[0][0]

        for fltline in faultLines.keys():
            if faultLines[fltline] != 0:
                temp = {'icon': ' <i class="fas fa-water"></i>', 'name': fltline,
                        'value': str(round(faultLines[fltline] / 1000, 2)) + ' km'}

                infographics_geological_fault_lines.append(temp)

        infographics_all['infographics_geological_fault_lines'] = infographics_geological_fault_lines

        # soil_type
        infographics_soil_properties_soil_type = []

        soil_properties_soil_type = {
            "fine grained soils: clay underlain by gravel and silty sand": 0,
            "fine grained & coarse grained soils: silt & clay underlain by silty sand": 0,
            "fine grained & coarse grained soils: clay & silty sand with rock fragments and exposed bedrock": 0,
            "fine grained & coarse grained soils: gravel overlain by clay": 0,
            "coarse grained soils: gravel overlain by caliche and silty sand": 0,
            "fine grained & coarse grained soils: clay & silty sand (shallow), silt & clay (moderately deep to deep)": 0,
            "fine grained soils: sandy silt": 0,
            "coarse grained soils: poorly graded sand": 0,
            "coarse grained:  gravel overlain by silty sand and clayey sand": 0,
            "fine grained & coarse grained soils: clay, silt, & sand": 0
        }
        soil_properties_soil_type_detail = session.query(SoilParametersSoilsType).filter(
            SoilParametersSoilsType.geom.ST_Intersects(kk.geom))

        for soiltype in soil_properties_soil_type_detail:
            soil__type = session.query(
                (cast(func.ST_Intersection(kk.geom, soiltype.geom), Geography).ST_Area()).label('area_final'))
            soil_properties_soil_type[soiltype.soiltype] = soil_properties_soil_type[soiltype.soiltype] + soil__type[0][
                0]

        for stype in soil_properties_soil_type.keys():
            if soil_properties_soil_type[stype] != 0:
                temp = {'icon': ' <i class="fas fa-water"></i>', 'name': stype,
                        'value': str(round(soil_properties_soil_type[stype] / 1000000, 2)) + ' sq.km'}
                infographics_soil_properties_soil_type.append(temp)

        infographics_all['infographics_soil_properties_soil_type'] = infographics_soil_properties_soil_type

        # soil_depth
        infographics_soil_properties_soil_depth = []
        soil_properties_soil_depth = {
            "moderately deep to deep": 0,
            "shallow": 0,
            "very deep": 0
        }
        soil_properties_soil_depth_detail = session.query(SoilParametersSoilsDepth).filter(
            SoilParametersSoilsDepth.geom.ST_Intersects(kk.geom))

        for soildepth in soil_properties_soil_depth_detail:
            soil__depth = session.query(
                (cast(func.ST_Intersection(kk.geom, soildepth.geom), Geography).ST_Area()).label('area_final'))
            soil_properties_soil_depth[soildepth.depth] = soil_properties_soil_depth[soildepth.depth] + \
                                                          soil__depth[0][0]

        for sdepth in soil_properties_soil_depth.keys():
            if soil_properties_soil_depth[sdepth] != 0:
                temp = {'icon': ' <i class="fas fa-water"></i>', 'name': sdepth,
                        'value': str(round(soil_properties_soil_depth[sdepth] / 1000000, 2)) + ' sq.km'}
                infographics_soil_properties_soil_depth.append(temp)

        infographics_all['infographics_soil_properties_soil_depth'] = infographics_soil_properties_soil_depth

        # marshland
        infographics_marshland = []
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

        for mland in marshland.keys():
            if marshland[mland] != 0:
                temp = {'icon': ' <i class="fas fa-water"></i>', 'name': mland,
                        'value': str(round(marshland[mland] / 1000000, 2)) + ' sq.km'}
                infographics_marshland.append(temp)

        infographics_all['infographics_marshland'] = infographics_marshland

        # lake
        infographics_waterbodies = []

        lake_detail = session.query(HydrologicalLake).filter(HydrologicalLake.geom.ST_Intersects(kk.geom))
        lakeall = 0
        for lk in lake_detail:
            l_k = session.query(
                (cast(func.ST_Intersection(kk.geom, lk.geom), Geography).ST_Area()).label('area_final'))
            lakeall = lakeall + l_k[0][0]

        temp_lakes = {'icon': ' <i class="fas fa-water"></i>', 'name': 'Lakes',
                      'value': str(round(lakeall / 1000000, 2)) + ' sq.km'}

        infographics_waterbodies.append(temp_lakes)

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

        for rvs in rivers.keys():
            if rivers[rvs] != 0:
                temp = {'icon': ' <i class="fas fa-water"></i>', 'name': rvs,
                        'value': str(round(rivers[rvs] / 1000, 2)) + ' km'}

                infographics_waterbodies.append(temp)

        infographics_all['infographics_waterbodies'] = infographics_waterbodies

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

        # Quick information Macro Watershed
        qiMicroLevelWatershed = session.query(HydrologicalMacroLevelWatershed).filter(
            HydrologicalMacroLevelWatershed.geom.ST_Intersects(kk.geom))
        totalarea = 0
        macroWatershed = ''
        for qi in qiMicroLevelWatershed:
            area = session.query(
                (cast(func.ST_Intersection(kk.geom, qi.geom), Geography).ST_Area()).label('area_final'))
            if area[0][0] != 0:
                totalarea = totalarea + area[0][0]
                macroWatershed = macroWatershed + '<li>' + qi.ws_name_f_ + '</li>'

        # Quick information Major Basin
        qiMajorBasin = session.query(HydrologicalMajorBasin).filter(HydrologicalMajorBasin.geom.ST_Intersects(kk.geom))
        majorBasin = ''
        for qi in qiMajorBasin:
            area = session.query(
                (cast(func.ST_Intersection(kk.geom, qi.geom), Geography).ST_Area()).label('area_final'))
            if area[0][0] != 0:
                majorBasin = majorBasin + '<li>' + qi.mj_basin_f + '</li>'

        # Quick information District Extent
        qiDistrict = session.query(AdminDistrictBoundry).filter(AdminDistrictBoundry.geom.ST_Intersects(kk.geom))
        districtExt = ''
        for qi in qiDistrict:
            area = session.query(
                (cast(func.ST_Intersection(kk.geom, qi.geom), Geography).ST_Area()).label('area_final'))
            if area[0][0] != 0:
                districtExt = districtExt + '<li>' + qi.dist_34_na + '</li>'

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

        data_quick_introduction['qi_watershed'] = macroWatershed
        data_quick_introduction['qi_basin'] = majorBasin
        data_quick_introduction['qi_total_area'] = str(round(totalarea / 1000000, 2)) + ' sq.km'
        data_quick_introduction['qi_num_of_village'] = villageCount
        # data_quick_introduction['qi_district']=districtExt
        data_quick_introduction['qi_provence'] = provinceExt

        if i == 1:
            break
        i += 1

    session.close()

    allData = {}
    allData['infographics'] = infographics_all
    allData['well_depth_data'] = data_well_depth
    allData['quick_info_data'] = data_well_depth
    allData['qi'] = data_quick_introduction
    return allData


def classifySlope(data):
    mappingDict = {'0-5': 0,
                   '5-10': 0,
                   '10-15': 0,
                   '15-20': 0,
                   '20-25': 0,
                   '25-30': 0,
                   '30-35': 0,
                   '35-40': 0,
                   '40-45': 0,
                   '45-50': 0,
                   '50-55': 0,
                   '55-60': 0,
                   '60-65': 0,
                   '65-70': 0,
                   '70-75': 0,
                   '75-80': 0,
                   '80-85': 0,
                   '85-90': 0
                   }
    slope = data.keys()
    for i in slope:
        a = float(i)
        if a >= 0 and a < 5:
            mappingDict['0-5'] = mappingDict['0-5'] + data[i]
        elif a >= 5 and a < 10:
            mappingDict['5-10'] = mappingDict['5-10'] + data[i]
        elif a >= 10 and a < 15:
            mappingDict['10-15'] = mappingDict['10-15'] + data[i]
        elif a >= 15 and a < 20:
            mappingDict['15-20'] = mappingDict['15-20'] + data[i]
        elif a >= 20 and a < 25:
            mappingDict['20-25'] = mappingDict['20-25'] + data[i]
        elif a >= 25 and a < 30:
            mappingDict['25-30'] = mappingDict['25-30'] + data[i]
        elif a >= 30 and a < 35:
            mappingDict['30-35'] = mappingDict['30-35'] + data[i]
        elif a >= 35 and a < 40:
            mappingDict['35-40'] = mappingDict['35-40'] + data[i]
        elif a >= 40 and a < 45:
            mappingDict['40-45'] = mappingDict['40-45'] + data[i]
        elif a >= 45 and a < 50:
            mappingDict['45-50'] = mappingDict['45-50'] + data[i]
        elif a >= 50 and a < 55:
            mappingDict['50-55'] = mappingDict['50-55'] + data[i]
        elif a >= 55 and a < 60:
            mappingDict['55-60'] = mappingDict['55-60'] + data[i]
        elif a >= 60 and a < 65:
            mappingDict['60-65'] = mappingDict['60-65'] + data[i]
        elif a >= 65 and a < 70:
            mappingDict['65-70'] = mappingDict['65-70'] + data[i]
        elif a >= 70 and a < 75:
            mappingDict['70-75'] = mappingDict['70-75'] + data[i]
        elif a >= 75 and a < 80:
            mappingDict['75-80'] = mappingDict['75-80'] + data[i]
        elif a >= 80 and a < 85:
            mappingDict['80-85'] = mappingDict['80-85'] + data[i]
        elif a >= 85 and a < 90:
            mappingDict['85-90'] = mappingDict['85-90'] + data[i]
    return mappingDict


def detailDataWatershedAll(indata):
    engine = app.get_persistent_store_database('watershed_afganistan', as_sessionmaker=False)
    engineURL=engine.url
    NewEngine = create_engine(engineURL, poolclass=NullPool)
    session = sessionmaker(bind=NewEngine)()



    controlBy = indata['controlBy']
    modelObject = None
    controlGid = None
    worinkgModelObjectQuery = None
    if int(controlBy) == 1:
        layerName = indata['layerName']
        if layerName == "country":
            modelObject = copy.deepcopy(AdminCountryBndry)
        elif layerName == "province":
            modelObject = copy.deepcopy(AdminProvienceBoundary)
        elif layerName == "district":
            modelObject = copy.deepcopy(AdminDistrictBoundry)
    elif int(controlBy) == 2:
        layerName = indata['layerName']
        if layerName == "basin":
            modelObject = copy.deepcopy(HydrologicalMajorBasin)
        elif layerName == "watershed":
            modelObject = copy.deepcopy(HydrologicalMacroLevelWatershed)
    # elif controlBy == 3:
    #     pass

    if (int(controlBy) != 3):
        controlGid = indata['controlGid']
        worinkgModelObjectQuery = session.query(modelObject).filter(modelObject.gid == controlGid)
    else:
        aoiWKT = indata['wkt']
        worinkgModelObjectQuery = session.query(
            func.ST_Transform(func.ST_SetSRID(func.ST_GeomFromText(aoiWKT), 3857), 4326).label('geom'))
        # worinkgModelObjectQuery = copy.deepcopy(cc)

    MacroGeoJSON = {}
    dirPath = os.getcwd() + "/SumanApp/tethysapp-AFWatershed/tethysapp/AFWatershed/raster/"
    elevation_raster = dirPath + 'topographical/DEM.tif'
    aspect_raster = dirPath + 'topographical/Aspect.tif'
    slope_raster = dirPath + 'topographical/Slope.tif'
    i = 1
    infographics_all = {}
    data_well_depth = [{
        "name": "Max",
        "data": []}, {
        "name": "Mean",
        "data": []}, {
        "name": "Min",
        "data": []}]
    data_quick_introduction = {}
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
                    'layerName': indata['layerName'],
                    'gid': indata['controlGid'],
                }
            }
        ]
    }
    mapExtent = None
    centroid = None
    for kk in worinkgModelObjectQuery:
        # watershedId=kk.gid
        poly = session.query(kk.geom.ST_AsText())[0]
        geoJSONstr = session.query(kk.geom.ST_AsGeoJSON())[0][0]
        geoJSON = ast.literal_eval(str(geoJSONstr))
        GeojsonObject['features'][0]['geometry'] = geoJSON

        ext = session.query(func.ST_Extent(func.ST_Transform(kk.geom, 3857))).group_by(kk.geom)[0][0]
        strExt = str(ext).replace('BOX(', '[').replace(')', ']').replace(' ', ',')
        mapExtent = ast.literal_eval(strExt)

        centroidStr = session.query(func.ST_AsGeoJSON(kk.geom.ST_Centroid()))[0][0]
        centroid = ast.literal_eval(str(centroidStr))['coordinates']

        # elevation
        elevation_stats = zonal_stats(poly, elevation_raster, stats="min max")
        elevMin = elevation_stats[0]['min']
        elevMax = elevation_stats[0]['max']

        ele_max = {'icon': ' <i class="fas fa-water"></i>', 'name': "Maximum", 'value': str(elevMax) + ' m'}
        ele_min = {'icon': ' <i class="fas fa-water"></i>', 'name': "minimum", 'value': str(elevMin) + ' m'}

        infographics_all['infographics_elevation'] = [ele_max, ele_min]
        # aspect
        infographics_aspect = []
        aspect_reference = {
            1: {"name": "Flat",
                "value": "",
                "nameandvalue": "Flat (-1)",
                'icon': ' <i class="fas fa-water"></i>'},
            2: {"name": "North",
                "value": "",
                "nameandvalue": "North (0-22.5)",
                'icon': ' <i class="fas fa-water"></i>'},
            3: {"name": "Northeast",
                "value": "",
                "nameandvalue": "Northeast (22.5-67.5)",
                'icon': ' <i class="fas fa-water"></i>'},
            4: {"name": "East",
                "value": "",
                "nameandvalue": "East (67.5-112.5)",
                'icon': ' <i class="fas fa-water"></i>'},
            5: {"name": "Southeast",
                "value": "",
                "nameandvalue": "Southeast (112.5-157.5)",
                'icon': ' <i class="fas fa-water"></i>'},
            6: {"name": "South",
                "value": "",
                "nameandvalue": "South (157.5-202.5)",
                'icon': ' <i class="fas fa-water"></i>'},
            7: {"name": "Southwest",
                "value": "",
                "nameandvalue": "Southwest (202.5-247.5)",
                'icon': ' <i class="fas fa-water"></i>'},
            8: {"name": "West",
                "value": "",
                "nameandvalue": "West (247.5-292.5)",
                'icon': ' <i class="fas fa-water"></i>'},
            9: {"name": "Northwest",
                "value": "",
                "nameandvalue": "Northwest (292.5-337.5)",
                'icon': ' <i class="fas fa-water"></i>'},
            10: {"name": "North",
                 "value": "",
                 "nameandvalue": "North (337.5-360)",
                 'icon': ' <i class="fas fa-water"></i>'}}

        aspect_stats = zonal_stats(poly, aspect_raster, copy_properties=True, nodata_value=0, categorical=True)
        aspectKeys = list(aspect_stats[0].keys())
        aspectKeys.sort()
        for jj in aspectKeys:
            temp = {'icon': ' <i class="fas fa-water"></i>', 'name': aspect_reference[jj]['name'],
                    'value': str(round(aspect_stats[0][jj] * 0.0081, 2)) + ' sq.km'}
            infographics_aspect.append(temp)

        infographics_all['infographics_aspect'] = infographics_aspect

        # slope
        infographics_slope = []
        slope_stats = zonal_stats(poly, slope_raster, copy_properties=True, nodata_value=0, categorical=True)
        classifiedData = classifySlope(slope_stats[0])

        for jj in classifiedData.keys():
            temp = {'icon': ' <i class="fas fa-water"></i>', 'name': str(jj) + ' %',
                    'value': str(round(classifiedData[jj] * 0.0081, 2)) + ' sq.km'}
            infographics_slope.append(temp)
        infographics_all['infographics_slope'] = infographics_slope

        # minerals type
        infographics_mineral_type = []
        mineral_types = {
            "Barite": 0,
            "Iron Ore": 0,
            "Gold": 0,
            "Copper": 0,
            "Sands and Gravels": 0,
            "Crude Oil": 0,
            "Graphite": 0,
            "Natural gas": 0,
            "Sulphuretted": 0,
            "Clays": 0,
            "Zinc and Lead": 0,
            "Rock Salt": 0,
            "Carbonated": 0,
            "Limestones,dolomites,marbles": 0,
            "Gem Stones": 0,
            "Beryllium": 0,
            "Asbestos": 0,
            "Sulphur": 0,
            "Coal": 0,
            "Chromium": 0,
            "Fluorite": 0,
            "Lazurite": 0,
            "Mica": 0,
            "Siliceous": 0,
            "Nitric": 0,
            "Bauxite": 0,
            "talc": 0,
            "Lithium": 0, }

        minerals_detail = session.query(GelogicalMineralType).filter(
            GelogicalMineralType.geom.ST_Intersects(kk.geom))

        # mineral_types={}
        # test_minerals_detail = session.query(GelogicalMineralType).filter(
        #     GelogicalMineralType.geom.ST_Intersects(kk.geom)).distinct(GelogicalMineralType.type)
        # for tt in test_minerals_detail:
        #     mineral_types[tt.type]=0

        for mineral in minerals_detail:
            mineral_types[mineral.type] = mineral_types[mineral.type] + 1

        for mine in mineral_types.keys():
            if mineral_types[mine] != 0:
                temp = {'icon': ' <i class="fas fa-water"></i>', 'name': mine,
                        'value': mineral_types[mine]}
                infographics_mineral_type.append(temp)

        infographics_all['infographics_mineral_type'] = infographics_mineral_type

        # rock_type
        infographics_rock_type = []
        rock_type = {"Bedrock continuously covered by > 20 ft. of soil": 0,
                     "Soft Rocks:  Sandstone, shale, conglomerate": 0,
                     "Hard Rocks:  Limestone, dolomite": 0,
                     "Hard Rocks:  Granite, basalt, gabbro": 0,
                     "Hard & Soft Rocks:  Gneiss, quartzite, marble, schist, slate": 0,
                     "Hard & Soft Rocks:  Limestone, sandstone, shale, conglomerate": 0}

        rock_type_detail = session.query(GelogicalRockType).filter(
            GelogicalRockType.geom.ST_Intersects(kk.geom))
        for georocktype in rock_type_detail:
            area_rock = session.query(
                (cast(func.ST_Intersection(kk.geom, georocktype.geom), Geography).ST_Area()).label('area_final'))
            # area_test=session.query((cast(kk.geom,Geography).ST_Area()).label('area_final'))
            rock_type[georocktype.descrip] = rock_type[georocktype.descrip] + area_rock[0][0]

        for rctype in rock_type.keys():
            if rock_type[rctype] != 0:
                temp = {'icon': ' <i class="fas fa-water"></i>', 'name': rctype,
                        'value': str(round(rock_type[rctype] / 1000000, 2)) + ' sq.km'}

                infographics_rock_type.append(temp)

        infographics_all['infographics_rock_type'] = infographics_rock_type

        # geological_templates
        infographics_geological_template = []
        geological_template = {"limestone": 0,
                               "granite": 0,
                               "clastic rock": 0,
                               "aeolian sands": 0,
                               "ophiolites": 0,
                               "foliated": 0,
                               "sand. gravel, unconsolidated seds.": 0,
                               "crystalline": 0,
                               "volcanic": 0}
        geological_template_detail = session.query(GelogicalGeologyTemplate).filter(
            GelogicalGeologyTemplate.geom.ST_Intersects(kk.geom))

        for geotemp in geological_template_detail:
            geo__temp = session.query(
                (cast(func.ST_Intersection(kk.geom, geotemp.geom), Geography).ST_Area()).label('area_final'))
            geological_template[geotemp.template] = geological_template[geotemp.template] + geo__temp[0][0]

        for gtemp in geological_template.keys():
            if geological_template[gtemp] != 0:
                temp = {'icon': ' <i class="fas fa-water"></i>', 'name': gtemp,
                        'value': str(round(geological_template[gtemp] / 1000000, 2)) + ' sq.km'}
                infographics_geological_template.append(temp)

        infographics_all['infographics_geological_template'] = infographics_geological_template

        # geological_fault_lines
        infographics_geological_fault_lines = []
        faultLines = {"Fault, trust, inferred": 0,
                      "Fault, normal, inferred": 0,
                      "Fault, normal, proven": 0,
                      "Fault, normal, buried": 0,
                      "Fault, trust, proven": 0}
        faultLines_detail = session.query(GelogicalFaultLine).filter(
            GelogicalFaultLine.geom.ST_Intersects(kk.geom))

        for faultlin in faultLines_detail:
            fault__line = session.query(
                (cast(func.ST_Intersection(kk.geom, faultlin.geom), Geography).ST_Length()).label('length_final'))
            faultLines[faultlin.name_type] = faultLines[faultlin.name_type] + fault__line[0][0]

        for fltline in faultLines.keys():
            if faultLines[fltline] != 0:
                temp = {'icon': ' <i class="fas fa-water"></i>', 'name': fltline,
                        'value': str(round(faultLines[fltline] / 1000, 2)) + ' km'}

                infographics_geological_fault_lines.append(temp)

        infographics_all['infographics_geological_fault_lines'] = infographics_geological_fault_lines

        # soil_type
        infographics_soil_properties_soil_type = []

        soil_properties_soil_type = {
            "fine grained soils: clay underlain by gravel and silty sand": 0,
            "fine grained & coarse grained soils: silt & clay underlain by silty sand": 0,
            "fine grained & coarse grained soils: clay & silty sand with rock fragments and exposed bedrock": 0,
            "fine grained & coarse grained soils: gravel overlain by clay": 0,
            "coarse grained soils:gravel overlain by caliche and silty sand": 0,
            "fine grained & coarse grained soils: clay & silty sand (shallow), silt & clay (moderately deep to deep)": 0,
            "fine grained soils: sandy silt": 0,
            "coarse grained soils: poorly graded sand": 0,
            "coarse grained: gravel overlain by silty sand and clayey sand": 0,
            "fine grained & coarse grained soils: clay, silt, & sand": 0
        }
        soil_properties_soil_type_detail = session.query(SoilParametersSoilsType).filter(
            SoilParametersSoilsType.geom.ST_Intersects(kk.geom))

        for soiltype in soil_properties_soil_type_detail:
            soil__type = session.query(
                (cast(func.ST_Intersection(kk.geom, soiltype.geom), Geography).ST_Area()).label('area_final'))
            soil_properties_soil_type[soiltype.soiltype] = soil_properties_soil_type[soiltype.soiltype] + soil__type[0][
                0]

        for stype in soil_properties_soil_type.keys():
            if soil_properties_soil_type[stype] != 0:
                temp = {'icon': ' <i class="fas fa-water"></i>', 'name': stype,
                        'value': str(round(soil_properties_soil_type[stype] / 1000000, 2)) + ' sq.km'}
                infographics_soil_properties_soil_type.append(temp)

        infographics_all['infographics_soil_properties_soil_type'] = infographics_soil_properties_soil_type

        # soil_depth
        infographics_soil_properties_soil_depth = []
        soil_properties_soil_depth = {
            "moderately deep to deep": 0,
            "shallow": 0,
            "very deep": 0
        }
        soil_properties_soil_depth_detail = session.query(SoilParametersSoilsDepth).filter(
            SoilParametersSoilsDepth.geom.ST_Intersects(kk.geom))

        for soildepth in soil_properties_soil_depth_detail:
            soil__depth = session.query(
                (cast(func.ST_Intersection(kk.geom, soildepth.geom), Geography).ST_Area()).label('area_final'))
            soil_properties_soil_depth[soildepth.depth] = soil_properties_soil_depth[soildepth.depth] + \
                                                          soil__depth[0][0]

        for sdepth in soil_properties_soil_depth.keys():
            if soil_properties_soil_depth[sdepth] != 0:
                temp = {'icon': ' <i class="fas fa-water"></i>', 'name': sdepth,
                        'value': str(round(soil_properties_soil_depth[sdepth] / 1000000, 2)) + ' sq.km'}
                infographics_soil_properties_soil_depth.append(temp)

        infographics_all['infographics_soil_properties_soil_depth'] = infographics_soil_properties_soil_depth

        # GwDepthFlow
        infographics_gw_depth_flow = []
        gw_depth_flow = {
            "Fresh water locally plentiful": 0,
            "Fresh water scarce or lacking": 0,
            "Fresh water generally plentiful": 0
        }
        GwDepthFlow_detail = session.query(HydrologicalGwDepthFlow2010).filter(
            HydrologicalGwDepthFlow2010.geom.ST_Intersects(kk.geom))

        for gwdf in GwDepthFlow_detail:
            groundwater__depthflow = session.query(
                (cast(func.ST_Intersection(kk.geom, gwdf.geom), Geography).ST_Area()).label('area_final'))
            gw_depth_flow[gwdf.descrip1] = gw_depth_flow[gwdf.descrip1] + \
                                           groundwater__depthflow[0][0]

        for gwdepth in gw_depth_flow.keys():
            if gw_depth_flow[gwdepth] != 0:
                temp = {'icon': ' <i class="fas fa-water"></i>', 'name': gwdepth,
                        'value': str(round(gw_depth_flow[gwdepth] / 1000000, 2)) + ' sq.km'}
                infographics_gw_depth_flow.append(temp)

        infographics_all['infographics_gw_depth_flow'] = infographics_gw_depth_flow

        # marshland
        infographics_marshland = []
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

        for mland in marshland.keys():
            if marshland[mland] != 0:
                temp = {'icon': ' <i class="fas fa-water"></i>', 'name': mland,
                        'value': str(round(marshland[mland] / 1000000, 2)) + ' sq.km'}
                infographics_marshland.append(temp)

        infographics_all['infographics_marshland'] = infographics_marshland

        # lake
        infographics_waterbodies = []

        lake_detail = session.query(HydrologicalLake).filter(HydrologicalLake.geom.ST_Intersects(kk.geom))
        lakeall = 0
        for lk in lake_detail:
            l_k = session.query(
                (cast(func.ST_Intersection(kk.geom, lk.geom), Geography).ST_Area()).label('area_final'))
            lakeall = lakeall + l_k[0][0]

        temp_lakes = {'icon': ' <i class="fas fa-water"></i>', 'name': 'Lakes',
                      'value': str(round(lakeall / 1000000, 2)) + ' sq.km'}

        infographics_waterbodies.append(temp_lakes)

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

        for rvs in rivers.keys():
            if rivers[rvs] != 0:
                temp = {'icon': ' <i class="fas fa-water"></i>', 'name': rvs,
                        'value': str(round(rivers[rvs] / 1000, 2)) + ' km'}

                infographics_waterbodies.append(temp)

        infographics_all['infographics_waterbodies'] = infographics_waterbodies

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

        # Quick information Macro Watershed
        qiMicroLevelWatershed = session.query(HydrologicalMacroLevelWatershed).filter(
            HydrologicalMacroLevelWatershed.geom.ST_Intersects(kk.geom))
        totalarea = 0
        macroWatershed = ''
        for qi in qiMicroLevelWatershed:
            area = session.query(
                (cast(func.ST_Intersection(kk.geom, qi.geom), Geography).ST_Area()).label('area_final'))
            if area[0][0] != 0:
                totalarea = totalarea + area[0][0]
                macroWatershed = macroWatershed + '<li>' + qi.ws_name_f_ + '</li>'

        # Quick information Major Basin
        qiMajorBasin = session.query(HydrologicalMajorBasin).filter(HydrologicalMajorBasin.geom.ST_Intersects(kk.geom))
        majorBasin = ''
        for qi in qiMajorBasin:
            area = session.query(
                (cast(func.ST_Intersection(kk.geom, qi.geom), Geography).ST_Area()).label('area_final'))
            if area[0][0] != 0:
                majorBasin = majorBasin + '<li>' + qi.mj_basin_f + '</li>'

        # Quick information District Extent
        qiDistrict = session.query(AdminDistrictBoundry).filter(AdminDistrictBoundry.geom.ST_Intersects(kk.geom))
        districtExt = ''
        for qi in qiDistrict:
            area = session.query(
                (cast(func.ST_Intersection(kk.geom, qi.geom), Geography).ST_Area()).label('area_final'))
            if area[0][0] != 0:
                districtExt = districtExt + '<li>' + qi.dist_34_na + '</li>'

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

        data_quick_introduction['qi_watershed'] = macroWatershed
        data_quick_introduction['qi_basin'] = majorBasin
        data_quick_introduction['qi_total_area'] = str(round(totalarea / 1000000, 2)) + ' sq.km'
        data_quick_introduction['qi_num_of_village'] = villageCount
        # data_quick_introduction['qi_district']=districtExt
        data_quick_introduction['qi_provence'] = provinceExt

        if i == 1:
            break
        i += 1

    session.close()

    allData = {}
    allData['infographics'] = infographics_all
    allData['well_depth_data'] = data_well_depth
    allData['quick_info_data'] = data_well_depth
    allData['qi'] = data_quick_introduction
    allData['geojson'] = GeojsonObject
    allData['extent'] = mapExtent
    allData['centroid'] = centroid
    return allData


def detailDataWatershedAll_new(indata):
    engine = app.get_persistent_store_database('watershed_afganistan', as_sessionmaker=False)
    engineURL=engine.url
    NewEngine = create_engine(engineURL, poolclass=NullPool)
    session = sessionmaker(bind=NewEngine)()
    modelObject = None
    layerName = indata['layerName']
    if layerName == "basin":
        modelObject = copy.deepcopy(HydrologicalMajorBasin)
    elif layerName == "watershed":
        modelObject = copy.deepcopy(HydrologicalMacroLevelWatershed)

    controlGid = indata['controlGid']
    worinkgModelObjectQuery = session.query(modelObject).filter(modelObject.gid == controlGid)
    # worinkgModelObjectQuery = session.query(modelObject).all()

    MacroGeoJSON = {}
    dirPath = os.getcwd() + "/SumanApp/tethysapp-AFWatershed/tethysapp/AFWatershed/raster/"
    elevation_raster = dirPath + 'topographical/DEM.tif'
    aspect_raster = dirPath + 'topographical/Aspect.tif'
    slope_raster = dirPath + 'topographical/Slope.tif'
    i = 1
    infographics_all = {}
    data_well_depth = [{
        "name": "Max",
        "data": []}, {
        "name": "Mean",
        "data": []}, {
        "name": "Min",
        "data": []}]
    SlopeChartData = []
    AspectChartdata = []
    GwDepthFlowChartData = []
    ElevationChartData = []
    DatawaterBodiesAndMarshland = []
    SoilDepthChartData = []
    SoilTypeChartData = []
    GeologicalTemplateChartData = []
    MineralTypeChartData = []
    FaultLinesChartData = []
    floodChartData = []
    data_quick_introduction = {}
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
                    'layerName': indata['layerName'],
                    'gid': indata['controlGid'],
                }
            }
        ]
    }
    GeojsonObject3857 = {
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
                    'layerName': indata['layerName'],
                    'gid': indata['controlGid'],
                }
            }
        ]
    }
    mapExtent = None
    centroid = None
    for kk in worinkgModelObjectQuery:
        # watershedId=kk.gid
        poly = session.query(kk.geom.ST_AsText())[0]
        # geoJSONstr = session.query(kk.geom.ST_AsGeoJSON())[0][0]
        geoJSONstr = session.query(func.ST_AsGeoJSON(func.ST_Transform(kk.geom, 3857)))[0][0]
        geoJSON = ast.literal_eval(str(geoJSONstr))
        GeojsonObject['features'][0]['geometry'] = geoJSON

        ext = session.query(func.ST_Extent(func.ST_Transform(kk.geom, 3857))).group_by(kk.geom)[0][0]
        strExt = str(ext).replace('BOX(', '[').replace(')', ']').replace(' ', ',')
        mapExtent = ast.literal_eval(strExt)

        centroidStr = session.query(func.ST_AsGeoJSON(kk.geom.ST_Centroid()))[0][0]
        centroid = ast.literal_eval(str(centroidStr))['coordinates']

        print("slope")
        # slope
        slope_stats = zonal_stats(poly, slope_raster, copy_properties=True, nodata_value=0, categorical=True)
        classifiedData = classifySlope_New(slope_stats[0])
        totalSlope = sum(v for (k, v) in classifiedData.items())
        SlopeKeyValueList = list(classifiedData.items())
        # SlopeChartData = list(map(lambda kk: {"name":kk[0],"y":round(kk[1]*100/totalSlope,2),"color":myColorDictionary[SlopeKeyValueList.index(kk)]},SlopeKeyValueList))
        SlopeChartData = list(map(lambda kk: {"name": kk[0], "y": round(kk[1] * 100 / totalSlope, 2),
                                              "color": slopeColors[SlopeKeyValueList.index(kk)]}, SlopeKeyValueList))


        print("aspect")
        # aspect
        # 2="North(0-22.5)" 10: "North(337.5-360)"
        aspect_referenceKeyValues = {
            1: "Flat",
            2: "North",
            3: "Northeast",
            4: "East",
            5: "Southeast",
            6: "South",
            7: "Southwest",
            8: "West",
            9: "Northwest",
            10: "North(337.5-360)"}

        aspect_stats = zonal_stats(poly, aspect_raster, copy_properties=True, nodata_value=0, categorical=True)
        a = aspect_stats[0][2] + aspect_stats[0][10]
        del aspect_stats[0][10]
        aspect_stats[0][2] = a

        aspectStatItemsList = list(aspect_stats[0].items())
        AspectKeys = list(map(lambda kk: aspect_referenceKeyValues[kk[0]], aspectStatItemsList))
        AspectValues = list(map(lambda kk: round(kk[1] * 0.001156, 2), aspectStatItemsList))
        AspectChartdata.append(AspectKeys)
        AspectChartdata.append(AspectValues)

        print("elevation")
        # elevation
        elevation_stats = zonal_stats(poly, elevation_raster, stats="min max")
        elevationStatTest = zonal_stats(poly, elevation_raster, copy_properties=True, nodata_value=0, categorical=True)
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

        print("welldepth")
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

        print("GwDepthFlow")
        # GwDepthFlow
        gw_depth_flow = {
            "Fresh water locally plentiful": 0,
            "Fresh water scarce or lacking": 0,
            "Fresh water generally plentiful": 0
        }
        GwDepthFlow_detail = session.query(HydrologicalGwDepthFlow2010).filter(
            HydrologicalGwDepthFlow2010.geom.ST_Intersects(kk.geom))

        for gwdf in GwDepthFlow_detail:
            groundwater__depthflow = session.query(
                (cast(func.ST_Intersection(kk.geom, gwdf.geom), Geography).ST_Area()).label('area_final'))
            gw_depth_flow[gwdf.descrip1] = gw_depth_flow[gwdf.descrip1] + \
                                           groundwater__depthflow[0][0]

        GwDepthFlowKey = list(
            map(lambda gwk: gwk[0], filter(lambda nm: round(nm[1] / 1000000, 2) != 0, gw_depth_flow.items())))
        GwDepthFlowValues = list(map(lambda gwk: round(gwk[1] / 1000000, 2),
                                     filter(lambda nm: round(nm[1] / 1000000, 2) != 0, gw_depth_flow.items())))
        GwDepthFlowChartData.append(GwDepthFlowKey)
        GwDepthFlowChartData.append(GwDepthFlowValues)

        print("flood all")
        # flood all
        hydrological_flood = {"High Severity": 0,
                              "Moderate Severity": 0,
                              "Severe Event": 0,
                              "Moderately Low Severity": 0,
                              "Very Low Severity": 0,
                              "Most Severe Event": 0,
                              "Low Severity": 0}
        hydrological_flood_detail = session.query(FloodAllFlood.gid,FloodAllFlood.flood,(cast(func.ST_Intersection(kk.geom, FloodAllFlood.geom), Geography).ST_Area()).label('area_final')).filter(
            FloodAllFlood.geom.ST_Intersects(kk.geom))
        print(hydrological_flood_detail.count())
        print(hydrological_flood_detail)
        cc=hydrological_flood_detail.count()
        floodCount=0
        printInterval=0
        for floodItem in hydrological_flood_detail:
            if(floodCount==printInterval):
                print(floodCount)
                printInterval+=1000
            # hydro__flood = session.query(
            #     (cast(func.ST_Intersection(kk.geom, floodItem.geom), Geography).ST_Area()).label('area_final'))
            hydrological_flood[floodItem.flood] = hydrological_flood[floodItem.flood] + floodItem.area_final
            floodCount+=1

        hydroFloodkeyValueList = list(hydrological_flood.items())
        totalfloodItem = sum(vm for (km, vm) in hydroFloodkeyValueList)
        floodChartData = list(
            map(lambda flood_kk: {"name": flood_kk[0], "y": round(flood_kk[1] * 100 / totalfloodItem, 2),
                                 "color": slopeColors[hydroFloodkeyValueList.index(flood_kk)]},
                list(filter(lambda nm: round(nm[1] * 100 / totalfloodItem, 2) != 0,
                            hydroFloodkeyValueList))))

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


        print("soil depth")
        # soil_depth
        soil_properties_soil_depth = {
            "moderately deep to deep": 0,
            "shallow": 0,
            "very deep": 0
        }
        soil_properties_soil_depth_detail = session.query(SoilParametersSoilsDepth).filter(
            SoilParametersSoilsDepth.geom.ST_Intersects(kk.geom))

        for soildepth in soil_properties_soil_depth_detail:
            soil__depth = session.query(
                (cast(func.ST_Intersection(kk.geom, soildepth.geom), Geography).ST_Area()).label('area_final'))
            soil_properties_soil_depth[soildepth.depth] = soil_properties_soil_depth[soildepth.depth] + \
                                                          soil__depth[0][0]

        soilDepthkeyValueList = list(soil_properties_soil_depth.items())
        totalsoildepth = sum(vm for (km, vm) in soilDepthkeyValueList)
        SoilDepthChartData = list(
            map(lambda soil_kk: {"name": soil_kk[0], "y": round(soil_kk[1] * 100 / totalsoildepth, 2),
                                 "color": slopeColors[soilDepthkeyValueList.index(soil_kk)]},
                list(filter(lambda nm: round(nm[1] * 100 / totalsoildepth, 2) != 0,
                            soilDepthkeyValueList))))
        print("soil type")

        # soil_type
        soil_properties_soil_type = {
            "fine grained soils: clay underlain by gravel and silty sand": 0,
            "fine grained & coarse grained soils: silt & clay underlain by silty sand": 0,
            "fine grained & coarse grained soils: clay & silty sand with rock fragments and exposed bedrock": 0,
            "fine grained & coarse grained soils: gravel overlain by clay": 0,
            "coarse grained soils:gravel overlain by caliche and silty sand": 0,
            "fine grained & coarse grained soils: clay & silty sand (shallow), silt & clay (moderately deep to deep)": 0,
            "fine grained soils: sandy silt": 0,
            "coarse grained soils: poorly graded sand": 0,
            "coarse grained: gravel overlain by silty sand and clayey sand": 0,
            "fine grained & coarse grained soils: clay, silt, & sand": 0
        }
        soil_properties_soil_type_detail = session.query(SoilParametersSoilsType).filter(
            SoilParametersSoilsType.geom.ST_Intersects(kk.geom))

        for soiltype in soil_properties_soil_type_detail:
            soil__type = session.query(
                (cast(func.ST_Intersection(kk.geom, soiltype.geom), Geography).ST_Area()).label('area_final'))
            soil_properties_soil_type[soiltype.soiltype] = soil_properties_soil_type[soiltype.soiltype] + soil__type[0][
                0]

        SoilTypeKey = list(
            map(lambda soilTy_kk: soilTy_kk[0],
                filter(lambda nm_stype: round(nm_stype[1] / 1000000, 2) != 0, soil_properties_soil_type.items())))
        SoilTypeValues = list(map(lambda soilTy_kk: round(soilTy_kk[1] / 1000000, 2),
                                  filter(lambda nm_stype: round(nm_stype[1] / 1000000, 2) != 0,
                                         soil_properties_soil_type.items())))
        SoilTypeChartData.append(SoilTypeKey)
        SoilTypeChartData.append(SoilTypeValues)

        print("rock type")
        # rock_type
        rock_type = {"Bedrock continuously covered by > 20 ft. of soil": 0,
                     "Soft Rocks:  Sandstone, shale, conglomerate": 0,
                     "Hard Rocks:  Limestone, dolomite": 0,
                     "Hard Rocks:  Granite, basalt, gabbro": 0,
                     "Hard & Soft Rocks:  Gneiss, quartzite, marble, schist, slate": 0,
                     "Hard & Soft Rocks:  Limestone, sandstone, shale, conglomerate": 0}

        rock_type_detail = session.query(GelogicalRockType).filter(
            GelogicalRockType.geom.ST_Intersects(kk.geom))
        for georocktype in rock_type_detail:
            area_rock = session.query(
                (cast(func.ST_Intersection(kk.geom, georocktype.geom), Geography).ST_Area()).label('area_final'))
            # area_test=session.query((cast(kk.geom,Geography).ST_Area()).label('area_final'))
            rock_type[georocktype.descrip] = rock_type[georocktype.descrip] + area_rock[0][0]

        rockTypekeyValueList = list(rock_type.items())
        totalrocktype = sum(vm for (km, vm) in rockTypekeyValueList)
        RockTypeChartData = list(
            map(lambda rtype_kk: {"name": rtype_kk[0], "y": round(rtype_kk[1] * 100 / totalrocktype, 2),
                                  "color": slopeColors[rockTypekeyValueList.index(rtype_kk)]},
                list(filter(lambda nm: round(nm[1] * 100 / totalrocktype, 2) != 0,
                            rockTypekeyValueList))))

        print("geological templates")
        # geological_templates
        geological_template = {"limestone": 0,
                               "granite": 0,
                               "clastic rock": 0,
                               "aeolian sands": 0,
                               "ophiolites": 0,
                               "foliated": 0,
                               "sand. gravel, unconsolidated seds.": 0,
                               "crystalline": 0,
                               "volcanic": 0}
        geological_template_detail = session.query(GelogicalGeologyTemplate).filter(
            GelogicalGeologyTemplate.geom.ST_Intersects(kk.geom))

        for geotemp in geological_template_detail:
            geo__temp = session.query(
                (cast(func.ST_Intersection(kk.geom, geotemp.geom), Geography).ST_Area()).label('area_final'))
            geological_template[geotemp.template] = geological_template[geotemp.template] + geo__temp[0][0]

        geologicalTemplateKey = list(
            map(lambda geotemp_kk: geotemp_kk[0],
                filter(lambda nm_geotype: round(nm_geotype[1] / 1000000, 2) != 0, geological_template.items())))
        geologicalTemplateValues = list(map(lambda geotemp_kk: round(geotemp_kk[1] / 1000000, 2),
                                            filter(lambda nm_geotype: round(nm_geotype[1] / 1000000, 2) != 0,
                                                   geological_template.items())))
        GeologicalTemplateChartData.append(geologicalTemplateKey)
        GeologicalTemplateChartData.append(geologicalTemplateValues)

        print("minerals type")
        # minerals type

        mineral_types = {
            "Barite": 0,
            "Iron Ore": 0,
            "Gold": 0,
            "Copper": 0,
            "Sands and Gravels": 0,
            "Crude Oil": 0,
            "Graphite": 0,
            "Natural gas": 0,
            "Sulphuretted": 0,
            "Clays": 0,
            "Zinc and Lead": 0,
            "Rock Salt": 0,
            "Carbonated": 0,
            "Limestones,dolomites,marbles": 0,
            "Gem Stones": 0,
            "Beryllium": 0,
            "Asbestos": 0,
            "Sulphur": 0,
            "Coal": 0,
            "Chromium": 0,
            "Fluorite": 0,
            "Lazurite": 0,
            "Mica": 0,
            "Siliceous": 0,
            "Nitric": 0,
            "Bauxite": 0,
            "talc": 0,
            "Lithium": 0, }

        minerals_detail = session.query(GelogicalMineralType).filter(
            GelogicalMineralType.geom.ST_Intersects(kk.geom))

        for mineral in minerals_detail:
            mineral_types[mineral.type] = mineral_types[mineral.type] + 1

        mineralTypeKey = list(
            map(lambda mineralType_kk: mineralType_kk[0],
                filter(lambda nm_mineralType: nm_mineralType[1] != 0, mineral_types.items())))
        mineralTypeValues = list(map(lambda mineralType_kk: int(mineralType_kk[1]),
                                     filter(lambda nm_mineralType: nm_mineralType[1] != 0, mineral_types.items())))
        MineralTypeChartData.append(mineralTypeKey)
        MineralTypeChartData.append(mineralTypeValues)

        print("geological fault lines")
        # geological_fault_lines
        infographics_geological_fault_lines = []
        faultLines = {"Fault, trust, inferred": 0,
                      "Fault, normal, inferred": 0,
                      "Fault, normal, proven": 0,
                      "Fault, normal, buried": 0,
                      "Fault, trust, proven": 0}
        faultLines_detail = session.query(GelogicalFaultLine).filter(
            GelogicalFaultLine.geom.ST_Intersects(kk.geom))

        for faultlin in faultLines_detail:
            fault__line = session.query(
                (cast(func.ST_Intersection(kk.geom, faultlin.geom), Geography).ST_Length()).label('length_final'))
            faultLines[faultlin.name_type] = faultLines[faultlin.name_type] + fault__line[0][0]

        faultLinesKey = list(
            map(lambda faultLines_kk: faultLines_kk[0],
                filter(lambda nm_faultLines: round(nm_faultLines[1] / 1000, 2) != 0, faultLines.items())))
        faultLinesValues = list(map(lambda faultLines_kk: round(faultLines_kk[1] / 1000, 2),
                                    filter(lambda nm_faultLines: round(nm_faultLines[1] / 1000, 2) != 0,
                                           faultLines.items())))
        FaultLinesChartData.append(faultLinesKey)
        FaultLinesChartData.append(faultLinesValues)

        print("Quick information Macro Watershed")
        # Quick information Macro Watershed
        qiMicroLevelWatershed = session.query(HydrologicalMacroLevelWatershed).filter(
            HydrologicalMacroLevelWatershed.geom.ST_Intersects(kk.geom))
        totalarea = 0
        macroWatershed = ''
        for qi in qiMicroLevelWatershed:
            area = session.query(
                (cast(func.ST_Intersection(kk.geom, qi.geom), Geography).ST_Area()).label('area_final'))
            if area[0][0] != 0:
                totalarea = totalarea + area[0][0]
                macroWatershed = macroWatershed + '<li>' + qi.ws_name_f_ + '</li>'

        print("Quick information Major Basin")
        # Quick information Major Basin
        qiMajorBasin = session.query(HydrologicalMajorBasin).filter(HydrologicalMajorBasin.geom.ST_Intersects(kk.geom))
        majorBasin = ''
        for qi in qiMajorBasin:
            area = session.query(
                (cast(func.ST_Intersection(kk.geom, qi.geom), Geography).ST_Area()).label('area_final'))
            if round(area[0][0] / 1000000, 2) != 0:
                majorBasin = majorBasin + '<li>' + qi.mj_basin_f + '</li>'

        # Quick information District Extent
        # qiDistrict = session.query(AdminDistrictBoundry).filter(AdminDistrictBoundry.geom.ST_Intersects(kk.geom))
        # districtExt = ''
        # for qi in qiDistrict:
        #     area = session.query(
        #         (cast(func.ST_Intersection(kk.geom, qi.geom), Geography).ST_Area()).label('area_final'))
        #     if area[0][0] != 0:
        #         districtExt = districtExt + '<li>' + qi.dist_34_na + '</li>'

        print("Quick information Province Extent")
        # Quick information Province Extent
        qiProvince = session.query(AdminProvienceBoundary).filter(AdminProvienceBoundary.geom.ST_Intersects(kk.geom))
        provinceExt = ''
        for qi in qiProvince:
            area = session.query(
                (cast(func.ST_Intersection(kk.geom, qi.geom), Geography).ST_Area()).label('area_final'))
            if round(area[0][0] / 1000000, 2) != 0:
                provinceExt = provinceExt + '<li>' + qi.prov_34_na + '</li>'

        print("Quick information Village Count")
        # Quick information Village Count
        villageCount = session.query(AdminVillages45533).filter(AdminVillages45533.geom.ST_Intersects(kk.geom)).count()

        data_quick_introduction['qi_watershed'] = macroWatershed
        data_quick_introduction['qi_basin'] = majorBasin
        data_quick_introduction['qi_total_area'] = str(round(totalarea / 1000000, 2)) + ' sq.km'
        data_quick_introduction['qi_num_of_village'] = villageCount
        # data_quick_introduction['qi_district']=districtExt
        data_quick_introduction['qi_provence'] = provinceExt

        # if i == 1:
        #     break
        # i += 1

    session.close()

    allData = {}
    allData['infographics'] = infographics_all
    allData['well_depth_data'] = data_well_depth
    allData['slope_chart_data'] = SlopeChartData
    allData['aspect_chart_data'] = AspectChartdata
    allData['elevation_chart_data'] = ElevationChartData
    allData['gwdepthflow_chart_data'] = GwDepthFlowChartData
    allData['flood_chart_data'] = floodChartData
    allData['waterbodiesInfographics'] = DatawaterBodiesAndMarshland
    allData['soildepth_chart_data'] = SoilDepthChartData
    allData['soiltype_chart_data'] = SoilTypeChartData
    allData['rocktype_chart_data'] = RockTypeChartData
    allData['geologicalTemplate_chart_data'] = GeologicalTemplateChartData
    allData['mineraltype_chart_data'] = MineralTypeChartData
    allData['faultline_chart_data'] = FaultLinesChartData
    allData['quick_info_data'] = data_well_depth
    allData['qi'] = data_quick_introduction
    allData['geojson'] = GeojsonObject
    allData['extent'] = mapExtent
    allData['centroid'] = centroid
    return allData


def classifySlope_New(data):
    mappingDict = {'0-5': 0,
                   '5-10': 0,
                   '10-15': 0,
                   '15-20': 0,
                   '20-25': 0,
                   '25-30': 0,
                   '30-35': 0,
                   '35-40': 0,
                   '40-45': 0,
                   '45-50': 0,
                   '50 and Above': 0,
                   }
    slope = data.keys()
    for i in slope:
        a = float(i)
        if a >= 0 and a < 5:
            mappingDict['0-5'] = mappingDict['0-5'] + data[i]
        elif a >= 5 and a < 10:
            mappingDict['5-10'] = mappingDict['5-10'] + data[i]
        elif a >= 10 and a < 15:
            mappingDict['10-15'] = mappingDict['10-15'] + data[i]
        elif a >= 15 and a < 20:
            mappingDict['15-20'] = mappingDict['15-20'] + data[i]
        elif a >= 20 and a < 25:
            mappingDict['20-25'] = mappingDict['20-25'] + data[i]
        elif a >= 25 and a < 30:
            mappingDict['25-30'] = mappingDict['25-30'] + data[i]
        elif a >= 30 and a < 35:
            mappingDict['30-35'] = mappingDict['30-35'] + data[i]
        elif a >= 35 and a < 40:
            mappingDict['35-40'] = mappingDict['35-40'] + data[i]
        elif a >= 40 and a < 45:
            mappingDict['40-45'] = mappingDict['40-45'] + data[i]
        elif a >= 45 and a < 50:
            mappingDict['45-50'] = mappingDict['45-50'] + data[i]
        elif a >= 50:
            mappingDict['50 and Above'] = mappingDict['50 and Above'] + data[i]
    return mappingDict


def StoringStats():
    # Get connection/session to database
    engine = app.get_persistent_store_database('watershed_afganistan', as_sessionmaker=False)
    engineURL=engine.url
    NewEngine = create_engine(engineURL, poolclass=NullPool)
    session = sessionmaker(bind=NewEngine)()

    layerGroup = session.query(HydrologicalMajorBasin).all()
    for i in layerGroup:
        currentGid = i.gid
        # currentGid = 6

        print(currentGid)
        inData = {"layerName": 'basin', 'controlGid': int(currentGid)}
        data = detailDataWatershedAll_new(inData)
        print(data)
        newData = Statistic(id=currentGid, gid=currentGid, layer_name='basin', data=data)
        session.add(newData)
        session.commit()
        # break

    layerGroup = session.query(HydrologicalMacroLevelWatershed).all()
    for i in layerGroup:
        print(i.gid)
        inData = {"layerName": 'watershed', 'controlGid': int(i.gid)}
        data = detailDataWatershedAll_new(inData)
        print(data)
        newData = Statistic(id=i.gid + 6, gid=i.gid, layer_name='watershed', data=data)
        session.add(newData)
        session.commit()

    session.close()
    allData = {}
    return allData


def getStatistics(indata):
    # Get connection/session to database
    # PrintingAllMapsMain()
    engine = app.get_persistent_store_database('watershed_afganistan', as_sessionmaker=False)
    engineURL=engine.url
    NewEngine = create_engine(engineURL, poolclass=NullPool)
    session = sessionmaker(bind=NewEngine)()
    layerName = indata['layerName']
    controlGid = indata['controlGid']
    worinkgModelObjectQuery = session.query(Statistic).filter(Statistic.layer_name == layerName).filter(
        Statistic.gid == controlGid)
    allData = worinkgModelObjectQuery[0].data
    session.close()
    return allData
