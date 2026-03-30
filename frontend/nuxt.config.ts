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
  runtimeConfig: {
    apiBaseUrl: 'http://localhost:8000',
    public: {
      apiBaseUrl: '/api',
    },
  },
  routeRules: {
    '/api/**': {
      proxy: { to: 'http://localhost:8000/**' },
    },
  },
  compatibilityDate: '2026-03-31',
})
