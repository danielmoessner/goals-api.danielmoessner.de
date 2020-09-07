module.exports = {
  plugins: {
    'postcss-discard-comments': { removeAll: true },
    'autoprefixer': {},
    'cssnano': { presets: 'default' }
  }
}