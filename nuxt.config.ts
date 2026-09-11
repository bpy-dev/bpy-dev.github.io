export default defineNuxtConfig({
  modules: ['@nuxt/ui'],
  css: ['~/assets/css/main.css'],
  ssr: true,
  devtools: { enabled: false },
  experimental: {
    prefetchPreloadTags: false
  },
  hooks: {
    'build:manifest': (manifest) => {
      for (const entry of Object.values(manifest)) {
        entry.dynamicImports = []
      }
    }
  },
  routeRules: {
    '/': { prerender: true }
  },
  nitro: {
    prerender: {
      routes: ['/'],
      crawlLinks: true
    }
  },
  app: {
    head: {
      htmlAttrs: { lang: 'en' },
      viewport: 'width=device-width, initial-scale=1',
      meta: [
        { name: 'theme-color', content: '#050505' }
      ]
    }
  },
  compatibilityDate: '2026-09-01'
})
