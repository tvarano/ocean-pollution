function refreshPage(month, year, data) {
    $("#date-header")[0].innerHTML = `${month}, ${year}`;

    importFromJSON(data);
    initMap();

    setAnalysis();
}

function setAnalysis() {

}


