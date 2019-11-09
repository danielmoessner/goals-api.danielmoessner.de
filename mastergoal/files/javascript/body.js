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


/* reset the layout if item is clicked */
$(document).on("click", ".reset-layout-on-click", function(){
	$(this).closest('.masonry--item').css('z-index', 1)
	resetLayout();
});


/* reset the layout if an items changes size and is suddenly bigger or smaller */
$('.adminator-box--toggle').on('click', function(){
	$(this).closest('.masonry--item').css('z-index', 1)
	resetLayout()
})


/* reset the layout on page load */
$(window).ready(function () {
	resetLayout()
})
