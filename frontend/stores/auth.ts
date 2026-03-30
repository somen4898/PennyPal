import type { TokenResponse, User } from '~/types'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(null)
  const user = ref<User | null>(null)
  const isAuthenticated = computed(() => !!token.value)

  function setToken(t: string) {
    token.value = t
    if (import.meta.client) {
      localStorage.setItem('settl_token', t)
    }
  }

  function loadToken() {
    if (import.meta.client) {
      const saved = localStorage.getItem('settl_token')
      if (saved) token.value = saved
    }
  }

  async function login(email: string, password: string) {
    const config = useRuntimeConfig()
    const data = await $fetch<TokenResponse>(`${config.public.apiBaseUrl}/v1/auth/login`, {
      method: 'POST',
      body: { email, password },
    })
    setToken(data.access_token)
    await fetchUser()
  }

  async function register(email: string, username: string, fullName: string, password: string) {
    const config = useRuntimeConfig()
    await $fetch(`${config.public.apiBaseUrl}/v1/auth/register`, {
      method: 'POST',
      body: { email, username, full_name: fullName, password },
    })
  }

  async function fetchUser() {
    if (!token.value) return
    const config = useRuntimeConfig()
    try {
      user.value = await $fetch<User>(`${config.public.apiBaseUrl}/v1/users/me`, {
        headers: { Authorization: `Bearer ${token.value}` },
      })
    }
    catch {
      logout()
    }
  }

  function logout() {
    token.value = null
    user.value = null
    if (import.meta.client) {
      localStorage.removeItem('settl_token')
    }
    navigateTo('/login')
  }

  return { token, user, isAuthenticated, login, register, fetchUser, logout, loadToken }
})
