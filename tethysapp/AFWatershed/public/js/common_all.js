myApp.InlineRadio = function (ID, name, InnerText, checked, LayerId) {
    let OuterDiv = myApp.createDiv('custom-control custom-radio custom-control-inline')

    let RadioInput = myApp.createInput('custom-control-input');
    RadioInput.setAttribute('type', 'radio');
    RadioInput.setAttribute('id', ID);
    RadioInput.setAttribute('LayerId', LayerId);
    RadioInput.setAttribute('name', name);
    RadioInput.checked = checked;

    let LavelTag = myApp.createLabel('custom-control-label');
    LavelTag.setAttribute('for', ID);
    LavelTag.innerText = InnerText;

    OuterDiv.append(RadioInput);
    OuterDiv.append(LavelTag);

    return OuterDiv
}

myApp.createElement = function (type, className) {
    var element = document.createElement(type);
    if (className) {
        let classList = className.split(" ")
        element.classList.add(...classList);
    }
    return element
}

myApp.createDiv = function (ClassName) {
    var div = myApp.createElement('div', ClassName);
    return div;
}

myApp.createSpan = function (ClassName) {
    var span = myApp.createElement('span', ClassName);
    return span;
}

myApp.createA = function (ClassName) {
    var a = myApp.createElement('a', ClassName);
    return a;
}
myApp.createButton = function (ClassName) {
    var a = myApp.createElement('button', ClassName);
    return a;
}
myApp.createI = function (ClassName) {
    var i = myApp.createElement('i', ClassName);
    return i;
}
myApp.createImg = function (ClassName) {
    var img = myApp.createElement('img', ClassName);
    return img;
}
myApp.createInput = function (ClassName) {
    var i = myApp.createElement('input', ClassName);
    return i;
}
myApp.createSelect = function (ClassName) {
    var i = myApp.createElement('select', ClassName);
    return i;
}
myApp.createOption = function (ClassName) {
    var i = myApp.createElement('option', ClassName);
    return i;
}
myApp.createH = function (HeadingNumber, ClassName) {
    var i = myApp.createElement('h' + HeadingNumber.toString(), ClassName);
    return i;
}
myApp.createLabel = function (ClassName) {
    var i = myApp.createElement('label', ClassName);
    return i;
}
myApp.createInput = function (ClassName) {
    var i = myApp.createElement('input', ClassName);
    return i;
}
myApp.createHr = function (ClassName) {
    var i = myApp.createElement('hr', ClassName);
    return i;
}
myApp.createP = function (ClassName) {
    var i = myApp.createElement('p', ClassName);
    return i;
}
myApp.createStrong = function (ClassName) {
    var i = myApp.createElement('strong', ClassName);
    return i;
}

let layerCheckBoxBinding = function (AppendingDivID, LayerObject, OpacitySlider, LegendDropDown, customCSSClass) {
    this.DivVisible = false;
    this.divID = AppendingDivID;
    this.layerObj = LayerObject;
    this.DisplayOpacity = OpacitySlider;
    this.DisplayLegendDropDown = LegendDropDown;
    this.maskObjList = [];
    this.createElement = function (type, className) {
        var element = document.createElement(type);
        if (className) {
            let classList = className.split(" ")
            element.classList.add(...classList);
        }
        return element
    };
    this.createDiv = function (ClassName) {
        var div = this.createElement('div', ClassName);
        return div;
    };
    this.createSpan = function (ClassName) {
        var span = this.createElement('span', ClassName);
        return span;
    };
    this.createA = function (ClassName) {
        var a = this.createElement('a', ClassName);
        return a;
    };
    this.createButton = function (ClassName) {
        var a = this.createElement('button', ClassName);
        return a;
    };
    this.createI = function (ClassName) {
        var i = this.createElement('i', ClassName);
        return i;
    };
    this.createImg = function (ClassName) {
        var img = this.createElement('img', ClassName);
        return img;
    };
    this.createInput = function (ClassName) {
        var i = this.createElement('input', ClassName);
        return i;
    };
    this.createSelect = function (ClassName) {
        var i = this.createElement('select', ClassName);
        return i;
    };
    this.createOption = function (ClassName) {
        var i = this.createElement('option', ClassName);
        return i;
    };
    this.createH = function (HeadingNumber, ClassName) {
        var i = this.createElement('h' + HeadingNumber.toString(), ClassName);
        return i;
    };
    this.createLabel = function (ClassName) {
        var i = this.createElement('label', ClassName);
        return i;
    };
    this.createInput = function (ClassName) {
        var i = this.createElement('input', ClassName);
        return i;
    };

    this.checkLayerProperties = function () {
        this.layerPropertiesObject = this.layerObj.getProperties();
        if (!this.layerPropertiesObject.id) {
            console.error("Please Provide Layer Id");
        }
        this.layerId = this.layerPropertiesObject.id

        if (!this.layerPropertiesObject.title) {
            console.error("Please Provide Layer title");
        }
        this.layerTitle = this.layerPropertiesObject.title;

        if (!this.layerPropertiesObject.legendPath) {
            console.error("Please Provide legend Path");
        }
        this.legendPath = this.layerPropertiesObject.legendPath;

        if (this.layerPropertiesObject.visible) {
            this.layerVisible = this.layerPropertiesObject.visible;
        } else {
            this.layerVisible = true;
        }
        this.layerVisible = this.layerPropertiesObject.visible;

        if (this.layerPropertiesObject.opacity) {
            this.layerOpacity = this.layerPropertiesObject.opacity;
        } else {
            this.layerOpacity = 1;
        }
    };

    this.LayerCheckbox = function () {
        this.outDIv = this.createDiv("LayerDiv");
        if (customCSSClass) {
            let classList = customCSSClass.split(" ")
            this.outDIv.classList.add(...classList)

        }
        let paddingDiv = this.createDiv("paddingForDiv");

        let OuterDiv = this.createDiv('custom-control custom-checkbox layerCheckPadding');
        this.CheckboxInput = this.createInput('custom-control-input');
        this.CheckboxInput.setAttribute('type', 'checkbox');
        this.CheckboxInput.setAttribute('id', this.layerId);
        this.CheckboxInput.setAttribute('LayerId', this.layerId);
        this.CheckboxInput.checked = this.layerVisible;
        let LavelTag = this.createLabel('custom-control-label');
        LavelTag.setAttribute('for', this.layerId);
        LavelTag.innerText = this.layerTitle;
        OuterDiv.append(this.CheckboxInput);
        OuterDiv.append(LavelTag);

        let ChevronDiv = this.createDiv('ChevronDiv');
        this.cheveronSapn = this.createSpan('glyphicon glyphicon-chevron-left');
        this.cheveronSapn.setAttribute('title', "Show/Hide Legend");
        this.cheveronSapn.setAttribute('show-legend', false);
        ChevronDiv.append(this.cheveronSapn)
        paddingDiv.append(OuterDiv)
        paddingDiv.append(ChevronDiv)
        this.outDIv.append(paddingDiv);


        this.legendDiv = this.createDiv('legend-div');
        this.legendDiv.style.display = 'none';
        let imgTag = this.createImg("legend-image");
        imgTag.setAttribute("src", this.legendPath);
        this.legendDiv.append(imgTag)
        this.outDIv.append(this.legendDiv);

        let LayerOpacityDiv = this.createDiv('opac-div');
        let LayerOpacityDivinner = this.createDiv();
        this.rangeInput = this.createInput('');
        this.rangeInput.setAttribute('type', 'text');
        this.rangeInput.setAttribute('data-slider-min', "0");
        this.rangeInput.setAttribute('data-slider-max', "100");
        this.rangeInput.setAttribute('data-slider-step', "1");
        this.rangeInput.setAttribute('data-slider-value', "100");
        this.rangeInput.setAttribute('data-slider-id', "ex1Slider");
        this.rangeInput.setAttribute('name', "OpacityRange");
        this.rangeInput.setAttribute('LayerId', this.layerId);
        this.rangeInput.setAttribute('id', this.layerId + "-Slider");

        LayerOpacityDivinner.append(this.rangeInput);
        LayerOpacityDiv.append(LayerOpacityDivinner);
        this.outDIv.append(LayerOpacityDiv);

        if (this.DisplayOpacity === false) {
            LayerOpacityDivinner.style.display = 'none';
        }
        return this.outDIv
    };

    this.bindEvents = function () {
        this.CheckboxInput.addEventListener("change", () => {
            this.layerObj.setVisible(this.CheckboxInput.checked);
            if (this.CheckboxInput.checked) {
                this.SliderObject.enable();
            } else {
                this.SliderObject.disable();
            }
        }, true);
        this.cheveronSapn.addEventListener("click", () => {
            let currentValue = this.cheveronSapn.getAttribute("show-legend");
            var isTrueSet = (currentValue === 'true');
            if (isTrueSet === true) {
                this.cheveronSapn.setAttribute("show-legend", false);
                this.legendDiv.style.display = 'none';
            } else {
                this.cheveronSapn.setAttribute("show-legend", true);
                this.legendDiv.style.display = 'block';
            }

        }, true);

        // Create a new 'change' event
        var event = new Event('change');
        // Dispatch it.
        this.CheckboxInput.dispatchEvent(event);
    };

    this.getProperties = function () {
        return this.layerObj.getProperties()
    };
    this.getDivVisible = function () {
        return this.DivVisible
    }

    this.getLayer = function () {
        return this.layerObj;
    }

    this.setVisible = function (param) {
        this.layerObj.setVisible(param);
        this.CheckboxInput.checked = param;
        this.outDIv.style.display = 'block';
        this.DivVisible = true;
        this.layerObj.visible = param;
    };

    this.setMask = function (Coods) {
        this.setMaskOrCrop(Coods, 'mask');
    };
    this.setCrop=function (Coods){
        this.setMaskOrCrop(Coods,'crop');
    }
    this.setMaskOrCrop = function (Coods, maskOrCrop) {
        let properties = this.layerObj.getProperties();
        if (properties.mask) {
            var f = new ol.Feature(new ol.geom.MultiPolygon(Coods));
            if (!this.maskObjList.length) {
                let layer = this.layerObj;
                if (properties.hasOwnProperty('ThreddsDataServerVersion')) {
                    layer.AllLayersList.forEach((timeDimensionLayer, index) => {
                        this.changeMask(timeDimensionLayer, Coods, index, false, maskOrCrop);
                    });
                } else {
                    this.changeMask(layer, Coods, 0, false, maskOrCrop);
                }
            } else {
                let layer = this.layerObj;
                if (properties.hasOwnProperty('ThreddsDataServerVersion')) {
                    layer.AllLayersList.forEach((timeDimensionLayer, index) => {
                        this.changeMask(timeDimensionLayer, Coods, index, true, maskOrCrop);
                    });
                } else {
                    this.changeMask(layer, Coods, 0, true, maskOrCrop);
                }
            }
        }
    }

    this.changeMask = (layer, Coods, ArrayIndex, deleteOrNot, maskOrCrop) => {
        if (deleteOrNot) {
            layer.removeFilter(this.maskObjList[ArrayIndex]);
        }
        var f = new ol.Feature(new ol.geom.MultiPolygon(Coods));

        let MOrC = null;
        if (maskOrCrop == 'crop') {
            MOrC = new ol.filter.Crop({feature: f, inner: false});
        } else {
            MOrC = new ol.filter.Mask({
                feature: f,
                inner: false,
                fill: new ol.style.Fill({color: [185, 185, 185, 0.7]})
            });
        }
        layer.addFilter(MOrC);
        MOrC.set('active', true);
        this.maskObjList[ArrayIndex] = MOrC;
    }

    this.setVisibleDivBind = function (param) {
        this.DivVisible = param;
        this.layerObj.setVisible(param);
        this.CheckboxInput.checked = param;
        if (param === true) {
            this.layerObj.visible = param;
            this.outDIv.style.display = 'block';
        } else {
            this.outDIv.style.display = 'none';
        }
    };

    this.init = function () {
        this.checkLayerProperties();
        let LayerCheckBox = this.LayerCheckbox();
        let AppendingDiv = document.querySelector(this.divID);
        AppendingDiv.append(LayerCheckBox);
        let that = this;
        // $('#' + this.layerId + '-Slider').slider({
        //     tooltip: 'always',
        //     value: this.layerOpacity * 100,
        //     step: 1,
        //     min: 0,
        //     max: 100,
        //     formatter: function (value) {
        //         var valueOp = parseInt(value) / 100;
        //         that.layerObj.setOpacity(valueOp);
        //         return value + " %";
        //     }
        // });

        // Without JQuery
        this.SliderObject = new Slider('#' + this.layerId + '-Slider', {
            tooltip: 'always',
            value: this.layerOpacity * 100,
            step: 1,
            min: 0,
            max: 100,
            formatter: function (value) {
                var valueOp = parseInt(value) / 100;
                that.layerObj.setOpacity(valueOp);
                return value + " %";
            }
        });

        this.bindEvents();
    };

    this.init();
}

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

myApp.notify = function (TextContent) {
    $.notify({
        // options
        icon: 'glyphicon glyphicon-warning-sign',
        title: '',
        message: TextContent,
    }, {
        // settings
        element: 'body',
        position: null,
        type: "warning",
        allow_dismiss: true,
        placement: {
            from: "top",
            align: "center"
        },
        offset: 20,
        spacing: 10,
        z_index: 1031,
        delay: 25,
        // timer: 60,
        animate: {
            enter: 'animated fadeInDown',
            exit: 'animated fadeOutUp'
        },
        icon_type: 'class',
        template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
            '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
            '<span data-notify="icon"></span> ' +
            '<span data-notify="title">{1}</span> ' +
            '<span data-notify="message">{2}</span>' +
            '<div class="progress" data-notify="progressbar">' +
            '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
            '</div>' +
            '<a href="{3}" target="{4}" data-notify="url"></a>' +
            '</div>'
    });
}

let MuntipleYearsLayer = async function (XMLCalalogURL, variableName, LayerTitle, Legend, layerVisibility, layerStyle, LayerCOLORSCALERANGE, zindex, outermostDivID, sld_body_thredds, htmlid, DataInterval, unit, mask) {
    let OuterDivLayerYearLayer = variableName + '__OuterDivMultiYearLayer'

    let appendingDiv = document.querySelector('#' + outermostDivID);
    let outerDivSelectSWEInst = myApp.createDiv(OuterDivLayerYearLayer);

    let hr1 = myApp.createHr();
    let p1 = myApp.createP()
    let st1 = myApp.createStrong();
    st1.innerText = LayerTitle;
    p1.append(st1)
    let divFormGroup = myApp.createDiv('form-group row');

    let label1 = myApp.createLabel('col-sm-6 col-form-label padding-right-0');
    label1.setAttribute('for', 'for-' + variableName);
    label1.innerText = 'Select Year:';

    let inputDiv = myApp.createDiv('col-sm-6 padding-left-0');

    let selectYYYY = myApp.createSelect("form-control form-control-sm");
    selectYYYY.setAttribute('id', 'selectYear__' + variableName);

    inputDiv.append(selectYYYY)

    divFormGroup.append(label1);
    divFormGroup.append(inputDiv);

    let layerListSWEInst = myApp.createDiv('layerList__' + variableName);

    let hr2 = myApp.createHr();

    outerDivSelectSWEInst.append(hr1);
    outerDivSelectSWEInst.append(p1);
    outerDivSelectSWEInst.append(divFormGroup);
    outerDivSelectSWEInst.append(layerListSWEInst);
    outerDivSelectSWEInst.append(hr2);

    appendingDiv.append(outerDivSelectSWEInst);

    let capabiliesXMl = await myApp.makeRequest('GET', XMLCalalogURL);
    let parser = new DOMParser();
    let xmlDoc = parser.parseFromString(capabiliesXMl, "text/xml");
    let Year_YYYY = []
    let allDataSet = xmlDoc.getElementsByTagName('dataset');
    for (let km of allDataSet) {
        let t1 = km.getAttribute('name')
        let t2 = km.getAttribute('name').replace('.ncml', '')
        if (t1 === t2) {

        } else {
            Year_YYYY.push(parseInt(t2));
        }
    }
    var min = Math.min.apply(null, Year_YYYY),
        max = Math.max.apply(null, Year_YYYY);
    var minYear = parseInt(min);
    var maxYear = parseInt(max);


    let WMSUrl = XMLCalalogURL.replace('/catalog/', '/wms/').replace("catalog.xml", '')
    myApp.AllLayers = []
    Year_YYYY.forEach(function (value) {
        $('#' + 'selectYear__' + variableName).prepend($('<option>', {
            value: value,
            text: value,
        }));

        let url = WMSUrl + value.toString() + '.ncml';
        let lyrTitle = LayerTitle.slice(0, -9) + ' (' + value.toString() + ")";
        let lyrId = variableName + "_" + value;
        var tt = new ol.layer.TimeDimensionTile({
            id: lyrId,
            title: lyrTitle,
            visible: layerVisibility,
            opacity: 0.7,
            legendPath: PROXY_PREFIX + Legend,
            showlegend: false,
            ThreddsDataServerVersion: "5",
            alignTimeSlider: 'left',
            timeSliderSize: 'small',
            zIndex: zindex,
            chartDivId: htmlid,
            ChartTitle: LayerTitle,
            DataInterval: DataInterval,
            unit: unit,
            aoi: true,
            source: {
                url: url,
                params: {
                    'VERSION': '1.1.1',
                    'LAYERS': variableName,
                    "STYLES": layerStyle,
                    "SLD_BODY": sld_body_thredds,
                }
            },
            changeWMSProxy: true,
            mask: mask,
        });
        tt.init().then(function (val) {
            myApp.map.addThreddsLayer(val);
            let l5 = new layerCheckBoxBinding("." + 'layerList__' + variableName, tt, true, true, 'withOpacSlider');
            myApp.AllBindedLayersList.push(l5);
            l5.setVisibleDivBind(false)
            myApp.AllLayers.push(l5);
        }, (error) => console.error(error))
    })
    // let currentLayer =AllLayers.filter(x => x.layerid === id)[0];
    let layerId = variableName + "_" + max.toString();

    myApp["intervalFunc_" + variableName] = function () {
        let currentLayer = myApp.AllLayers.filter(function (item) {
            let prop = item.getProperties();
            return layerId === prop.id
        })[0];
        console.log(currentLayer);
        if (currentLayer) {
            if (currentLayer.getLayer().getInitilizationStatus()) {
                currentLayer.setVisible(false);
                clearInterval(myApp["initialLayerStartInterval_" + variableName]);
                console.log("cleared");
                console.log("----------------------------------------------------------------");
                let year = layerId.replace(variableName + "_", "");
                $('#' + 'selectYear__' + variableName).val(year);
            }
        }
    }

    myApp["initialLayerStartInterval_" + variableName] = setInterval(myApp["intervalFunc_" + variableName], 20);
    $('#' + 'selectYear__' + variableName).on('change', function () {
        let layerStyle = variableName + "_";
        let LayerId = variableName + "_" + this.value;
        myApp.AllLayers.forEach(function (curObj) {
            let prop = curObj.getProperties();
            if (layerStyle === prop.id.slice(0, -4)) {
                if (LayerId === prop.id) {
                    curObj.setVisibleDivBind(true);
                } else {
                    curObj.setVisibleDivBind(false);
                }
            }
        })
    });

}

let createUILagend = function (obj) {
    this.objectProperties = obj;
    let createUI = () => {
        let layerLegendItem = myApp.createDiv('layer-legend-item');
        let checkBox = myApp.createDiv('form-check');
        this.inputCheckBox = myApp.createInput('form-check-input');
        this.inputCheckBox.setAttribute('type', 'checkbox');
        this.inputCheckBox.setAttribute('id', this.objectProperties.id + '__checkboxId');
        let label = myApp.createLabel('form-check-label');
        label.setAttribute('for', this.objectProperties.id + '__checkboxId');
        label.innerText = this.objectProperties.title;

        checkBox.append(this.inputCheckBox);
        checkBox.append(label);

        let legendImage = myApp.createImg('legend-image');
        legendImage.setAttribute('src', this.objectProperties.legendPath);

        layerLegendItem.append(checkBox);
        layerLegendItem.append(legendImage);
        this.UI = layerLegendItem;
        calculateHeightWidth();
        // setTimeout(() => {
        //     console.log(this.height);
        //     console.log(this.width);
        // }, 900)


    }


    let bindControl = () => {
        this.inputCheckBox.addEventListener("change", () => {
            let vis = this.inputCheckBox.checked;
            this.objectProperties.visible = vis;
            console.log("changeeeeee")
        }, true);


    }

    this.getUI = () => {
        return this.UI
    }

    this.setSelection = function (param) {
        this.objectProperties.visible = param;
        this.inputCheckBox.checked = param
    };
    let calculateHeightWidth = () => {
        //    height calculation
        const img = new Image();
        img.src = this.objectProperties.legendPath;
        let that = this
        img.onload = function () {
            that.objectProperties.imgWidth = this.width;
            that.objectProperties.imgHeight = this.height;
        }
    }
    let init = () => {
        createUI();
    }

    init();
    bindControl();
}
