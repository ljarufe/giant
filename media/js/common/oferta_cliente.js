var color = "#ff0303"

function load() {
	if(GBrowserIsCompatible()) {
		// Propiedades del mapa
		map = new GMap2(document.getElementById("map"));
		map.setCenter(new GLatLng(latitud, longitud), 15);
		map.addControl(new GMapTypeControl());
		map.addControl(new GLargeMapControl());
		map.addControl(new GScaleControl());
		
		// Nuevo punto para la ubicación
		var punto = new GLatLng(latitud, longitud);					
		var marker = new GMarker(punto);
		map.addOverlay(marker);
		
		for(j = 0; j < poligonos.length; j++) {
			var p = [];
			for(k = 0; k < poligonos[j].length; k++) {
				p_inicio = new GLatLng(poligonos[j][k].lat, poligonos[j][k].lng);
				p.push(p_inicio);
			}
			p_inicio = new GLatLng(poligonos[j][0].lat, poligonos[j][0].lng);
			p.push(p_inicio);
			var polygon = new GPolygon(p, color, 2, 0.8, color, 0.5);
			map.addOverlay(polygon);
		}
	}
}

