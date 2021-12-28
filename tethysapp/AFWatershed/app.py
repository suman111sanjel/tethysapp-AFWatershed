from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import PersistentStoreDatabaseSetting


class AFWatershed(TethysAppBase):
    """


    Tethys app class for Watershed Afgan.


    """

    name = 'Watershed Characterization System for Afghanistan'
    index = 'AFWatershed:home'
    icon = 'AFWatershed/images/icon.gif'
    package = 'AFWatershed'
    root_url = 'AFWatershed'
    color = '#007196'
    description = 'Place a brief description of your app here.'
    tags = 'watershed'
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='AFWatershed',
                controller='AFWatershed.controllers.home.Home'
            ),
            UrlMap(
                name='Gelogical__Rock_type',
                url='AFWatershed/Gelogical--Rock-type',
                controller='AFWatershed.controllers.Geological.RockType'
            ),
            UrlMap(
                name='Gelogical__Geological_Template',
                url='AFWatershed/Gelogical--Geological-Template',
                controller='AFWatershed.controllers.Geological.GeologicalTemplate'
            ),
            UrlMap(
                name='Gelogical__Mineral_Types',
                url='AFWatershed/Gelogical--Mineral-Types',
                controller='AFWatershed.controllers.Geological.MineralTypes'
            ),
            UrlMap(
                name='Gelogical__Fault_Line',
                url='AFWatershed/Gelogical--Fault-Line',
                controller='AFWatershed.controllers.Geological.FaultLine'
            ),
            UrlMap(
                name='Hydrological__Yearly_Well_Depth_Trend',
                url='AFWatershed/Hydrological--Yearly-Well-Depth-Trend',
                controller='AFWatershed.controllers.Hydrological.YearlyWellDepthTrend'
            ), UrlMap(
                name='Hydrological__Ground_Water_Depth_Flow',
                url='AFWatershed/Hydrological--Ground-Water-Depth-Flow',
                controller='AFWatershed.controllers.Hydrological.GroundWaterDepthFlow'
            ), UrlMap(
                name='Hydrological__Flood_Risk',
                url='AFWatershed/Hydrological--Flood-Risk',
                controller='AFWatershed.controllers.Hydrological.FloodRisk'
            ), UrlMap(
                name='Hydrological__Water_Bodies',
                url='AFWatershed/Hydrological--water-bodies',
                controller='AFWatershed.controllers.Hydrological.WaterBodies'
            ), UrlMap(
                name='Hydrological__DrainageDensity',
                url='AFWatershed/Hydrological--DrainageDensity',
                controller='AFWatershed.controllers.Hydrological.DrainageDensity'
            ), UrlMap(
                name='Hydrological__GroundWaterPotentialZone',
                url='AFWatershed/Hydrological--GroundWaterPotentialZone',
                controller='AFWatershed.controllers.Hydrological.GroundWaterPotentialZone'
            ), UrlMap(
                name='Topographical__slope',
                url='AFWatershed/Topographical--slope',
                controller='AFWatershed.controllers.Topographical.Slope'
            ), UrlMap(
                name='Topographical__aspect',
                url='AFWatershed/Topographical--aspect',
                controller='AFWatershed.controllers.Topographical.Aspect'
            ), UrlMap(
                name='Topographical__Elevation',
                url='AFWatershed/Topographical--Elevation',
                controller='AFWatershed.controllers.Topographical.Elevation'
            ), UrlMap(
                name='Topographical__PlanCurvature',
                url='AFWatershed/Topographical--PlanCurvature',
                controller='AFWatershed.controllers.Topographical.PlanCurvature'
            ), UrlMap(
                name='Topographical__ProfileCurvature',
                url='AFWatershed/Topographical--ProfileCurvature',
                controller='AFWatershed.controllers.Topographical.ProfileCurvature'
            ), UrlMap(
                name='SoilParameter__SoilDepth',
                url='AFWatershed/SoilParameter--SoilDepth',
                controller='AFWatershed.controllers.SoilParameter.SoilDepth'
            ), UrlMap(
                name='SoilParameter__SoilType',
                url='AFWatershed/SoilParameter--SoilType',
                controller='AFWatershed.controllers.SoilParameter.SoilType'
            ), UrlMap(
                name='Population__PopulationDensity',
                url='AFWatershed/Population--PopulationDensity',
                controller='AFWatershed.controllers.Population.PopulationDensity'
            ), UrlMap(
                name='Population__VillageDensity',
                url='AFWatershed/Population--VillageDensity',
                controller='AFWatershed.controllers.Population.VillageDensity'
            ), UrlMap(
                name='LandCover__LandCover',
                url='AFWatershed/LandCover--LandCover',
                controller='AFWatershed.controllers.LandCover.LandCover'
            ), UrlMap(
                name='Climate__ClimateTimeSeries',
                url='AFWatershed/Climate--ClimateTimeSeries',
                controller='AFWatershed.controllers.Climate.ClimateTimeSeries'
            ), UrlMap(
                name='getgeojson',
                url='AFWatershed/getgeojson/',
                controller='AFWatershed.controllers.home.GetGeoJson'
            ), UrlMap(name='QuickIntroduction',
                url='AFWatershed/QuickIntroduction/',
                controller='AFWatershed.controllers.home.QuickIntroduction'
              ), UrlMap(name='WMSProxy',
                url='AFWatershed/WMSProxy/(?P<url>.*)',
                # url='AFWatershed/WMSProxy/',
                # url=r'AFWatershed/WMSProxy/(?P<variable_name>.*)$',
                # regex=r'^[ A-Za-z0-9_@./#&+-]*$',
                controller='AFWatershed.controllers.viewer.WMSProxy',
                # regex='variable_name'
            ),
            # re_path(r'^proxy2/(?P<url>.*)$', HttpProxy.as_view(base_url=settings.PROXY_BASE_URL))

            # commented for testing
            # UrlMap(
            #     name='watershed_detail',
            #     url='AFWatershed/watershed_detail',
            #     controller='AFWatershed.controllers.watershed_detail',
            # ),
            # UrlMap(
            #     name='watershed_detail_final',
            #     url='AFWatershed/watershed_detail_final',
            #     controller='AFWatershed.controllers.watershed_detail_final',
            # ),
            # UrlMap(
            #     name='watershed_detail_final_new',
            #     url='AFWatershed/watershed_detail_final_new',
            #     controller='AFWatershed.controllers.watershed_detail_final_new',
            # ),
        )
        return url_maps

    def persistent_store_settings(self):
        """
        Define Persistent Store Settings.
        """
        ps_settings = (
            PersistentStoreDatabaseSetting(
                name='watershed_afganistan',
                description='afgan watershed',
                initializer='AFWatershed.model.init_primary_db',
                required=True,
                spatial=True
            ),

        )
        return ps_settings

