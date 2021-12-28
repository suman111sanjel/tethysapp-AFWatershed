var myApp = {};
var aoiInitilization = true
let initialLayerStartIntervalCAMPM25;
myApp.AllBindedLayersList = [];
var legendInfos = [];
myApp.LegendUIList = []
// let legendInfos = [];
var currentSelectedLocation = {
    "layerName": "",
    "controlGid": "",
}
// let threddDataSource = 'http://tethys.icimod.org:7000/thredds/'
// let threddDataSource = 'http://192.168.11.242:8081/thredds/'
// let threddDataSource = 'http://192.168.11.242:8082/thredds/'
// let threddDataSource = 'http://192.168.11.242:8888/thredds/'
// let threddDataSource = 'http://110.34.30.197:8080/thredds/'

// let datasource = 'http://192.168.11.242:8888/geoserver/AirPollutionWatch/wms';
// let LegendSource = 'http://192.168.11.242:8888/geoserver/AirPollutionWatch/wms?Service=WMS&REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&LEGEND_OPTIONS=forceLabels:off&LAYER='

var PROXY_PREFIX = '/apps/AFWatershed/WMSProxy/';
var address = PROXY_PREFIX+"http://110.34.30.197:8080/geoserver/AfghanistanWatershed/wms?Service=WMS&REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=14&HEIGHT=14&LEGEND_OPTIONS=forceLabels:on&LAYER=";

var datasource = 'http://110.34.30.197:8080/geoserver/AfghanistanWatershed/wms';

myApp.INDICES = [
    ["PM", "PM", "Pollutant"],
    ["PM1", "PM Satellite"],
    ["PM2", "PM Model"],
    ["PM3", "PM Observation"],
    ["ozone", "Ozone", "Pollutant"],
    ["ozone1", "Ozone Satellite"],
    ["ozone2", "Ozone Model"],
    ["ozone3", "Ozone Observation"],
    ["SO2", "SO2", "Pollutant"],
    ["SO21", "SO2 Satellite"],
    ["SO22", "SO2 Model"],
    ["SO23", "SO2 Observation"],
    ["NOX", "NOX", "Pollutant"],
    ["NOX1", "NOX Satellite"],
    ["NOX2", "NOX Model"],
    ["NOX3", "NOX Observation"],
    ["CO", "CO", "Pollutant"],
    ["CO1", "CO Satellite"],
    ["CO2", "CO Model"],
    ["CO3", "CO Observation"],
];

myApp.constants = {
    recent: {
        layerId: {
            TerraModisTrueColor: 'recent__TerraModisTrueColor',
            PM_AeronetAOD: 'recent__aeronet',
            PM_usembassy: 'recent__usembassy',
            GEOS_PM2p5: 'recent__GEOS_PM2p5',
            TerraModisAOD: 'recent__TerraModisAOD'
        }
    },
    archive: {
        layerId: {
            TerraModisTrueColor: 'archive__TerraModisTrueColor',
            GEOS_PM2p5: 'archive__GEOS_PM2p5',
            TerraModisAOD: 'archive__TerraModisAOD'
        }
    },
}

myApp.treeSelect = {
    mainTitle: 'Pollutants',
    datatree: [{
        title: 'PM',
        value: 1,
        child: [
            {
                title: 'AERONET AOD',
                value: 11,
                layerId: myApp.constants.recent.layerId.PM_AeronetAOD,
                otherval: "test",
                child: []
            },
            {
                title: 'US Embassy PM2.5',
                layerId: myApp.constants.recent.layerId.PM_usembassy,
                value: 12,
                child: []
            },
            {
                title: 'GEOS PM2.5',
                layerId: myApp.constants.recent.layerId.GEOS_PM2p5,
                value: 13,
                child: []
            },
            {
                title: 'TerraModis-AOD',
                layerId: myApp.constants.recent.layerId.TerraModisAOD,
                value: 14,
                child: []
            }
        ]
    }, {
        title: 'Ozone',
        value: 2,
        child: [
            {
                title: 'Ozone 1',
                value: 21,
                child: []
            },
            {
                title: 'Ozone 2',
                value: 22,
                child: []
            },
            {
                title: 'Ozone 3',
                value: 23,
                child: []
            }
        ]
    },
        {
            title: 'SO2',
            value: 3,
            child: [
                {
                    title: 'SO2 1',
                    value: 31,
                    child: []
                },
                {
                    title: 'SO2 2',
                    value: 32,
                    child: []
                },
                {
                    title: 'SO2 3',
                    value: 33,
                    child: []
                }
            ]
        },
        {
            title: 'NOX',
            value: 4,
            child: [
                {
                    title: 'NOX 1',
                    value: 41,
                    child: []
                },
                {
                    title: 'NOX 2',
                    value: 42,
                    child: []
                },
                {
                    title: 'NOX 3',
                    value: 43,
                    child: []
                }
            ]
        },
        {
            title: 'CO',
            value: 5,
            child: [
                {
                    title: 'CO 1',
                    value: 51,
                    child: []
                },
                {
                    title: 'CO 2',
                    value: 52,
                    child: []
                },
                {
                    title: 'CO 3',
                    value: 53,
                    child: []
                }
            ]
        }],
    onOpen: function () {
    },
    OnSelect: function (selected) {
        let data_period = $('#selectl1').val()
        let oldVal = this.CurrentValue;
        let newVal = selected;

        myApp.selectChangeOld(oldVal.value, this.CurrentIndex);

        if (newVal.value === 11) {
            myApp.selectChangeNewValueCompute(myApp.constants.recent.layerId.PM_AeronetAOD, myApp.AeronetAODStyleFun, '11', 'Please Select AERONET AOD Station on map');
        }
        if (newVal.value === 12) {
            myApp.selectChangeNewValueCompute(myApp.constants.recent.layerId.PM_usembassy, myApp.USEmbassyPM25StyleFun, '12', 'Please Select US Embassy 2.5 Station on map');
        }
        if (newVal.value === 13) {
            myApp.selectChangeNewValueComputeTimeSeries2D(myApp.constants.recent.layerId.GEOS_PM2p5, 13, this.CurrentIndex);
        }
        if (newVal.value === 14) {
            myApp.selectChangeNewValueComputeTimeSeries2D(myApp.constants.recent.layerId.TerraModisAOD, 14, this.CurrentIndex);
        }


        this.CurrentValue = selected;
    },
    OnChange: function (oldVal, newVal) {

    },
    onClose: function () {
    },

};

myApp.APICollection = {
    api: {
        GetGeojson: '/apps/AFWatershed/getgeojson/',
        QuickIntroduction: '/apps/AFWatershed/QuickIntroduction/',
    },
    chartAPI: {
        Gelogical__Rock_Type: '/apps/AFWatershed/Gelogical--Rock-type/',
        Gelogical__Geological_Template: '/apps/AFWatershed/Gelogical--Geological-Template/',
        Gelogical__Mineral_Types: '/apps/AFWatershed/Gelogical--Mineral-Types/',
        Gelogical__Fault_Line: '/apps/AFWatershed/Gelogical--Fault-Line/',
        Hydrological__Yearly_Well_Depth_Trend: '/apps/AFWatershed/Hydrological--Yearly-Well-Depth-Trend/',
        Hydrological__Ground_Water_Depth_Flow: '/apps/AFWatershed/Hydrological--Ground-Water-Depth-Flow/',
        Hydrological__Hydrological__Flood_Risk: '/apps/AFWatershed/Hydrological--Flood-Risk/',
        Hydrological__Hydrological__water_bodies: '/apps/AFWatershed/Hydrological--water-bodies/',
        Hydrological__DrainageDensity: '/apps/AFWatershed/Hydrological--DrainageDensity/',
        Hydrological__GroundWaterPotentialZone: '/apps/AFWatershed/Hydrological--GroundWaterPotentialZone/',
        Topographical__slope: '/apps/AFWatershed/Topographical--slope/',
        Topographical__aspect: '/apps/AFWatershed/Topographical--aspect/',
        Topographical__Elevation: '/apps/AFWatershed/Topographical--Elevation/',
        Topographical__PlanCurvature: '/apps/AFWatershed/Topographical--PlanCurvature/',
        Topographical__ProfileCurvature: '/apps/AFWatershed/Topographical--ProfileCurvature/',
        SoilParameter__SoilDepth: '/apps/AFWatershed/SoilParameter--SoilDepth/',
        SoilParameter__SoilType: '/apps/AFWatershed/SoilParameter--SoilType/',
        Population__PopulationDensity: '/apps/AFWatershed/Population--PopulationDensity/',
        Population__VillageDensity: '/apps/AFWatershed/Population--VillageDensity/',
        LandCover__LandCover: '/apps/AFWatershed/LandCover--LandCover/',
        Climate__ClimateTimeSeries: '/apps/AFWatershed/Climate--ClimateTimeSeries/',
    }
};

myApp.LoadDefaults = function () {
    myApp.DefaultINDICES = ["PM", "ozone", "SO2", "NOX"];
};

// myApp.IndexColors = ['#53A9EB', '#F5D657', '#F06368', '#52AE9A'];
myApp.IndexColors = ['#0C6CE9', '#962422', '#1D5430', '#F76743'];
myApp.OnlyOnce = true;

myApp.layerswitcher = function () {
    let olOverlaycontainer = document.querySelector('div.ol-overlaycontainer-stopevent');


    myApp.LayerSwitcherButton = myApp.createDiv('ol-unselectable ol-control');
    myApp.LayerSwitcherButton.setAttribute("id", "layer-switcher");
    let button = myApp.createButton();
    button.setAttribute("type", "button");
    button.setAttribute("title", "Layers");
    let img = myApp.createImg();
    img.setAttribute("src", "/static/AFWatershed/images/layers.svg");
    img.setAttribute("style", "height: 20px; width: 20px;");

    button.append(img);
    myApp.LayerSwitcherButton.append(button);

    olOverlaycontainer.append(myApp.LayerSwitcherButton)


    myApp.layerSwitcherDiv = myApp.createDiv()
    myApp.layerSwitcherDiv.setAttribute('id', 'layer');

    //base map start
    let upperDiv = myApp.createDiv();
    let headingBaseMap = myApp.createH('6', 'centering font-weight-bold');
    headingBaseMap.innerText = 'Base Maps';

    let RadioDiv1 = myApp.InlineRadio("inlineRadio1", "inLineRadioBaseMap", "None", false, "none");
    let RadioDiv2 = myApp.InlineRadio("inlineRadio2", "inLineRadioBaseMap", "OSM", true, 'osm');

    upperDiv.append(headingBaseMap);
    upperDiv.append(RadioDiv1);
    upperDiv.append(RadioDiv2);

    //base map end


    let lowerDiv = myApp.createDiv("layerSwitcherLowerdiv");

    let OtherLayersH4 = myApp.createH(6, 'centering font-weight-bold');
    OtherLayersH4.innerText = 'Layers';
    let layerCollectionDiv = myApp.createDiv("layerCollection");


    lowerDiv.append(OtherLayersH4);
    lowerDiv.append(layerCollectionDiv);
    myApp.layerSwitcherDiv.append(upperDiv);
    // myApp.layerSwitcherDiv.append(lowerDiv);
    olOverlaycontainer.append(myApp.layerSwitcherDiv)


    $('#satellite-Slider').slider({
        tooltip: 'always', step: 1, min: 0, max: 100,
        formatter: function (value) {
            return value + " %";
        }
    });
};

myApp.DrawUI = function () {

    let DrawSection = myApp.createDiv('draw-section');
    DrawSection.setAttribute("id", "draw-section");
    // let DrawPannel = myApp.createDiv('draw-pannel');
    let polygonAnchor = myApp.createA('ol-draw-polygon');
    polygonAnchor.setAttribute("title", "Draw a polygon");
    let pointAnchor = myApp.createA('ol-draw-point');
    pointAnchor.setAttribute("title", "Draw a point");

    // DrawPannel.append(polygonAnchor);
    // DrawPannel.append(pointAnchor);

    DrawSection.append(polygonAnchor)

    let olOverlaycontainer = document.querySelector('div.ol-overlaycontainer-stopevent');
    olOverlaycontainer.append(DrawSection);

    let deleteFeature = myApp.createDiv('clear-features');
    let deleteFeaturePannel = myApp.createDiv('clear-feature');
    let clearFeatureAnchor = myApp.createA('clear-layer');
    clearFeatureAnchor.setAttribute("title", "Clear AOI");
    deleteFeaturePannel.append(clearFeatureAnchor);
    deleteFeature.append(deleteFeaturePannel);
    olOverlaycontainer.append(deleteFeature);

    this.PrintMap = myApp.createDiv('map-print');
    let PrintMapPannel = myApp.createDiv('map-print-div');
    let printMapAnchor = myApp.createI('map-print-anchor');
    printMapAnchor.setAttribute("title", "Print Map");
    let PrintIcon = myApp.createI('fa fa-print')
    printMapAnchor.append(PrintIcon);
    PrintMapPannel.append(printMapAnchor);
    this.PrintMap.append(PrintMapPannel);
    olOverlaycontainer.append(this.PrintMap);


    polygonAnchor.addEventListener("click", () => {
        console.log("polygon");
        myApp.map.removeInteraction(myApp.drawPoint);
        myApp.map.addInteraction(myApp.drawPolygon);
    }, true);

    // pointAnchor.addEventListener("click", () => {
    //     myApp.map.removeInteraction(myApp.drawPolygon);
    //     myApp.map.addInteraction(myApp.drawPoint);
    // }, true);

    clearFeatureAnchor.addEventListener("click", () => {
        // myApp.map.removeInteraction(myApp.drawPolygon);
        // myApp.map.addInteraction(myApp.drawPoint);
        myApp.map.removeInteraction(myApp.drawPolygon);
        myApp.map.removeInteraction(myApp.drawPoint);
        myApp.Drawsource.clear();

        console.log("point");
        // myApp.revertAbout();
    }, true);
}
myApp.CreateAccordianCardsLayerGrouups = function () {
    let accordianOuterDiv = document.querySelector('#layerAccordian-outer');

    layerDetail.forEach(function (arrayItem, outerIndex) {
        let currentCartBodyId = arrayItem.htmlid + "__body"
        let cardDiv = myApp.AccordianCard(arrayItem.htmlid, arrayItem.name, "layerAccordian-outer");
        accordianOuterDiv.append(cardDiv);
        arrayItem.layers.forEach(function (layerArray, layerindex) {
            layerDetail[outerIndex].layers[layerindex].currentCartBodyId = currentCartBodyId;
            if (layerArray.isLayer) {
                if (layerArray.server_type === "geoserver") {
                    var layvisibility = false;
                    if (layerArray.layervisibility) {
                        var layvisibility = true;
                    }
                    var newLayer;
                    if (layerArray.data_type == 'raster') {

                        if (layerArray.wmsTileType == 'TileWMS') {
                            newLayer = new ol.layer.Tile({
                                id: layerArray.htmlid,
                                title: layerArray.htmltext,
                                visible: layvisibility,
                                legendPath: address + layerArray.layernamegeoserver,
                                source: new ol.source.TileWMS({
                                    url: datasource,
                                    hidpi: false,
                                    params: {
                                        'VERSION': '1.1.1',
                                        'LAYERS': layerArray.layernamegeoserver,
                                    },
                                    serverType: 'geoserver'
                                }),
                                changeWMSProxy:true,
                                mask:layerArray.mask,
                            });
                        } else {
                            newLayer = new ol.layer.Image({
                                id: layerArray.htmlid,
                                title: layerArray.htmltext,
                                visible: layvisibility,
                                legendPath: address + layerArray.layernamegeoserver,
                                source: new ol.source.ImageWMS({
                                    url: datasource,
                                    hidpi: false,
                                    params: {
                                        'VERSION': '1.1.1',
                                        'LAYERS': layerArray.layernamegeoserver,
                                    },
                                    serverType: 'geoserver'
                                }),
                                changeWMSProxy:true,
                                mask:layerArray.mask,
                            });
                        }
                        newLayer.setZIndex(layerArray.zindex);
                    }
                    myApp.map.addLayer(newLayer);
                    let l8 = new layerCheckBoxBinding("#" + layerArray.currentCartBodyId, newLayer, false, true);
                    myApp.AllBindedLayersList.push(l8)
                } else {
                    var layvisibility = false;
                    if (layerArray.layervisibility) {
                        var layvisibility = true;
                    }

                    if (layerArray.annual_monthly == 'annual') {
                        var tt2 = new ol.layer.TimeDimensionTile({
                            id: layerArray.htmlid,
                            title: layerArray.htmltext,
                            visible: layvisibility,
                            opacity: 0.7,
                            legendPath: PROXY_PREFIX+layerArray.legend,
                            showlegend: false,
                            ThreddsDataServerVersion: "5",
                            alignTimeSlider: 'left',
                            timeSliderSize: 'small',
                            aoi: true,
                            chartDivId: layerArray.htmlid,
                            ChartTitle: layerArray.htmltext,
                            DataInterval: layerArray.annual_monthly,
                            unit: layerArray.unit,
                            zIndex: layerArray.zindex,
                            source: {
                                url: layerArray.wms_url,
                                params: {
                                    'VERSION': '1.1.1',
                                    'LAYERS': layerArray.layernamegeoserver,
                                    // 'styles': layerArray.style,
                                    'SLD_BODY': layerArray.sld_body_thredds
                                    // 'SLD_BODY': '<?xml version="1.0" encoding="ISO-8859-1"?><StyledLayerDescriptor version="1.1.0" xsi:schemaLocation="http://www.opengis.net/sldStyledLayerDescriptor.xsd" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:se="http://www.opengis.net/se" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><NamedLayer>     <se:Name>Annual_LST_MODIS</se:Name>     <UserStyle>     <se:Name>Thesholded colour scheme</se:Name>     <se:CoverageStyle>     <se:Rule>     <se:RasterSymbolizer>     <se:Opacity>1.0</se:Opacity>     <se:ColorMap>     <se:Categorize fallbackValue="#00000000">     <se:LookupValue>Rasterdata</se:LookupValue>     <se:Value>#ff0000</se:Value>     <se:Threshold>15</se:Threshold>     <se:Value>#fb8005</se:Value>     <se:Threshold>20</se:Threshold>     <se:Value>#feff01</se:Value>     <se:Threshold>25</se:Threshold>     <se:Value>#8ecd0b</se:Value>     <se:Threshold>30</se:Threshold>     <se:Value>#34a803</se:Value>     <se:Threshold>33</se:Threshold>     <se:Value>#34a803</se:Value> </se:Categorize> </se:ColorMap> </se:RasterSymbolizer> </se:Rule> </se:CoverageStyle> </UserStyle> </NamedLayer></StyledLayerDescriptor>'
                                }
                            },
                            changeWMSProxy:true,
                            mask:layerArray.mask,
                        });

                        tt2.init().then(function (val) {
                            myApp.map.addThreddsLayer(val);
                            let l5 = new layerCheckBoxBinding("#" + layerArray.currentCartBodyId, tt2, true, true, 'withOpacSlider');
                            l5.setVisible(false);
                            myApp.AllBindedLayersList.push(l5)
                        }, (error) => console.error(error));
                    } else {
                        var layvisibility = false;
                        if (layerArray.layervisibility) {
                            var layvisibility = true;
                        }
                        MuntipleYearsLayer(layerArray.wms_url, layerArray.layernamegeoserver, layerArray.htmltext, layerArray.legend, layvisibility, layerArray.style, layerArray.color_scale_range, layerArray.zindex, layerArray.currentCartBodyId, layerArray.sld_body_thredds, layerArray.htmlid, layerArray.annual_monthly, layerArray.unit, layerArray.mask)
                        console.log(layerArray)
                    }
                }
            }
        });
    });
    console.log(layerDetail);
}

myApp.addingLayersToMap = async function () {

    // myApp.Drawsource = new ol.source.Vector({wrapX: false});
    let drawStyle = new ol.style.Style({
        image: new ol.style.Icon({
            src: '/static/AFWatershed/images/location-icon.png',
            // fill: new ol.style.Fill({color: '#53A9EB'}),
            // stroke: new ol.style.Stroke({color: 'white', width: 1}),
            rotateWithView: true,
            anchor: [.5, 0.90],
            anchorXUnits: 'fraction', anchorYUnits: 'fraction',
            opacity: 1
        })
    });

    myApp.DrawPolygonLayer = new ol.layer.Vector({
        id: 'DrawPolygonLayer',
        title: 'DrawPolygonLayer',
        source: myApp.Drawsource,
        style: new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: '#000000',
                width: 2
            }),
            fill: new ol.style.Fill({
                color: [255, 0, 0, 0]
                // color:'#1abc9c00'
            })
        }),
        zIndex: 99
    });
    myApp.map.addLayer(myApp.DrawPolygonLayer);


    myApp.drawPoint = new ol.interaction.Draw({
        source: myApp.Drawsource,
        type: 'Point',
        style: drawStyle
    });
    myApp.drawPoint.on('drawend', function (e) {
        myApp.PointDrawEventObjet = e;
        let lastFeature = e.feature;
        var co = lastFeature.getGeometry().getCoordinates();
        var format = new ol.format.WKT();
        point = format.writeGeometry(lastFeature.getGeometry());
        myApp.map.removeInteraction(myApp.drawPoint);
        myApp.pointPixel = myApp.map.getPixelFromCoordinate(co);
        myApp.PointCoordinate = co;
        var coordinate = co;

        setTimeout(async function () {
            myApp.Drawsource.clear();
            // try {
            //
            //     var Layers = myApp.map.forEachLayerAtPixel(myApp.pointPixel,
            //         function (layer) {
            //             return layer;
            //         });
            //
            //     let selectedLayeris = myApp.getUpperLayer();
            //
            //     console.log("Layers");
            //     console.log(Layers);
            //     var source = Layers.getProperties().source;
            //     // myApp.map.fore
            //     let Properties = Layers.getProperties();
            //     console.log("Properties");
            //     console.log(Properties);
            //     var params = {
            //         // REQUEST: "GetFeatureInfo",
            //         // BBOX: myApp.map.getView().calculateExtent().toString(),
            //         // X: myApp.pointPixel[0],
            //         // Y: myApp.pointPixel[1],
            //         INFO_FORMAT: 'text/xml',
            //         QUERY_LAYERS: source.getParams().LAYERS,
            //         // WIDTH: myApp.map.getSize()[0],
            //         // HEIGHT: myApp.map.getSize()[1],
            //         // LAYERS: source.getParams().LAYERS,
            //         TIME: source.getParams().TIME,
            //         // SERVICE: 'WMS',
            //         // VERSION: '1.1.1'
            //     };
            //
            //     var view = myApp.map.getView();
            //     var viewResolution = view.getResolution();
            //     var url = source.getFeatureInfoUrl(
            //         myApp.PointCoordinate, viewResolution, view.getProjection().code_,
            //         params);
            //
            //     if (Properties.timeSeries) {
            //
            //     } else {
            //         let xmlResponse = await myApp.makeRequest('GET', url);
            //         let parser = new DOMParser();
            //         let xmlDoc = parser.parseFromString(xmlResponse, "text/xml");
            //         let ValueTag = xmlDoc.getElementsByTagName("value")[0]
            //         let valueString = ValueTag.textContent.trim();
            //         console.log(valueString);
            //         let aaa = parseFloat(valueString).toFixed(2)
            //         let bbb = parseFloat(valueString) * 1000000;
            //         console.log(valueString);
            //         console.log(aaa);
            //         console.log(bbb);
            //         if (aoiInitilization === true) {
            //             $("#about-aoi").html("Area Of Interest (AOI)");
            //             $("#about-aoi-body").html('<div class="parent-block-query full-height full-width"><h6>Data Layer: ' + Properties.title + '</h6><h6 class="child-query-value"><strong>Value:</strong> ' + aaa + ' ' + Properties.unit + '</h6></div>');
            //         }
            //     }
            //
            //
            // } catch (err) {
            //
            //     console.log("some error");
            //
            // }
            let selectedLayeris = myApp.getUpperLayer();

            if (selectedLayeris) {
                let layer = selectedLayeris.getLayer();
                let SourceParam = null;
                let SourceURL = null;
                let layerProperties = null;

                if (layer.getProperties().hasOwnProperty('ThreddsDataServerVersion')) {
                    layerProperties = layer.getCurrentLayer().getProperties();
                    SourceParam = layer.getCurrentLayer().getProperties().source.getParams();
                    SourceURL = layer.getCurrentLayer().getProperties().source.getUrls()[0].split('wms')[1];
                } else {
                    layerProperties = layer.getProperties();
                    SourceParam = layer.source.getParams();
                    SourceURL = layer.source.getUrls()[0].split('wms')[1];
                }

                var params = {
                    // REQUEST: "GetFeatureInfo",
                    // BBOX: myApp.map.getView().calculateExtent().toString(),
                    // X: myApp.pointPixel[0],
                    // Y: myApp.pointPixel[1],
                    INFO_FORMAT: 'text/xml',
                    QUERY_LAYERS: SourceParam.LAYERS,
                    // WIDTH: myApp.map.getSize()[0],
                    // HEIGHT: myApp.map.getSize()[1],
                    // LAYERS: source.getParams().LAYERS,
                    TIME: SourceParam.TIME,
                    // SERVICE: 'WMS',
                    // VERSION: '1.1.1'
                };

                var view = myApp.map.getView();
                var viewResolution = view.getResolution();
                var url = layerProperties.source.getFeatureInfoUrl(
                    myApp.PointCoordinate, viewResolution, view.getProjection().code_,
                    params);

                if (layerProperties.timeSeries) {

                } else  {
                    let xmlResponse = await myApp.makeRequest('GET', url);
                    let parser = new DOMParser();
                    let xmlDoc = parser.parseFromString(xmlResponse, "text/xml");
                    let ValueTag = xmlDoc.getElementsByTagName("value")[0]
                    let valueString = ValueTag.textContent.trim();
                    console.log(valueString);
                    let aaa = parseFloat(valueString).toFixed(2)
                    let bbb = parseFloat(valueString) * 1000000;
                    console.log(valueString);
                    console.log(aaa);
                    console.log(bbb);
                    if (aoiInitilization === true) {
                        $("#about-aoi").html("Area Of Interest (AOI)");
                        $("#about-aoi-body").html('<div class="parent-block-query full-height full-width"><h6>Data Layer: ' + layerProperties.title + '</h6><h6 class="child-query-value"><strong>Value:</strong> ' + aaa + ' ' + layerProperties.unit + '</h6></div>');
                    }
                }


            } else {
                // console.log("There is no any layer ");
                myApp.notify('Warning ! Please add a layer first');
                myApp.revertAbout();
            }
        }, 60);
        setTimeout(function () {
            myApp.Drawsource.clear();
        }, 30);


    });
    myApp.drawPoint.on('drawstart', function (e) {
        myApp.Drawsource.clear();
    });

    myApp.drawPolygon = new ol.interaction.Draw({
        freehandCondition: ol.events.condition.never,
        source: myApp.Drawsource,
        type: 'Polygon',
    });

    myApp.drawPolygon.on('drawend', function (e) {
        myApp.PolygonEventFeature = e.feature;
        setTimeout(async function () {
            // myApp.Drawsource.clear();
            myApp.PolygonDrawOpereation();
        }, 100);

        console.log("below settimeout")
        myApp.map.removeInteraction(myApp.drawPolygon);
    });

    myApp.PolygonDrawOpereation = function () {

        setTimeout(async function () {
            var format = new ol.format.WKT();
            // let wktPolygon = format.writeGeometry(myApp.PolygonEventFeature.getGeometry(), {
            //     featureProjection: 'EPSG:3857',
            //     dataProjection: 'EPSG:4326'
            // });
            let wktPolygon = format.writeGeometry(myApp.PolygonEventFeature.getGeometry());
            currentSelectedLocation['is_wkt'] = true;
            currentSelectedLocation['wkt'] = wktPolygon;
            myApp.getRelatedData(false);
        }, 100);

    }


    myApp.drawPolygon.on('drawstart', function (e) {
        myApp.Drawsource.clear();
    });


    myApp.HighLightedLayer = new ol.layer.Vector({
        id: "highlightedlayer",
        title: "highlightedlayer",
        style: new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: '#000000',
                width: 2
            }),
            fill: new ol.style.Fill({
                color: [255, 0, 0, 0]
                // color:'#1abc9c00'
            })
        }),
        legendPath: address + 'watershed:admin_country_bndry&styles=watershed:Selected_Basin_watershed',
        source: myApp.Drawsource,
        mask: 0,
        changeWMSProxy:false
    });

    myApp.HighLightedLayer.setZIndex(300);
    myApp.map.addLayer(myApp.HighLightedLayer);
    myApp.AllBindedLayersList.push(myApp.HighLightedLayer);

};


myApp.BindControls = function () {

    myApp.LayerSwitcherButton.addEventListener("click", () => {
        if (getComputedStyle(myApp.layerSwitcherDiv)["display"] === "block") {
            myApp.layerSwitcherDiv.style.animation = 'MoveLeft 0.4s';
            setTimeout(function () {
                myApp.layerSwitcherDiv.style.display = 'none';
            }, 300)
        } else {
            myApp.layerSwitcherDiv.style.display = 'block';
            myApp.layerSwitcherDiv.style.animation = 'MoveRight 0.4s';
        }
    }, true);

    $("input[type='radio'][name='inLineRadioBaseMap']").change(function () {
        var value = $(this).attr('LayerId');
        myApp.BaseLayerList.forEach(function (item) {
            let lyId = item.getProperties()['id'];
            if (lyId === value) {
                item.setVisible(true);
            } else {
                item.setVisible(false);
            }
        })
    });

    // $("input[type='text'][name='OpacityRange']").change(function () {
    //     var value = parseInt($(this).val()) / 100;
    //     var LayerId = $(this).attr('LayerId');
    //     let layer = myApp.getLayer(LayerId);
    //     layer.setOpacity(value);
    // });

    $('input:radio[name="watershed-radio"]').change(function () {
        if ($(this).val() == 'basin') {
            $('#select_Basin').attr('disabled', false);
            $('#select_Watershed').attr('disabled', true);
        } else if ($(this).val() == 'watershed') {
            $('#select_Watershed').attr('disabled', false);
            $('#select_Basin').attr('disabled', true);
        }
    });

    $("input[type='radio'][name='watershed-radio'], .select_watershed_basin").on('change', function (e) {
        myApp.mapControlFunction();
        if (parseInt(currentSelectedLocation.controlGid)) {
            currentSelectedLocation['is_wkt'] = false;
            myApp.getRelatedData(true);
        }
    });

    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        let currentTab = e.target.getAttribute('id').replace('NavTab-tab', '');
        currentSelectedLocation['tabName'] = currentTab;
        if (parseInt(currentSelectedLocation.controlGid)) {
            myApp.getRelatedData(false);
        } else if (currentSelectedLocation['is_wkt'] == true) {
            myApp.getRelatedData(false);
        }
    });

    this.PrintMap.addEventListener("click", () => {
        if (!$('#MapPrint').hasClass('show')) {

            $('#MapPrint').modal('show');
            myApp.WMSCropOrMask('crop');
            let target = document.querySelector('#map-control-printing');
            myApp.map.setTarget(target);
            setTimeout(function () {
                myApp.map.updateSize();
            }, 300);
            let LayerList = document.querySelector('.layer-legend-list');
            LayerList.innerHTML = ''
            document.querySelector('#toggle-all-legend-items').checked = false;
            legendInfos = [];
            myApp.LegendUIList = [];
            proxifyWMSLayers();

            myApp.AllBindedLayersList.filter(function (obj) {
                let Properties = obj.getProperties();
                if (Properties.visible === true) {
                    let prop = obj.getProperties();
                    let objj = {
                        id: prop.id,
                        visible: false,
                        title: prop.title,
                        legendPath: prop.legendPath
                    }
                    legendInfos.push(objj);
                    let createUILagendObj = new createUILagend(objj);
                    let ui = createUILagendObj.getUI();
                    LayerList.append(ui);
                    myApp.LegendUIList.push(createUILagendObj);
                }
                return true
            });
        }
    }, true);

    $('#MapPrint').on('hide.bs.modal', function () {

        let target = document.querySelector('#map-container');
        myApp.map.setTarget(target);
        setTimeout(function () {
            myApp.map.updateSize();
        }, 300);
        deproxifyWMSLayers();
        myApp.WMSCropOrMask('mask');

    });

    document.querySelector('#toggle-all-legend-items').addEventListener("change", (e) => {
        let is_checked = e.target.checked;
        myApp.LegendUIList.forEach(function (obj) {
            obj.setSelection(is_checked);
        });
        console.log('--------------------------');
    }, true);

    $('#print-process-btn').on('click', (event) => {

        const layout = getMapPDFLayout();
        const title = $("#map-title-for-print").val();
        const outputfilename = $("#map-print-filename").val();
        if(!title || !outputfilename){

            if (!title){
                myApp.WarningToast("Please Enter Map Title")
            }
            if (!outputfilename){
                myApp.WarningToast("Please Enter Output Filename")
            }
            return "Do Nothing"
        }
          $("#loading-modal").show();


        const mapSize = myApp.map.getSize();
        const mapResolution = myApp.map.getView().getResolution();
        myApp.map.once("rendercomplete", () => {
            // setting up the canvas
            const canvas = document.createElement("canvas");
            canvas.width = layout.mapFrameSizePxl[0];
            canvas.height = layout.mapFrameSizePxl[1];
            const context = canvas.getContext("2d");

            // sort the legend by height
            let legendInfos1 = legendInfos.filter(function (curObje){ return curObje.visible===true; }).sort((item1, item2) => item1.imgHeight - item2.imgHeight);

            copyOLMapTo(context);
            console.log(legendInfos1)

            legendInfos1.length && addLegendsTo(context, {
                legendInfos:legendInfos1,
                pos: layout.legendBoxPxl.pos,
                columnWidth: layout.legendBoxPxl.columnWidth,
                height: layout.legendBoxPxl.height
            });

            drawPolygon(context, "black", layout.northArrowCoordsPxl)
            drawScaleBar(context, {x: canvas.width, y: canvas.height})
            context.strokeStyle = "black";
            context.strokeRect(0, 0, canvas.width, canvas.height) // map frame border

            createMapPDF(title, outputfilename, canvas, layout)
            // reset original map size
            myApp.map.setSize(mapSize);
            myApp.map.getView().setResolution(mapResolution);
            $("#loading-modal").hide();
            $("#MapPrint .close").click().trigger("click");
        });

        // set map size to print frame size
        const frameSize = layout.mapFrameSizePxl;
        myApp.map.setSize(frameSize);
        const scaling = Math.min(frameSize[0] / mapSize[0], frameSize[1] / mapSize[1]);
        myApp.map.getView().setResolution(mapResolution / scaling);


    })
};

myApp.getLayer = function (id) {
    var layer;
    for (i = 0; i < myApp.AllBindedLayersList.length; i++) {
        if (id == myApp.AllBindedLayersList[i].getProperties().id) { ///popDensityLayer.getProperties().id
            layer = myApp.AllBindedLayersList[i].getLayer();

            break;
        }
    }
    return layer;
};
myApp.getBindedLayer = function (id) {
    var layer;
    for (i = 0; i < myApp.AllBindedLayersList.length; i++) {
        if (id == myApp.AllBindedLayersList[i].getProperties().id) { ///popDensityLayer.getProperties().id
            layer = myApp.AllBindedLayersList[i];
            break;
        }
    }
    return layer;
};
myApp.makeRequest = function (method, url) {
    return new Promise(function (resolve, reject) {
        let xhr = new XMLHttpRequest();
        xhr.open(method, url);
        xhr.onload = function () {
            if (this.status >= 200 && this.status < 300) {
                resolve(xhr.response);
            } else {
                reject({
                    status: this.status,
                    statusText: xhr.statusText
                });
            }
        };
        xhr.onerror = function () {
            reject({
                status: this.status,
                statusText: xhr.statusText
            });
        };
        xhr.send();
    });
};
myApp.makeRequestWithCookieCSRFToken = function (method, url, data) {
    return new Promise(function (resolve, reject) {
        let csrftokenCookie = myApp.getCookie('csrftoken');
        let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        let dataStr = ''
        for (var key in data) {
            dataStr += key.toString() + '=' + JSON.stringify(data[key]).toString() + '&'
        }
        dataStr += 'csrfmiddlewaretoken' + '=' + csrftoken.toString()
        let xhr = new XMLHttpRequest();
        xhr.open(method, url);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
        xhr.setRequestHeader('X-CSRFToken', csrftokenCookie);
        xhr.onload = function () {
            if (this.status >= 200 && this.status < 300) {
                resolve(xhr.response);
            } else {
                reject({
                    status: this.status,
                    statusText: xhr.statusText
                });
            }
        };
        xhr.onerror = function () {
            reject({
                status: this.status,
                statusText: xhr.statusText
            });
        };
        xhr.send(dataStr);
    });
};

myApp.getUpperLayer = function () {
    let selectedLayer = null;
    myApp.AllBindedLayersList.forEach(function (Layer) {
        let Properties = Layer.getProperties();
        console.log("----")
        console.log(Properties)
        console.log(Properties.hasOwnProperty('aoi'))
        console.log(Properties.visible === true)
        console.log("----")

        if (Properties.hasOwnProperty('aoi') && Properties.visible === true) {
            if (selectedLayer === null) {
                selectedLayer = Layer
            } else {
                if (selectedLayer.getProperties().zIndex < Properties.zIndex) {
                    selectedLayer = Layer
                }
            }
        }
    });
    return selectedLayer;
};

myApp.revertAbout = function () {
    $("#about-aoi").html("About");
    $("#about-aoi-body").html(' <p style="text-align:justify;font-size:12px;">' +
        'ICIMOD is developing an integrated information platform linking weather and climate data' +
        'with agriculture practices in the region. The platform provides data analysis support to' +
        'professionals responsible for developing agro-met advisories for government agencies and ...' +
        '</p><a data-toggle="modal" href="#aboutModal"><b>View More ...</b></a>');
};


myApp.getCookie = function (name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// 192.168.75.153:8000/apps/AFWatershed/
// 192.168.56.1:8000/apps/AFWatershed/
// 192.168.4.16:8000/apps/AFWatershed/




myApp.getMapImageURL = function () {

};





