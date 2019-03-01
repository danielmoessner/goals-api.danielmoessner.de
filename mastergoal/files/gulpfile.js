var gulp = require("gulp"),
	shell = require("gulp-shell");


	gulp.task("sass", shell.task("sassc -t compressed scss/main.scss app/css/main.css"));


	gulp.task("watch-sass", function(){
		gulp.watch("./scss/**/*.scss", gulp.task("sass"))
	});


	gulp.task("js", shell.task("browserify javascript/global.js -o app/js/global.js; browserify javascript/body.js -o app/js/body.js"))


	gulp.task("watch-js", function(){
		gulp.watch("./javascript/**/*.js", gulp.task("js"))
	});


	gulp.task("default", gulp.parallel("watch-sass", "watch-js"));
