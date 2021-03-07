import json
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


from sqlalchemy import BigInteger, Column, Date, Integer, Numeric, String, text, ForeignKey, Boolean, JSON,Text, text,Float
from geoalchemy2.types import Geometry
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

def init_primary_db(engine, first_time):
    """
    Initializer for the primary database.
    """
    
    # Create all the tables
    Base.metadata.create_all(engine)

    # Add data
    if first_time:
        # Make session
        Session = sessionmaker(bind=engine)
        session = Session()
        session.commit()
        session.close()

class InfoGraphicsReference(Base):
    __tablename__= 'infographics_reference'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    icon_html = Column(String(200), nullable=False)
    div_id = Column(String(200), nullable=False)
    order_rank = Column(Integer, nullable=False)


class InfoGraphics(Base):
    __tablename__= 'infographics'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    watershedid = Column(String(200), nullable=False)
    value =  Column(String(200), nullable=False)
    infographics_id = Column(ForeignKey('public.infographics_reference.id', deferrable=True, initially='DEFERRED'),
                                nullable=False, index=True)
    infographics=relationship('InfoGraphicsReference')


class WatershedLayergroupone(Base):
    __tablename__ = 'watershed_layergroupone'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    order = Column(Integer, nullable=False)
    htmlText = Column(String(200), nullable=False)
    htmlId = Column(String(200), nullable=False)
    is_group_layer=Column(Boolean, nullable=False)


class WatershedLayergrouptwo(Base):
    __tablename__ = 'watershed_layergrouptwo'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    order = Column(Integer)
    htmlText = Column(String(200))
    htmlId = Column(String(200))
    isLayer = Column(Boolean)
    LayerGroupOneId_id = Column(ForeignKey('public.watershed_layergroupone.id', deferrable=True, initially='DEFERRED'), index=True)
    zIndex = Column(Integer)
    defaultLayerVisibility = Column(Boolean)
    layernamegeoserver = Column(String(200))
    data_type = Column(String(200))
    wmsTileType = Column(String(200))
    mask = Column(Boolean)
    server_type = Column(String(20))
    style = Column(String(20))
    wms_url = Column(String(200))
    legend = Column(Text)
    color_scale_range = Column(String(200))
    annual_monthly = Column(String(200))
    opacity_slider = Column(Boolean)
    sld_body_thredds = Column(Text)
    tds_version = Column(Float(53))
    unit = Column(String(200))

    LayerGroupOneId = relationship('WatershedLayergroupone')


class Statistic(Base):
    __tablename__ = 'statistics'
    __table_args__ = {'schema': 'public'}

    layer_name = Column(String(50), primary_key=True, nullable=False)
    gid = Column(Integer, primary_key=True, nullable=False)
    gelogical__rock_type = Column(JSON)
    gelogical__geologica_template = Column(JSON)
    gelogical__fault_line = Column(JSON)
    gelogical__mineral_type = Column(JSON)
    hydrological_yearly_well_depth_trend = Column(JSON)
    hydrological_ground_water_depth_flow = Column(JSON)
    hydrological_flood_risk = Column(JSON)
    hydrological_water_bodies = Column(JSON)
    soil_parameters_soil_depth = Column(JSON)
    soil_parameters_soil_type = Column(JSON)
    topographical_slope_degree = Column(JSON)
    topographical_aspect = Column(JSON)
    topographical_elevation = Column(JSON)
    topographical_plan_curvature = Column(JSON)
    topographical_profile_curvature = Column(JSON)
    hydrological_ground_water_potential_zone = Column(JSON)
    hydrological_drainage_density = Column(JSON)
    population_population_density = Column(JSON)
    population_village_density = Column(JSON)
    landcover_landcover = Column(JSON)
    quick_introduction = Column(JSON)




class AdminCountryBndry(Base):
    __tablename__ = 'admin_country_bndry'
    __table_args__ = {'schema': 'gis'}

    gid = Column(Integer, primary_key=True)
    objectid_1 = Column(BigInteger)
    objectid = Column(BigInteger)
    prov_34_id = Column(BigInteger)
    prov_34_na = Column(String(50))
    area_sqkm = Column(Numeric)
    hectares = Column(Numeric)
    prov_34_n = Column(String(50))
    shape_leng = Column(Numeric)
    haj = Column(Integer)
    imsma_prov = Column(Integer)
    imsma_guid = Column(Integer)
    amac_id = Column(Integer)
    province_r = Column(String(25))
    shape_le_1 = Column(Numeric)
    shape_area = Column(Numeric)
    geom = Column(Geometry('MULTIPOLYGON', 4326), index=True)


class AdminDistrictBoundry(Base):
    __tablename__ = 'admin_district_boundry'
    __table_args__ = {'schema': 'gis'}

    gid = Column(Integer, primary_key=True)
    objectid_1 = Column(BigInteger)
    objectid_2 = Column(BigInteger)
    objectid = Column(BigInteger)
    prov_34_id = Column(BigInteger)
    prov_34_na = Column(String(20))
    dist_34_id = Column(BigInteger)
    dist_34_na = Column(String(50))
    area_sqkm = Column(Numeric)
    hectares = Column(Numeric)
    shape_leng = Column(Numeric)
    imsma_dist = Column(String(254))
    imsma_guid = Column(String(254))
    plan = Column(String(50))
    ruleid = Column(BigInteger)
    district_r = Column(String(25))
    shape_le_1 = Column(Numeric)
    shape_area = Column(Numeric)
    geom = Column(Geometry('MULTIPOLYGON', 4326), index=True)


class AdminProvienceBoundary(Base):
    __tablename__ = 'admin_provience_boundary'
    __table_args__ = {'schema': 'gis'}

    gid = Column(Integer, primary_key=True)
    objectid_1 = Column(BigInteger)
    objectid = Column(BigInteger)
    prov_34_id = Column(BigInteger)
    prov_34_na = Column(String(50))
    area_sqkm = Column(Numeric)
    hectares = Column(Numeric)
    prov_34_n = Column(String(50))
    shape_leng = Column(Numeric)
    haj = Column(Integer)
    imsma_prov = Column(Integer)
    imsma_guid = Column(Integer)
    amac_id = Column(Integer)
    province_r = Column(String(25))
    shape_le_1 = Column(Numeric)
    shape_area = Column(Numeric)
    geom = Column(Geometry('MULTIPOLYGON', 4326), index=True)


class AdminProvienceCentre(Base):
    __tablename__ = 'admin_provience_centres'
    __table_args__ = {'schema': 'gis'}

    gid = Column(Integer, primary_key=True)
    objectid = Column(BigInteger)
    geocode = Column(String(254))
    name = Column(String(80))
    lat = Column(Numeric)
    lon = Column(Numeric)
    type = Column(Numeric)
    dist_id = Column(Numeric)
    dist_nam = Column(String(254))
    prov_id = Column(Numeric)
    prov_nam = Column(String(254))
    x_coord = Column(Numeric)
    y_coord = Column(Numeric)
    prov_cente = Column(String(50))
    geom = Column(Geometry('POINT', 4326), index=True)


class AdminVillages45533(Base):
    __tablename__ = 'admin_villages_45533'
    __table_args__ = {'schema': 'gis'}

    gid = Column(Integer, primary_key=True)
    objectid = Column(BigInteger)
    serial_num = Column(Numeric)
    source = Column(String(254))
    village_na = Column(String(254))
    vil_uid = Column(String(254))
    point_y = Column(Numeric)
    point_x = Column(Numeric)
    bndsce = Column(String(254))
    dstcode = Column(String(254))
    mistidis = Column(String(254))
    provcode = Column(String(254))
    province = Column(String(254))
    rc = Column(String(254))
    wave1 = Column(String(254))
    wave1code = Column(Numeric)
    w1st_dat = Column(Date)
    w1ed_dat = Column(Date)
    wave2 = Column(String(254))
    wave2code = Column(String(254))
    w2st_dat = Column(Date)
    w2ed_dat = Column(Date)
    wave3 = Column(String(254))
    wave3code = Column(String(254))
    w3st_dat = Column(Date)
    w3ed_dat = Column(Date)
    center = Column(String(254))
    cntr_code = Column(Numeric)
    dcname = Column(String(254))
    dcdistm = Column(Numeric)
    dctypeid = Column(Numeric)
    dctype = Column(String(254))
    dclon = Column(Numeric)
    dclat = Column(Numeric)
    pcname = Column(String(254))
    pcdistm = Column(Numeric)
    pctypeid = Column(Numeric)
    pctype = Column(String(254))
    pclon = Column(Numeric)
    pclat = Column(Numeric)
    capname = Column(String(254))
    capdistm = Column(Numeric)
    compound = Column(Numeric)
    compop = Column(Numeric)
    yalepop = Column(Numeric)
    wave4 = Column(String(3))
    geom = Column(Geometry('POINT', 4326), index=True)


class FloodAllFlood(Base):
    __tablename__ = 'flood_all_flood'
    __table_args__ = {'schema': 'gis'}

    gid = Column(Integer, primary_key=True)
    objectid = Column(BigInteger)
    id = Column(Numeric)
    gridcode = Column(Numeric)
    flood = Column(String(254))
    shape_star = Column(Numeric)
    shape_stle = Column(Numeric)
    shape_leng = Column(Numeric)
    shape_le_1 = Column(Numeric)
    shape_area = Column(Numeric)
    layer = Column(String(100))
    path = Column(String(200))
    geom = Column(Geometry('MULTIPOLYGON', 4326), index=True)


class GelogicalFaultLine(Base):
    __tablename__ = 'gelogical_fault_lines'
    __table_args__ = {'schema': 'gis'}

    gid = Column(Integer, primary_key=True)
    objectid = Column(BigInteger)
    fnode_ = Column(Numeric)
    tnode_ = Column(Numeric)
    lpoly_ = Column(Numeric)
    rpoly_ = Column(Numeric)
    length = Column(Numeric)
    faults_ = Column(Numeric)
    faults_id = Column(Numeric)
    name_type = Column(String(70))
    l_code = Column(Numeric)
    shape_leng = Column(Numeric)
    geom = Column(Geometry('MULTILINESTRING', 4326), index=True)


class GelogicalGeologyStructure(Base):
    __tablename__ = 'gelogical_geology_structure'
    __table_args__ = {'schema': 'gis'}

    gid = Column(Integer, primary_key=True)
    objectid = Column(BigInteger)
    type = Column(String(50))
    conf = Column(Integer)
    shape_leng = Column(Numeric)
    shape_le_1 = Column(Numeric)
    geom = Column(Geometry('MULTILINESTRING', 4326), index=True)


class GelogicalGeologyTemplate(Base):
    __tablename__ = 'gelogical_geology_template'
    __table_args__ = {'schema': 'gis'}

    gid = Column(Integer, primary_key=True)
    objectid = Column(BigInteger)
    area = Column(Numeric)
    perimeter = Column(Numeric)
    afggeol8_ = Column(Numeric)
    afggeol8_i = Column(Numeric)
    old_geol_u = Column(String(10))
    old_geol_a = Column(String(25))
    old_geol_l = Column(String(110))
    template = Column(String(50))
    shape_leng = Column(Numeric)
    shape_area = Column(Numeric)
    geom = Column(Geometry('MULTIPOLYGON', 4326), index=True)


class GelogicalMineralType(Base):
    __tablename__ = 'gelogical_mineral_type'
    __table_args__ = {'schema': 'gis'}

    gid = Column(Integer, primary_key=True)
    objectid = Column(BigInteger)
    id = Column(BigInteger)
    type = Column(String(30))
    geom = Column(Geometry('POINT', 4326), index=True)


class GelogicalRockType(Base):
    __tablename__ = 'gelogical_rock_type'
    __table_args__ = {'schema': 'gis'}

    gid = Column(Integer, primary_key=True)
    objectid = Column(BigInteger)
    mapunit = Column(String(4))
    descrip = Column(String(70))
    shape_leng = Column(Numeric)
    shape_area = Column(Numeric)
    geom = Column(Geometry('MULTIPOLYGON', 4326), index=True)
    descrip_new = Column(String(70))


class HydrologicalAfgAllRiver(Base):
    __tablename__ = 'hydrological_afg_all_rivers'
    __table_args__ = {'schema': 'gis'}

    gid = Column(Integer, primary_key=True)
    objectid = Column(BigInteger)
    name = Column(String(24))
    class_ = Column('class', Integer)
    river_type = Column(String(50))
    shape_leng = Column(Numeric)
    geom = Column(Geometry('MULTILINESTRING', 4326), index=True)


class HydrologicalGwDepthFlow2010(Base):
    __tablename__ = 'hydrological_gw_depth_flow_2010'
    __table_args__ = {'schema': 'gis'}

    gid = Column(Integer, primary_key=True)
    objectid = Column(BigInteger)
    area = Column(Numeric)
    perimeter = Column(Numeric)
    mapunit = Column(String(4))
    descrip1 = Column(String(35))
    descrip2 = Column(String(110))
    quantmin = Column(String(20))
    quantmax = Column(String(20))
    depthmax = Column(BigInteger)
    shape_leng = Column(Numeric)
    shape_area = Column(Numeric)
    geom = Column(Geometry('MULTIPOLYGON', 4326), index=True)


class HydrologicalLake(Base):
    __tablename__ = 'hydrological_lakes'
    __table_args__ = {'schema': 'gis'}

    gid = Column(Integer, primary_key=True)
    objectid = Column(BigInteger)
    id_ = Column(String(16))
    name1_ = Column(String(64))
    name2_ = Column(String(64))
    parts_ = Column(Integer)
    points_ = Column(BigInteger)
    length_ = Column(Numeric)
    area_ = Column(Numeric)
    shape_leng = Column(Numeric)
    shape_area = Column(Numeric)
    geom = Column(Geometry('MULTIPOLYGON', 4326), index=True)


class HydrologicalMacroLevelWatershed(Base):
    __tablename__ = 'hydrological_macro_level_watershed'
    __table_args__ = {'schema': 'gis'}

    gid = Column(Integer, primary_key=True)
    objectid = Column(BigInteger)
    mj_basin__ = Column(String(40))
    ws_name_f_ = Column(String(50))
    area = Column(Numeric)
    hectares = Column(Numeric)
    sq_km = Column(Numeric)
    perimeter = Column(Numeric)
    basin_name = Column(String(25))
    shape_leng = Column(Numeric)
    shape_area = Column(Numeric)
    z_min = Column(Numeric)
    z_max = Column(Numeric)
    sarea = Column(Numeric)
    min_slope = Column(Numeric)
    max_slope = Column(Numeric)
    geom = Column(Geometry('MULTIPOLYGON', 4326), index=True)


class HydrologicalMajorBasin(Base):
    __tablename__ = 'hydrological_major_basin'
    __table_args__ = {'schema': 'gis'}

    gid = Column(Integer, primary_key=True)
    objectid = Column(BigInteger)
    mj_basin_f = Column(String(40))
    count = Column(Numeric)
    first_rvrn = Column(String(50))
    last_rvrna = Column(String(50))
    first_basi = Column(String(40))
    last_basin = Column(String(40))
    count_basi = Column(String(40))
    first_majb = Column(String(25))
    last_majba = Column(String(25))
    count_majb = Column(String(25))
    area = Column(BigInteger)
    shape_leng = Column(Numeric)
    shape_area = Column(Numeric)
    geom = Column(Geometry('MULTIPOLYGON', 4326), index=True)


class HydrologicalMarshland(Base):
    __tablename__ = 'hydrological_marshland'
    __table_args__ = {'schema': 'gis'}

    gid = Column(Integer, primary_key=True)
    objectid = Column(BigInteger)
    lccsuslb = Column(String(50))
    dist_name = Column(String(50))
    prov_name = Column(String(50))
    shape_leng = Column(Numeric)
    shape_area = Column(Numeric)
    lc_class = Column(String(50))
    geom = Column(Geometry('MULTIPOLYGON', 4326), index=True)


class HydrologicalRiversRegion(Base):
    __tablename__ = 'hydrological_rivers_region'
    __table_args__ = {'schema': 'gis'}

    gid = Column(Integer, primary_key=True)
    objectid = Column(BigInteger)
    id_ = Column(String(16))
    name1_ = Column(String(64))
    name2_ = Column(String(64))
    parts_ = Column(Integer)
    points_ = Column(BigInteger)
    length_ = Column(Numeric)
    area_ = Column(Numeric)
    class_ = Column('class', Integer)
    name_river = Column(String(25))
    shape_leng = Column(Numeric)
    shape_area = Column(Numeric)
    geom = Column(Geometry('MULTIPOLYGON', 4326), index=True)


class HydrologicalWellsDepth(Base):
    __tablename__ = 'hydrological_wells_depth'
    __table_args__ = {'schema': 'gis'}

    gid = Column(Integer, primary_key=True)
    objectid = Column(BigInteger)
    rowid_ = Column(BigInteger)
    code = Column(String(10))
    type = Column(String(11))
    agency = Column(String(14))
    donor = Column(String(11))
    province = Column(String(13))
    district = Column(String(18))
    village = Column(String(19))
    longitude = Column(Numeric)
    latitude = Column(Numeric)
    year = Column(BigInteger)
    month = Column(BigInteger)
    day = Column(BigInteger)
    public = Column(String(1))
    trad_impr = Column(String(1))
    well_depth = Column(Numeric)
    swl = Column(Numeric)
    well_dia = Column(Numeric)
    pump_depth = Column(Numeric)
    casing_dia = Column(Numeric)
    casing_ty = Column(String(30))
    filter_lgh = Column(Numeric)
    casing_lgh = Column(Numeric)
    pump_code = Column(String(50))
    pump_manuf = Column(String(30))
    pump_type = Column(String(30))
    pump_pwr = Column(String(5))
    wp_status = Column(String(30))
    pmp_status = Column(String(30))
    hit_ec = Column(BigInteger)
    location = Column(String(30))
    elder = Column(String(50))
    mechanic = Column(String(50))
    benef_hh = Column(BigInteger)
    hyg_edu_hh = Column(BigInteger)
    latrine_no = Column(BigInteger)
    baths_no = Column(BigInteger)
    sps_villg = Column(String(50))
    team_code = Column(String(6))
    wq_avail = Column(String(1))
    dlog_avail = Column(String(1))
    ptst_avail = Column(String(1))
    prov_id = Column(BigInteger)
    dist_id = Column(BigInteger)
    villg_id = Column(String(13))
    geom = Column(Geometry('POINT', 4326), index=True)


class SoilParametersSoilsDepth(Base):
    __tablename__ = 'soil_parameters_soils_depth'
    __table_args__ = {'schema': 'gis'}

    gid = Column(Integer, primary_key=True)
    objectid = Column(BigInteger)
    area = Column(Numeric)
    perimeter = Column(Numeric)
    soil_unit = Column(String(10))
    depth = Column(String(30))
    linkfile = Column(String(30))
    area_sqkm = Column(Numeric)
    shape_leng = Column(Numeric)
    shape_area = Column(Numeric)
    geom = Column(Geometry('MULTIPOLYGON', 4326), index=True)


class SoilParametersSoilsType(Base):
    __tablename__ = 'soil_parameters_soils_types'
    __table_args__ = {'schema': 'gis'}

    gid = Column(Integer, primary_key=True)
    objectid = Column(BigInteger)
    area = Column(Numeric)
    perimeter = Column(Numeric)
    soil_unit = Column(String(10))
    soiltype = Column(String(110))
    linkfile = Column(String(30))
    shape_leng = Column(Numeric)
    shape_area = Column(Numeric)
    area_sqkm = Column(Numeric)
    geom = Column(Geometry('MULTIPOLYGON', 4326), index=True)

