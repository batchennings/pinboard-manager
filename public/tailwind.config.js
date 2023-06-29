/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './**/*.html',
        '../**/*.html'
    ],
    theme: {
        screens: {
            'phone': '480px',
            'tablet': '640px',
            'laptop': '1024px',
            'desktop': '1440px',
        },
        extend: {
            backgroundImage: {
                'header-image': 'url("assets/images/header.png")',
                'site-texture': ''
            }
        },
        colors: {
            transparent: 'transparent',
            'white': '#ffffff',
            blue: {
                400: '#367CCF',
                600: '#2B5485',
                750: '#1D334E',
                800: '#0F2743'
            },
            orange: {
                200: '#f8f8ee',
                600: '#FABA2F'
            },
            green: {
                800: '#23844D',
                600: '#38C674'
            },
            gray: {
                100: '#EBEAF1',
                200: '#DCDAE7',
                300: '#B3B0C1',
                400: '#706D81',
                500: '#444251',
                700: '#26252E',
                900: '#121216',
            }
        }
    },
    plugins: [],
}

