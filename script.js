
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
  document.getElementById("gauge").setAttribute("data-value", value);
}, 1800);
}