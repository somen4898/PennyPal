export function useApi() {
  const config = useRuntimeConfig()
  const authStore = useAuthStore()

  const baseURL = config.public.apiBaseUrl as string

  function headers(): Record<string, string> {
    const h: Record<string, string> = { 'Content-Type': 'application/json' }
    if (authStore.token) {
      h.Authorization = `Bearer ${authStore.token}`
    }
    return h
  }

  async function get<T>(url: string): Promise<T> {
    return await $fetch<T>(`${baseURL}${url}`, { headers: headers() })
  }

  async function post<T>(url: string, body?: unknown): Promise<T> {
    return await $fetch<T>(`${baseURL}${url}`, {
      method: 'POST',
      headers: headers(),
      body,
    })
  }

  async function put<T>(url: string, body?: unknown): Promise<T> {
    return await $fetch<T>(`${baseURL}${url}`, {
      method: 'PUT',
      headers: headers(),
      body,
    })
  }

  async function del<T>(url: string): Promise<T> {
    return await $fetch<T>(`${baseURL}${url}`, {
      method: 'DELETE',
      headers: headers(),
    })
  }

  return { get, post, put, del }
}
