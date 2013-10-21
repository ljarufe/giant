$(document).ready(function(){
		/*Activar la transparencia de las imagenes PNG en IE6*/
		$(document).pngFix();
		
		/*Menú de Contacto Desplegable*/
		$("#menu_sec_flotante").css("display","none").css("opacity","0");
		$("#menu_contactanos_li").hover(function() {
			$("#menu_sec_flotante").css("display","block");
			$("#menu_sec_flotante").animate({opacity: "1"}, { duration: "100" });
		}, function () {
			$("#menu_sec_flotante").animate({opacity: "0"}, "100", "linear", function(){$("#menu_sec_flotante").css("display","none").clearQueue();} );
		});
		$("#menu_contactanos_li").click(function() {
			$("#menu_sec_flotante").css("display","block");
			$("#menu_sec_flotante").animate({opacity: "1"}, { duration: "100" });
		});
		
		/*Centrar Contender Verticalmentee*/
		$('#contenedor_principal').css('margin-top', ($('#contenedor_principal').parent().height() - $('#contenedor_principal').height()) / 2);
	});