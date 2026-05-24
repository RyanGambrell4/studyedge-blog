/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        bg:        '#F7F6F3',
        card:      '#FFFFFF',
        border:    'rgba(0,0,0,0.07)',
        text:      '#111111',
        muted:     '#6B6B6B',
        dim:       '#9B9B9B',
        accent:    '#3B61C4',
        accentDark:'#2d4fa3',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'Segoe UI', 'sans-serif'],
      },
      maxWidth: {
        prose: '720px',
      },
    },
  },
  plugins: [],
};
