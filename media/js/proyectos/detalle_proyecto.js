	var color = "#0024C1";
	
	
	function load() {
		if (GBrowserIsCompatible()) {		
            var i = 0; 
			var icono = new GIcon(G_DEFAULT_ICON);
			icono.shadow = "";
			icono.iconSize = new GSize(32, 37);
			var gmarkers = [];
			var htmls = [];
			
			var map = new GMap2(document.getElementById("map"));
			var geocoder = new GClientGeocoder();

			map.setCenter(new GLatLng(latitud, longitud), 15);
			map.addControl(new GMapTypeControl());
			map.addControl(new GLargeMapControl());
			map.addControl(new GScaleControl());
			var bounds = map.getBounds();
			var southWest = bounds.getSouthWest();
			var northEast = bounds.getNorthEast();
	         function addtag(point, address) {
	               var centro = new GMarker(point);
	               map.addOverlay(centro);
	            return centro;
			 }
			 
			 var point = new GLatLng(latitud, longitud);
	         var centro = addtag(point,address);
	         GEvent.addListener(centro, "click", function(){
	             		centro.openInfoWindowHtml(address);
	         });
			 
			function crearPunto(point,adress){
				
				if (referencias[i].icono == "/media/") {
					icono.image = "http://maps.gstatic.com/intl/es_es/mapfiles/ms/micons/ylw-pushpin.png";
					icono.shadow = "http://maps.gstatic.com/intl/es_es/mapfiles/ms/micons/pushpin_shadow.png";
					icono.iconSize = new GSize(32, 32);
				}
				else {
					icono.image = referencias[i].icono;
				}
				var marker = new GMarker(point, {icon:icono});
				GEvent.addListener(marker, "click", function(){
					marker.openInfoWindowHtml(adress);
				});
				gmarkers[i] = marker;
				htmls[i] = adress;
				i++;
				return marker;	
			}
			
			function myclick(i) {
				gmarkers[i].openInfoWindowHtml(htmls[i]);
			} 
			
			for(j = 0; j < referencias.length; j++) {
				var point = new GLatLng(referencias[j].lat, referencias[j].lng);
				adress = "<h1>" + referencias[j].nombre + "</h1><p>" + referencias[j].desc + "</p>";
				var marker = crearPunto(point, adress);
				map.addOverlay(marker); 
			}
			
			for(j = 0; j < poligonos.length; j++) {
				var p = [];
				for(k = 0; k < poligonos[j].length; k++) {
					p_inicio = new GLatLng(poligonos[j][k].lat, poligonos[j][k].lng);
					p.push(p_inicio);
				}
				//p_inicio = new GLatLng(poligonos[j][0].lat, poligonos[j][0].lng);
				//p.push(p_inicio);
				var polygon = new GPolygon(p, color, 2, 0.7, color, 0.2);
				map.addOverlay(polygon);
			}
		}
	}
$(document).ready(function(){
	load();
	$("#share, #toggle_fechas, #toggle_pago, #toggle_caracteristicas, #toggle_detalle,#toggle_modelo,#toggle_terreno").hide();

	$("#trigger_share").click(function(){
		$("#share").slideToggle();
	});
	
	$(".toggle").click(function(){
		var id = $(this).attr("idb");
		$("#toggle_" + id).slideToggle();
		var source = $(this).parent().find("img").css("background-position");
		if(source == "15px 0px")
			$(this).parent().find("img").css("background-position","30px 0px");
		else
			$(this).parent().find("img").css("background-position","15px 0px");	
	});
	//$("#imagen_detalle a").colorbox();
	$('a[rel="light"]').colorbox();
	$('a[rel="models"]').colorbox();
	$('a[rel="models_table"]').colorbox();
	$(".tresd_detalle").not($(".tresd_detalle:first")).hide();
	$(".super_mini:first").css("border","1px solid red");
	$(".super_mini").click(function(event){
		var attr = $(this).attr("id");
		$(".super_mini").css("border","1px solid black");
		$(this).css("border","1px solid red");
		$(".tresd_detalle").hide();
		$("#large"+attr).fadeIn();
		return false;
		event.preventDefault();
	});
	var d = $(".tresd_detalle");
	var i = 0;
	var avance = 0;
	$("#sig").click(function(){
		if (d.length > 4){
			if ((d.length - i) == 4){
				
			}
			else{
				avance = avance + 102;
				$(".mini").scrollLeft(avance,"slow");
				i++;
			}
			
		}
		
	});
	$("#ant").click(function(){
		if (d.length > 4){
			if (avance == 0){
				
			}
			else{
				avance = avance - 102;
				$(".mini").scrollLeft(avance);
				i--;
			}
			
		}
		
		
	});
})
	
