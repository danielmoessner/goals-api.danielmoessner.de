module.exports = function () {
	$('.masonry').masonry({
		itemSelector: '.masonry--item',
		columnWidth: '.masonry--sizer',
		percentPosition: true
	});
}();
