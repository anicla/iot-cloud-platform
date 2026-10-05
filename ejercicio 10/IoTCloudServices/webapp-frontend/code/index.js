let map;
const server_address = `${window.location.protocol}//${window.location.hostname}:5003/`;

window.initMap = initMap;
setInterval(initMap, 60000);

async function initMap() {
  const position = { lat: 40.33256, lng: -3.76516 };
  const { Map } = await google.maps.importLibrary("maps");
  await google.maps.importLibrary("marker");
  map = new Map(document.getElementById("map"), {
    center: position,
    zoom: 10,
    mapId: "DEMO_MAP_ID",
  });

  const infoWindow = new google.maps.InfoWindow();
  $.getJSON(server_address + "containers/active/", function(result) {
    $.each(result, function(index, item) {
      const markerPosition = {
        lat: parseFloat(item.Latitude),
        lng: parseFloat(item.Longitude),
      };
      const pin = new google.maps.marker.PinElement({ glyphText: "C", glyphColor: "white" });
      const marker = new google.maps.marker.AdvancedMarkerElement({
        map: map,
        position: markerPosition,
        content: pin.element,
        title: item.Container_id,
        gmpClickable: true,
      });
      marker.addListener("click", () => {
        infoWindow.close();
        infoWindow.setContent(`
          <div>
            <h3>${item.Container_id}</h3>
            <p><a href="./telemetry.html?container=${item.Container_id}">Telemetria</a></p>
            <p><a href="./configuration.html?container=${item.Container_id}">Configuracion</a></p>
          </div>
        `);
        infoWindow.open(marker.map, marker);
      });
    });
  });
}
