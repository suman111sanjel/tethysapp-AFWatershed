myApp.myMap = function () {
    // var bounds = [7505834.272637911, 2173824.4936588546, 11292218.905772403, 4414346.666753941]// var zoomToExtentControl = new ol.control.ZoomToExtent({
    //     extent: bounds
    // });

    //for adjusting View
    //     ol.proj.transform(myApp.map.getView().getCenter(), 'EPSG:3857', 'EPSG:4326')

    // let bbox=myApp.map.getView().calculateExtent()
    // let longMinLatMin=ol.proj.transform([bbox[0],bbox[1]], 'EPSG:3857', 'EPSG:4326')
    // let longMaxLatMax=ol.proj.transform([bbox[2],bbox[3]], 'EPSG:3857', 'EPSG:4326')



    myApp.view = new ol.View({
        center: ol.proj.transform([68.4931296981239, 34.01881012957911], 'EPSG:4326', 'EPSG:3857'),
        zoom: 5.460313685949168,
        // extent:[6053035.553709263, 3378871.474829893, 9196205.087956328, 4683784.618572736]
    });

    var OSMLayer = new ol.layer.Tile({
        id: "osm",
        title: "Open Street Map",
        visible: true,
        opacity: 0.7,
        source: new ol.source.OSM(),
        mask: 0
    });

    myApp.BaseLayerList = [OSMLayer];
    // var HighLightedLayerSource = new ol.source.Vector();
    myApp.Drawsource = new ol.source.Vector({wrapX: false});

    var mousePositionControl = new ol.control.MousePosition({
        coordinateFormat: ol.coordinate.createStringXY(4),
        projection: 'EPSG:4326',
        // comment the following two lines to have the mouse position
        // be placed within the map.
        //className: 'custom-mouse-position',
        //target: document.getElementById('mouse-position'),
        undefinedHTML: ''
    });

    var fullScreenMode = new ol.control.FullScreen();

    var scaleType = 'scaleline';
    var scaleBarSteps = 4;
    var scaleBarText = true;
    var control;

    function scaleControl() {
        control = new ol.control.ScaleLine({
            units: 'metric'
        });
        return control;
    }

    var layers = [];
    layers.push(OSMLayer);
    // layers.push(myApp.HighLightedLayer);
    myApp.map = new ol.Map({
        target: 'map-container',
        layers: layers,
        // renderer: 'canvas',
        // controls: ol.control.defaults({
        //     attribution: false
        // }).extend([
        //     mousePositionControl,
        // ]),
        controls: ol.control.defaults({
            attribution: false
        }).extend([scaleControl()]),
        view: myApp.view,
        loadTilesWhileAnimating: true,
    });
    // myApp.map.getView().fit(bounds);


    // let ExtentButton = document.querySelector('.ol-zoom-extent button');
    // let extentHomeI = myApp.createI('glyphicon glyphicon-home');
    // ExtentButton.innerText = "";
    // ExtentButton.style.paddingRight = "2px";
    // ExtentButton.append(extentHomeI);
}

myApp.init = function () {
    myApp.myMap();
    myApp.LoadDefaults();
    myApp.layerswitcher();
    myApp.DrawUI();
    myApp.CreateAccordianCardsLayerGrouups();
    myApp.addingLayersToMap();
    myApp.BindControls();
    myApp.addingChooseOptionToSelect();
    myApp.initialSelectedWatershedBasin();
    myApp.InitOwlCarousel();
    $("#select_Watershed").val("19");
    $("#select_Watershed").trigger("change");
}

myApp.init();

