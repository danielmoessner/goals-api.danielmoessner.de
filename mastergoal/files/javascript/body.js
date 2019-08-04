require ('./modules/masonry');
require ('./modules/sidebar');
require ('./modules/perfect-scrollbar');
require ('./modules/skycons');
require ('./modules/search');
require ('./modules/charts');

/* resets the masonry layout */
function resetLayout() {
	setTimeout(function() {$(".masonry").masonry()}, 0)
	setTimeout(function() {$(".masonry").masonry()}, 50)
	setTimeout(function() {$(".masonry").masonry()}, 100)
	setTimeout(function() {$(".masonry").masonry()}, 200)
	setTimeout(function() {$(".masonry").masonry()}, 500)
}


/* reset the layout if an items changes size and is suddenly bigger or smaller */
$('.adminator-box--toggle').on('click', function(){
	$(this).closest('.masonry-item').css('z-index', 1)
	resetLayout()
})

/* reset the layout on page load */
$(window).ready(function () {
	resetLayout()
})

/* custom pulldown refresh */
// var eTop = $('#pulldown').offset().top;
// $(window).scroll(function() {
// 	var pos = eTop - $(window).scrollTop()
// 	console.log(pos)
// 	if (pos > 100) {
// 		$("#pulldown").css("color", "#03a9f4");
// 	} else {
// 		$("#pulldown").css("color", "inherit");
// 	}
// 	if (pos > 120) {
// 		location.reload();
// 	}
// });
