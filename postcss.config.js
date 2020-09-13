const cssnano = require('cssnano')
const autoprefixer = require('autoprefixer');

module.exports = ({env}) => ({
    plugins: [
        require("postcss-import"),
        require("postcss-nested"),
        require("tailwindcss"),
        env === 'production' ? autoprefixer() : null,
        env === 'production' ? cssnano({
            preset: 'default'
        }) : null,
    ],
})
