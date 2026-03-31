export default defineNuxtConfig({
  modules: [
    '@nuxt/ui',
    '@pinia/nuxt',
  ],
  css: ['~/assets/css/main.css'],
  app: {
    head: {
      link: [
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Serif+Display&family=JetBrains+Mono:wght@400;500;600&display=swap',
        },
      ],
    },
  },
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
