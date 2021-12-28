//global variables
let isDashboard = true;
let teraiGeoJSON = null;
var current_mode = "BAT", select_line;
var process, MHPAllDetail;
var select;
var newMHP_point, newMHP_selected_arcid, newMHP_processing_type, newMHP_project_id;
var line_selected_check = false;
var forsavingdataProject, forsavingdataProjectDetail;

function zoomToProjectExtent() {
    if ($('#ppp').length) // use this if you are using id to check
    {
        projectID = $('#ppp').attr("projectID");
        $.ajax({
            url: '/project-extent',
            data: {
                id: projectID
            },
            success: function (data) {
                map.getView().fit(data.extent, map.getSize());
            }
        })
    }
}

function resetResultSection(resetMessage)

{
    const resultsHTML = `
        <div class='result-description clearfix' id='accordion'>
            <div class="result-main">
                <a data-toggle="collapse" data-parent="#accordion" href="#collapse1">
                    <div class="result-evaluate">
                        <div class="result-shape"><i class="fa fa-angle-up"></i></div>
                    </div>
                </a>
                <div id="collapse1" class="panel-collapse collapse in">
                    <div class="table-bar-main row">
                        <div class="col-sm-12">
                            <div class="tab-content">
                                <div id="scenario" class="tab-pane fade in active">
                                    <div class="alert alert-success">${ resetMessage }</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
`
    $('.results-wrap').html(resultsHTML);
}

function closeCurrentProject() {
    // remove the old title
    $('#projectname').empty();

    // remove bat project's layer
    clusterLayer.getSource().clear();
    batPolygonOverlay.getSource().clear();
    // remove mhp project's layer
    ['Dam', 'Power_House', 'Upstreams', 'Upstreams', 'AOI'].forEach(layerId => {
        getLayer(layerId).getSource().clear();
    });
    // sampling project layer
    getLayer('spatialsamplingtool').getSource().clear();
    // add select a project or complete the project
    resetResultSection("Select a project or complete the project");
}

function selectRegion(in_scode, in_sdd, in_ddmmm) {
    const $selState = $('.selState')
    const $selDistrict = $('.selDistrict');
    const $selGaunagar = $('.selGaunagar');

    const dcode = parseInt(in_sdd.toString().slice(1));
    const allSDDs = state2Dist[in_scode]["dcode"];
    const allDDMMMs = gapanapaCode[dcode];

    // selecting the scode
    $selState.val(parseInt(in_scode));
    $selState.trigger('change');
    // adding the districts options
    const districtOptionHTML = allSDDs.reduce(
        (prevHTML, currSdd, i) => prevHTML + `<option value="${currSdd}">${state2Dist[in_scode]["dist"][i]}</option>`,
        ""
    );
    $selDistrict.html(districtOptionHTML);
    // selecting the district
    $selDistrict.val(parseInt(in_sdd));
    $selDistrict.trigger('change');
    // adding the gapanapa options
    const gapanapaOptionsHTML = allDDMMMs.reduce(
        (prevHTML, currDdmmm, i) => prevHTML + `<option value="${currDdmmm}">${gapanapa[dcode][i]}</option>`,
        ""
    );
    $selGaunagar.html(gapanapaOptionsHTML);
    $selGaunagar.val(parseInt(in_ddmmm));
    $selGaunagar.trigger('change');
}

function MakeGoToInputLocationButton() {
    // the main outer container div
    const $goToInputLocContainer = $('<div/>');
    $goToInputLocContainer
        .addClass('ol-unselectable ol-control added-button')
        .css({ left: "0.5em", top: "181px" })
        .attr("id", 'go-to-input-loc-button')
        .attr("title", "Go to input Longitude, Latitude");
    // button to toggle the input field
    const $inputToggler = $('<button/>');
    $inputToggler.html('<i style="color: white;" class="fas fa-search-location"></i>');
    // the actual input for entering location
    const $locationInput = $('<input/>');
    $locationInput
        .attr('type', "text")
        .addClass("form-control");
    const $form = $('<form/>');
    $form.append($locationInput);
    // append the toggler and input into the main container
    $goToInputLocContainer.append($inputToggler);
    $goToInputLocContainer.append($form);
    // setting the on change handler
    $form.submit(event => {
        event.preventDefault();
        const inputValue = $locationInput.val();
        const lonLatInStr = inputValue.includes(",") ? inputValue.split(",") : inputValue.split(" ");
        const lonLat = lonLatInStr.map(parseFloat);
        if (!(lonLat.some(isNaN)) && lonLat.length === 2) {
            const view = map.getView();
            view.animate(
                {
                    center: lonLat,
                    easing: ol.easing.inAndOut
                },
                {
                    zoom: 10,
                    duration: 2000,
                    easing: ol.easing.inAndOut
                });
            // view.setZoom( 12 );
        }
    });
    // hide the input on default
    $form.hide();
    // setting the click handler
    $inputToggler.click(() => $form.toggle());
    return $goToInputLocContainer;
}

function getMapScaleDenominator(map) {
    const dpi = window.devicePixelRatio * 96;
    const metersPerMapUnit = ol.proj.METERS_PER_UNIT[map.getView().getProjection().getUnits()];
    const inchesPerMapUnit = metersPerMapUnit * 39.37007874;
    const groundDistanceInInchesPerInch = map.getView().getResolution() * dpi * inchesPerMapUnit;
    return groundDistanceInInchesPerInch;
}

//setting
function openSideNav() {
    const settingNav = document.getElementById("settingNav");
    settingNav.style.display = 'block';
    setTimeout(() => settingNav.setAttribute("style", "width: 250px; opacity: 1"), 100);
}

/* Set the width of the side navigation to 0 */
function closeNav() {
    const settingNav = document.getElementById("settingNav");
    settingNav.style.width = 0;
    settingNav.style.opacity = 0;
    settingNav.addEventListener('transitionend', event => event.target.style.display = "none", { once: true });
}

const capitalize = text => text.slice(0, 1).toUpperCase() + text.slice(1).toLowerCase();

$("#catchmentapiprocessing").on("click", function () {
    var P = parseFloat($('#tab1-power').val());
    var Q = parseFloat($('#tab1-flow-rate').val());
    var intvMHP = parseInt($('#id_interval').val());
    mhp_interval = intvMHP
    if (P && Q) {
        $('#largeModal').modal('hide');
        MHPProcessing(newMHP_point, newMHP_selected_arcid, newMHP_processing_type, P, Q, newMHP_project_id, intvMHP);
    }
});

function MHPStreamSelectInteraction() {
    select_line.on('select', function (e) {
        if (e.selected[0]) {
            line_selected_check = true;
            var selected_arcid = e.selected[0].get('arcid');
            var format_line = new ol.format.WKT();
            var selected_line = format_line.writeGeometry(e.selected[0].getGeometry());
            //checking weather project is loaded or not
            var working_project = $("#projectname #ppp");
            var processing_type = 1;
            var project_id = 0;

            // for new MHP processing
            newMHP_selected_arcid = selected_arcid;
            newMHP_processing_type = processing_type;
            newMHP_project_id = project_id;

            if (working_project.length) {
                project_id_current = $('#ppp').attr('projectid');
                MHPProcessing(point, newMHP_selected_arcid, newMHP_processing_type, mhp_power_in_kw, mhp_discharge, project_id_current, mhp_interval);
            } else {
                $('#largeModal').modal('show');
            }
        }

        map.removeInteraction(select_line);
        map.addInteraction(select);


    });

}

function MHPProcessing(point, selected_arcid, processing_type, P, Q, project_id, intervalMHP) {
    var process = $("#loader-ouer");
    $.ajax({
        //type: "POST",
        url: "/MultileMHPAPI/",
        data: {
            point: point,
            arcid: selected_arcid,
            process_type: processing_type,
            p: P,
            q: Q,
            project_ID: project_id,
            intervalMHP: intervalMHP
        },
        beforeSend: function () {
            process.show()
        },
        success: function (data) {
            if (select_line) {
                select_line.getFeatures().clear();
            }
            if (data.invalid) {
                if (data.has_next_stream) {
                    swal({
                        title: "Boundry Error",
                        text: "Intake and Powerhouse must be inside single GauNagarpalika."
                    });
                    batPolygonOverlay.getSource().clear();
                    drawSource.clear();
                    clusterLayer.getSource().clear();
                } else {
                    swal({
                        title: "Downstream Error",
                        text: "You Don't have enough streams for that height"
                    });
                    batPolygonOverlay.getSource().clear();
                    drawSource.clear();
                    clusterLayer.getSource().clear();
                }
            } else {
                $('.results-wrap').html("");
                $('.results-wrap').append(data);
                batPolygonOverlay.getSource().clear();
                drawSource.clear();
                clusterLayer.getSource().clear();
            }
        },
        error: error => {
            swal({
                title: "Error",
                text: `Error ${error.status}: ${error.statusText}`,
            });
            batPolygonOverlay.getSource().clear();
            drawSource.clear();
            clusterLayer.getSource().clear();
        },
        complete: () => process.hide(),
    });
}


function AOIGrenerationMHP() {
    // console.log("AOIGrenerationMHP function");
    // console.log(MHPAllDetail);
    var MHPALLlenght = MHPAllDetail.length;
    getLayer("AOI").getSource().clear();
    for (var i = 0; i < MHPALLlenght; i++) {

        $.ajax({
            url: "/MHPAOIJSON/",
            data: {
                power: MHPAllDetail[i].power,
                wkt: MHPAllDetail[i].wkt,
                demandPHH: MHPAllDetail[i].demandPHH,
            },
            success: function (data) {
                var parser = new ol.format.GeoJSON();
                var result_location = parser.readFeatures(data);
                as_geojson_location = parser.writeFeatures(result_location, {
                    featureProjection: 'EPSG:4326',
                    dataProjection: 'EPSG:4326'
                });

                var features_location = parser.readFeatures(as_geojson_location);
                getLayer("AOI").getSource().addFeatures(features_location);

                var my_extent = getLayer("AOI").getSource().getExtent();
                map.getView().fit(my_extent, map.getSize());
            }
        });
    }
}

$(document).delegate("#submit", "vclick", function () {
    alert($("#flip-1").val());
});

//setting

$(window).on('load', function () {
    $('.modal-dialog.resize').parent().css(
        'box-shadow', 'none'
    );
});

$(document).ready(function () {

    var project_selected;
    init();

    $('button.navbar-toggle').on('click', function () {
        $('.sidebar ').toggleClass('is-active');
        if ($('.sidebar ').hasClass('is-active')) {
            $('.sidebar').css('visibility', 'visible');
        }
        else {
            $('.sidebar').css('visibility', 'hidden');
        }
    });
    //show-hide export
    $(".export-icon").on("click", function (e) {
        $(".export").addClass("expanded");
        $(".export-icon").hide();
        $(".results-icon").hide();
        $("html, body").animate({
            scrollTop: $(document).height()
        }, 1000);
    });

    $(".close-export").on("click", function (e) {
        $(".export").removeClass("expanded");
        $(".export-icon").show();
        $(".results-icon").show();
    });

    // this is used for tool selection on the project
    $(".tools-sel").on('change', function () {
        // removing if there are any map interactions left
        removeAllToolInteractions()
        const toolSelectContainer = $('.switch');
        var currentToolSpan = $('.sub-project');
        var $projectNameSpan = $("#projectname");
        $projectNameSpan.text("");
        var toolLayersContainer = $('.tab');
        var toolLayersAccordion = $('.sampling-accor');
        var selectedTool = $(this).children("option:selected").val();
        if (selectedTool == "MHP") {
            toolLayersContainer.addClass('enabled');
            currentToolSpan.text('[ MHP ]');

            toolLayersAccordion.removeClass('enabled-sst');
            $(".absolute-block.btm-left.tooltip-width").show()
        } else if (selectedTool == "BAT") {
            toolSelectContainer.removeClass("mhp");
            toolSelectContainer.removeClass('sst');

            toolLayersContainer.removeClass('enabled');
            currentToolSpan.text('[ BAT ]');

            toolLayersAccordion.removeClass('enabled-sst');
            $(".absolute-block.btm-left.tooltip-width").show()
        } else if (selectedTool == "SS") {
            toolSelectContainer.removeClass("mhp");
            toolSelectContainer.addClass('sst');


            toolLayersContainer.removeClass('enabled');
            currentToolSpan.text('[ SST ]');

            toolLayersAccordion.addClass('enabled-sst');
            $(".absolute-block.btm-left.tooltip-width").show();
        }
        // reappend the empty project name span into it's container
        currentToolSpan.append($projectNameSpan);
    });

    //resize
    $('.btn-resize').click(function () {
        var resize = $('.resize');
        resize.toggleClass('md');
        if (resize.hasClass('md')) {
            resize.find('.flex-box').toggleClass('disabled');
        } else {
            resize.find('.flex-box').removeClass('disabled');
        }
    })

    //show-hide results
    $(".results-icon").on("click", function (e) {
        $(".results").addClass("expanded");
        $(".results-icon").hide();
        $(".export-icon").hide();
        $("html, body").animate({
            scrollTop: $(document).height()
        }, 1000);
    });

    $(document).on("click", ".results .close-button", function (e) {
        $(".results").removeClass("expanded");
        $(".results-icon").show();
        $(".export-icon").show();
    });

    //Tooltip
    $('[data-toggle="tooltip"]').tooltip({
        'placement': 'top'
    });
    //Scrollbar
    $('.scrollbar-macosx').scrollbar();

    /** Sticky Header **/
    $(window).scroll(function () {
        if ($(this).scrollTop() > 200) {
            $('.header-navigation').addClass("sticky-header").css('top', '-150px');
            $("#brand-logo").attr("src", "images/logo.png");
        } else {
            $('.header-navigation').removeClass("sticky-header").css('top', '0');
            $("#brand-logo").attr("src", "images/logo-white.png");
        }

        if ($(this).scrollTop() > 500) {
            $('.sticky-header').addClass("slow").css('top', '0').fadeTo(500, 1);
        } else {
            $('.sticky-header').removeClass("slow");
            $('.sticky-header').css('top', '-150px');
        }
    });

    // Declare Carousel jquery object
    var owl = $('.banner-wrap');
    // Carousel initialization
    owl.owlCarousel({
        loop: false,
        margin: 0,
        navSpeed: 500,
        nav: false,
        pagination: true,
        autoplay: true,
        autoplayHoverPause: true,
        rewind: true,
        items: 1
    });
    $('.map-carousel').owlCarousel({
        loop: false,
        nav: true,
        margin: 10,
        responsive: {
            0: { items: 1 },
            550: { items: 2 },
            1000: { items: 3 }
        }
    });


    // add animate.css class(es) to the elements to be animated
    function setAnimation(_elem, _InOut) {
        // Store all animationend event name in a string.
        // cf animate.css documentation
        var animationEndEvent = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';

        _elem.each(function () {
            var $elem = $(this);
            var $animationType = 'animated ' + $elem.data('animation-' + _InOut);

            $elem.addClass($animationType).one(animationEndEvent, function () {
                $elem.removeClass($animationType); // remove animate.css Class at the end of the animations
            });
        });
    }

    // Fired before current slide change
    owl.on('change.owl.carousel', function (event) {
        var $currentItem = $('.owl-item', owl).eq(event.item.index);
        var $elemsToanim = $currentItem.find("[data-animation-out]");
        setAnimation($elemsToanim, 'out');
    });

    // Fired after current slide has been changed
    var round = 0;
    owl.on('changed.owl.carousel', function (event) {

        var $currentItem = $('.owl-item', owl).eq(event.item.index);
        var $elemsToanim = $currentItem.find("[data-animation-in]");

        setAnimation($elemsToanim, 'in');
    })

    owl.on('translated.owl.carousel', function (event) {
        if (event.item.index == (event.page.count - 1)) {
            if (round < 1) {
                round++
            } else {
                owl.trigger('stop.owl.autoplay');
                var owlData = owl.data('owl.carousel');
                owlData.settings.autoplay = true; //don't know if both are necessary
                owlData.options.autoplay = true;
                owl.trigger('refresh.owl.carousel');
            }
        }
    });

    /*Equal MaxHeight  */
    var elements = $('.js-equal-height');
    elements.removeAttr('style');
    var maxHeight = -1;
    elements.each(function () {
        maxHeight = maxHeight > $(this).height() ? maxHeight : $(this).height();
    });
    elements.each(function () {
        $(this).height(maxHeight);
    })
    $(window).resize(function () {
        elements.removeAttr('style');
        setTimeout(function () {
            var maxHeight = -1;
            elements.each(function () {
                maxHeight = maxHeight > $(this).height() ? maxHeight : $(this).height();
            });
            elements.each(function () {
                $(this).height(maxHeight);
            })
        }, 500)
    })

    /*Equal MaxHeight  */
    var elements = $('.js-equal-height2');
    elements.removeAttr('style');
    var maxHeight = -1;
    elements.each(function () {
        maxHeight = maxHeight > $(this).height() ? maxHeight : $(this).height();
    });
    elements.each(function () {
        $(this).height(maxHeight);
    })
    $(window).resize(function () {
        elements.removeAttr('style');
        setTimeout(function () {
            var maxHeight = -1;
            elements.each(function () {
                maxHeight = maxHeight > $(this).height() ? maxHeight : $(this).height();
            });
            elements.each(function () {
                $(this).height(maxHeight);
            })
        }, 500)
    })
    //Bootstrap Carousel
    $(".carousel").swipe({

        swipe: function (event, direction, distance, duration, fingerCount, fingerData) {

            if (direction == 'left') $(this).carousel('next');
            if (direction == 'right') $(this).carousel('prev');

        },
        allowPageScroll: "vertical"

    });

    //Fancybox
    $('.fancybox').fancybox({
        helpers: {
            title: {
                type: 'inside'
            },
        },
    });


    $('.time-carousel').owlCarousel({
        center: true,
        loop: false,
        items: 1,
        nav: true
    });

    $('.chart-carousel').owlCarousel({
        loop: true,
        items: 3,
        margin: 10,
        nav: true,
        navSpeed: 1000,
        autoplayHoverPause: true,
        autoplay: false,
    });

    $(document).on('click', '.owl-item>div', function () {
        owl.trigger('to.owl.carousel', $(this).data('position'));
    });

    //on click item selection
    $('.section').find('.list-style li').on('click', function (elem) {
        $("li").removeClass("current-item");
        $(this).addClass('current-item');
        if (that.itemClicked) {
            that.itemClicked('hello i am here');
        }
    });

    // ############### Ending of Design Section ###############################

    var suitable_energy = {
        1: {
            'solar': true,
            'grid': false,
            'mhp': false
        },
        2: {
            'solar': false,
            'grid': false,
            'mhp': true
        },
        3: {
            'solar': true,
            'grid': false,
            'mhp': true
        },
        4: {
            'solar': false,
            'grid': true,
            'mhp': false
        },
        5: {
            'solar': true,
            'grid': true,
            'mhp': false
        },
        6: {
            'solar': false,
            'grid': true,
            'mhp': true
        },
        7: {
            'solar': true,
            'grid': true,
            'mhp': true
        },
        0: {
            'solar': false,
            'grid': false,
            'mhp': false
        }
    };

    //for draw tool
    $(document).on("click", ".draw-title", function () {
        batPolygonOverlay.getSource().clear();
        drawSource.clear();
        clusterLayer.getSource().clear();
        var drawtype = $(this).attr("drawtype");
        addDrawInteraction(drawtype);
    });
    const $selState = $(".selState");
    let scodeBeforeFocus = 0; // var to store scode before focus clear selState
    $selState.on('focus', () => {
        scodeBeforeFocus = $selState.val();
        $selState.val("none")
    });
    $selState.on('blur', (event) => {
        if (event.target.value === "none") {
            event.target.value = scodeBeforeFocus;
        }
    });
    $selState.change(function () {
        var scode = $selState.val();
        selected_adminid = scode;
        // if the switch-map has the link to go to MEP tools visible,
        // then this is the dashboard, and the chart has to be shown
        if (isDashboard) {
            highchartDataAjaxCall('Country', scode);
        }
        // console.log(feature);
        var htmtxt = '';
        var ext = adminState[$selState.val()];
        // console.log(ext);
        map.getView().fit(ext, map.getSize());
        for (var i = 0; i < state2Dist[scode]["dcode"].length; i++) {
            htmtxt += '<option value="' + state2Dist[scode]["dcode"][i] + '">' + capitalize(state2Dist[scode]["dist"][i]) + "</option>"
        }
        htmtxt += '<option value="none" hidden>Select One</option>';

        var html = '<option value="none" selected="selected">None</option>';
        if (scode === '0') {
            // dropDownLayerSelection(layerOption['country'], scode);
            $('.selDistrict').empty();
            $('.selDistrict').append(html);

            $('.selGaunagar').empty();
            $('.selGaunagar').append(html);
            $('.selState').val(scode);
        } else {
            // dropDownLayerSelection(layerOption['state'], scode);
            $('.selDistrict').empty();
            $('.selDistrict').append(htmtxt);

            $('.selGaunagar').empty();
            $('.selGaunagar').append(html);
            $('.selState').val(scode);
        }
        mapNavigator.handleStateSelection(parseInt(scode), true);
        $selState.blur();
    });

    const $selDistrict = $(".selDistrict");
    let dcodeBeforeFocus = null; // var to store dcode before focus clear selDistrict
    $selDistrict.on('focus', () => {
        dcodeBeforeFocus = $selDistrict.val();
        $selDistrict.val("none");
    });
    $selDistrict.on('blur', () => {
        if ($selDistrict.val() === "none") {
            $selDistrict.val(dcodeBeforeFocus);
        }
    });
    $selDistrict.change(function () {
        var htmtxt = '';
        var dcode = $(this).val();
        var scode = $(this).parent().children('.selState').val();
        // if the switch-map has the link to go to MEP tools visible,
        // then this is the dashboard, and the chart has to be shown

        if (dcode === scode) {
            selected_adminid = scode;
            var ext = adminState[scode];
            map.getView().fit(ext, map.getSize());
            if (isDashboard) {
                highchartDataAjaxCall('Country', scode)
            }
            var scode = $('.selState').val();
            var html = '<option value="none" selected="selected">None</option>';
            $('.selGaunagar').empty();
            $('.selDistrict').val(dcode);
            $('.selGaunagar').append(html);
        } else {
            selected_adminid = dcode;
            if (isDashboard) {
                highchartDataAjaxCall('District', dcode)
            }
            var dcode_old = select_district(dcode);
            for (var i = 0; i < gapanapaCode[String(parseInt(dcode_old))].length; i++) {
                htmtxt += '<option value="' + gapanapaCode[String(parseInt(dcode_old))][i] + '">' + gapanapa[String(parseInt(dcode_old))][i] + "</option>"
            }
            $('.selDistrict').val(dcode);
            $('.selGaunagar').empty();
            $('.selGaunagar').append(htmtxt);
        }
        mapNavigator.handleDistrictSelection(parseInt(dcode.slice(1)), null, true);
        $selDistrict.blur();
    });

    // required layers: mhpProjectsOwned, mhpProjectsOthers, batProjectsOwned, batProjectsOthers
    const addMunicipalityProjectsLayers = (ddmmm) => {
        const replaceFeaturesInLayers = (ownedLayer, othersLayer, geoJSONData) => {
            const ownedSource = ownedLayer.getSource();
            const othersSource = othersLayer.getSource();
            // clearing sources
            ownedSource.clear();
            othersSource.clear();
            // reading and adding features to layer's source
            const geoJsonFormat = new ol.format.GeoJSON();
            ownedSource.addFeatures(geoJsonFormat.readFeatures(geoJSONData["owned"]));
            othersSource.addFeatures(geoJsonFormat.readFeatures(geoJSONData["others"]));
        };

        fetch(`/projects/${ddmmm}`)
            .then(response => response.json())
            .then(json => replaceFeaturesInLayers(ownedProjectsLayer, othersProjectsLayer, json))
            .catch(() => showErrorToast("Couldn't load projects"));

    };

    const $selGaunagar = $(".selGaunagar");
    $selGaunagar.change(function () {
        // if the switch-map has the link to go to MEP tools visible,
        // then this is the dashboard, and the chart has to be shown
        var gcode = $(this).val();
        if (gcode == '00') {
            var dcode = $('.selDistrict').val();
            selected_adminid = dcode;
            $('.selGaunagar').val('00');
            select_district(dcode)
            if (isDashboard) {
                highchartDataAjaxCall('District', dcode)
            }
        } else {
            var ext = adminGauNagar[gcode];
            $('.selGaunagar').val(gcode);
            var scode_c = parseInt($(this).parent().children('.selState').val());
            // var dcode_c
            var dcode_c = Math.floor(gcode / 1000);
            var mcode_c = gcode % 1000;
            var adminid_sddmmm = (scode_c * 100 + dcode_c) * 1000 + mcode_c;
            selected_adminid = (scode_c * 100 + dcode_c) * 100 + mcode_c;
            if (isDashboard) {
                highchartDataAjaxCall('Municipality', adminid_sddmmm, selected_adminid)
                const municipalityCode = parseInt(gcode);
                if (municipalityCode) {
                    addMunEnergyData(municipalityCode); // this will also add the mundata-download-link 
                }
                else {
                    // removing extra divs of municipal energy chart
                    const nInitialDivs = total_item;
                    const nCurrentDivs = $(".count-item").length;
                    for (let i = nCurrentDivs - 1; i > (nInitialDivs - 1); i--) {
                        $('.owl-carousel').trigger('remove.owl.carousel', i).trigger('refresh.owl.carousel');
                    }
                    // fade out the loading modal
                    $('#loading-modal').fadeOut()
                }
            }
            addMunicipalityProjectsLayers(gcode);
            map.getView().fit(ext, map.getSize());
        }
        const sddCode = $('.selDistrict').val();
        const sddmm = sddCode + gcode.slice(-2)
        mapNavigator.handleMunicipalitySelection(parseInt(sddmm), true);
    });

    map.getView().on('propertychange', function (e) {
        switch (e.key) {
            case 'resolution':
                if (map.getView().getResolution() < 0.00069) {
                    $('#buildings').attr('disabled', false);
                    $('#gaunagar').attr('disabled', false);
                    $('#settlement').attr('disabled', false);
                } else {
                    $('#buildings').attr('disabled', true);
                    $('#gaunagar').attr('disabled', true);
                    $('#settlement').attr('disabled', true);
                }
                break;
        }
    });


    select = new ol.interaction.Select({
        layers: [batPolygonOverlay]
    });
    select.set('name', 'select');


    var modify = new ol.interaction.Modify({
        features: select.getFeatures()
    });
    modify.set('name', 'modify');
    /**
     * Create an overlay to anchor the popup to the map.
     */
    var container = document.getElementById('popup');
    var content = document.getElementById('popup-content');
    var closer = document.getElementById('popup-closer');


    /**
     * Create an overlay to anchor the popup to the map.
     */
    var overlay = new ol.Overlay({
        element: container,
        autoPan: true,
        autoPanAnimation: {
            duration: 250
        }
    });

    map.addOverlay(overlay);
    /**
     * Add a click handler to hide the popup.
     * @return {boolean} Don't follow the href.
     */
    closer.onclick = function () {
        overlay.setPosition(undefined);
        closer.blur();
        return false;
    };

    function energySuitablePopup(value) {
        $('#grid-suitable-check').empty();
        if (suitable_energy[value].grid) {
            $('#grid-suitable-check').append('<i class="fa fa-check"></i>');

        } else {
            $('#grid-suitable-check').append('<i class="fa fa-times"></i>');
        }

        $('#solar-mini-suitable-check').empty();
        $('#solar-mini-grid-suitable-check').empty();
        if (suitable_energy[value].solar) {
            $('#solar-mini-suitable-check').append('<i class="fa fa-check"></i>');
            $('#solar-mini-grid-suitable-check').append('<i class="fa fa-check"></i>');

        } else {
            $('#solar-mini-suitable-check').append('<i class="fa fa-times"></i>');
            $('#solar-mini-grid-suitable-check').append('<i class="fa fa-times"></i>');
        }

        $('#mhp-suitable-check').empty();
        if (suitable_energy[value].mhp) {
            $('#mhp-suitable-check').append('<i class="fa fa-check"></i>');

        } else {
            $('#mhp-suitable-check').append('<i class="fa fa-times"></i>');
        }

    }

    /* code for spatial restriction */
    var rewindedPolygons;
    var conditionNoModifierKeysWithin;
    var pointerMoveHandler;


    //restriction layer
    /**
     * Currently drawn feature.
     * @type {ol.Feature}
     */
    var sketch;
    /**
     * The help tooltip element.
     * @type {Element}
     */
    var helpTooltipElement;
    /**
     * Overlay to show the help messages.
     * @type {ol.Overlay}
     */
    var helpTooltip;
    /**
     * Message to show when the user is drawing a polygon.
     * @type {string}
     */
    var continuePolygonMsg = 'Click to continue drawing the polygon';

    var avoidDrawingHere = 'You are outside the allowed area to draw';

    /**
     * Handle pointer move.
     * @param {ol.MapBrowserEvent} evt The event.
     */
    var key;
    var drawTool; // global so we can remove it later
    function createHelpTooltip() {
        if (helpTooltipElement) {
            helpTooltipElement.parentNode.removeChild(helpTooltipElement);
        }
        helpTooltipElement = document.createElement('div');
        helpTooltipElement.className = 'tooltip hidden';
        helpTooltip = new ol.Overlay({
            element: helpTooltipElement,
            offset: [10, 0],
            positioning: 'center-left'
        });
        helpTooltip.set('name', 'helpTooltip');
        map.addOverlay(helpTooltip);
    }

    /*  end code for spatial restriction */
    function addDrawInteraction(drawtype) {
        map.removeLayer(vectorLayer2);
        removeAllToolInteractions();
        if (drawtype == 'Point') {
            // console.log('point');
            var geometryFunction, maxPoints;
            map.getViewport().style.cursor = "crosshair";
            drawTool = new ol.interaction.Draw({
                source: drawSource,
                type: /** @type {ol.geom.GeometryType} */ (drawtype),
                geometryFunction: geometryFunction,
                maxPoints: maxPoints
            });
            drawTool.set('name', 'drawTool');
            drawTool.on('drawend', function (e) {
                // console.log('point_added');
                sketch = null;
                lastFeature = e.feature;
                map.getViewport().style.cursor = "pointer";
                var co = lastFeature.getGeometry().getCoordinates();
                var format = new ol.format.WKT();
                point = format.writeGeometry(lastFeature.getGeometry());
                $.ajax({
                    url: "/point_query_energy",
                    data: {
                        point: point,
                    },
                    success: function (data, status) {
                        energySuitablePopup(parseInt(data.result))
                    }
                });
                overlay.setPosition(co);
                map.removeInteraction(drawTool);
                ol.Observable.unByKey(key);
            });
            drawTool.on('drawstart', function (e) {
                drawSource.clear();
                $('.legends').addClass("hidden");
                sketch = e.feature;
            });

            map.addInteraction(drawTool);

        }
        if (drawtype == 'Polygon') {
            key = map.on('pointermove', pointerMoveHandler);

            map.getViewport().addEventListener('mouseout', function () {
                helpTooltipElement.classList.add('hidden');
            });
            var geometryFunction, maxPoints;
            map.getViewport().style.cursor = "crosshair";
            drawTool = new ol.interaction.Draw({
                condition: conditionNoModifierKeysWithin,
                freehandCondition: ol.events.condition.never,
                source: drawSource,
                type: /** @type {ol.geom.GeometryType} */ (drawtype),
                geometryFunction: geometryFunction,
                maxPoints: maxPoints
            });
            drawTool.set('name', 'drawTool');
            drawTool.on('drawend', function (e) {
                sketch = null;
                lastFeature = e.feature;
                map.getViewport().style.cursor = "default";
                var co = lastFeature.getGeometry().getCoordinates();
                polygon = JSON.stringify(co);

                var format = new ol.format.WKT();
                poly = format.writeGeometry(lastFeature.getGeometry());
                $('#ppp').textContent
                var process = $("#loader-ouer")
                if ($('#ppp').length) // use this if you are using id to check
                {
                    projectID = $('#ppp').attr("projectID");
                    // result of household data
                    $.ajax({
                        //type: "POST",
                        url: "/zonal_stats_existing",
                        data: {
                            poly: poly,
                            projectID: projectID
                        },
                        beforeSend: function () {
                            process.show()
                        },
                        success: function (data, status) {
                            if (data.invalid) {
                                swal({
                                    title: "Boundry Error",
                                    text: "Polygon must be inside single GauNagarpalika."
                                });
                                batPolygonOverlay.getSource().clear();
                                drawSource.clear();
                                clusterLayer.getSource().clear();

                            } else {
                                $('.results-wrap').empty();
                                $('.results-wrap').append(data);
                            }
                        },
                        error: error => {
                            swal({
                                title: "Error",
                                text: `Error ${error.status}: ${error.statusText}`,
                            });
                        },
                        complete: () => process.hide()
                    });
                } else {
                    $.ajax({
                        //type: "POST",
                        url: "/zonal_stats_new",
                        data: {
                            poly: poly,
                        },
                        beforeSend: function () {
                            process.show();
                        },
                        success: function (data) {
                            if (data.invalid) {
                                swal({
                                    title: "Boundry Error",
                                    text: "Polygon must be inside single GauNagarpalika."
                                });
                                batPolygonOverlay.getSource().clear();
                                drawSource.clear();
                                clusterLayer.getSource().clear();
                            }
                            else {
                                $('.results-wrap').html("");
                                $('.results-wrap').append(data);
                            }
                        },
                        error: error => {
                            swal({
                                title: "Error",
                                text: `Error ${error.status}: ${error.statusText}`,
                            });
                        },
                        complete: () => process.hide(),
                    });
                }
                drawTool.setActive(false);
                map.removeInteraction(drawTool);
                ol.Observable.unByKey(key);
            })
            drawTool.on('drawstart', function (e) {
                drawSource.clear();
                $('.legends').addClass("hidden");
                sketch = e.feature;
            });

            map.addInteraction(drawTool);
            createHelpTooltip();
        }

        if (drawtype == 'Point_for_selection') {
            const pointIsInTerai = point => teraiGeoJSON.features.some(feature => turf.booleanPointInPolygon(point, feature));
            const pointerMoveEventKey = map.on('pointermove', (event) => {
                let helpMsg = "Click on a stream.";
                if (pointIsInTerai(event.coordinate)) {
                    helpMsg = "MHP tool isn't meant for terai region.";
                }
                helpTooltipElement.innerHTML = helpMsg;
                helpTooltip.setPosition(event.coordinate);

                helpTooltipElement.classList.remove('hidden');
            });
            map.getViewport().addEventListener('mouseout', function () {
                helpTooltipElement.classList.add('hidden');
            });
            map.removeInteraction(select);
            map.getViewport().style.cursor = "pointer";
            select_line = new ol.interaction.Select({
                condition: function (event) {
                    return ol.events.condition.click(event) &&
                        !ol.events.condition.altKeyOnly(event) &&
                        !ol.events.condition.altShiftKeysOnly(event) &&
                        !ol.events.condition.shiftKeyOnly(event) &&
                        !pointIsInTerai(event.coordinate);
                },
                multi: false,
                layers: [riverWFSLayer]
            });
            select_line.set('name', 'select_line');
            drawTool = new ol.interaction.Draw({
                source: drawSource,
                type: /** @type {ol.geom.GeometryType} */ ('Point'),
            });
            drawTool.set('name', 'drawTool');
            line_selected_check = false;
            MHPStreamSelectInteraction();
            drawTool.on('drawstart', function (e) {
                map.getViewport().style.cursor = "pointer";
                drawSource.clear();
                $('.legends').addClass("hidden");
                sketch = e.feature;
            });
            drawTool.on('drawend', function (e) {
                // console.log('point_added');
                sketch = null;
                lastFeature = e.feature;
                const coordinate = lastFeature.getGeometry().getCoordinates();
                map.getViewport().style.cursor = "default";
                var format = new ol.format.WKT();
                point = format.writeGeometry(lastFeature.getGeometry());
                // console.log(point);
                newMHP_point = point;
                vectorLayer.getSource().clear();
                map.removeInteraction(drawTool);
                ol.Observable.unByKey(pointerMoveEventKey);
                helpTooltip.setPosition(undefined);
                setTimeout(function () {
                    if (pointIsInTerai(coordinate)) {
                        swal({
                            title: "Selection Error",
                            text: "MHP tool isn't meant for terai region."
                        });
                    }
                    else if (!line_selected_check) {
                        swal({
                            title: "Selection Error",
                            text: "Please Select One Stream"
                        });
                    }
                    map.removeInteraction(select_line);
                    // administrative layer highlight
                    map.addInteraction(select);
                }, 200);
            });
            map.removeInteraction(select);
            map.addInteraction(drawTool);
            map.addInteraction(select_line);
            createHelpTooltip();
        }
    }

    // message in form
    setTimeout(function () {
        $('#final_msg').fadeOut();
    }, 10000);

    //for base maps
    $(document).on("click", ".map-wrap", function () {
        // $(".map-wrap").click(function () {
        var bmap = $(this).text().trim();
        if (bmap == "None") {
            osmLayer.setVisible(false);
            bingLayer.setVisible(false);
        } else if (bmap == "OSM") {
            osmLayer.setVisible(true);
            bingLayer.setVisible(false);
        } else {
            bingLayer.setVisible(true);
            osmLayer.setVisible(false);
        }
    });

    // for layer on off
    $(document).on("click", ".layer", function () {
        var id = $(this).attr("id");
        var l = getLayer(id);

        if ($(this).prop("checked") == true) {
            l.setVisible(true);
        } else {
            l.setVisible(false);
        }
    });

    var locationLayer = new ol.layer.Vector({
        map: map,
        source: new ol.source.Vector()
    });
    var geolocation = new ol.Geolocation({
        projection: view.getProjection()
    });
    var accuracyFeature = new ol.Feature();
    geolocation.on('change:accuracyGeometry', function () {
        accuracyFeature.setGeometry(geolocation.getAccuracyGeometry());
    });

    var positionFeature = new ol.Feature();
    positionFeature.setStyle(new ol.style.Style({
        image: new ol.style.Circle({
            radius: 6,
            fill: new ol.style.Fill({
                color: '#FEA47F'
            }),
            stroke: new ol.style.Stroke({
                color: '#2C3A47',
                width: 2
            })
        })
    }));
    accuracyFeature.setStyle(new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'blue',
            width: 3
        }),
        fill: new ol.style.Fill({
            color: 'rgba(0, 0, 255, 0)'
        })
    }));

    geolocation.on('change:position', function () {
        var coordinates = geolocation.getPosition();
        positionFeature.setGeometry(coordinates ?
            new ol.geom.Point(coordinates) : null);


        var ext = positionFeature.getGeometry().getExtent();
        map.getView().fit(ext, map.getSize());
    });


    function addproject_function() {
        $('#qnimate .popup-head .popup-head-left').empty()
        $('#qnimate .popup-head .popup-head-left').append('Project Create Form')
        $('#qnimate .form-load').empty()
        $('.form-load').load('/addproject', function () {
            formAjaxSubmit('.ibox-content form');
        });
        $('#qnimate').addClass('popup-box-on');
    }

    // user management
    // project delete
    $(".del-user").on("click", function () {
        userID = $(this).attr("id");
        bootbox.confirm({
            title: "Delete User?",
            message: "you are about to delete the User. Are you sure?",
            buttons: {
                confirm: {
                    label: 'Yes',
                    className: 'btn-danger'
                },
                cancel: {
                    label: 'No',
                    className: 'btn-success'
                }
            },
            callback: function (result) {
                if (result == true) {
                    $.ajax({
                        url: "/admin-login/del_user",
                        data: {
                            id: userID
                        },
                        success: function (data, status) {
                            $("#" + userID).parents("tr").remove();

                        }
                    });
                }
            }
        });
    });

    function onMoveEnd(evt) {
        const map = evt.map;
        const extent = map.getView().calculateExtent(map.getSize());
        const resolution = map.getView().getResolution();
        if (resolution < 0.0006866455078125 && current_mode === "MHP") {
            fetch(`/streamlines/?extent=[${extent.join(',')}]`)
                .then(response => response.json())
                .then(geojson => {
                    getLayer('MHPRivers').getSource().addFeatures(
                        (new ol.format.GeoJSON()).readFeatures(geojson)
                    );
                });
        }
    }


    map.on('moveend', onMoveEnd);

    function select_district(dcode) {
        var dcode1 = dcode;
        if (dcode.length == 3) {
            var dcode_old = dcode.substring(1, 3);
        }
        dcode = dcode.substring(1, 3);
        if (dcode_old.startsWith('0')) {
            dcode_old = String(parseInt(dcode_old));
        }
        var codeIndex = Districts.Code.indexOf(dcode1);
        var dName = Districts.District[codeIndex];
        var ext = adminDistrict[dName]
        map.getView().fit(ext, map.getSize());
        return dcode_old
    }

    $("#addClass").click(function () {
        $('#edit').modal('hide');
        $('#edit-button-list').show();
        $('#draw-polygon-button-list').show();
        map.removeInteraction(select);
        map.removeInteraction(modify);
        batPolygonOverlay.getSource().clear();
        drawSource.clear();
        $('.modal-title').empty();
        $('.modal-title').append('Project Create Form');
        if (current_mode == "BAT") {
            $('.create-model').load('/addproject', function () {
                formAjaxSubmit('.ibox-content form');
            });
        } else if (current_mode == "MHP") {
            $('.create-model').load('/addproject_mhp', function () {
                formAjaxSubmit('.ibox-content form');
                $('.tab-content.catchment-option').hide();
                $('#tab-1').show();
            });
        } else if (current_mode == "SST") {
            $('.create-model').load('/createsamplingproject', function () {
                formAjaxSubmit('.ibox-content form');
            });
        }
    });
    $("#openClass").click(function () {
        if (current_mode == "BAT") {
            $('#edit').modal('hide');
            drawSource.clear();
            map.removeInteraction(select);
            map.removeInteraction(modify);
            $('.modal-title').empty();
            $('.modal-title').append('Project Open Form');
            $.ajax({
                url: "/open_project",
                success: function (data, status) {
                    $('.open-model').empty();
                    $('.open-model').append(data);
                }
            });
            if ($('#ppp').length) // use this if you are using id to check
            {
                projectID = $('#ppp').attr("projectID");
            }
        }
        else if (current_mode == "MHP") {
            $('#edit').modal('hide');
            drawSource.clear();
            map.removeInteraction(select);
            map.removeInteraction(modify);
            $('.modal-title').empty();
            $('.modal-title').append('Project Open Form');
            $.ajax({
                url: "/open_projectMHP",
                success: function (data, status) {
                    $('.open-model').empty();
                    $('.open-model').append(data);
                }
            });
            if ($('#ppp').length) // use this if you are using id to check
            {
                projectID = $('#ppp').attr("projectID");
            }
        }
        else if (current_mode == "SST") {
            $('.modal-title').empty();
            $('.modal-title').append('Project Open Form');
            $.ajax({
                url: "/open_sampling_project",
                success: data => {
                    $('.open-model').empty();
                    $('.open-model').append(data);
                }
            });
            if ($('#ppp').length) // use this if you are using id to check
            {
                projectID = $('#ppp').attr("projectID");
            }
        }

    });
    $(document).on("click", "#editClass", function () {

        $('.modal-title').empty()
        $('.modal-title').append('Project Edit Form')
        $('.edit-model').empty()
        var projectID;
        if ($('#ppp').length) // use this if you are using id to check
        {
            projectID = $('#ppp').attr("projectID");
            if (current_mode == "BAT") {
                $('.edit-model').load('/editproject/?id=' + projectID, function () {
                    map.getInteractions().extend([select]);
                    map.getInteractions().extend([modify]);

                    modify.on('modifyend', function (e) {
                        var features = e.features.getArray();
                        for (var i = 0; i < features.length; i++) {
                            var geometry1 = e.features.getArray()[0].getGeometry();
                            var format = new ol.format.WKT();
                            poly = format.writeGeometry(geometry1);
                        }
                        $('#id_polygon').val(poly);

                    });
                    formAjaxSubmit('.ibox-content form');
                });
            } else if (current_mode == "MHP") {
                $('.edit-model').load('/editprojectMHP/?id=' + projectID, function () {
                    map.getInteractions().extend([select_MHP]);
                    map.getInteractions().extend([modify_MHP]);

                    modify_MHP.on('modifyend', function (e) {
                        var features = e.features.getArray();
                        var selected_arcid;
                        for (var i = 0; i < features.length; i++) {
                            var geometry1 = e.features.getArray()[0].getGeometry();
                            var format = new ol.format.WKT();
                            point = format.writeGeometry(geometry1);
                            var coordinate = geometry1.getCoordinates();
                            selected_arcid = riverWFSLayer.getSource().getClosestFeatureToCoordinate(coordinate).get('arcid');
                        }
                        $('#id_damPoint').val(point);
                        $('#id_selected_stream_arcid').val(selected_arcid);

                    });
                    formAjaxSubmit('.ibox-content form');
                });
            } else if (current_mode == "SST") {
                $('.edit-model').load('/editsamplingproject/' + projectID, () => {
                    formAjaxSubmit('.ibox-content form');
                });
            }
        } else {
            html = "<div class='alert alert-danger'>Please Select The Project First</div>" +
                '<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>'
            $('.edit-model').append(html);

        }

    });

    $("#shareClass").on("click", function () {
        $('#edit').modal('hide');
        projectID = $('#ppp').attr("projectID");
        user_id = $('#projectname').attr("userid");
        var options = [];
        if (projectID) {
            options.push({
                value: 0,
                text: 'Please Select the User for Sharing',
            });
            $.each(project_user, function (key, v) {
                options.push({
                    value: key.toString(),
                    text: v,
                })
            });
            bootbox.prompt({
                title: "This is a prompt with select!",
                inputType: 'select',
                inputOptions: options,
                value: 0,
                callback: function (result) {
                    if (result !== null) {
                        let share_project_url = null;
                        if (current_mode == "BAT") {
                            share_project_url = "/shared_project";
                        }
                        else if (current_mode == "MHP") {
                            share_project_url = "/shared_projectMHP";
                        }
                        else if (current_mode == "SST") {
                            share_project_url = "/share_sampling_project"
                        }

                        share_project_url && $.ajax(
                            {
                                url: share_project_url,
                                data: {
                                    projectID: projectID,
                                    user_id: result,
                                },
                                success: function (data) {
                                    bootbox.alert(data.response);
                                }
                            });
                    }
                }
            });
        }
        else {
            bootbox.alert({
                title: "Share Your Project",
                message: "<div class='alert alert-danger'>Please Select The Project First</div>"
            });
        }
    });

    /**  PRINTING FUNCTIONALITIES START **/
    let legendInfos = [];
    function getLegendImgWidth(layer)
    {
        return layer.get("legendImgWidth") || 25;
    }
    function getLegendImgHeight(layer)
    {
        return layer.get("legendImgHeight") || 25;
    }
    function getLegendInfoItem(layer)
    {
        return {
            layerId: layer.get("id"),
            title: layer.get("title"),
            src: layer.get("legendPath"),
            imgWidth: getLegendImgWidth(layer),
            imgHeight: getLegendImgHeight(layer),
        };
    }

    function createLegendCheckboxes(selector, in_layers)
    {
        const sortedLayers = in_layers.sort((lyr1, lyr2) => getLegendImgHeight(lyr1) - getLegendImgHeight(lyr2));
        const htmlContent =sortedLayers.reduce((prevHTML, layer) =>
        {
            return prevHTML +
                `<div class="layer-item">
                    <input type="checkbox" id="p-${layer.get("id")}"> ${layer.get("title")}
                    <br>
                    <img src="${layer.get('legendPath')}" width="${getLegendImgWidth(layer)}" height="${getLegendImgHeight(layer)}">
                </div>`;
        }, "");
        $(selector).html(htmlContent);
        in_layers.forEach( layer =>
        {
            const layerId = layer.get("id");
            $(`#p-${layerId}`).click(event =>
            {
                if (event.target.checked)
                { 
                    legendInfos.push( getLegendInfoItem( layer ) );
                }
                else
                {
                    legendInfos = legendInfos.filter(info => info.layerId !== layerId);
                }
            });
        })
    }

    function getPossibleLayersForLegends()
    {
        return layers.filter(layer =>
        {
            const source = layer.getSource();
            if (source.constructor===ol.source.Vector && source.getFeatures().length===0)
                return false;
            if (!layer.getVisible() || !layer.get("legendPath"))
                return false;
            return true;
        });
    }
    function proxifyWMSLayers()
    {
        tileWMSLayers.forEach(layer =>
        {
            const source = layer.getSource();
            const currUrl = source.getUrls()[0];
            currUrl.includes(PROXY_PREFIX) || source.setUrls([ PROXY_PREFIX + currUrl ]);
        });
    }
    function deproxifyWMSLayers()
    {
        tileWMSLayers.forEach(layer =>
        {
            const source = layer.getSource();
            source.setUrls([ source.getUrls()[0].replace(PROXY_PREFIX,"") ]);
        });
    }
    // Open print modal
    $("#open-print-modal").click( () =>
    {
        $("#map-title").val("");
        $("#map-outfilename").val("");
        $("#toggle-all-legend-items").prop("checked", false);
        legendInfos = [];
        proxifyWMSLayers()
        map.setTarget("printer-map-container");
        // gotta wait 500ms to update the map size since modal isn't drawn immediately or the map won't show
        setTimeout(() => map.updateSize(), 500);
        createLegendCheckboxes("#layer-legend-list", getPossibleLayersForLegends());
    });
    // adding retarget map on print map modal closing events
    const resetMapToEnlargedDiv = () =>
    {
        deproxifyWMSLayers();
        map.setTarget("map-enlarged");
    }
    $("#print-map-modal .close").click(resetMapToEnlargedDiv);
    $("#print-map-modal").click( event =>
    {
        if (event.target===event.currentTarget) $("#print-map-modal .close").trigger('click');
    });
    // selecting all-legend-items
    $("#toggle-all-legend-items").click(event =>
    {
        $("#layer-legend-list .layer-item input").each( (_, checkbox) =>
        {
            $(checkbox).prop( "checked", !event.target.checked ).trigger("click");
        });
    });
    $("#print-map-form").keydown( event =>
    {
        if (event.key === "Escape") resetMapToEnlargedDiv();
    });
    function getMapPDFLayout()
    {
        const DPI = 120; // pdf's dpi
        const mmToPixel = dim_mm => dim_mm * DPI / 25.4; // 1 inch = 25.4 mm
        // all measurements are in mm if not suffixed by pxl
        const margin = 10;
        const topMargin = 15;
        const pageWidth = 297;
        const pageHeight = 210;
        const mapWidth = pageWidth - 2*margin; // 272
        const mapHeight = pageHeight - topMargin - margin; // 180
        const mapHeightPxl = mmToPixel(mapHeight);
        // legend positions are relative to mapframe
        legendHeightPercent = 0.42;
        legendHeightPxl = mapHeightPxl * legendHeightPercent;
        legendPosPxl = {
            x: mmToPixel(2),
            y: mapHeightPxl * (1-legendHeightPercent) - mmToPixel(2)
        }
        // northArrow Coords: also relative to mapFrame
        const arrowBaseWidth = 9;
        const arrowHeight = 12;
        const arrowTop = 6;
        const arrowCenterX = mapWidth - (6 + arrowBaseWidth/2);
        const northArrowCoords = [
            [arrowCenterX, arrowTop], // top coordinate
            [arrowCenterX + arrowBaseWidth/2, arrowTop + arrowHeight], // rightCoordinate
            [arrowCenterX, arrowTop + 2*arrowHeight/3], // middleCoordinate
            [arrowCenterX - arrowBaseWidth/2, arrowTop + arrowHeight], // leftCoordinate
        ];
        return {
            format: "a4",
            pageDim: [pageWidth, pageHeight],
            margin,
            topMargin,
            mapFrameSize: [mapWidth, mapHeight],
            mapFrameSizePxl: [mmToPixel(mapWidth), mapHeightPxl],
            northArrowCoordsPxl: northArrowCoords.map(pt => pt.map(mmToPixel) ),
            legendBoxPxl: {
                pos: legendPosPxl,
                height: legendHeightPxl,
                columnWidth: 230
            },
        };
    }

    $("#print-map-form").submit(event =>
    {
        event.preventDefault();
        $("#loading-modal").show();

        const layout = getMapPDFLayout();
        const title = $("#map-title").val();
        const outputfilename = $("#map-outfilename").val();
        const mapSize = map.getSize();
        const mapResolution = map.getView().getResolution();

        map.once("rendercomplete", () =>
        {
            // setting up the canvas
            const canvas = document.createElement("canvas");
            canvas.width = layout.mapFrameSizePxl[0];
            canvas.height = layout.mapFrameSizePxl[1];
            const context = canvas.getContext("2d");
            // sort the legend by height
            legendInfos = legendInfos.sort((item1, item2) => item1.imgHeight - item2.imgHeight);

            copyOLMapTo(context);
            console.log(legendInfos)
            legendInfos.length && addLegendsTo(context, {
                legendInfos,
                pos: layout.legendBoxPxl.pos,
                columnWidth: layout.legendBoxPxl.columnWidth,
                height: layout.legendBoxPxl.height
            });
            drawPolygon(context, "black", layout.northArrowCoordsPxl)
            drawScaleBar(context, {x: canvas.width, y: canvas.height })
            context.strokeStyle = "black";
            context.strokeRect(0,0,canvas.width,canvas.height) // map frame border

            createMapPDF(title, outputfilename, canvas, layout)
            // reset original map size
            map.setSize(mapSize);
            map.getView().setResolution(mapResolution);
            $("#loading-modal").hide();
            $("#print-map-modal .close").click().trigger("click");
        });
        // set map size to print frame size
        const frameSize = layout.mapFrameSizePxl;
        map.setSize(frameSize);
        const scaling = Math.min(frameSize[0] / mapSize[0], frameSize[1] / mapSize[1]);
        map.getView().setResolution(mapResolution / scaling);
    });

    function getLegendBoxDimension(margin, labelHeight, columnWidth, legendInfos, maxBoxHeight)
    {
        let bottomMostLegendItemY = 0;
        const lastLegendItemPos = legendInfos.reduce((prevSize, legend) =>
        {
            const itemHeight = legend.imgHeight + labelHeight + margin;
            if (prevSize.y + itemHeight  > maxBoxHeight)
            {
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
    function getScaleBarInfo()
    {
        const scaleLine = document.querySelector(".ol-scale-line-inner");
        return {width: scaleLine.clientWidth, text: scaleLine.innerText};
    }
    function drawScaleBar(context, rightBottomPos)
    {
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
        context.fillRect(pos.x, pos.y, width+margin*2, height + margin * 2 )
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
        context.fillText(text, x + width/2, y + height - margin);
    }
    function addLegendsTo(context, {legendInfos, pos, columnWidth, height: maxHeight})
    {
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
        legendInfos.forEach( legend =>
        {
            const itemHeight = legend.imgHeight + labelHeight + margin;
            if (offsetY + itemHeight > maxHeight)
            {
                offsetX += margin + columnWidth;
                offsetY = margin;
            }
            const left = pos.x + offsetX;
            const top = pos.y + offsetY;
            const img = document.createElement("img");
            img.setAttribute("src", legend.src);
            context.fillText(legend.title, left, top + labelHeight);
            context.drawImage(img, left, top + labelHeight, legend.imgWidth, legend.imgHeight);
            // update to offsetY
            offsetY += itemHeight;
        });
        context.lineWidth = 1;
        context.closePath();
        context.strokeRect(pos.x, pos.y, legendBoxWidth, legendBoxHeight);
    };
    function drawPolygon(context, color, coords)
    {
        context.lineWidth = 2;
        context.fillStyle = color;
        context.beginPath();
        context.moveTo(...coords[0]);
        for (let i = 1; i < coords.length; i++)
        {
            context.lineTo(...coords[i]);
        }
        context.closePath();
        context.fill();
    }
    function copyOLMapTo(context)
    {
        context.fillStyle = "white";
        context.fillRect(0, 0, context.canvas.width, context.canvas.height);
        document.querySelectorAll(".ol-layer canvas").forEach(mapCanvas =>
        {
            if (mapCanvas.width > 0)
            {
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
    function createMapPDF(title, filename, mapCanvas, {margin, topMargin, mapFrameSize, pageDim, format})
    {
        const pdf = new jsPDF("landscape", undefined, format);
        pdf.setFont("Times").setFontType("bold").setFontSize(15);
        pdf.text(title, parseInt(pageDim[0] / 2), 9, null, null, "center");
        try
        {
            pdf.addImage(mapCanvas.toDataURL("image/png"), "JPEG", margin, topMargin, mapFrameSize[0], mapFrameSize[1]);
            pdf.save(`${filename}.pdf`);
        }
        catch (error)
        {
            showErrorToast("Error Occurred! Please try it again."); console.log(error);
        }
    }
    /* JSPDF version of mapprint end */

    $(document).on("click", "#submit_pro", function () {
        map.removeInteraction(select);
        map.removeInteraction(modify);
    });

    $(document).on("click", ".project-selector", function ()
    {
        const projectId = $(this).attr('projectid');
        const handleSuccess = data =>
        {
            if (typeof data === "object")
            {
                showErrorToast("Failed To Open Project!");
                return;
            }
            // adding the project name
            $('#projectname').empty();
            var html = "<i class='fa fa-edit'></i>Working Project: <span id='ppp' shared = '0' projectID ='" + projectId + "'>" + project_list[projectId] + " </span>"
            $('#projectname').append(html);
            // adding the project list html
            $('.results-wrap').html("");
            $('.results-wrap').append(data);
            // console.log(data);
            showSuccessToast("Project Opened Successfully")
        };
        const handleError = () => showErrorToast("Couldn't open project. Something went wrong.");
        const handleComplete = () => $("#open").modal("hide");
        if (current_mode == "BAT") {
            $('#open').modal('hide');
            $('#edit-button-list').show();
            $('#draw-polygon-button-list').show();

            batPolygonOverlay.getSource().clear();
            drawSource.clear();
            clusterLayer.getSource().clear();
            $.ajax({
                //type: "POST",
                url: `/project_select/${projectId}`,
                success: function (data) {
                    handleSuccess(data);
                    $('#result-box > div.result-title > div > ul > li:nth-child(1) > a').click()
                },
                error: handleError,
                complete: handleComplete
            });
        }
        else if (current_mode == "MHP") {
            $('#edit-button-list').show();
            $('#draw-polygon-button-list').show();

            batPolygonOverlay.getSource().clear();
            drawSource.clear();
            clusterLayer.getSource().clear();
            $.ajax({
                //type: "POST",`
                url: `/MHPproject_select/${projectId}`,
                success: function (data) {
                    handleSuccess(data);
                    $('#result-box > div.result-title > div > ul > li:nth-child(1) > a').click()
                },
                error: handleError,
                complete: handleComplete
            });

            $.ajax({
                //type: "POST",
                url: "/sidebar_select",
                data: {
                    shared: '0'
                },
                success: function (data) {
                    $('.side-layers').empty();
                    $('.side-layers').append(data);
                    $('#myModal3').modal('hide');
                }
            });
        }
        else if (current_mode == "SST") {
            const layer = getLayer('spatialsamplingtool');
            layer.getSource().clear();
            $.ajax({
                url: "/samplingprojects/" + projectId,
                success: data => {
                    if (typeof data === "object") {
                        showErrorToast("Failed To Open Project!");
                        return;
                    }
                    // adding the project name
                    $('#projectname').empty();
                    var html = "<i class='fa fa-edit'></i>Working Project: <span id='ppp' shared = '0' projectID ='" + projectId + "'>" + project_list[projectId] + " </span>"
                    $('#projectname').append(html);
                    // adding the project list html
                    $('.results-wrap').html("");
                    $('.results-wrap').append(data);
                    showSuccessToast("Project Opened Successfully")
                },
                error: handleError,
                complete: handleComplete
            });
        }
    });

    $(document).on("click", ".shared-project-selector", function () {
        $('#open').modal('hide');
        $('#share-on-off').empty();
        $('#projectname').empty();
        $('#edit-button-list').hide();
        $('#draw-polygon-button-list').hide();
        batPolygonOverlay.getSource().clear();
        drawSource.clear();
        clusterLayer.getSource().clear();
        var projectID = $(this).attr('projectid');

        if (projectID !== '99999') {
            html = "<i class='fa fa-edit'></i>Working Project: <span id='ppp' shared = '1' projectID ='" + projectID + "'>" + shared_project[projectID].name + " </span>"
            $('#projectname').append(html);
            var shared_url = `/project_select/${projectID}`;

            if (current_mode == "BAT") {
                shared_url = `/project_select/${projectID}`;
            } else if (current_mode == "MHP") {
                shared_url = `/MHPproject_select/${projectID}`;
                $('#streamselection').append('<div class="absolute-block overlay-block" id="polygon_draw_loader"></div>')
            }


            $.ajax({
                //type: "POST",
                url: shared_url,
                success: function (data, status) {
                    // console.log(data);
                    $('.results-wrap').empty();
                    $('.results-wrap').append(data);
                }
            });

            $.ajax({
                //type: "POST",
                url: "/sidebar_select",
                data: {
                    shared: '1'
                },

                success: function (data, status) {
                    // console.log(data);
                    $('.side-layers').empty();
                    $('.side-layers').append(data);

                    $('#myModal3').modal('hide');
                }
            });

        } else {
            $('.results-wrap').empty();
            var empty_result = "<div class='result-description clearfix' id='accordion'>"
            empty_result += '<div class="result-main">'
            empty_result += '<a data-toggle="collapse" data-parent="#accordion" href="#collapse1">'
            empty_result += '<div class="result-evaluate">'
            empty_result += '<div class="result-shape"> <i class="fa fa-angle-up"></i> </div>'
            empty_result += '</div>'
            empty_result += '</a>'
            empty_result += '<div id="collapse1" class="panel-collapse collapse in">'
            empty_result += '<div class="table-bar-main row">'
            empty_result += '<div class="col-sm-12">'
            empty_result += '<div class="tab-content">'
            empty_result += '<div id="result" class="tab-pane fade">'
            empty_result += '<div class="alert alert-success">Select or Create Project First</div>'
            empty_result += '</div>'
            empty_result += '<div id="scenario" class="tab-pane fade in active">'
            empty_result += '<div class="alert alert-success">Select or Create Project First</div>'

            empty_result += "</div></div></div></div></div></div></div>"

            $('.results-wrap').append(empty_result);

        }
    });


    $(document).on("click", ".project-delete", function () {
        projectID = $(this).attr('id');
        projectID_cwp = $('#ppp').attr("projectID");
        if (projectID === projectID_cwp) {
            bootbox.alert({
                message: "You Can't Delete While project is Open!",
                className: 'bb-alternate-modal'
            });

        } else {

            bootbox.confirm({
                title: "Remove?",
                message: "You are about to remove the project. Are you sure?",
                buttons: {
                    confirm: {
                        label: 'Yes',
                        className: 'btn-danger'
                    },
                    cancel: {
                        label: 'No',
                        className: 'btn-success'
                    }
                },
                callback: function (result) {

                    if (result == true) {

                        var delete_url = "";
                        var method = "GET";
                        if (current_mode == "BAT") {
                            delete_url = "/project_delete";
                        } else if (current_mode == "MHP") {
                            delete_url = "/MHPproject_delete";
                        } else if (current_mode == "SST") {
                            delete_url = "/samplingprojects/" + projectID;
                            method = "DELETE"
                        }

                        $.ajax({
                            type: method,
                            url: delete_url,
                            data: method !== "DELETE" ? { project_id: projectID } : null,
                            beforeSend: xhr => xhr.setRequestHeader("X-CSRFToken", CSRF_TOKEN),
                            success: result => {
                                if (result.success) {
                                    $("#" + projectID).parents("tr").remove();
                                }
                            }
                        });

                    }
                }
            });


        }
    });


    $(document).on("click", ".del-shared-project", function () {
        projectID = $(this).attr("id");
        var user = $(this).attr("user");
        bootbox.confirm({
            title: "Remove Project Share?",
            message: "you are about to remove the project shared. Are you sure?",
            buttons: {
                confirm: {
                    label: 'Yes',
                    className: 'btn-danger'
                },
                cancel: {
                    label: 'No',
                    className: 'btn-success'
                }
            },
            callback: function (result) {
                if (result == true) {
                    $.ajax({
                        url: "/remove_share",
                        data: {
                            user: user,
                            projectID: projectID
                        },
                        success: function (data, status) {
                            $("#" + projectID).parents("tr").remove();

                        }
                    });
                }
            }
        });


    });


    $(document).on("change", "#id_tier", function () {
        var tier = $("#id_tier").val();
        if (tier == 1) {
            $("#id_demand").attr("min", 3);
            $("#id_demand").attr("max", 50);
            $("#id_demand").val(3);
        } else if (tier == 2) {
            $("#id_demand").attr("min", 50);
            $("#id_demand").attr("max", 200);
            $("#id_demand").val(50);
        } else if (tier == 3) {
            $("#id_demand").attr("min", 200);
            $("#id_demand").attr("max", 800);
            $("#id_demand").val(200);
        } else if (tier == 4) {
            $("#id_demand").attr("min", 800);
            $("#id_demand").attr("max", 2000);
            $("#id_demand").val(800);
        } else {
            $("#id_demand").attr("min", 2000);
            // $("#id_demandHH").attr("max", 2000);
            $("#id_demand").val(2000);
        }
    });
    $(document).on("change", ".js-example-basic-single", function () {

        var poly_id = $(this).val();
        // console.log(poly_id);
        if (poly_id == 104008) {
            $('#gauriganj').show();
            MTFElectricityTierLayer.setVisible(true);
            ElectricityTechnologyLayer.setVisible(false);
            PrimaryCookingFuelLayer.setVisible(false);
            PrimaryStoveTypeLayer.setVisible(false);
        } else {
            MTFElectricityTierLayer.setVisible(false);
            ElectricityTechnologyLayer.setVisible(false);
            PrimaryCookingFuelLayer.setVisible(false);
            PrimaryStoveTypeLayer.setVisible(false);
            $('#gauriganj').hide();
        }
        $.ajax({
            url: "/survey/extent/",
            data: {
                id: poly_id
            },
            success: function (data) {
                // SurveyOverlay

                var parser = new ol.format.GeoJSON()
                var result = parser.readFeatures(JSON.parse(data.geo_project));
                as_geojson = parser.writeFeatures(result, {
                    featureProjection: 'EPSG:4326',
                    dataProjection: 'EPSG:4326'
                });
                var features = parser.readFeatures(as_geojson)
                SurveyOverlay.getSource().clear();
                SurveyOverlay.getSource().addFeatures(features);
                map.getView().fit(data.extent, map.getSize());
            }
        });
    });

    var select_survey = new ol.interaction.Select({
        layers: [SurveyOverlay]
    });
    select_survey.set('name', 'select_survey');

    map.getInteractions().extend([select_survey]);


    // use the features Collection to detect when a feature is selected,
    // the collection will emit the add event
    var selectedFeatures = select_survey.getFeatures();
    selectedFeatures.on('add', function (event) {
        var feature = event.target.item(0);
        $.ajax({
            //type: "POST",
            url: `/project_select/${projectId}`,
            success: function (data) {
                $('.results-wrap').empty();
                $('.results-wrap').append(data);
            }
        });

    });

    // when a feature is removed, clear the photo-info div
    selectedFeatures.on('remove', function (event) {

        clusterLayer.getSource().clear();
        $('.results-wrap').empty();
        var empty_result = "<div class='result-description clearfix' id='accordion'>"
        empty_result += '<div class="result-main">'
        empty_result += '<a data-toggle="collapse" data-parent="#accordion" href="#collapse1">'
        empty_result += '<div class="result-evaluate">'
        empty_result += '<div class="result-shape"> <i class="fa fa-angle-up"></i> </div>'
        empty_result += '</div>'
        empty_result += '</a>'
        empty_result += '<div id="collapse1" class="panel-collapse collapse in">'
        empty_result += '<div class="table-bar-main row">'
        empty_result += '<div class="col-sm-12">'
        empty_result += '<div class="tab-content">'
        empty_result += '<div id="result" class="tab-pane fade">'
        empty_result += '<div class="alert alert-success">Select or Create Project First</div>'
        empty_result += '</div>'
        empty_result += '<div id="scenario" class="tab-pane fade in active">'
        empty_result += '<div class="alert alert-success">Select or Create Project First</div>'

        empty_result += "</div></div></div></div></div></div></div>"

        $('.results-wrap').append(empty_result);
    });
    $(document).on("click", ".close-button", function () {
        $(this).parent().removeClass('active in');
        $('.icon-bar > .nav-tabs > li').removeClass('active');
    });

    // cluster for MIS Layers
    fetch("/misclusterdata/")
        .then(response => response.json())
        .then(clusterdata => {
            const misLayerSources = {
                "shs": shsSource,
                "solar_photo": solar_photoSource,
                "pico_hydro": picoHydroSource,
                "micro_hydro": microHydroSource,
                "iwm": iwmSource,
                "mics": micsSource,
                "d_biogas": dBiogasSource,
                "biomass_rocket": bioMassRocketSource
            };
            const format = new ol.format.GeoJSON();
            Object.keys(misLayerSources).forEach(layerName => {
                const layerFeatures = format.readFeatures(clusterdata[layerName]);
                misLayerSources[layerName].addFeatures(layerFeatures);
            });
        });

    updatePopulationData(2011, 0, false);
    // updating infographics for admin id 0 i.e whole country
    updateInfographicsADEF(0).then(() => {
        // select elements to inject and do the injection
        SVGInjector(document.querySelectorAll('img.svg-dynamic-icon'));
    });

    var button_geo = '<div class="geolocation ol-unselectable ol-control added-button" id="geolocation-on">';
    button_geo += '<button type="button" title="Geolocation on off"><img class="svg-icon-ol-interaction" src="/static/img/locationIcon.svg"/></button>';

    button_geo += '</div>'

    $('.ol-zoom-extent button').empty();
    $('.ol-zoom-extent button').append('<img class="svg-icon-ol-extent" src="/static/img/extent.svg"/>');
    var mySVGsToInject3 = document.querySelectorAll('img.svg-icon-ol-extent');

    // Do the injection
    SVGInjector(mySVGsToInject3);

    var button_p_ext = '<div class="project-extent ol-unselectable ol-control added-button project-ext" id="project-extent-zoom">';
    button_p_ext += '<button type="button" id="prj_ext" onclick="zoomToProjectExtent()" title="Go to Project Extent"><img class="svg-icon-ol-interaction" src="/static/img/zoom-to-extent.svg"/></button>';
    button_p_ext += '</div>'
    const $goToInputLocBtn = MakeGoToInputLocationButton().hide();
    $('.ol-overlaycontainer-stopevent').append($goToInputLocBtn);

    $('.results-icon').hide();
    $('#switch-map a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        var currentTab = $(e.target).text(); // get current tab

        if (currentTab == 'Dashboard') {
            $('#geolocation-on').remove();
            $('#project-extent-zoom').remove();
            $goToInputLocBtn.hide();
            $(".results").removeClass("expanded");
            $('.results-icon').hide();
            batPolygonOverlay.getSource().clear();
            drawSource.clear();
            clusterLayer.getSource().clear();

            if ($('#ppp').length) // use this if you are using id to check
            {
                project_selected = $('#ppp').attr("projectID");
                $('#projectname').empty();
            }
            removeAllToolInteractions();
            map.setTarget('map');
            isDashboard = true; // current page is dashboard
        } else if (currentTab == 'MEP Tool') {
            isDashboard = false; // current page is not dashboard
            map.setTarget('map-enlarged');
            $('.ol-overlaycontainer-stopevent').append(button_geo);
            $('.ol-overlaycontainer-stopevent').append(button_p_ext);
            $goToInputLocBtn.show();

            var mySVGsToInject2 = document.querySelectorAll('img.svg-icon-ol-interaction');

            // Do the injection
            SVGInjector(mySVGsToInject2);

            $('.results-icon').show();
            if (typeof project_selected !== "undefined") {
                var html = "<i class='fa fa-edit'></i>Working Project: <span id='ppp' shared = '0' projectID ='" + project_selected + "'>" + project_list[project_selected] + " </span>"
                $('#projectname').append(html);
                $.ajax({
                    //type: "POST",
                    url: `/project_select/${projectId}`,
                    success: function (data, status) {
                        // console.log(data);
                        $('.results-wrap').empty();
                        $('.results-wrap').append(data);
                    }
                });
            }
        }
    });
    $('.gutter-lt a').on('click', function () {
        // console.log($(this).text());
        var txt = $(this).text();
        // console.log($(this).hasClass('collapsed'));
        if ($(this).hasClass('collapsed')) {
            // console.log('ok');
            $('.sidebar .select-box .timeline span').empty();
            $('.sidebar .select-box .timeline span').append(txt);
        } else {
            $('.sidebar .select-box .timeline span').empty();
            $('.sidebar .select-box .timeline span').append('Layers Visibility');
        }
    })

    $('.select-picker').select2({
        width: '100%'
    });
    $('#year-select-infoGraphics').on('change', function () {
        var year = $(this).val();
        updatePopulationData(year, selected_adminid, false);
    })
    if (target_set) {
        map.setTarget('map-enlarged');
        // console.log('kk');
        $('.ol-overlaycontainer-stopevent').append(button_geo);
        $('.ol-overlaycontainer-stopevent').append(button_p_ext)
        $('.ol-overlaycontainer-stopevent').append($goToInputLocBtn);
        SVGInjector(document.querySelectorAll('img.svg-icon-ol-interaction'));

        $('.results-icon').show();
    } else {
        map.setTarget('map');
        // console.log('ll');
    }


    $(document).on("click", "#geolocation-on", function () {
        a = geolocation.getTracking();
        if (a) {
            geolocation.setTracking(false);
            locationLayer.getSource().clear();


        } else {
            geolocation.setTracking(true);
            locationLayer.getSource().clear();
            locationLayer.getSource().addFeatures([accuracyFeature, positionFeature]);

        }
    });


    $('#gauriganj').hide();
    /**
     * Elements that make up the popup.
     */
    var container1 = document.getElementById('popup1');
    var content1 = document.getElementById('popup-content1');
    var closer1 = document.getElementById('popup-closer1');

    /**
     * Create an overlay to anchor the popup to the map.
     */
    var overlay1 = new ol.Overlay({
        element: container1,
        autoPan: true,
        autoPanAnimation: {
            duration: 250
        }
    });
    /**
     * Add a click handler to hide the popup.
     * @return {boolean} Don't follow the href.
     */
    closer1.onclick = function () {
        overlay1.setPosition(undefined);
        closer1.blur();
        return false;
    };

    map.addOverlay(overlay1);

    ol.Feature.prototype.getLayer = function (map) {
        var this_ = this, layer_, layersToLookFor = [];
        /**
         * Populates array layersToLookFor with only
         * layers that have features
         */
        var check = function (layer) {
            var source = layer.getSource();
            if (source instanceof ol.source.Vector) {
                var features = source.getFeatures();
                if (features.length > 0) {
                    layersToLookFor.push({
                        layer: layer,
                        features: features
                    });
                }
            }
        };
        //loop through map layers
        map.getLayers().forEach(function (layer) {
            if (layer instanceof ol.layer.Group) {
                layer.getLayers().forEach(check);
            } else {
                check(layer);
            }
        });
        layersToLookFor.forEach(function (obj) {
            var found = obj.features.some(function (feature) {
                return this_ === feature;
            });
            if (found) {
                //this is the layer we want
                layer_ = obj.layer;
            }
        });
        return layer_;
    };

    map.on('singleclick', function (evt) {
        var titles = ["MTF Electricity Tier", "Electricity Technology", "Primary Cooking Fuel", "Primary Stove Type"]
        var feature = map.forEachFeatureAtPixel(evt.pixel,
            function (feature, gausala_wards) {
                return feature;
            });
        var coordinate = evt.coordinate;
        if (feature) {
            var layer = feature.getLayer(map);
            if (layer) {
                var layer_title = layer.get("title");
                if (layer_title == titles[0] || layer_title == titles[1] || layer_title == titles[2] || layer_title == titles[3]) {

                    var data_length = Object.keys(feature.N).length; //feature.T.getKeys().length;
                    var attr = feature.N;
                    var key = Object.keys(feature.N);
                    var contents1 = '';
                    for (i = 0; i < data_length; i++) {
                        if (key[i] != "geometry") {
                            contents1 = contents1 + '<tr class="project-row"><td class="project-description-gauri">' + key[i] + '</td><td class="project-description-gauri">' + attr[key[i]] + '</td></tr>'
                            // console.log(attr[key[i]]);
                        }
                    }
                    $("#layername").html(layer.get("title"));
                    $("#popup1attribute").html(contents1);
                    overlay1.setPosition(coordinate);
                }
            }
        }
    });


    $(document).on("click", ".closemodal-energy", function () {
        $('#justfortest').modal('hide');
    });

    $(document).on("click", "#institutionbtn", function () {
        $('.input-title').html('Institutional Parameters');
        $('.input-body').load('/addinstitutions', function () {
            //console.log('kkdkdkd');
            formAjaxSubmit('.ibox-content form');
        });
    });
    $(document).on("click", "#msmesbtn", function () {
        $('.input-title').html('msmestitle');
        $('.input-body').html('msmesbobdy');
    });
    $(document).on("click", "#igabtn", function () {
        $('.input-title').html('igatitle');
        $('.input-body').html('igabody');
    });

    var modal = document.querySelector('.modal-dialog');
    $(modal).css({ "min-width": "800px", "margin": "auto" });


    function owltemplete(item_name) {
        var owt_item_template = `
        <div class="item max-height count-item">
            <div class="border-box max-height">
                <div class="map" style="min-height: 279px;">
                    <a class="fancybox table-block icon-absolute" data-fancybox-group="chart"  href="#${item_name}" title="">
                        <div class="valign-middle">
                            <i class="fa fa-search-plus"></i>
                        </div> 
                    </a> 
                    <div id="${item_name}" class="chart" style="width:100%; height: 100%;">
                    </div>
                </div> 
            </div> 
        </div>`;
        return owt_item_template
    }

    const dataNameToDivIdMap = {
        "Figure 1": "Fig1_Access_to_Electricity",
        "Figure 1a": "Fig1a_Access_to_Electricity_Gender",
        "Figure 2": "Fig2_Access_to_PriCookStv",
        "Figure 2a": "Fig2a_Access_to_PriCookStv_Gender",
        "Figure 2b": "Fig2b_Access_to_PriFuelSrc",
        "Figure 4": "Fig4_Electr_prod_Activities",
        "Figure 14": "Fig14_Electr_Service_Satisf",
        "Figure 15a": "Fig15a_Electr_Serv_Dissatisf_sec_reas",
        "Figure 15": "Fig15_Electr_Serv_Dissatisf_prim_reas",
        "Figure 16": "Fig16_Cooking_Service_Satisf",
        "Figure 19": "Fig19_Multi_Tireframework",
        "Figure 20": "Fig20_Access_PriCooking_Based_On_Fuel",
        "Figure 21": "Fig21_Fuel_SimpleframeworkStacked",
        "Figure 22": "Fig22_Cooking_Improvement_Table",
    };

    const dataNameToChartTitleMap = {
        "Figure 1": "Access To Electricity",
        "Figure 1a": "Primary Electricity Source Grouped By Gender of Head",
        "Figure 2": "Access To Primary Cooking Stove",
        "Figure 2a": "Primary Cooking Stove Grouped By Gender of Head",
        "Figure 2b": "Access to Primary Fuel Source",
        "Figure 4": "Productive use of Electricity: Activities",
        "Figure 14": "Household Electricity Service Satisfaction",
        "Figure 15a": "Electricity Service Dissatisfaction: Secondary Reason",
        "Figure 15": "Electricity Service Dissatisfaction: Primary Reason",
        "Figure 16": "Household Cooking Service",
        "Figure 19": "Multi-Tire Framework, Final Tire Distribution ",
        "Figure 20": "Access To Primary Cooking Based On Fuelwood",
        "Figure 21": "Primary Household Cooking Fuel as per Simplified Framework",
        "Figure 22": "Overall Improvement Scenarios",
    };

    var total_item = $(".count-item").length


    // function to reset mun information stuffs
    const removeExtraMunicipalityStuffs = (dontHideLayers) => {
        // removing extra divs of municipal energy chart
        const nInitialDivs = total_item;
        const nCurrentDivs = $(".count-item").length;
        for (let i = nCurrentDivs - 1; i > (nInitialDivs - 1); i--) {
            $('.owl-carousel').trigger('remove.owl.carousel', i).trigger('refresh.owl.carousel');
        }
        // remove mundata download button
        $("#mundata-download-link").remove();
        // removing municipality old features of project layers
        if (!dontHideLayers) {
            projectLayers.forEach(layer => layer.getSource().clear());
        }
    };
    // function to add extra divs for energy chart if not available
    const addDivsForCharts = divIds => {
        for (let i = 0; i < divIds.length; i++) {
            $('.owl-carousel').trigger('add.owl.carousel', [owltemplete(divIds[i])])
                .trigger('refresh.owl.carousel');
        }
        $("a.fancybox").fancybox();
    };

    const isNestedObject = data => Object.keys(data)[0] && typeof data[Object.keys(data)[0]] === 'object';
    const dataObjectToCSVContent = (title, data) => {
        let content = title.toUpperCase() + "\n";
        if (isNestedObject(data)) {
            Object.keys(data).forEach(key => {
                if (Object.prototype.toString.call(data[key]) === '[object Object]') {
                    content += dataObjectToCSVContent(key, data[key]); // key is the title for nested data
                }
                else if (Array.isArray(data[key])) // this is only for multitier data
                {
                    content += key + "\n"; // key is the title for nested data
                    content += data[key].join(",") + "\n";
                }
            });
            return content;
        }
        content += Object.keys(data).join(", ") + "\n";
        content += Object.values(data).join(", ") + "\n";
        return content;
    };

    // function to add download of availableData
    const addDataDownloadBtn = (availableData, municipality) => {
        let csvContent = "";
        availableData.forEach(dataItem => {
            csvContent += dataObjectToCSVContent(
                dataNameToChartTitleMap[dataItem.Name],
                dataItem.Data
            ) + "\n";
        });
        const container_li = document.createElement('li');
        container_li.id = 'mundata-download-link';

        const downloadBtn = document.createElement('a');
        downloadBtn.href = 'data:text/csv;chartset=utf-8,' + encodeURI(csvContent);
        downloadBtn.target = '_blank';
        downloadBtn.download = `${municipality} - Municipal Energy Data.csv`;
        downloadBtn.textContent = `Download ${municipality} Energy Data`;

        container_li.appendChild(downloadBtn);
        $("#navbarToggle > ul > li.dropdown > ul").append(container_li);
    }

    // function to check if a single chart data is there or not
    const dataExists = data => {
        if (data === null || data === undefined) return false;
        if (Object.keys(data).length === 0) return false;
        return true;
    };
    // function to handle the success of api data retrieval
    const handleChartDataSuccess = data => {
        // filtering divIds data-figure-names for only data that exists
        const availableData = data.filter(item => dataExists(item.Data));
        const availableDataNames = availableData.map(item => item.Name);
        const divIds = availableDataNames.map(name => dataNameToDivIdMap[name]);
        removeExtraMunicipalityStuffs(true); // removing old charts and button
        addDivsForCharts(divIds);
        draw_energy_highcharts(data, divIds, dataNameToDivIdMap, dataNameToChartTitleMap);
        const municipality = data[0].name;
        addDataDownloadBtn(availableData, municipality);
        showSuccessToast(`${municipality} Energy Data Charts Loaded`)
    };

    function addMunEnergyData(municipalityCode) {
        // removing other municipalities munlevel charts
        removeExtraMunicipalityStuffs();
        // adding energy charts from okapi 
        let dataIsAvailable = false;
        $.ajax({
            url: "/odkapi/all/",
            data: {
                mun: municipalityCode
            },
            beforeSend: () => $('#loading-modal').show(),
            success: data => {
                dataIsAvailable = data[0].result;
                if (dataIsAvailable) handleChartDataSuccess(data);
            },
            error: () => showErrorToast("Couldn't load data from ODK. Trying the MEP database."),
            // in the ajax complete function, only hiding the loading modal if dataIsAvailable in odk else hiding modal will be done in mepapi ajax call
            complete: () => dataIsAvailable && $('#loading-modal').fadeOut(),
        }).always(() => {
            // if data is not available odk api, trying mepapi
            if (!dataIsAvailable) {
                $.ajax({
                    url: "/mepapi/",
                    data: {
                        mun: municipalityCode
                    },
                    success: data => {
                        dataIsAvailable = data[0].result;
                        (dataIsAvailable) ?
                            handleChartDataSuccess(data)
                            :
                            showInfoToast(`Energy data for Municipality is unavailable`);
                    },
                    beforeSend: () => $('#loading-modal').show(),
                    complete: () => $('#loading-modal').fadeOut(),
                    error: () => showErrorToast("Couldn't load data from Mep Database"),
                });
            }
        });
    }

    $('.selDistrict').on('change', function () {
        removeExtraMunicipalityStuffs()
    });
    $('.selState').on('change', function () {
        removeExtraMunicipalityStuffs()
    });
    $('.clean-point').on('click', function () {
        // console.log("it's ok");
        drawSource.clear();
    });
    $('.select-focus .item a').on('click', function () {
        $(this).addClass('active');
        $(this).parent().siblings().find('a').removeClass('active');
    });


    // catchment processing form start

    //hide all tabs first
    $('.tab-content.catchment-option').hide();
    //show the first tab content
    $('#tab-1').show();
    $(document).on('change', '#select-catchment-processing-option', function () {
        var dropdown = $('#select-catchment-processing-option').val();
        //first hide all tabs again when a new option is selected
        $('.tab-content.catchment-option').hide();
        //then show the tab content of whatever option value was selected
        $('#' + "tab-" + dropdown).show();
    });

    // catchment processing form end
    $(".tools-sel").on('change', function () {

        clusterLayer.getSource().clear();
        batPolygonOverlay.getSource().clear();
        $('#projectname').html("");
        for (var i = 0; i < MHP_layer_list.length; i++) {
            getLayer(MHP_layer_list[i]["layer_id"]).getSource().clear();
        }
        var selectToolName = $(this).children("option:selected").val()
        if (selectToolName == "MHP") {
            current_mode = "MHP";
            setMyLayersVisibility("MHPRivers", true)
        } else if (selectToolName == "BAT") {
            current_mode = "BAT";
            setMyLayersVisibility("MHPRivers", false)
        } else {
            current_mode = "SST"
            setMyLayersVisibility("MHPRivers", false)
        }
        $.ajax({
            url: "/change_tool_tab_contents",
            data: {
                mode: current_mode
            },
            success: function (data, status) {
                $('.changetab-content').empty();
                $('.changetab-content').html(data);
            }
        });
        $.ajax({
            url: "/change_tool_tab",
            data: {
                mode: current_mode
            },
            success: function (data, status) {
                $('.changetab').empty();
                $('.changetab').html(data);
            }
        });
        $.ajax({
            url: "/change_result_footer",
            data: {
                mode: current_mode
            },
            success: function (data, status) {
                $('#result-box').empty();
                $('#result-box').html(data);
            }
        });
    });

    var MHP_layer_list = [
        { layer_id: 'Dam',         layer_name: 'Intake',      style: dam },
        { layer_id: 'Power_House', layer_name: 'Power House', style: powerhouse },
        { layer_id: 'Upstreams',   layer_name: 'Upstreams',   style: upstream },
        { layer_id: 'MHPRivers',   layer_name: 'MHP Rivers',  style: rivers_style },
        { layer_id: 'AOI',         layer_name: 'AOI',         style: BATPolygon },
    ];

    const makeLayerControlItem = (layerId, layerName) => `
        <div class="checkbox">
            <label>
                <input type="checkbox" class="layer check-layer" id="${ layerId}" checked> ${layerName}
            </label>
            <div class="label-img"></div>
        </div>`;

    // adding the mhp layers and it's on off checkbox(layer control item)
    MHP_layer_list.forEach(({ layer_id, layer_name, style }) => {
        $('.mhp-layers').append(makeLayerControlItem(layer_id, layer_name));
        addingvectorlayers(layer_id, layer_name, style, `/static/img/MHPResulticons/${layer_name}.svg`, 15, 15);
    });
    // sampling layers
    var spatialSamplingToolLayersList = [
        { "layer_id": 'spatialsamplingtool', "layer_name": 'Sampling', 'style': samplingStyle }
    ];

    // adding the sst layers and it's on off checkbox(layer control item)
    spatialSamplingToolLayersList.forEach(({ layer_id, layer_name, style }) => {
        $('.sst-layers').append(makeLayerControlItem(layer_id, layer_name));
        addingvectorlayers(layer_id, layer_name, style, `/static/img/spatialsamplingTool/${layer_name}.svg`, 18, 18);
    });

    getLayer('MHPRivers').setSource(mhpRiversSource);

    var riverWFSLayer = getLayer('MHPRivers');
    // document.querySelector('img.svg-dynamic');

    var select_MHP = new ol.interaction.Select({
        layers: [getLayer('Dam')]
    });
    select_MHP.set('name', 'select_MHP');

    var modify_MHP = new ol.interaction.Modify({
        features: select_MHP.getFeatures()
    });
    modify_MHP.set('name', 'modify_MHP');

    setMyLayersVisibility("MHPRivers", false)

    $('#result-box > div.result-title > div > ul > li').click(() => {
        setTimeout(function () {
            Highcharts.charts.forEach(chart => {
                if (chart && chart.chartHeight < 450) {
                    chart.reflow();
                }
            })
        }, 500);
    });

    $(document).on("click", "#sst-process", function (e) {
        var selmuni = parseInt($(".selGaunagar").val());
        var process = $("#loader-ouer");
        const data = { ddmmm: selmuni };
        if ($('#ppp').length) // check this to see if a project is open
        {
            data.project_id = $('#ppp').attr('projectid');
            data.existing_project = true;
        }
        if (selmuni) {
            $.ajax({
                url: "/spatialsampling/",
                data: data,
                beforeSend: function () {
                    process.show()
                },
                success: function (data) {
                    if (data.invalid) {
                        swal({
                            title: "Processing Error",
                            text: "Something Went Wrong"
                        });
                    } else {
                        $('.results-wrap').empty();
                        $('.results-wrap').append(data);
                    }
                },
                error: error => {
                    swal({
                        title: "Processing Error",
                        text: `Error ${error.status}: ${error.statusText}`,
                    });
                },
                complete: () => process.hide()
            });
        } else {
            swal({
                title: "Municipality is not selected",
                text: "Please select municipality from the drop down menu"
            });
        }
    });
    $(".layer").parent().parent().each(function () {
        $(this).addClass("alignTop");
        var a = $(this).html();
        var updateHtml = "<div>" + a + "</div>"
        $(this).html(updateHtml);
        // console.log(a);
        var a = $(this).children().eq(0).children().eq(0).children().eq(0).attr('id');
        if (metaData[a]) {
            var html = '<div><i class="fa fa-info-circle info-icon" title="<strong>Source:</strong> ' + metaData[a]["Source"] + '<br/> <strong>Description:</strong> ' + metaData[a]["Description"] + '"></i></div>';
            $(this).children().eq(0).after(html);
        }
    });

    $('.info-icon').tooltip({
        content: function () {
            return $(this).attr('title');
        }
    });

    $('#accordion2').children().each(function (index) {
        var OuterHeadingDiv = $(this).children().eq(0);
        var currentCheckboxClassName = OuterHeadingDiv.children().eq(0).children().eq(0).text();
        var oldhtml = OuterHeadingDiv.html();
        var newHTMl = '<div class="alignTop">\n' +
            '    <div>' + oldhtml + '</div>\n' +
            '    <div>\n' +
            '        <input type="checkbox" class="' + currentCheckboxClassName.trim() + '-title' + '">\n' +
            '    </div>\n' +
            '</div>';
        OuterHeadingDiv.html(newHTMl);

        $(this).find('.layer').addClass(currentCheckboxClassName.trim() + '-layergroup');
        //  Layer change effect on select all layer on
        $(this).find('.layer').change(function () {
            // console.log(this);
            if ($(this).prop('checked') == false) {
                $('.' + currentCheckboxClassName.trim() + '-title').prop('checked', false)
            } else {
                var totalCountLayer = $('.' + currentCheckboxClassName.trim() + '-layergroup').length;
                var totalCountCheckedLayer = $('.' + currentCheckboxClassName.trim() + '-layergroup:checked').length;
                if (totalCountLayer == totalCountCheckedLayer) {
                    $('.' + currentCheckboxClassName.trim() + '-title').prop('checked', true)
                }
            }
        });
        //select all layer change effect action
        $(document).on('change', '.' + currentCheckboxClassName.trim() + '-title', function () {
            if ($('.' + currentCheckboxClassName.trim() + '-title').prop('checked') == true) {
                $('.' + currentCheckboxClassName.trim() + '-layergroup').prop('checked', true);
                $('.' + currentCheckboxClassName.trim() + '-layergroup').each(function (index1) {
                    var layer_id = $(this).attr('id');
                    getLayer(layer_id).setVisible(true);
                })
            } else {
                $('.' + currentCheckboxClassName.trim() + '-layergroup').prop('checked', false);
                $('.' + currentCheckboxClassName.trim() + '-layergroup').each(function (index1) {
                    var layer_id = $(this).attr('id');
                    getLayer(layer_id).setVisible(false);
                })
            }
        });
    });

    window.onload = () => {
        // adding legend for layers
        $(".check-layer").each(function () {
            const layerId = $(this).attr("id");
            var legend = getLayer(layerId).get("legendPath");
            var imgHTMl = `<img name="${layerId}" src="${legend}">`;
            $(imgHTMl).prependTo($(this).parents().children("div.label-img"));
        });

        // deferred loaded layers
        Object.entries(gauriganjSurveyLayers).forEach(([filename, layer]) => {
            fetch(`/static/js/layers/${filename}.json`)
                .then(response => response.json())
                .then(layerData => {
                    layer.getSource().addFeatures((new ol.format.GeoJSON()).readFeatures(layerData));
                });
        });
        // deferred teraigeojson loading
        fetch('/static/js/layers/terai.json')
            .then(response => response.json())
            .then(geojson => teraiGeoJSON = geojson);
        // restriction layer or working area ajax call
        $.ajax({
            url: "/working_area_extent",
            beforeSend() {
                $('#draw-polygon-button-list').append('<div class="absolute-block overlay-block" id="polygon_draw_loader"><i class="fa fa-spinner fa-spin centered-block" style="font-size: 39px;"></i></div>')
            },
            complete() {
                $('#polygon_draw_loader').remove();
            },
            success(data) {
                const restrictionSource = vectorRestrictionLayer.getSource();
                const parser = new ol.format.GeoJSON();
                restrictionSource.clear();
                restrictionSource.addFeatures(parser.readFeatures(data));
                // restriction layer
                const contour = data;
                rewindedPolygons = turf.rewind(contour);
                conditionNoModifierKeysWithin = function (mapBrowserEvent) {
                    var drawWithin = rewindedPolygons.features.some(feat => {
                        return turf.booleanPointInPolygon(mapBrowserEvent.coordinate, feat);
                    });
                    var originalEvent = mapBrowserEvent.originalEvent;
                    return (
                        !originalEvent.altKey &&
                        !(originalEvent.metaKey || originalEvent.ctrlKey) &&
                        !originalEvent.shiftKey && drawWithin
                    );
                };

                pointerMoveHandler = function (evt) {
                    if (evt.dragging) {
                        return;
                    }
                    /** @type {string} */
                    var helpMsg = 'Click to start drawing';

                    if (sketch) {
                        var geom = (sketch.getGeometry());
                        var withinSketched = turf.booleanPointInPolygon(evt.coordinate, rewindedPolygons.features[0]);
                        if (withinSketched) {
                            helpMsg = continuePolygonMsg;
                        } else {
                            helpMsg = avoidDrawingHere;
                        }
                    } else {
                        var within = rewindedPolygons.features.some(feat => {
                            return turf.booleanPointInPolygon(evt.coordinate, feat);
                        });
                        if (!within) {
                            helpMsg = 'You are not allowed to start drawing from here'
                        }
                    }
                    helpTooltipElement.innerHTML = helpMsg;
                    helpTooltip.setPosition(evt.coordinate);

                    helpTooltipElement.classList.remove('hidden');
                };
            }
        });
    };
});

function removeAllToolInteractions() {
    const toolInteractions = ['select_line', 'drawTool', 'select']
    map.getInteractions().forEach(interaction => {
        if (interaction && toolInteractions.includes(interaction.get('name'))) {
            map.getInteractions().remove(interaction);
        }
    });
    map.getOverlays().forEach(overlay => {
        if (overlay.get('name') === 'helpTooltip') {
            map.getOverlays().remove(overlay);
        }
    });
    map.getViewport().style.cursor = 'default';
}
// for highcharts fit to extent on window resize
let resizerTimeout;
window.addEventListener('resize', () => {
    clearTimeout(resizerTimeout)
    resizerTimeout = window.setTimeout(() => {
        let fitChartToDiv = chart => chart && chart.reflow();
        // if this is the dashboard
        if (isDashboard) {
            // function to manually resize div
            // gotta resize the dashboard charts like this cause the population chart just keeps getting taller on chart.reflow()
            fitChartToDiv = (chart) => {
                if (chart) {
                    const containerWidth = chart.renderTo.offsetWidth;
                    const containerHeight = chart.renderTo.offsetHeight;
                    chart.setSize(containerWidth, containerHeight);
                    if (chart.chartHeight > 270) {
                        chart.setSize(chart.chartWidth, 270);
                    }
                }
            }
        }
        // fitting all charts to containerdiv
        Highcharts.charts.forEach(fitChartToDiv);
        // handling sidebars visibility
        if (window.innerWidth > 767) {
            $('.sidebar').css('visibility', 'visible');
        }
        else {
            $('.sidebar').css('visibility', 'hidden');
        }
    }, 350);
});