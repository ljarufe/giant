// Variables globales para los poligonos
var poly_puntos = [];
var polygonos = [];
var poly = [];
var polygon = [];
var map;
i = 0;
j = 0;
l = 0;
var color = "#0024C1";

// Despliega un mapa para seleccionar un terreno
function initialize() {		
	if (GBrowserIsCompatible()) {
		map = new GMap2(document.getElementById("map"));
		map.addControl(new GMapTypeControl());
		map.addControl(new GLargeMapControl());
		var center = new GLatLng(-16.398778,-71.536996);	
		map.setCenter(center, 16);
		var marker = new GMarker(center, {draggable: true});
		map.addOverlay(marker);
				
		// Obtener un link con la ubicación seleccionada a google maps
		GEvent.addListener(marker, "dragend", function() {
			var location = marker.getPoint().toUrlValue();
			var latlng = location.split(",");
			$("#id_latitud").val(latlng[0]);
			$("#id_longitud").val(latlng[1]);
		});
		
		// Manejo de poligonos
		GEvent.addListener(map, 'click', function(overlay, latlng){
			checkeado = $("#crearPolygon").attr("value");
			if(checkeado  == "false") {
				poly_puntos[i] = new GLatLng(latlng.lat(), latlng.lng());
				poly[i] = new GPolyline([poly_puntos[i-1], poly_puntos[i]], color, 3, 0.9, color, 0.2);
				i++;
				for(l=0;l<i;l++){
					map.addOverlay(poly[l]);
				}
				
							
			}			
		});
			
		$("#crearPolygon[value=false]").live('click' , function(event){
			$("#crearPolygon").attr("value", "true");
			$("#crearPolygon").html("Dibujar terreno")
			$("#map div").css("cursor","url(http://maps.gstatic.com/intl/es_ALL/mapfiles/openhand_8_8.cur), default");
			polygonos[j] = poly_puntos;
			polygon[j] = new GPolygon(polygonos[j], color, 2, 1, color, 0.3);
			for(l=0;l<i;l++){
				map.removeOverlay(poly[l]);
			}
			map.addOverlay(polygon[j]);
			for(x = 0; x < i; x++) {
				$("#poligonos").append("<input type='hidden' value='" + poly_puntos[x].lat() + "' name='lat_" + j + "_" + x + "'>");
				$("#poligonos").append("<input type='hidden' value='" + poly_puntos[x].lng() + "' name='lng_" + j + "_" + x + "'>");
			}
			j++;
			poly_puntos = [];
			i = 0;
			return false;
			event.preventDefault();
		});
	}
}

$(document).ready(function() {
	initialize();
	$("#id_latitud").val(-16.385532);
	$("#id_longitud").val(-71.541681);
	
	$("#crearPolygon[value=true]").live('click', function(event){
		$("#map div").css("cursor","crosshair");
		$("#crearPolygon").attr("value", "false");
		$("#crearPolygon").html("Cerrar el terreno");
		return false;
		event.preventDefault();
	});
	
	$("#ayuda").click(function(event){
		return false;
		event.preventDefault();
	});
	$("#limpiarPoligono").click(function(event){
		for(l=0;l<j;l++){
			map.removeOverlay(polygon[l]);
		}
		$("#poligonos").html("");
		$("#num_ini_pol").val(j);
		return false;
		event.preventDefault();
	});
	
	$("#save").click(function(event){
		$("#num_pol").val(j);
		for(x = 0; x < j; x++) {
			$("#poligono").append("<input type='hidden' name='num_pol_" + x + "' value='" + polygonos[x].length + "'>");
		}
	});
})
