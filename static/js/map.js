let map, heatmap, data;

function toLatLng(lat, lng) {
    return new google.maps.LatLng(lat, lng);
}

function fromJSON(json) {
    let input = JSON.parse(json.replace(/&#34;/g, '"'))
    console.log(input)
    data = [];
    for (let key in input) {
        if (input.hasOwnProperty(key))
            data.push({location: toLatLng(input[key].lat, input[key].lng), weight: input[key].count})
    }
    console.log(data)
}

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
    zoom: 13,
    center: {lat: 40, lng: -75.146},
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
