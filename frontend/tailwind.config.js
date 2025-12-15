/** @type {import('tailwindcss').Config} */
export default {
    content: ['./src/**/*.{html,js,svelte,ts}'],
    theme: {
        extend: {
            colors: {
                'imap-bg': '#242329',
                'imap-header': '#82368C',
                'imap-primary': '#00A89E',
                'imap-primary-hover': '#33B9B1',
                'imap-text': '#000000',
            },
            fontFamily: {
                sans: ['Poppins', 'sans-serif'],
            },
            borderRadius: {
                DEFAULT: '0',
                none: '0',
                sm: '0',
                md: '0',
                lg: '0',
                xl: '0',
                '2xl': '0',
                '3xl': '0',
                full: '9999px', // Keeping full for circular elements if needed, but defaults are flattened
            },
        },
    },
    plugins: [],
}
