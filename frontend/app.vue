<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup lang="ts">
const auth = useAuthStore()

onMounted(() => {
  auth.loadToken()
  if (auth.isAuthenticated) {
    auth.fetchUser()
  }
})
</script>
