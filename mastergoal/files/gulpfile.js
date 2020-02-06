//
// Variables ==============================
//

//
// Dependencies ===========================
//
const browserify = require("gulp-browserify")
const sourcemaps = require('gulp-sourcemaps')
const cleancss = require('gulp-clean-css')
const npmdist = require('gulp-npm-dist')
const postcss = require('gulp-postcss')
const concat = require('gulp-concat')
const uglify = require('gulp-uglify')
const babel = require('gulp-babel')
const sass = require('gulp-sass')
const gulp = require('gulp')
const del = require('del')

//
// Paths ==================================
//

const paths = {
  base:   {
    base:         {
      dir:    './'
    },
    node:         {
      dir:    './node_modules'
    },
    packageLock:  {
      files:  './package-lock.json'
    }
  },
  src: {
    base : {
      dir: './src',
      files: '.src/**/*'
    },
    js: {
      dir:    './src/js',
      files:  './src/js/**/*',
      global: './src/js/global.js',
      body:   './src/js/body.js'
    },
    scss: {
      dir:    './src/scss',
      files:  './src/scss/**/*',
      main:   './src/scss/*.scss'
    },
    img: {
      dir: './src/img',
      files: './src/img/**/*'
    },
    fonts: {
      dir: './src/fonts',
      files: './src/fonts/**/*'
    }
  },
  dist:   {
    base:   {
      dir:    './dist',
      files:  './dist/**/*'
    },
    libs:   {
      dir:    './dist/libs',
      files:  './dist/libs/**/*'
    },
    js: {
      dir:    './dist/js',
      files:  './dist/js/**/*'
    },
    css:    {
      dir:    './dist/css',
      files:  './dist/css/**/*'
    },
    img:    {
      dir:    './dist/img',
      files:  './dist/img/**/*'
    },
    fonts: {
      dir: './dist/fonts',
      files: './dist/fonts/**/*'
    }
  }
}

//
// Tasks ==================================
//

function css(cb) {
  gulp
    .src(paths.src.scss.main)
    .pipe(sourcemaps.init())
    .pipe(sass({includePaths: [paths.base.node.dir]}).on('error', sass.logError))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(paths.dist.css.dir))
  cb()
}

function cssBuild(cb) {
  gulp
    .src(paths.src.scss.main)
    .pipe(sass({includePaths: [paths.base.node.dir]}).on('error', sass.logError))
    .pipe(postcss())
    .pipe(gulp.dest('./dist/css/'))
  cb()
}

function cssClean(cb) {
  del(paths.dist.css.files)
  cb()
}

function js(cb) {
  gulp
    .src(paths.src.js.body)
    .pipe(sourcemaps.init())
    .pipe(browserify())
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(paths.dist.js.dir))
  gulp
    .src(paths.src.js.global)
    .pipe(sourcemaps.init())
    .pipe(browserify())
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(paths.dist.js.dir))
  cb()
}

function jsBuild(cb) {
  gulp
    .src(paths.src.js.body)
    .pipe(browserify())
    // .pipe(uglify())
    .pipe(gulp.dest(paths.dist.js.dir))
  gulp
    .src(paths.src.js.global)
    .pipe(browserify())
    // .pipe(uglify())
    .pipe(gulp.dest(paths.dist.js.dir))
  cb()
}

function jsClean(cb) {
  del(paths.dist.js.files)
  cb()
}

function libs(cb) {
  gulp
    .src(npmdist(), {base: paths.base.node.dir})
    .pipe(gulp.dest(paths.dist.libs.dir))
  cb()
}

function libsClean(cb) {
  del(paths.dist.libs.files)
  cb()
}

function img(cb) {
  gulp
    .src(paths.src.img.files)
    .pipe(gulp.dest(paths.dist.img.dir))
  cb()
}

function imgClean(cb) {
  del(paths.dist.img.files)
  cb()
}

function fonts(cb) {
  gulp
    .src(paths.src.fonts.files)
    .pipe(gulp.dest(paths.dist.fonts.dir))
  cb()
}

function fontsClean(cb) {
  del(paths.dist.fonts.files)
  cb()
}

//
// Exports ================================
//

exports.default = function() {
  gulp.parallel(css, js, libs, img, fonts)()
  gulp.watch(paths.src.scss.files, css)
  gulp.watch(paths.src.js.files, js)
}

exports.build = gulp.series(gulp.parallel(cssClean, jsClean, imgClean, fontsClean, libsClean), gulp.parallel(img, fonts, libs, cssBuild, jsBuild))

exports.clean = gulp.parallel(cssClean, jsClean, imgClean, fontsClean, libsClean)

exports.dev = gulp.parallel(libs, img, fonts, css, js)
