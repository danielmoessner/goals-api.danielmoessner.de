require('popper.js');
global.jQuery = global.$ = require('jquery');
require('bootstrap');

var jQueryBridget = require('jquery-bridget');
var Masonry = require('masonry-layout');
jQueryBridget('masonry', Masonry, $);

function resetLayout() {
	setTimeout(function() {$(".masonry").masonry()}, 0)
	setTimeout(function() {$(".masonry").masonry()}, 50)
	setTimeout(function() {$(".masonry").masonry()}, 100)
	setTimeout(function() {$(".masonry").masonry()}, 200)
	setTimeout(function() {$(".masonry").masonry()}, 500)
}