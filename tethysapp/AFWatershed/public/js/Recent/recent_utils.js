myApp.initialSelectedWatershedBasin = function () {
    $("input[name='watershed-radio'][value='watershed']").prop("checked", true);
    $('input:radio[name="watershed-radio"]').trigger("change");
}
myApp.addingChooseOptionToSelect = function () {
    $('#select_Basin').prepend($('<option>', {
        value: 0,
        text: 'Choose Basin',
        disabled: 'disabled'
    }));
    $('#select_Watershed').prepend($('<option>', {
        value: 0,
        text: 'Choose Watershed',
        disabled: 'disabled'
    }));
    $('#select_Basin').val("0");
    $('#select_Watershed').val("0");
}

myApp.AccordianCard = function (htmlid, NameHTML, parentAccordianId) {
    let cardDiv = myApp.createDiv("card");
    let HeadingID = htmlid + "__heading"
    let collapseID = htmlid + "__collapse"
    let bodyID = htmlid + "__body"

    let CardHearder = myApp.createDiv("card-header");
    CardHearder.setAttribute("id", HeadingID);
    let h2 = myApp.createH(2, "mb-0");

    let ButtonHeading = myApp.createButton("btn btn-link btn-block text-left collapsed");
    ButtonHeading.setAttribute("type", "button");
    ButtonHeading.setAttribute("data-toggle", "collapse");
    ButtonHeading.setAttribute("data-target", "#" + collapseID);
    ButtonHeading.setAttribute("aria-expanded", "true");
    ButtonHeading.setAttribute("aria-controls", collapseID);
    ButtonHeading.innerText = NameHTML
    h2.append(ButtonHeading);
    CardHearder.append(h2);

    let collapseDiv = myApp.createDiv("collapse");
    collapseDiv.setAttribute("id", collapseID);
    collapseDiv.setAttribute("aria-labelledby", HeadingID);
    collapseDiv.setAttribute("data-parent", "#" + parentAccordianId);
    let BodyDiv = myApp.createDiv("card-body");
    BodyDiv.setAttribute("id", bodyID);
    collapseDiv.append(BodyDiv);

    cardDiv.append(CardHearder);
    cardDiv.append(collapseDiv);
    return cardDiv
}

myApp.InitOwlCarousel = function () {
    jQuery(document).ready(function ($) {
        "use strict";
        $('#Gelogical-owlcarousel').owlCarousel({
            loop: false,
            // center: true,
            items: 3,
            margin: 10,
            autoplay: false,
            dots: false,
            nav: true,
            // autoplayTimeout: 8500,
            // smartSpeed: 450,
            navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
            responsive: {
                0: {
                    items: 1
                },
                768: {
                    items: 2
                },
                1170: {
                    items: 3
                }
            }
        });
        $('#Hydrological-owlcarousel').owlCarousel({
            loop: false,
            // center: true,
            items: 3,
            margin: 10,
            autoplay: false,
            dots: false,
            nav: true,
            // autoplayTimeout: 8500,
            // smartSpeed: 450,
            navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
            responsive: {
                0: {
                    items: 1
                },
                768: {
                    items: 2
                },
                1170: {
                    items: 3
                }
            }
        });
        $('#Polulation-owlcarousel').owlCarousel({
            loop: false,
            // center: true,
            items: 2,
            margin: 10,
            autoplay: false,
            dots: false,
            nav: true,
            // autoplayTimeout: 8500,
            // smartSpeed: 450,
            navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
            responsive: {
                0: {
                    items: 1
                },
                768: {
                    items: 2
                },
                1170: {
                    items: 2
                }
            }
        });
        $('#Topographical-owlcarousel').owlCarousel({
            loop: false,
            // center: true,
            items: 3,
            margin: 10,
            autoplay: false,
            dots: false,
            nav: true,
            // autoplayTimeout: 8500,
            // smartSpeed: 450,
            navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
            responsive: {
                0: {
                    items: 1
                },
                768: {
                    items: 2
                },
                1170: {
                    items: 3
                }
            }
        });
        $('#Soil_Parameters-owlcarousel').owlCarousel({
            loop: false,
            // center: true,
            items: 2,
            margin: 10,
            autoplay: false,
            dots: false,
            nav: true,
            // autoplayTimeout: 8500,
            // smartSpeed: 450,
            navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
            responsive: {
                0: {
                    items: 1
                },
                768: {
                    items: 2
                },
                1170: {
                    items: 2
                }
            }
        });
        $('#LandCover-owlcarousel').owlCarousel({
            loop: false,
            // center: true,
            items: 2,
            margin: 10,
            autoplay: false,
            dots: false,
            nav: true,
            // autoplayTimeout: 8500,
            // smartSpeed: 450,
            navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
            responsive: {
                0: {
                    items: 1
                },
                768: {
                    items: 2
                },
                1170: {
                    items: 2
                }
            }
        });
        $('#Climate-owlcarousel').owlCarousel({
            loop: false,
            // center: true,
            items: 2,
            margin: 10,
            autoplay: false,
            dots: false,
            nav: true,
            // autoplayTimeout: 8500,
            // smartSpeed: 450,
            navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
            responsive: {
                0: {
                    items: 1
                },
                768: {
                    items: 2
                },
                1170: {
                    items: 2
                }
            }
        });
    });
}

myApp.mapControlFunction = function () {
    //Basin and watershed
    var selectedValueWatershed = $("input[type='radio'][name='watershed-radio']:checked").val();
    currentSelectedLocation["layerName"] = selectedValueWatershed;
    $("input[type='radio'][name='watershed-radio']").each(function (value) {
        var currentValue = $(this).val();
        if (currentValue == selectedValueWatershed) {
            var gid = $(this).parent().parent().find('.select_watershed_basin option').filter(":selected").val();
            currentSelectedLocation["controlGid"] = gid;
        }
    });
    let activeTab = $(".tab-pane.active").attr('id').replace('NavTab', '');
    currentSelectedLocation['tabName'] = activeTab
}

myApp.getRelatedData = async function (getGeojsonOrNot) {
    if (getGeojsonOrNot) {
        let featureGeojson = await myApp.makeRequestWithCookieCSRFToken('POST', myApp.APICollection.api.GetGeojson, currentSelectedLocation);
        let ParsedfeatureGeojson = JSON.parse(featureGeojson);
        var layerSelecd = myApp.HighLightedLayer.getSource();
        layerSelecd.clear();
        var parser = new ol.format.GeoJSON();
        var features = parser.readFeatures(ParsedfeatureGeojson['geojson']);
        var perveiousExtent = myApp.view.calculateExtent();
        var zoom_pervious = myApp.view.getZoom();
        myApp.view.fit(ParsedfeatureGeojson.extent, myApp.map.getSize());
        var zoom_final = myApp.view.getZoom();
        myApp.view.fit(perveiousExtent, myApp.map.getSize());
        layerSelecd.addFeatures(features);
        var location = ol.proj.fromLonLat(ParsedfeatureGeojson.centroid);
        myApp.flyTo(location, zoom_pervious, zoom_final, function () {
        });
        currentSelectedLocation.Coords = ParsedfeatureGeojson.geojson.features[0].geometry.coordinates;
        //    change title of HighLightedLayer
    }


    if (currentSelectedLocation.is_wkt) {
        var wkt_format = new ol.format.WKT();
        var testFeature = wkt_format.readFeature(currentSelectedLocation.wkt);
        var wkt_options = {};
        var geojson_format = new ol.format.GeoJSON(wkt_options);
        var out = geojson_format.writeFeature(testFeature);
        var ParsedJSON = JSON.parse(out);
        currentSelectedLocation.Coords = [ParsedJSON.geometry.coordinates];
    }

    myApp.WMSCropOrMask('mask');


    let QuickInformation = await myApp.makeRequestWithCookieCSRFToken('POST', myApp.APICollection.api.QuickIntroduction, currentSelectedLocation);
    let ParsedQI = JSON.parse(QuickInformation);
    console.log(ParsedQI);
    var QuickInfo = Object.keys(ParsedQI.data_quick_introduction);
    QuickInfo.forEach(function (value) {
        $("#" + value).html(ParsedQI.data_quick_introduction[value]);
    });
    myApp.changeHighlightedLayer();
    myApp.GetDataFromBackend();
}

myApp.flyTo = function (location, zi, zf, done) {
    var duration = 2000;
//  var zoom = view.getZoom();
    var zoom = zf;
    var parts = 2;
    var called = false;

    function callback(complete) {
        --parts;
        if (called) {
            return;
        }
        if (parts === 0 || !complete) {
            called = true;
            done(complete);
        }
    }

    myApp.view.animate({
        center: location,
        duration: duration
    }, callback);

    myApp.view.animate({
        zoom: zoom - 1,
        duration: duration / 2
    }, {
        zoom: zoom,
        duration: duration / 2
    }, callback);
}

myApp.GetDataFromBackend = function () {
    if (currentSelectedLocation['tabName'] === "Gelogical") {
        myApp.GeoLogicalRockType();
        myApp.GeoLogicalTemplate();
        myApp.GeoLogicalMineralTpye();
        myApp.GeoLogicalFaultLines();
    }
    if (currentSelectedLocation['tabName'] === "Hydrological") {
        myApp.HydrologicalYearWellDepthTrend();
        myApp.HydrologicalGroundWaterDepthFlow();
        myApp.HydrologicalFloodRisk();
        myApp.HydrologicalWaterBodies();
        myApp.HydrologicalDrainageDensity();
        myApp.HydrologicalGroundWaterPotentialZone();
    }

    if (currentSelectedLocation['tabName'] === "Topographical") {
        myApp.TopologicalSlope();
        myApp.TopologicalAspect();
        myApp.TopologicalElevation();
        myApp.TopologicalPlanCurvature();
        myApp.TopologicalProfileCurvature();
    }
    if (currentSelectedLocation['tabName'] === "Soil_Parameters") {
        myApp.SoilParameterSoilDepth();
        myApp.SoilParameterType();
    }
    if (currentSelectedLocation['tabName'] === "Polulation") {
        myApp.PopulationPopulationDensity();
        myApp.PopulationVillageDensity();
    }
    if (currentSelectedLocation['tabName'] === "LandCover") {
        myApp.LandCover();
        myApp.AllBindedLayersList.forEach(function (Layer) {
            let Properties = Layer.getProperties();
            console.log(Properties.id);
            if (Properties.hasOwnProperty('aoi') && Layer.getDivVisible() === true) {
                if (Properties.chartDivId == 'Annual_NDVI_MODIS_2009_2018' || Properties.chartDivId == 'Monthly_NDVI_MODIS_2009_2018') {
                    let SourceParam = Layer.getLayer().GetFirstLayer().getProperties().source.getParams();
                    let SourceURL = Layer.getLayer().GetFirstLayer().getProperties().source.getUrls()[0].split('wms')[1];
                    currentSelectedLocation.DATADIR = SourceURL;
                    currentSelectedLocation.LAYER = SourceParam.LAYERS;
                    currentSelectedLocation.type = "polygon";
                    currentSelectedLocation.DataInterval = Properties.DataInterval;
                    let divToDrawTimeSeriesChart = "TimeSeries_" + Properties.chartDivId;
                    myApp.ClimateChart(divToDrawTimeSeriesChart, currentSelectedLocation, Properties);
                }
            }
        });
    }
    if (currentSelectedLocation['tabName'] === "Climate") {
        myApp.AllBindedLayersList.forEach(function (Layer) {
            let Properties = Layer.getProperties();
            if (Properties.hasOwnProperty('aoi') && Layer.getDivVisible() === true) {
                let InterestedLayers = ['Annual_LST_MODIS_2009_2018', 'Annual_ET_MODIS_2009_2018', 'Annual_Percipitation_chirips_2009_2018', 'Annual_Snow_Cover_MODIS_2009_2018', 'Monthly_LST_MODIS_2009_2018', 'Monthly_Precipitation_CHIRIPS_2009_2018', 'Monthly_Snow_Cover_MODIS_2009_2018'];
                if (InterestedLayers.includes(Properties.chartDivId)) {
                    let SourceParam = Layer.getLayer().GetFirstLayer().getProperties().source.getParams();
                    let SourceURL = Layer.getLayer().GetFirstLayer().getProperties().source.getUrls()[0].split('wms')[1];
                    currentSelectedLocation.DATADIR = SourceURL;
                    currentSelectedLocation.LAYER = SourceParam.LAYERS;
                    currentSelectedLocation.type = "polygon";
                    currentSelectedLocation.DataInterval = Properties.DataInterval;
                    let divToDrawTimeSeriesChart = "TimeSeries_" + Properties.chartDivId;
                    myApp.ClimateChart(divToDrawTimeSeriesChart, currentSelectedLocation, Properties);
                }
            }
        });
    }
    console.log(currentSelectedLocation['tabName']);
}

myApp.GeoLogicalRockType = async function () {
    //RockType
    let gelogicalRocktypeChartId = 'gelogical__rocktype'
    $('#' + gelogicalRocktypeChartId).html('<div class="vertically-center" ><div  class="spinner-border text-primary" role="status">\n' +
        '  <span class="sr-only">Loading...</span>\n' +
        '</div></div></div>');
    let response = await myApp.makeRequestWithCookieCSRFToken('POST', myApp.APICollection.chartAPI.Gelogical__Rock_Type, currentSelectedLocation);
    let ParseResponse = JSON.parse(response);
    let HighchartsObject = myApp.HighchartsPieChartObject('Rock type', 'Rock type', ParseResponse.seriesData)
    myApp.DrawChart(gelogicalRocktypeChartId, HighchartsObject);


}
myApp.GeoLogicalTemplate = async function () {


    //gelogicalTemplate
    let gelogicalTemplateChartId = 'gelogical__gelogical_template'
    $('#' + gelogicalTemplateChartId).html('<div class="vertically-center" ><div  class="spinner-border text-primary" role="status">\n' +
        '  <span class="sr-only">Loading...</span>\n' +
        '</div></div></div>');
    let GeoLogicalResponse = await myApp.makeRequestWithCookieCSRFToken('POST', myApp.APICollection.chartAPI.Gelogical__Geological_Template, currentSelectedLocation);
    let ParseGeologicalTemplateResponse = JSON.parse(GeoLogicalResponse);
    let HighchartsObjectGeologicalTemplate = myApp.HighchartsColumnChartObject('Geological template', ParseGeologicalTemplateResponse.seriesData[0], 'Area (sq.km)', 'sq.km', 'Geological template', ParseGeologicalTemplateResponse.seriesData[1])
    console.log(HighchartsObjectGeologicalTemplate);
    myApp.DrawChart(gelogicalTemplateChartId, HighchartsObjectGeologicalTemplate);

}

myApp.GeoLogicalMineralTpye = async function () {

    //Mineral Types
    let gelogical_mineral_type_ChartId = 'Gelogical__Mineral_Types'
    $('#' + gelogical_mineral_type_ChartId).html('<div class="vertically-center" ><div  class="spinner-border text-primary" role="status">\n' +
        '  <span class="sr-only">Loading...</span>\n' +
        '</div></div></div>');
    let GeoLogicalMineralTypeResponse = await myApp.makeRequestWithCookieCSRFToken('POST', myApp.APICollection.chartAPI.Gelogical__Mineral_Types, currentSelectedLocation);
    let ParseGeologicalMineralTypeResponse = JSON.parse(GeoLogicalMineralTypeResponse);
    let HighchartsObjectGeologicalMineralType = myApp.HighchartsColumnChartObject('Mineral type', ParseGeologicalMineralTypeResponse.seriesData[0], 'Count', '', 'Mineral', ParseGeologicalMineralTypeResponse.seriesData[1])
    console.log(HighchartsObjectGeologicalMineralType);
    myApp.DrawChart(gelogical_mineral_type_ChartId, HighchartsObjectGeologicalMineralType);


}
myApp.GeoLogicalFaultLines = async function () {

    //Fault lines
    let gelogical_fault_lines_ChartId = 'Gelogical__Fault_Line'
    $('#' + gelogical_fault_lines_ChartId).html('<div class="vertically-center" ><div  class="spinner-border text-primary" role="status">\n' +
        '  <span class="sr-only">Loading...</span>\n' +
        '</div></div></div>');
    let GeoLogicalFaultLinesResponse = await myApp.makeRequestWithCookieCSRFToken('POST', myApp.APICollection.chartAPI.Gelogical__Fault_Line, currentSelectedLocation);
    let ParseGeologicalFaultLineResponse = JSON.parse(GeoLogicalFaultLinesResponse);
    let HighchartsObjectGeologicalFault = myApp.HighchartsColumnChartObject('Fault line', ParseGeologicalFaultLineResponse.seriesData[0], 'Length (Km)', 'Km', 'Fault lines', ParseGeologicalFaultLineResponse.seriesData[1])
    console.log(HighchartsObjectGeologicalFault);
    myApp.DrawChart(gelogical_fault_lines_ChartId, HighchartsObjectGeologicalFault);
}

myApp.HydrologicalYearWellDepthTrend = async function () {
    //Fault lines
    let div_ChartId = 'Hydrological--Yearly-Well-Depth-Trend'
    $('#' + div_ChartId).html('<div class="vertically-center" ><div  class="spinner-border text-primary" role="status">\n' +
        '  <span class="sr-only">Loading...</span>\n' +
        '</div></div></div>');
    let Response = await myApp.makeRequestWithCookieCSRFToken('POST', myApp.APICollection.chartAPI.Hydrological__Yearly_Well_Depth_Trend, currentSelectedLocation);
    let ParsedResponse = JSON.parse(Response);
    let HighchartsObject = myApp.HighchartsLineGraphObject('Yearly Well depth trend', 'Date', 'Depth (m)', 'Well depth', 'm', ParsedResponse.seriesData)
    console.log(HighchartsObject);
    myApp.DrawChart(div_ChartId, HighchartsObject);
};
myApp.HydrologicalGroundWaterDepthFlow = async function () {

    let ChartId = 'Hydrological__Ground_Water_Depth_Flow'
    $('#' + ChartId).html('<div class="vertically-center" ><div  class="spinner-border text-primary" role="status">\n' +
        '  <span class="sr-only">Loading...</span>\n' +
        '</div></div></div>');
    let Response = await myApp.makeRequestWithCookieCSRFToken('POST', myApp.APICollection.chartAPI.Hydrological__Ground_Water_Depth_Flow, currentSelectedLocation);
    let ParseResponse = JSON.parse(Response);
    let HighchartsObject = myApp.HighchartsColumnChartObject('Ground Water depth flow (2010)', ParseResponse.seriesData[0], 'Area (sq.km)', 'sq.km', 'Ground Water depth flow', ParseResponse.seriesData[1])
    console.log(HighchartsObject);
    myApp.DrawChart(ChartId, HighchartsObject);

}
myApp.HydrologicalFloodRisk = async function () {

    let ChartId = 'Hydrological--Flood-Risk'
    $('#' + ChartId).html('<div class="vertically-center" ><div  class="spinner-border text-primary" role="status">\n' +
        '  <span class="sr-only">Loading...</span>\n' +
        '</div></div></div>');
    let response = await myApp.makeRequestWithCookieCSRFToken('POST', myApp.APICollection.chartAPI.Hydrological__Hydrological__Flood_Risk, currentSelectedLocation);
    let ParseResponse = JSON.parse(response);
    let HighchartsObject = myApp.HighchartsPieChartObject('Flood risk', 'Flood risk', ParseResponse.seriesData)
    myApp.DrawChart(ChartId, HighchartsObject);

}
myApp.HydrologicalWaterBodies = async function () {
    let response = await myApp.makeRequestWithCookieCSRFToken('POST', myApp.APICollection.chartAPI.Hydrological__Hydrological__water_bodies, currentSelectedLocation);
    let data = JSON.parse(response);
    $("#infographics_lake").text(data.seriesData[0]["lake"]);
    $("#infographics_marshland").text(data.seriesData[0]["marshland"]);
    $("#infographics_majorRiver").text(data.seriesData[0]["majorRiver"]);
    $("#infographics_minorRivers").text(data.seriesData[0]["MinroRiver"]);
}
myApp.HydrologicalDrainageDensity = async function () {

    let ChartId = 'Hydrological__DrainageDensity'
    $('#' + ChartId).html('<div class="vertically-center" ><div  class="spinner-border text-primary" role="status">\n' +
        '  <span class="sr-only">Loading...</span>\n' +
        '</div></div></div>');
    let response = await myApp.makeRequestWithCookieCSRFToken('POST', myApp.APICollection.chartAPI.Hydrological__DrainageDensity, currentSelectedLocation);
    let ParseResponse = JSON.parse(response);
    let HighchartsObject = myApp.HighchartsPieChartObject('Drainage density', 'Drainage density', ParseResponse.seriesData)
    myApp.DrawChart(ChartId, HighchartsObject);


}
myApp.HydrologicalGroundWaterPotentialZone = async function () {
    let ChartId = 'Hydrological__GroundWaterPotentialZone'
    $('#' + ChartId).html('<div class="vertically-center" ><div  class="spinner-border text-primary" role="status">\n' +
        '  <span class="sr-only">Loading...</span>\n' +
        '</div></div></div>');
    let Response = await myApp.makeRequestWithCookieCSRFToken('POST', myApp.APICollection.chartAPI.Hydrological__GroundWaterPotentialZone, currentSelectedLocation);
    let ParseResponse = JSON.parse(Response);
    let HighchartsObject = myApp.HighchartsColumnChartObject('Ground Water potential zone', ParseResponse.seriesData[0], 'Area (sq.km)', 'sq.km', 'Ground Water potential zone', ParseResponse.seriesData[1])
    console.log(HighchartsObject);
    myApp.DrawChart(ChartId, HighchartsObject);

}

myApp.TopologicalSlope = async function () {

    let ChartId = 'Topographical--slope'
    $('#' + ChartId).html('<div class="vertically-center" ><div  class="spinner-border text-primary" role="status">\n' +
        '  <span class="sr-only">Loading...</span>\n' +
        '</div></div></div>');
    let response = await myApp.makeRequestWithCookieCSRFToken('POST', myApp.APICollection.chartAPI.Topographical__slope, currentSelectedLocation);
    let ParseResponse = JSON.parse(response);
    let HighchartsObject = myApp.HighchartsPieChartObject('Slope (Degree)', 'Slope', ParseResponse.seriesData)
    myApp.DrawChart(ChartId, HighchartsObject);

}
myApp.TopologicalAspect = async function () {

    let ChartId = 'Topographical--aspect'
    $('#' + ChartId).html('<div class="vertically-center" ><div  class="spinner-border text-primary" role="status">\n' +
        '  <span class="sr-only">Loading...</span>\n' +
        '</div></div></div>');
    let Response = await myApp.makeRequestWithCookieCSRFToken('POST', myApp.APICollection.chartAPI.Topographical__aspect, currentSelectedLocation);
    let ParseResponse = JSON.parse(Response);
    let HighchartsObject = myApp.HighchartsColumnChartObject('Aspect', ParseResponse.seriesData[0], 'Area (sq.km)', 'sq.km', 'Aspect', ParseResponse.seriesData[1])

    console.log(HighchartsObject);
    myApp.DrawChart(ChartId, HighchartsObject);
}
myApp.TopologicalElevation = async function () {
    let ChartId = 'Topographical__Elevation';

    $('#' + ChartId).html('<div class="vertically-center" ><div  class="spinner-border text-primary" role="status">\n' +
        '  <span class="sr-only">Loading...</span>\n' +
        '</div></div></div>');
    let Response = await myApp.makeRequestWithCookieCSRFToken('POST', myApp.APICollection.chartAPI.Topographical__Elevation, currentSelectedLocation);
    let ParseResponse = JSON.parse(Response);
    let HighchartsObject = myApp.HighchartsColumnChartObject('Elevation interval (m)', ParseResponse.seriesData[0], 'Meter', 'm', 'Elevation', ParseResponse.seriesData[1])

    console.log(HighchartsObject);
    myApp.DrawChart(ChartId, HighchartsObject);
}
myApp.TopologicalPlanCurvature = async function () {

    let ChartId = 'Topographical__PlanCurvature'
    $('#' + ChartId).html('<div class="vertically-center" ><div  class="spinner-border text-primary" role="status">\n' +
        '  <span class="sr-only">Loading...</span>\n' +
        '</div></div></div>');
    let response = await myApp.makeRequestWithCookieCSRFToken('POST', myApp.APICollection.chartAPI.Topographical__PlanCurvature, currentSelectedLocation);
    let ParseResponse = JSON.parse(response);
    let HighchartsObject = myApp.HighchartsPieChartObject('Plan curvature', 'Plan curvature', ParseResponse.seriesData)
    myApp.DrawChart(ChartId, HighchartsObject);

}
myApp.TopologicalProfileCurvature = async function () {

    let ChartId = 'Topographical__ProfileCurvature'
    $('#' + ChartId).html('<div class="vertically-center" ><div  class="spinner-border text-primary" role="status">\n' +
        '  <span class="sr-only">Loading...</span>\n' +
        '</div></div></div>');
    let response = await myApp.makeRequestWithCookieCSRFToken('POST', myApp.APICollection.chartAPI.Topographical__ProfileCurvature, currentSelectedLocation);
    let ParseResponse = JSON.parse(response);
    let HighchartsObject = myApp.HighchartsPieChartObject('Profile curvature', 'Profile curvature', ParseResponse.seriesData)
    myApp.DrawChart(ChartId, HighchartsObject);

}

myApp.SoilParameterSoilDepth = async function () {

    let ChartId = 'SoilParameter__SoilDepth'
    $('#' + ChartId).html('<div class="vertically-center" ><div  class="spinner-border text-primary" role="status">\n' +
        '  <span class="sr-only">Loading...</span>\n' +
        '</div></div></div>');
    let response = await myApp.makeRequestWithCookieCSRFToken('POST', myApp.APICollection.chartAPI.SoilParameter__SoilDepth, currentSelectedLocation);
    let ParseResponse = JSON.parse(response);
    let HighchartsObject = myApp.HighchartsPieChartObject('Soil depth', 'Soil depth', ParseResponse.seriesData)
    myApp.DrawChart(ChartId, HighchartsObject);

}
myApp.SoilParameterType = async function () {
    let ChartId = 'SoilParameter__SoilType';

    $('#' + ChartId).html('<div class="vertically-center" ><div  class="spinner-border text-primary" role="status">\n' +
        '  <span class="sr-only">Loading...</span>\n' +
        '</div></div></div>');
    let Response = await myApp.makeRequestWithCookieCSRFToken('POST', myApp.APICollection.chartAPI.SoilParameter__SoilType, currentSelectedLocation);
    let ParseResponse = JSON.parse(Response);
    let HighchartsObject = myApp.HighchartsColumnChartObject('Soil type', ParseResponse.seriesData[0], 'Area (sq.km)', 'sq.km', 'Soil type', ParseResponse.seriesData[1])

    console.log(HighchartsObject);
    myApp.DrawChart(ChartId, HighchartsObject);
}

myApp.PopulationPopulationDensity = async function () {

    let ChartId = 'Population__PopulationDensity'
    $('#' + ChartId).html('<div class="vertically-center" ><div  class="spinner-border text-primary" role="status">\n' +
        '  <span class="sr-only">Loading...</span>\n' +
        '</div></div></div>');
    let response = await myApp.makeRequestWithCookieCSRFToken('POST', myApp.APICollection.chartAPI.Population__PopulationDensity, currentSelectedLocation);
    let ParseResponse = JSON.parse(response);
    let HighchartsObject = myApp.HighchartsPieChartObject('Population density', 'Population density', ParseResponse.seriesData)
    myApp.DrawChart(ChartId, HighchartsObject);

}
myApp.PopulationVillageDensity = async function () {

    let ChartId = 'Population__VillageDensity'
    $('#' + ChartId).html('<div class="vertically-center" ><div  class="spinner-border text-primary" role="status">\n' +
        '  <span class="sr-only">Loading...</span>\n' +
        '</div></div></div>');
    let response = await myApp.makeRequestWithCookieCSRFToken('POST', myApp.APICollection.chartAPI.Population__VillageDensity, currentSelectedLocation);
    let ParseResponse = JSON.parse(response);
    let HighchartsObject = myApp.HighchartsPieChartObject('Village density', 'Village density', ParseResponse.seriesData)
    myApp.DrawChart(ChartId, HighchartsObject);

}

myApp.LandCover = async function () {

    let ChartId = 'LandCover__LandCover'
    $('#' + ChartId).html('<div class="vertically-center" ><div  class="spinner-border text-primary" role="status">\n' +
        '  <span class="sr-only">Loading...</span>\n' +
        '</div></div></div>');
    let Response = await myApp.makeRequestWithCookieCSRFToken('POST', myApp.APICollection.chartAPI.LandCover__LandCover, currentSelectedLocation);
    let ParseResponse = JSON.parse(Response);
    let HighchartsObject = myApp.HighchartsColumnChartObject('Land cover (2018)', ParseResponse.seriesData[0], 'Area (sq.km)', 'sq.km', 'Land cover', ParseResponse.seriesData[1])
    console.log(HighchartsObject);
    myApp.DrawChart(ChartId, HighchartsObject);

}

myApp.ClimateChart = async function (divId, currentData, layerProperties) {
    $('#' + divId).html('<div class="vertically-center" ><div  class="spinner-border text-primary" role="status">\n' +
        '  <span class="sr-only">Loading...</span>\n' +
        '</div></div></div>');
    let Response = await myApp.makeRequestWithCookieCSRFToken('POST', myApp.APICollection.chartAPI.Climate__ClimateTimeSeries, currentData);
    let ParseResponse = JSON.parse(Response);
    let Title = layerProperties.ChartTitle.slice(0, -9) + ParseResponse.DateRange;
    let subTitle = "";
    let YaxisLabel = layerProperties.unit;
    let SeriesName = layerProperties.ChartTitle.slice(0, -9)
    let random = Math.floor(Math.random() * myApp.IndexColors.length);
    let highchartsObj = myApp.datetimeChartObj(Title, subTitle, ParseResponse.SeriesData, SeriesName, YaxisLabel, 'Date', myApp.IndexColors[random])
    myApp.DrawChart(divId, highchartsObj);

}


myApp.HighchartsPieChartObject = function (ChartTitle, seriesName, seriesData) {

    let HcObj = {
        chart: {
            // backgroundColor: '#EFEFEF',
            margin: [25, 0, 30, 0],
            spacingBottom: 5,
            spacingTop: 5,
            spacingLeft: 0,
            spacingRight: 0,
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: ChartTitle
        },
        credits: {
            enabled: false
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: false
                },
                showInLegend: true
            }
        },
        legend: {
            align: 'center',
            verticalAlign: 'bottom',
            layout: 'horizontal',
            maxHeight: '40'
        },
        series: [{
            name: seriesName,
            colorByPoint: true,
            data: seriesData
        }]
    };
    return HcObj
}

myApp.HighchartsColumnChartObject = function (ChartTitle, categoriesList, yAxisTitle, tooltipUnit, seriesName, seriesData) {
    let HcObj = {
        chart: {
            // backgroundColor: '#EFEFEF',
            //            margin: [25, 0, 0, 0],
            spacingBottom: 5,
            spacingTop: 5,
            spacingLeft: 0,
            spacingRight: 0,
            type: 'column'
        },
        title: {
            text: ChartTitle
        },
        xAxis: {
            categories: categoriesList,
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: yAxisTitle
            }
        },
        credits: {
            enabled: false
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f}' + tooltipUnit + '</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0,
                showInLegend: false
            }
        },
        series: [{
            name: seriesName,
            data: seriesData
        }]
    };
    return HcObj
}

myApp.HighchartsLineGraphObject = function (ChartTitle, xAxisTitle, yAxisTitle, tooltipName, toolTipUnit, seriesData) {

    let HcObj = {
        chart: {
            type: 'spline',
            // backgroundColor: '#EFEFEF',
//      margin: [25, 0, 0, 0],
            spacingBottom: 5,
            spacingTop: 5,
            spacingLeft: 0,
            spacingRight: 0,

        },
        title: {
            text: ChartTitle
        },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: { // don't display the dummy year
                month: '%e. %b',
                year: '%b'
            },
            labels: {
                format: '{value:%Y}'
            },
            title: {
                text: xAxisTitle
            }
        },
        yAxis: {
            title: {
                text: yAxisTitle
            },
            min: 0
        },
        credits: {
            enabled: false
        },
        tooltip: {
            headerFormat: '<b>{series.name}</b><br>',
            pointFormat: 'Year: {point.x:%Y} <br>' + tooltipName + '{point.y:.2f} ' + toolTipUnit
        },

        plotOptions: {
            series: {
                marker: {
                    enabled: true
                }
            }
        },

        colors: ['#6CF', '#39F', '#06C', '#036', '#000'],

        // Define the data points. All series have a dummy year
        // of 1970/71 in order to be compared on the same x axis. Note
        // that in JavaScript, months start at 0 for January, 1 for February etc.
        series: seriesData,

        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    plotOptions: {
                        series: {
                            marker: {
                                radius: 2.5
                            }
                        }
                    }
                }
            }]
        }
    };
    return HcObj
}

myApp.DrawChart = function (divId, HighchartsObj) {
    if ($("#" + divId).highcharts()) {
        $("#" + divId).highcharts().destroy();
    } else {
        $("#" + divId).html('')
    }
    $("#" + divId).highcharts(HighchartsObj);
}

myApp.datetimeChartObj = function (title, subTitle, SeriesData, SeriesName, YaxisLabel, XaxisLabel, plotColor) {
    let data = {
        title: {
            text: title,
            fontSize: '10px'
        },
        subtitle: {
            text: subTitle,
            fontSize: '8px'
        },
        series: [{
            name: SeriesName,
            data: SeriesData
        }],
        xAxis: {
            type: 'datetime',
            title: {
                text: XaxisLabel,
                align: 'high',
            }
        },
        yAxis: {
            title: {
                text: YaxisLabel
            }
        },
        legend: {
            enabled: false
        },
        credits: {
            enabled: false
        },
        plotOptions: {
            series: {
                color: plotColor
            }
        },
        exporting: {
            buttons: {
                contextButton: {
                    menuItems: ["printChart",
                        "separator",
                        "downloadPNG",
                        "downloadJPEG",
                        "downloadPDF",
                        "downloadSVG",
                        "separator",
                        "downloadCSV",
                        "downloadXLS",
                        //"viewData",
                        "openInCloud"]
                }
            }
        }
    };
    return data
};

myApp.changeHighlightedLayer = function () {
    let LayerTitle = '';
    if (currentSelectedLocation.is_wkt === true) {
        LayerTitle = 'Area of Interest';
    } else {
        if (currentSelectedLocation.layerName === "watershed") {
            LayerTitle = $("#select_Watershed option[value='" + currentSelectedLocation.controlGid + "']")[0].innerText;
        } else {
            LayerTitle = $("#select_Basin option[value='" + currentSelectedLocation.controlGid + "']")[0].innerText;
        }
    }
    myApp.HighLightedLayer.set('title', LayerTitle);

};

myApp.WMSCropOrMask = function (CropOrMask) {
    myApp.AllBindedLayersList.forEach(function (layerobj) {
        let properties = layerobj.getProperties();
        if (properties.mask) {
            if (CropOrMask == 'crop') {
                layerobj.setCrop(currentSelectedLocation.Coords);
            } else {
                layerobj.setMask(currentSelectedLocation.Coords);
            }
        }
    });
};

function getMapPDFLayout() {
    const DPI = 120; // pdf's dpi
    const mmToPixel = dim_mm => dim_mm * DPI / 25.4; // 1 inch = 25.4 mm
    // all measurements are in mm if not suffixed by pxl
    const margin = 10;
    const topMargin = 15;
    const pageWidth = 297;
    const pageHeight = 210;
    const mapWidth = pageWidth - 2 * margin; // 272
    const mapHeight = pageHeight - topMargin - margin; // 180
    const mapHeightPxl = mmToPixel(mapHeight);
    // legend positions are relative to mapframe
    legendHeightPercent = 0.42;
    legendHeightPxl = mapHeightPxl * legendHeightPercent;
    legendPosPxl = {
        x: mmToPixel(2),
        y: mapHeightPxl * (1 - legendHeightPercent) - mmToPixel(2)
    }
    // northArrow Coords: also relative to mapFrame
    const arrowBaseWidth = 9;
    const arrowHeight = 12;
    const arrowTop = 6;
    const arrowCenterX = mapWidth - (6 + arrowBaseWidth / 2);
    const northArrowCoords = [
        [arrowCenterX, arrowTop], // top coordinate
        [arrowCenterX + arrowBaseWidth / 2, arrowTop + arrowHeight], // rightCoordinate
        [arrowCenterX, arrowTop + 2 * arrowHeight / 3], // middleCoordinate
        [arrowCenterX - arrowBaseWidth / 2, arrowTop + arrowHeight], // leftCoordinate
    ];
    return {
        format: "a4",
        pageDim: [pageWidth, pageHeight],
        margin,
        topMargin,
        mapFrameSize: [mapWidth, mapHeight],
        mapFrameSizePxl: [mmToPixel(mapWidth), mapHeightPxl],
        northArrowCoordsPxl: northArrowCoords.map(pt => pt.map(mmToPixel)),
        legendBoxPxl: {
            pos: legendPosPxl,
            height: legendHeightPxl,
            columnWidth: 230
        },
    };
};

function copyOLMapTo(context) {
    context.fillStyle = "white";
    context.fillRect(0, 0, context.canvas.width, context.canvas.height);
    document.querySelectorAll(".ol-layer canvas").forEach(mapCanvas => {
        if (mapCanvas.width > 0) {
            const opacity = mapCanvas.parentNode.style.opacity;
            context.globalAlpha = opacity === "" ? 1 : Number(opacity);
            // get the map's transform parameters from the style's transform matrix
            const matrix = (mapCanvas.style.transform).match(/^matrix\((.*)\)$/)[1].split(",").map(Number);
            // apply the transform to the exporting temp canvas's context
            context.setTransform(...matrix);
            context.drawImage(mapCanvas, 0, 0);
        }
    });
    context.setTransform(1, 0, 0, 1, 0, 0);
}

function addLegendsTo(context, {legendInfos, pos, columnWidth, height: maxHeight}) {
    // debugger;
    const margin = 10;
    let offsetX = margin;
    let offsetY = margin;
    const labelHeight = 22;
    const [legendBoxWidth, legendBoxHeight] = getLegendBoxDimension(margin, labelHeight, columnWidth, legendInfos, maxHeight);
    // re-adjust pos y according to legend Box Height
    pos.y += maxHeight - legendBoxHeight;
    // write legend title
    context.textBaseline = "bottom";
    context.fillStyle = "black";
    context.font = "bold 25px Times"
    context.fillText("Legends", pos.x + margin, pos.y - margin);
    // create white canvas on legendbox
    context.fillStyle = "white";
    context.fillRect(pos.x, pos.y, legendBoxWidth, legendBoxHeight);
    // configure text style
    context.fillStyle = "black";
    context.font = "100 18px Times";
    legendInfos.forEach(legend => {
        const itemHeight = legend.imgHeight + labelHeight + margin;
        if (offsetY + itemHeight > maxHeight) {
            offsetX += margin + columnWidth;
            offsetY = margin;
        }
        const left = pos.x + offsetX;
        const top = pos.y + offsetY;
        const img = document.createElement("img");
        // img.crossOrigin = "anonymous";
        // img.setAttribute("src", '/static/AFWatershed/images/Afghanistan_logo.png');
        img.setAttribute("src", legend.legendPath);
        context.fillText(legend.title, left, top + labelHeight);
        context.drawImage(img, left, top + labelHeight, legend.imgWidth, legend.imgHeight);
        // update to offsetY
        offsetY += itemHeight;
    });
    context.lineWidth = 1;
    context.closePath();
    context.strokeRect(pos.x, pos.y, legendBoxWidth, legendBoxHeight);
}

function getLegendBoxDimension(margin, labelHeight, columnWidth, legendInfos, maxBoxHeight) {
    let bottomMostLegendItemY = 0;
    const lastLegendItemPos = legendInfos.reduce((prevSize, legend) => {
        const itemHeight = legend.imgHeight + labelHeight + margin;
        if (prevSize.y + itemHeight > maxBoxHeight) {
            prevSize.x += margin + columnWidth;
            prevSize.y = margin;
        }
        prevSize.y += itemHeight;
        if (bottomMostLegendItemY < prevSize.y) bottomMostLegendItemY = prevSize.y;
        return prevSize;
    }, {x: margin, y: margin});
    const width = lastLegendItemPos.x + columnWidth + margin;
    const height = bottomMostLegendItemY;
    return [width, height];
}

function drawPolygon(context, color, coords) {
    context.lineWidth = 2;
    context.fillStyle = color;
    context.beginPath();
    context.moveTo(...coords[0]);
    for (let i = 1; i < coords.length; i++) {
        context.lineTo(...coords[i]);
    }
    context.closePath();
    context.fill();
}

function drawScaleBar(context, rightBottomPos) {
    const {width, text} = getScaleBarInfo();
    const height = 30;
    const margin = 8;
    const rightOffset = 15;
    const bottomOffset = 15;
    const pos = {
        x: rightBottomPos.x - (width + margin * 2) - rightOffset,
        y: rightBottomPos.y - (height + margin * 2) - bottomOffset
    };
    // draw background
    context.globalAlpha = 0.75;
    context.fillStyle = "grey";
    context.fillRect(pos.x, pos.y, width + margin * 2, height + margin * 2)
    context.globalAlpha = 1;
    context.lineWidth = 1.5;
    context.closePath()
    context.strokeStyle = "white";
    // draw the scale line shape
    const x = pos.x + margin;
    const y = pos.y + margin;
    context.beginPath()
    context.moveTo(x, y);
    context.lineTo(x, y + height)
    context.lineTo(x + width, y + height)
    context.lineTo(x + width, y);
    context.stroke()
    // write length text below the legend box
    context.textBaseline = "bottom";
    context.textAlign = "center"
    context.fillStyle = "white";
    context.font = "15px Times";
    context.fillText(text, x + width / 2, y + height - margin);
}

function createMapPDF(title, filename, mapCanvas, {margin, topMargin, mapFrameSize, pageDim, format}) {
    const pdf = new jsPDF("landscape", undefined, format);
    pdf.setFont("Times").setFontType("bold").setFontSize(15);
    pdf.text(title, parseInt(pageDim[0] / 2), 9, null, null, "center");
    try {
        pdf.addImage(mapCanvas.toDataURL("image/png"), "JPEG", margin, topMargin, mapFrameSize[0], mapFrameSize[1]);
        pdf.save(`${filename}.pdf`);
    } catch (error) {
        // showErrorToast("Error Occurred! Please try it again.");
        console.log(error);
    }
}

function getScaleBarInfo() {
    const scaleLine = document.querySelector(".ol-scale-line-inner");

    return {width: scaleLine.clientWidth, text: scaleLine.innerText};
}

function proxifyWMSLayers() {
    myApp.AllBindedLayersList.forEach(function (layerobj) {
        let properties = layerobj.getProperties();
        if (properties.changeWMSProxy) {
            let layer = layerobj.getLayer();
            if (properties.hasOwnProperty('ThreddsDataServerVersion')) {
                layer.AllLayersList.forEach(function (timeDimensionLayer) {
                    const source = timeDimensionLayer.getSource();
                    const currUrl = source.getUrls()[0];
                    currUrl.includes(PROXY_PREFIX) || source.setUrls([PROXY_PREFIX + currUrl]);
                });
            } else {
                const source = layer.getSource();
                if (layer.getSource().constructor === ol.source.TileWMS) {
                    const currUrl = source.getUrls()[0];
                    currUrl.includes(PROXY_PREFIX) || source.setUrls([PROXY_PREFIX + currUrl]);
                } else {
                    const currUrl = source.getUrl();
                    currUrl.includes(PROXY_PREFIX) || source.setUrl(PROXY_PREFIX + currUrl);
                }
            }
        }
    });

}

function deproxifyWMSLayers() {
    console.log('--------deproxy');
    myApp.AllBindedLayersList.forEach(function (layerobj) {
        let properties = layerobj.getProperties();
        if (properties.changeWMSProxy) {
            let layer = layerobj.getLayer();
            if (properties.hasOwnProperty('ThreddsDataServerVersion')) {
                layer.AllLayersList.forEach(function (timeDimensionLayer) {
                    const source = timeDimensionLayer.getSource();
                    source.setUrls([source.getUrls()[0].replace(PROXY_PREFIX, "")]);
                });
            } else {
                const source = layer.getSource();
                if (layer.getSource().constructor === ol.source.TileWMS) {
                    source.setUrls([source.getUrls()[0].replace(PROXY_PREFIX, "")]);
                } else {
                    source.setUrl(source.getUrl()[0].replace(PROXY_PREFIX, ""));
                }
            }
        }
    });
}


myApp.WarningToast = function (message) {
    $.toast({
        heading: 'Warning',
        text: message,
        showHideTransition: 'plain',
        icon: 'warning',
        position: 'top-center'
    })
}
