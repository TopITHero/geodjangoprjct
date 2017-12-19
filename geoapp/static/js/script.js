$(document).ready(function(){
	$('#scroll').click(function(){
	$('html,body').animate({scrollTop: $(window).height()}, 1500);
	});
	$('#scroll2').click(function(){
	$('html,body').animate({scrollTop: $(document).height()*2}, 2000);
	});
	///change = false;
	// problem with many signals
	/*
	$(document).bind('DOMMouseScroll', function(e){
     if(e.originalEvent.detail > 0) {
         //scroll down
         $('html,body').animate({scrollTop: $(window).height()}, 1500);
         change = true;
         console.log("Down")
     }else {
         $('html,body').animate({scrollTop: 0}, 1500);
         console.log("up")
         change = true;
         }

     //prevent page fom scrolling
     return false;
    }).delay( 1500 ).fadeIn( 400 );;
	*/
});
 