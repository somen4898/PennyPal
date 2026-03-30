export default defineNuxtRouteMiddleware((to) => {
  const auth = useAuthStore()
  auth.loadToken()

  const publicRoutes = ['/login', '/register', '/landing']

  if (!auth.isAuthenticated && !publicRoutes.includes(to.path)) {
    return navigateTo('/landing')
  }

  if (auth.isAuthenticated && ['/login', '/register', '/landing'].includes(to.path)) {
    return navigateTo('/')
  }
})
