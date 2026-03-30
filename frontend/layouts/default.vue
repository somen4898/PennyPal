<template>
  <div class="min-h-screen bg-[#0d0d0d] grain">
    <!-- Top navigation bar -->
    <nav class="fixed top-0 left-0 right-0 z-50 border-b border-white/[0.04] bg-[#0d0d0d]/80 backdrop-blur-xl">
      <div class="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
        <NuxtLink to="/" class="flex items-center gap-2">
          <span class="font-serif text-2xl tracking-tight text-[#e5fe40]">SETTL</span>
          <span class="text-[10px] font-semibold uppercase tracking-[0.2em] text-[#6a6a6a]">.</span>
        </NuxtLink>

        <div class="flex items-center gap-1">
          <NuxtLink
            to="/"
            class="rounded-lg px-4 py-2 text-sm font-medium text-[#b0b0b0] transition-colors hover:bg-white/[0.04] hover:text-[#efefef]"
            active-class="!text-[#efefef] bg-white/[0.06]"
          >
            Dashboard
          </NuxtLink>
          <NuxtLink
            to="/groups"
            class="rounded-lg px-4 py-2 text-sm font-medium text-[#b0b0b0] transition-colors hover:bg-white/[0.04] hover:text-[#efefef]"
            active-class="!text-[#efefef] bg-white/[0.06]"
          >
            Groups
          </NuxtLink>
          <NuxtLink
            to="/settlements"
            class="rounded-lg px-4 py-2 text-sm font-medium text-[#b0b0b0] transition-colors hover:bg-white/[0.04] hover:text-[#efefef]"
            active-class="!text-[#efefef] bg-white/[0.06]"
          >
            Settle
          </NuxtLink>
          <NuxtLink
            to="/chat"
            class="rounded-lg px-4 py-2 text-sm font-medium text-[#b0b0b0] transition-colors hover:bg-white/[0.04] hover:text-[#efefef]"
            active-class="!text-[#efefef] bg-white/[0.06]"
          >
            AI
          </NuxtLink>
        </div>

        <div class="flex items-center gap-3">
          <button
            class="flex h-9 w-9 items-center justify-center rounded-full bg-white/[0.06] text-sm font-bold text-[#e5fe40] transition-colors hover:bg-white/[0.1]"
            @click="handleProfile"
          >
            {{ userInitial }}
          </button>
        </div>
      </div>
    </nav>

    <!-- Main content -->
    <main class="mx-auto max-w-6xl px-6 pb-12 pt-24">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
const auth = useAuthStore()

const userInitial = computed(() => {
  if (auth.user?.full_name) return auth.user.full_name[0].toUpperCase()
  if (auth.user?.username) return auth.user.username[0].toUpperCase()
  return '?'
})

function handleProfile() {
  auth.logout()
}
</script>
