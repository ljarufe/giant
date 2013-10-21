// Funciones invocadas desde flash
function intro_saltar() {
	$("#flashContent").css("display", "none");
}

function intro_fade_start() {
	$('#flashContent').animate({opacity:0}, 700, function(){ $('#flashContent').css('display','none');});
}

$(document).ready(function(){
	$(".proyectos p").click(function(event) {
		event.preventDefault();
		return false;
	});
	
});
