function galeria() {
	var indice = 0; //Indice que apunta a la primera imagen del trio de imagenes activo
	var indices = new Array(); //Arreglo de Indices de trios
	var semaforo = true;
	var semaforo_carga = true;
	
	for(i=0; i<imagenes.length; i++)
		if(i%3==0)
			indices[indices.length] = i;	//Capturar los Indices de trios
			
	cambia_imagenes();
	
	cargar_tipo_proyecto();
	
	$('#sig').click(function() {
		if(semaforo) {
			indice = (indice+1<indices.length)?indice+1:0;
			cambia_imagenes();
		}
	});
	
	$('#ant').click(function() {
		if(semaforo) {
			indice = (indice-1<0)?indices.length-1:indice-1;
			cambia_imagenes();
		}
	});
	
	function display_resumen_proyecto(id) {	
		if(semaforo_carga && id!=-1) {
			semaforo_carga = false;
			var velocidad = 200;
			$('#resumen_proyecto, #info_empresa').clearQueue().animate({opacity:0}, velocidad, function(){
				json_url = "/proyectos/get_proyecto_json/" + id;
				$.getJSON(json_url, function(proyecto){
					$('#resumen_proyecto, #info_empresa').html("");
					url_detalles = "/proyectos/detalle_proyecto/" + proyecto.id;
					url_info = "/clientes/registrar_cliente/" + proyecto.id;
					$('#resumen_proyecto, #info_empresa').append("<div><h1>" + proyecto.nombre + "</h1></div>");
					$('#resumen_proyecto, #info_empresa').append("<div><h3>" + proyecto.tipo + "</h3></div>");
					$('#resumen_proyecto, #info_empresa').append("<a href="+ url_detalles +" class='vinculo_img'/>");
					$('#resumen_proyecto .vinculo_img, #info_empresa vinculo_img').append("<img src=" + proyecto.imagen + " />");
					$('#resumen_proyecto, #info_empresa').append("<div><p>" + proyecto.descripcion + "</p></div>");
					$('#resumen_proyecto, #info_empresa').append("<hr />");
					$('#resumen_proyecto, #info_empresa').append("<div class='div_vinculo'></div>");
					$('#resumen_proyecto .div_vinculo, #info_empresa .div_vinculo').append("<a href='" + url_info + "' class='vinculo' >Cont&aacute;ctanos</a> ");
					$('#resumen_proyecto .div_vinculo, #info_empresa .div_vinculo').append("<a href='" + url_detalles + "' class='vinculo' >Ver toda la información</a>");
					$('#resumen_proyecto, #info_empresa').append("<div class='clear'></div>");
					$('#resumen_proyecto, #info_empresa').clearQueue().animate({opacity:1}, velocidad);
					semaforo_carga = true;
				});
			});
			
		}
	}
	
	function set_imagenes() {
		for(i=0; i<3; i++)
			if(indices[indice]+i < imagenes.length) {
				$($(".img")[i]).css("background-image","url("+imagenes[indices[indice]+i][1]+")");
				$($(".img")[i]).attr("id",imagenes[indices[indice]+i][0]);
				$($(".img")[i]).html("").append("<div class='des'><h3>" + imagenes[indices[indice]+i][2] + "</h3></div>");
				$($(".img")[i]).click(function() {
					display_resumen_proyecto($(this).attr("id"));	
				});
			} else {
				$($(".img")[i]).css("background-image","none");
				$($(".img")[i]).attr("id","-1");
				$($(".img")[i]).html("");
			}
	}
	
	function cambia_imagenes() {
		semaforo = false;
		$(".img").hover( function(){ 
			$(".img").css({"opacity":"0.75"});
			$(this).css({"opacity":"1"});
			/*$(this).children().children().css({"font-weight":"bold"});*/
		} , function(){
			$(".img").css({"opacity":"1"});
			$(this).css({"opacity":"1"});
			/*$(this).children().children().css({"font-weight":"normal"});*/
		});
		for(i=0; i<3; i++) {
			$($(".rel")[i]).css("background-image",$($(".nor")[i]).css("background-image"));
			$($(".img")[i]).html("").append($($(".nor")[i]).html());
		}
		set_imagenes();
		$(".rel").css({"display":"inherit","opacity":"1"});
		$(".rel").clearQueue().animate({ "opacity": "0" },400, function() {$(this).css("display","none"); semaforo=true;});
	}
	
	function cargar_tipo_proyecto() {
		var texto = tipo_proyecto;
		switch(tipo_proyecto) {
			case "Actual" : texto += "es"; break;
			default: texto += "s"; break;
		}
		$('#botonera_texto').append(texto);
	}
}

$(document).ready(function(){
	galeria();
})

