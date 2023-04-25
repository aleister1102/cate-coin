/** @type {import('tailwindcss').Config} */
export default {
	content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
	theme: {
		extend: {
			colors: {
				primary: '#ef6387',
				secondary: '#faa400',
				brown: '#cf782e',
			},
		},
	},
	plugins: [],
}
