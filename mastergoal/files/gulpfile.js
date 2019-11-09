const gulp = require("gulp");
const browserify = require("gulp-browserify");
const sass = require('gulp-sass');
const rename = require('gulp-rename');


gulp.task("scss", function(done) {
	gulp.src('./scss/**/*.scss')
		.pipe(sass().on('error', sass.logError))
		.pipe(gulp.dest('./app/css'));
	done();
});


gulp.task('js-head', function(done) {
    gulp.src('./javascript/global.js')
        .pipe(browserify())
        .pipe(gulp.dest('./app/js'));
    done();
});
gulp.task('js-body', function(done) {
    gulp.src('./javascript/body.js')
        .pipe(browserify())
        .pipe(gulp.dest('./app/js'));
    done();
});


gulp.task("watch-sass", function(){
	gulp.watch("./scss/**/*.scss", gulp.task("sass"))
});
gulp.task("watch-js", function(){
	gulp.watch("./javascript/**/*.js", gulp.parallel("js-head", "js-body"))
});


gulp.task("default", gulp.parallel("watch-sass", "watch-js"));
