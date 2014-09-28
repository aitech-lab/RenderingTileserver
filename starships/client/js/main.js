// Generated by CoffeeScript 1.7.1
window.init = function() {
  var tl;
  console.log("create map");
  console.log("leaflet version " + L.version);
  L.CRS.Simple = L.Util.extend({}, L.CRS, {
    projection: L.Projection.LonLat,
    transformation: new L.Transformation(1, 0, 1, 0),
    scale: function(zoom) {
      return 256 * Math.pow(2, zoom);
    }
  });
  tl = L.tileLayer("http://localhost:9090/tile/{z}/{x}/{y}", {
    maxZoom: 10,
    minZoom: 10
  });
  window.map = L.map('map', {
    center: [0.5, 0.5],
    zoom: 0,
    minZoom: 10,
    maxZoom: 10,
    crs: L.CRS.Simple,
    tms: false,
    attributionControl: false,
    zoomControl: false,
    tileSize: 256
  });
  return map.addLayer(tl);
};
