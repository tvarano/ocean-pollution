let map, heatmap, data;
let weightMetric = 0
// 0 = count, 1 = weight, 2 = people, 3 = weight / person, 4 = weight /adult

function toLatLng(lat, lng) {
    return new google.maps.LatLng(lat, lng);
}

function importMapData(input) {
    data = [];
    for (let key in input) {
        if (key != "null" && input.hasOwnProperty(key) && !isNum(input[key])) {
            data.push({location: toLatLng(input[key].Lat, input[key].Long), weight: input[key].lbs})
        }
    }
}

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: {lat: 39.834508, lng:  -97.972085},
    mapTypeId: 'satellite'
});

heatmap = new google.maps.visualization.HeatmapLayer({
        data: data,
        map: map
    });
}
  
function toggleHeatmap() {
    heatmap.setMap(heatmap.getMap() ? null : map);
}


function isNum(n){
    return Number(n) === n;
}