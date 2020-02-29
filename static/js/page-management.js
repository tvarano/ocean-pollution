let activeFilters = [];

function setInitialFilters() {
    setFilters($("#option-form").serializeArray());
}

function setFilters(filts) {
    activeFilters = [];
    filts.forEach((f) => {
        if (f.value == 'on')
        activeFilters.push(f.name);
    })
}

function submitFilters() {
    $.post("/query", $("#option-form").serializeArray(), function(data) {
        refreshPage(readDate(), data);
    });
}

function refreshPage(date, raw) {
    if (date.month == -1) 
        $("#date-header")[0].innerHTML = 'All Data';
    else 
        $("#date-header")[0].innerHTML = `${date.month} / ${date.year}`;
    let data = JSON.parse(raw.replace(/&#34;/g, '"'))

    importMapData(data);
    initMap();
    setAvailableZones(data)

    refreshAnalysis(date)
    $('#load').hide();
    closeNav();
}

function refreshAnalysis(date) {
    if (!date)
        date = readDate()
    $.post("/zone", zoneFilters(date), function(data) {
		//console.log(data)
        let meas = $('input[name="measurement"]:checked').val();
        console.log(meas)
		if (data)
             setAnalysis(meas, data);
    });
}

function setAvailableZones(data) {
    const dropdown = $('#zone-selection')
    dropdown.empty()
    for (const key of Object.keys(data)) {
        //console.log(dropdown)
        if (key.endsWith("USA"))
            dropdown.append(`<option value=\'${key}\'>${key}</option>`)
    }
}

function zoneFilters(date) {
    let zone = $("#zone-selection option:selected" ).text();
    return {"month": date["month"], "year": date["year"], zone:zone, filters:JSON.stringify(activeFilters)}

}

function setAnalysis(meas, data) {
    //find min, max
    var size = 300;
	//console.log(meas);
	data = JSON.parse(data);
	console.log(data["lbs_mile"]);
    if (meas == 'lbs') {
        radialLaunch(0, 616, data["lbs"],size, "lbs", "per")
        radialLaunch(0, 440, data["lbs_mile"],size,"lbs / mile", "per-mile")
        radialLaunch(0, 33, data["lbs_person"],size, "lbs / person", "per-person")
        //radialLaunch(0, 100, data["lbs_adult"],size, "lbs / adult", "per-adult")
    } else {
        radialLaunch(0, 1006, data["num_items"],size, "items", "per")
        radialLaunch(0, 720, data["cnt_mile"],size, "items / mile", "per-mile")
        radialLaunch(0, 53, data["cnt_person"],size, "items / person", "per-person")
        //radialLaunch(0, 100, data["cnt_adult"],size, "items / adult", "per-adult")
    }
}


function readDate() {
    return {month: $("#month-input").val(), year: $("#year-input").val() }
}


// radial control

function radialLaunch(min, max, value,size,units, renderTo){
    var diff = max - min;
    var avg = diff/6;
    var gauge = new RadialGauge({
        renderTo: renderTo,
        width: size,
        height: size,
        units: units,
        value: min,
        minValue: min,
        startAngle: 90,
        ticksAngle: 180,
        valueBox: true,
        maxValue: max,
        majorTicks: [
            ""+Math.floor(min+(avg*0)),
            ""+Math.floor(min+(avg*1)),
            ""+Math.floor(min+(avg*2)),
            ""+Math.floor(min+(avg*3)),
            ""+Math.floor(min+(avg*4)),
            ""+Math.floor(min+(avg*5)),
            ""+max,
        ],
        minorTicks: 2,
        strokeTicks: true,
        highlights: [
            {
              "from": min,
              "to": (min+(avg*2)),
              "color": "rgba(200, 50, 50, .75)"
            },
            {
              "from": (min+(avg*2)),
              "to": (min+(avg*4)),
              "color": "rgba(220, 200, 0, .75)"
            },
            {
                "from": (min+(avg*4)),
                "to": max,
                "color": "rgba(100, 255, 100, .2)"
            }
        ],
        colorPlate: "#fff",
        borderShadowWidth: 0,
        borders: false,
        needleType: "arrow",
        needleWidth: 5,
        needleCircleSize: 2,
        needleCircleOuter: true,
        needleCircleInner: false,
        animationDuration: 1500,
        animationRule: "linear"
    }).draw();
    
    setInterval(function() {
      
      // update the above chart...
      gauge.value = value;
      
      // Update the declarative chart...
      document.getElementById(renderTo).setAttribute("data-value", value);
    }, 1800);
}
