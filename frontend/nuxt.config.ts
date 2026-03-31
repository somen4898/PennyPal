export default defineNuxtConfig({
  modules: [
    '@nuxt/ui',
    '@pinia/nuxt',
  ],
  css: ['~/assets/css/main.css'],
  colorMode: {
    preference: 'dark',
    fallback: 'dark',
  },
  devtools: { enabled: true },
  telemetry: false,
  runtimeConfig: {
    apiBaseUrl: 'http://localhost:8000',
    public: {
      apiBaseUrl: '/api',
    },
  },
  routeRules: {
    '/api/**': {
      proxy: { to: 'http://localhost:8000/api/**' },
    },
  },
  compatibilityDate: '2026-03-31',
})
