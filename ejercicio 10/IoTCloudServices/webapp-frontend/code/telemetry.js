const server_address = `${window.location.protocol}//${window.location.hostname}:5003/`;

function load_telemetry() {
  const urlParams = new URLSearchParams(window.location.search);
  const containerId = urlParams.get("container");
  const table = document.createElement("table");
  table.innerHTML = "<tr><th>Temperatura</th><th>Humedad</th><th>Puerta</th><th>Motor</th><th>Tiempo</th></tr>";

  $.getJSON(server_address + "containers/telemetry/", { container_id: containerId }, function(result) {
    $.each(result, function(index, item) {
      const row = document.createElement("tr");
      row.innerHTML = `<td>${item.temperature}</td><td>${item.humidity}</td><td>${item.door_open}</td><td>${item.refrigerator_fan}</td><td>${item.time_stamp}</td>`;
      table.appendChild(row);
    });
    document.getElementById("telemetry_list").appendChild(table);
  });
}
