module.exports = {
    content: [
        'apps/*/templates/**/*.html',
        'apps/*/templates/**/*.txt',
        'templates/**/*.html',
        'templates/**/*.txt',
    ],
    theme: {
        extend: {
            screens: {
                'print': {'raw': 'print'},
                '3xl': '1921px'
            },
            colors: {
                form: "rgb(82, 82, 82)",
            }
        },
    },
    plugins: [
        require('@tailwindcss/typography'),
    ],
}
