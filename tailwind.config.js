const { colors } = require('tailwindcss/defaultTheme')

module.exports = {
  purge: ["./**/templates/**/*.*", "./**/jinja2/**/*.*"],
  theme: {
    extend: {
      colors: {
        blue: {
          ...colors.blue,
          '900': '#143c52'
        }
      }
    },
  },
  variants: {
    borderWidth: ({ after }) => after(['first', 'last']),
    margin:  ({ after }) => after(['first', 'last']),
  },
  plugins: [],
  future: {
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true,
  },
}
