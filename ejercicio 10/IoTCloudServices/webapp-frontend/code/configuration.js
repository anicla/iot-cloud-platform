const server_address = `${window.location.protocol}//${window.location.hostname}:5003/`;

function get_container_id() {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get("container");
}

function search_container_configuration() {
  const containerId = get_container_id();
  const table = document.createElement("table");
  table.innerHTML = "<tr><th>Frecuencia sensores</th><th>Frecuencia telemetria</th><th>Estado</th></tr>";

  $.getJSON(server_address + "containers/config/", { container_id: containerId }, function(result) {
    const row = document.createElement("tr");
    row.innerHTML = `<td>${result.sensors_rate || "N/A"}</td><td>${result.telemetry_rate || "N/A"}</td><td>${result.status || "N/A"}</td>`;
    table.appendChild(row);
    document.getElementById("configuration_viewer").appendChild(table);
  });
}

function update_configuration() {
  const body = {
    container_id: get_container_id(),
    sampling: $("#samplingFrequencyInputText").val(),
    rate: $("#sendingFrequencyInputText").val(),
  };
  $.post(server_address + "containers/config/", body, function() {
    alert("Configuracion actualizada correctamente");
  }).fail(function(xhr) {
    alert("Error actualizando configuracion");
    console.error(xhr.responseText);
  });
}
