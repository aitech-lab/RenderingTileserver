
window.init = ()->
    console.log "create map"
    console.log "leaflet version #{L.version}"


    L.CRS.Simple = L.Util.extend {}, L.CRS,
        projection: L.Projection.LonLat,
        transformation: new L.Transformation(1, 0, 1, 0)
        scale: (zoom)->256* Math.pow(2, zoom)


    tl = L.tileLayer("http://localhost:9090/tile/{z}/{x}/{y}", {maxZoom: 10, minZoom: 0})

    window.map = L.map 'map', 
        center            : [0.5, 0.5] 
        zoom              : 0
        minZoom           : 0 
        maxZoom           : 12
        crs               : L.CRS.Simple
        attributionControl: false

    map.addLayer tl

