module.exports = function () {
	$('.masonry').masonry({
		itemSelector: '.masonry--item',
		columnWidth: '.masonry--sizer',
		gutter: '.masonry--gutter',
		percentPosition: true
	});
}();
