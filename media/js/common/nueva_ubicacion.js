// Variables globales para las referencias
var c = 0;
var vlp = 0;
var references = new Array();
var map;
var poly = [];
var polygon = [];
// Variables globales para los poligonos
var poly_puntos = [];
var polygonos = [];
i = 0;
j = 0;
l = 0;
var color = "#0024C1";

function Reference() {
	
	this.id = null;
	this.marker = null;
	
	this.create = function() {
		this.id = c;
		var punto = new GLatLng(map.getCenter().lat(), map.getCenter().lng());
		var baseIcon = new GIcon(G_DEFAULT_ICON);;
		if (c < 10) {
			baseIcon.image = "/media/img/recursos/googleMapsIcons/black0" + c + ".png";
		}
		else{
			baseIcon.image = "/media/img/recursos/googleMapsIcons/black" + c + ".png";
		}
		this.marker = new GMarker(punto, {icon:baseIcon, draggable:true});
		map.addOverlay(this.marker);
		this.marker.enableDragging();		
		
		GEvent.addListener(this.marker, "dragend", function() {
			var location = references[vlp].marker.getPoint().toUrlValue();
			var poly_puntos = location.split(",");
			document.getElementById("lat" + references[vlp].id).value = poly_puntos[0];
			document.getElementById("lng" + references[vlp].id).value = poly_puntos[1];
		});
	}
	
	this.borrar = function() {
		map.removeOverlay(this.marker);
		delete this;
	}
}

function load() {
	if(GBrowserIsCompatible()) {
		// Propiedades del mapa
		map = new GMap2(document.getElementById("map"));
		map.setCenter(new GLatLng(-16.385532,-71.541681), 13);
		map.addControl(new GMapTypeControl());
		map.addControl(new GLargeMapControl());
		map.addControl(new GScaleControl());
		
		// Nuevo punto para el proyecto
		var punto = new GLatLng(-16.385532,-71.541681);					
		var baseIcon = new GIcon(G_DEFAULT_ICON);
		var marker = new GMarker(punto ,{icon:baseIcon,draggable:true});
		map.addOverlay(marker);
		marker.enableDragging();
		
		GEvent.addListener(marker, "dragstart", function() {
			map.closeInfoWindow();
		});

		GEvent.addListener(marker, "dragend", function() {
			var location = marker.getPoint().toUrlValue();
			var poly_puntos = location.split(",");
			document.getElementById("id_latitud").value=poly_puntos[0];
			document.getElementById("id_longitud").value=poly_puntos[1];
		});
		
		// Manejo de referencias
		$(".agregar").click(function(){
			c++;
			$(".elem").append("<div class='info'><ul><li>Detalles para el punto " + c + "<li><h3>Nombre:</h3><input type='text' class='nombre' name='nombre" + c + "' /></li><li><h3>Descripción:</h3><textarea class='coment' name='des" + c + "'></textarea></li><li><h3>Icono:</h3><input type='file' id='imagen' name='img" + c + "' /></li><li><div class='eliminar' id='del" + c + "'>Eliminar</div></li><input type='hidden' id='lng" + c + "' name='lng" + c + "' value='-71.541681' /><input type='hidden' id='lat" + c + "' name='lat" + c + "' value='-16.385532'/></ul></div>");
			references[c] = new Reference();
			references[c].create(punto);
		});
	
		$(".eliminar").live('click', function(event) {
			cl = $(this).attr('id').split("l");
			$(this).parent().parent().parent().remove();
			references[cl[1]].borrar();
			return false;
			event.preventDefault();
		});
	
		$("map[name]").live('mouseover' , function(){
			vl = $(this).attr('name');
			vlp = vl.split("p")
			vlp = vlp[1];
		});
	
		$("img[id]").live('mouseover' , function(){
			vl = $(this).attr('id');
			vlp = vl.split("_")
			vlp = vlp[2];
		});
		
		GEvent.addListener(map, 'click', function(overlay, latlng){
			checkeado = $("#crearPolygon").attr("value");
			if(checkeado  == "false") {
				poly_puntos[i] = new GLatLng(latlng.lat(), latlng.lng());
				poly[i] = new GPolyline([poly_puntos[i-1], poly_puntos[i]], color, 3, 0.9, color, 0.2);
				i++;
				for (l = 0; l < i; l++) {
					map.addOverlay(poly[l]);
				}			
			}			
		});
			
		$("#crearPolygon[value=false]").live('click' , function(event){
			$("#crearPolygon").attr("value", "true");
			$("#crearPolygon").html("Dibujar terreno");
			$("#map div").css("cursor", "url(http://maps.gstatic.com/intl/es_ALL/mapfiles/openhand_8_8.cur), default");
			polygonos[j] = poly_puntos;
			polygon[j] = new GPolygon(polygonos[j], color, 2, 1, color, 0.3);
			for (l = 0; l < i; l++) {
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

$(document).ready(function(){
	$("#id_latitud").val(-16.385532);
	$("#id_longitud").val(-71.541681);
	$("#ayuda_poligono").css("display", "none");
	
	$("#crearPolygon[value=true]").live('click', function(event){
		$("#map div").css("cursor","crosshair");
		$("#crearPolygon").attr("value", "false");
		$("#crearPolygon").html("Cerrar el terreno");
		return false;
		event.preventDefault();
	});
	
	$("#save").click(function(event){
		$("#num_ref").val(c);
		$("#num_pol").val(j);
		for(x = 0; x < j; x++) {
			$("#poligono").append("<input type='hidden' name='num_pol_" + x + "' value='" + polygonos[x].length + "'>");
		}
	});
	
	$("#limpiarPoligono").click(function(event){
		for (l = 0; l < j ; l++){
			map.removeOverlay(polygon[l]);	
		}
		$("#poligonos").html("");
		$("#num_ini_pol").val(j);
		return false;
		event.preventDefault();
	});
})
