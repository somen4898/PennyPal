<script setup lang="ts">
definePageMeta({ layout: 'auth', middleware: 'auth' })

const authStore = useAuthStore()

const email = ref('')
const username = ref('')
const fullName = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
const success = ref(false)
const showPassword = ref(false)

async function handleRegister() {
  error.value = ''
  loading.value = true

  try {
    await authStore.register(email.value, username.value, fullName.value, password.value)
    success.value = true
    setTimeout(() => {
      navigateTo('/login')
    }, 1500)
  }
  catch (e: any) {
    error.value
      = e?.data?.detail
        || e?.statusMessage
        || 'Registration failed. Please try again.'
  }
  finally {
    loading.value = false
  }
}
</script>

<template>
  <div>
    <!-- Heading -->
    <div class="stagger-enter mb-8 text-center" style="animation-delay: 0.05s">
      <h2 class="font-serif text-3xl tracking-tight text-[#efefef]">
        Create account
      </h2>
      <p class="mt-2 text-sm text-[#6a6a6a]">
        Join SETTL and start splitting
      </p>
    </div>

    <!-- Card -->
    <div
      class="stagger-enter rounded-2xl border border-white/[0.04] bg-[#121212] p-8"
      style="animation-delay: 0.15s"
    >
      <!-- Success message -->
      <Transition
        enter-active-class="transition-all duration-300 ease-out"
        enter-from-class="opacity-0 -translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition-all duration-200 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 -translate-y-2"
      >
        <div
          v-if="success"
          class="mb-6 flex items-center gap-3 rounded-xl border border-[#3bffad]/20 bg-[#3bffad]/[0.08] px-4 py-3"
        >
          <svg class="h-4 w-4 shrink-0 text-[#3bffad]" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
          </svg>
          <p class="text-sm text-[#3bffad]">
            Account created! Redirecting to sign in...
          </p>
        </div>
      </Transition>

      <!-- Error -->
      <Transition
        enter-active-class="transition-all duration-300 ease-out"
        enter-from-class="opacity-0 -translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition-all duration-200 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 -translate-y-2"
      >
        <div
          v-if="error"
          class="mb-6 flex items-center gap-3 rounded-xl border border-[#ee4d37]/20 bg-[#ee4d37]/[0.08] px-4 py-3"
        >
          <svg class="h-4 w-4 shrink-0 text-[#ee4d37]" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
          <p class="text-sm text-[#ee4d37]">
            {{ error }}
          </p>
        </div>
      </Transition>

      <form class="space-y-5" @submit.prevent="handleRegister">
        <!-- Email -->
        <div>
          <label for="reg-email" class="mb-2 block text-xs font-medium uppercase tracking-widest text-[#6a6a6a]">
            Email
          </label>
          <input
            id="reg-email"
            v-model="email"
            type="email"
            required
            autocomplete="email"
            placeholder="you@example.com"
            class="w-full rounded-xl border border-white/[0.06] bg-[#161616] px-4 py-3 text-sm text-[#efefef] placeholder-[#4a4a4a] outline-none transition-all duration-200 focus:border-[#e5fe40]/30 focus:ring-1 focus:ring-[#e5fe40]/20"
          >
        </div>

        <!-- Username -->
        <div>
          <label for="reg-username" class="mb-2 block text-xs font-medium uppercase tracking-widest text-[#6a6a6a]">
            Username
          </label>
          <input
            id="reg-username"
            v-model="username"
            type="text"
            required
            autocomplete="username"
            placeholder="Choose a username"
            class="w-full rounded-xl border border-white/[0.06] bg-[#161616] px-4 py-3 text-sm text-[#efefef] placeholder-[#4a4a4a] outline-none transition-all duration-200 focus:border-[#e5fe40]/30 focus:ring-1 focus:ring-[#e5fe40]/20"
          >
        </div>

        <!-- Full Name -->
        <div>
          <label for="reg-fullname" class="mb-2 block text-xs font-medium uppercase tracking-widest text-[#6a6a6a]">
            Full Name
          </label>
          <input
            id="reg-fullname"
            v-model="fullName"
            type="text"
            required
            autocomplete="name"
            placeholder="Your full name"
            class="w-full rounded-xl border border-white/[0.06] bg-[#161616] px-4 py-3 text-sm text-[#efefef] placeholder-[#4a4a4a] outline-none transition-all duration-200 focus:border-[#e5fe40]/30 focus:ring-1 focus:ring-[#e5fe40]/20"
          >
        </div>

        <!-- Password -->
        <div>
          <label for="reg-password" class="mb-2 block text-xs font-medium uppercase tracking-widest text-[#6a6a6a]">
            Password
          </label>
          <div class="relative">
            <input
              id="reg-password"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              required
              autocomplete="new-password"
              placeholder="Create a strong password"
              class="w-full rounded-xl border border-white/[0.06] bg-[#161616] px-4 py-3 pr-12 text-sm text-[#efefef] placeholder-[#4a4a4a] outline-none transition-all duration-200 focus:border-[#e5fe40]/30 focus:ring-1 focus:ring-[#e5fe40]/20"
            >
            <button
              type="button"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-[#6a6a6a] transition-colors hover:text-[#b0b0b0]"
              tabindex="-1"
              @click="showPassword = !showPassword"
            >
              <svg v-if="!showPassword" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
              </svg>
              <svg v-else class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M3.707 2.293a1 1 0 00-1.414 1.414l14 14a1 1 0 001.414-1.414l-1.473-1.473A10.014 10.014 0 0019.542 10C18.268 5.943 14.478 3 10 3a9.958 9.958 0 00-4.512 1.074l-1.78-1.781zm4.261 4.26l1.514 1.515a2.003 2.003 0 012.45 2.45l1.514 1.514a4 4 0 00-5.478-5.478z" clip-rule="evenodd" />
                <path d="M12.454 16.697L9.75 13.992a4 4 0 01-3.742-3.741L2.335 6.578A9.98 9.98 0 00.458 10c1.274 4.057 5.065 7 9.542 7 .847 0 1.669-.105 2.454-.303z" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Submit -->
        <button
          type="submit"
          :disabled="loading || success"
          class="settl-btn-primary mt-2 flex w-full items-center justify-center gap-2 text-sm disabled:cursor-not-allowed disabled:opacity-50"
        >
          <svg
            v-if="loading"
            class="h-4 w-4 animate-spin"
            viewBox="0 0 24 24"
            fill="none"
          >
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          {{ loading ? 'Creating account...' : 'Create account' }}
        </button>
      </form>
    </div>

    <!-- Footer link -->
    <p class="stagger-enter mt-8 text-center text-sm text-[#6a6a6a]" style="animation-delay: 0.25s">
      Already have an account?
      <NuxtLink
        to="/login"
        class="text-[#e5fe40] transition-colors hover:text-[#e5fe40]/80"
      >
        Sign in
      </NuxtLink>
    </p>
  </div>
</template>
