var mymap = L.map('mapid').setView([1.3146631, 103.8454093], 13);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1Ijoiam9kaWVldGhlbGRhIiwiYSI6ImNrYTd5NjRncTA3N2EyeHBwcm9pMmo5Z3MifQ.5d3yOSlKUEHOVCFJAU_EnQ'
}).addTo(mymap);

var source = new EventSource('/topic/twitterdata1');

source.addEventListener('message', function (e) {
    obj = JSON.parse(e.data);
    console.log(obj);
    lat = obj.place.bounding_box.coordinates[0][0][1];
    long = obj.place.bounding_box.coordinates[0][0][0];
    username = obj.user.name;
    tweet = obj.text;
    place = obj.place.full_name;

    marker = L.marker([lat, long]).addTo(mymap).bindPopup('Username: <strong>' + username + '</strong><br>Tweet: <strong>' + tweet + '</strong>' + '<br>Place: <strong>' + place + '</strong>');


}, false);