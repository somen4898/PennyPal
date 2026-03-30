<template>
  <div>
    <!-- Header -->
    <div class="mb-8">
      <h1 class="font-serif text-3xl tracking-tight text-[#efefef]">Settlements</h1>
      <p class="mt-2 text-sm text-[#6a6a6a]">Track and manage money owed between you and others.</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="h-6 w-6 animate-spin rounded-full border-2 border-[#e5fe40] border-t-transparent" />
    </div>

    <template v-else>
      <!-- Pending Settlements -->
      <section class="mb-10">
        <h2 class="mb-4 font-serif text-xl text-[#efefef]">Pending</h2>

        <div v-if="pendingSettlements.length === 0" class="rounded-2xl border border-white/[0.04] bg-[#121212] p-8 text-center">
          <p class="text-sm text-[#6a6a6a]">No pending settlements.</p>
        </div>

        <div v-else class="space-y-3">
          <div
            v-for="s in pendingSettlements"
            :key="s.id"
            class="group rounded-2xl border border-white/[0.04] bg-[#121212] p-5 transition-colors hover:border-white/[0.08]"
          >
            <div class="flex items-start justify-between gap-4">
              <div class="min-w-0 flex-1">
                <!-- Direction -->
                <div class="flex items-center gap-2">
                  <span class="text-sm font-medium text-[#efefef]">{{ directionLabel(s).from }}</span>
                  <svg class="h-4 w-4 flex-shrink-0 text-[#6a6a6a]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                  <span class="text-sm font-medium text-[#efefef]">{{ directionLabel(s).to }}</span>
                </div>

                <!-- Description -->
                <p v-if="s.description" class="mt-1.5 text-xs text-[#6a6a6a]">{{ s.description }}</p>

                <!-- Badge -->
                <span class="mt-2.5 inline-flex items-center rounded-full bg-[#ffcb45]/10 px-2.5 py-0.5 text-[11px] font-semibold uppercase tracking-wider text-[#ffcb45]">
                  Pending
                </span>
              </div>

              <div class="flex flex-col items-end gap-3">
                <!-- Amount -->
                <span class="font-mono text-xl font-semibold text-[#ffcb45]">
                  {{ s.currency || '$' }}{{ Number(s.amount).toFixed(2) }}
                </span>

                <!-- Actions -->
                <div v-if="isInvolved(s)" class="flex items-center gap-2">
                  <button
                    class="rounded-lg border border-[#3bffad]/30 px-3 py-1.5 text-xs font-semibold text-[#3bffad] transition-all hover:border-[#3bffad]/60 hover:bg-[#3bffad]/5 active:scale-95 disabled:opacity-40"
                    :disabled="updating === s.id"
                    @click="markComplete(s.id)"
                  >
                    <span v-if="updating === s.id" class="flex items-center gap-1.5">
                      <span class="h-3 w-3 animate-spin rounded-full border border-[#3bffad] border-t-transparent" />
                      Updating
                    </span>
                    <span v-else>Mark Complete</span>
                  </button>
                  <button
                    class="rounded-lg border border-[#ee4d37]/30 px-3 py-1.5 text-xs font-semibold text-[#ee4d37] transition-all hover:border-[#ee4d37]/60 hover:bg-[#ee4d37]/5 active:scale-95 disabled:opacity-40"
                    :disabled="updating === s.id"
                    @click="cancelSettlement(s.id)"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Completed Settlements -->
      <section>
        <h2 class="mb-4 font-serif text-xl text-[#efefef]">Completed</h2>

        <div v-if="completedSettlements.length === 0" class="rounded-2xl border border-white/[0.04] bg-[#121212] p-8 text-center">
          <p class="text-sm text-[#6a6a6a]">No completed settlements yet.</p>
        </div>

        <div v-else class="space-y-3">
          <div
            v-for="s in completedSettlements"
            :key="s.id"
            class="rounded-2xl border border-white/[0.04] bg-[#121212] p-5 opacity-60"
          >
            <div class="flex items-start justify-between gap-4">
              <div class="min-w-0 flex-1">
                <!-- Direction -->
                <div class="flex items-center gap-2">
                  <span class="text-sm font-medium text-[#efefef]">{{ directionLabel(s).from }}</span>
                  <svg class="h-4 w-4 flex-shrink-0 text-[#6a6a6a]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                  <span class="text-sm font-medium text-[#efefef]">{{ directionLabel(s).to }}</span>
                </div>

                <!-- Description -->
                <p v-if="s.description" class="mt-1.5 text-xs text-[#6a6a6a]">{{ s.description }}</p>

                <div class="mt-2.5 flex items-center gap-3">
                  <!-- Badge -->
                  <span class="inline-flex items-center rounded-full bg-[#3bffad]/10 px-2.5 py-0.5 text-[11px] font-semibold uppercase tracking-wider text-[#3bffad]">
                    Completed
                  </span>
                  <!-- Settled date -->
                  <span v-if="s.settled_at" class="text-[11px] text-[#6a6a6a]">
                    {{ formatDate(s.settled_at) }}
                  </span>
                </div>
              </div>

              <!-- Amount -->
              <span class="font-mono text-xl font-semibold text-[#6a6a6a]">
                {{ s.currency || '$' }}{{ Number(s.amount).toFixed(2) }}
              </span>
            </div>
          </div>
        </div>
      </section>
    </template>

    <!-- Error toast -->
    <Transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="translate-y-4 opacity-0"
      enter-to-class="translate-y-0 opacity-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="translate-y-0 opacity-100"
      leave-to-class="translate-y-4 opacity-0"
    >
      <div
        v-if="error"
        class="fixed bottom-6 left-1/2 -translate-x-1/2 rounded-xl border border-[#ee4d37]/20 bg-[#1a0a08] px-5 py-3 text-sm text-[#ee4d37] shadow-2xl"
      >
        {{ error }}
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import type { Settlement } from '~/types'

definePageMeta({ middleware: 'auth' })

const api = useApi()
const auth = useAuthStore()

const settlements = ref<Settlement[]>([])
const loading = ref(true)
const updating = ref<number | null>(null)
const error = ref('')

const pendingSettlements = computed(() =>
  settlements.value.filter(s => s.status === 'pending'),
)

const completedSettlements = computed(() =>
  settlements.value.filter(s => s.status === 'completed'),
)

function isInvolved(s: Settlement): boolean {
  const userId = auth.user?.id
  return s.payer_id === userId || s.payee_id === userId
}

function directionLabel(s: Settlement): { from: string, to: string } {
  const userId = auth.user?.id
  if (s.payer_id === userId) {
    return { from: 'You', to: `User #${s.payee_id}` }
  }
  if (s.payee_id === userId) {
    return { from: `User #${s.payer_id}`, to: 'You' }
  }
  return { from: `User #${s.payer_id}`, to: `User #${s.payee_id}` }
}

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}

async function fetchSettlements() {
  loading.value = true
  try {
    settlements.value = await api.get<Settlement[]>('/v1/settlements/')
  }
  catch {
    showError('Failed to load settlements.')
  }
  finally {
    loading.value = false
  }
}

async function markComplete(id: number) {
  updating.value = id
  try {
    await api.put(`/v1/settlements/${id}`, { status: 'completed' })
    await fetchSettlements()
  }
  catch {
    showError('Failed to update settlement.')
  }
  finally {
    updating.value = null
  }
}

async function cancelSettlement(id: number) {
  updating.value = id
  try {
    await api.put(`/v1/settlements/${id}`, { status: 'cancelled' })
    await fetchSettlements()
  }
  catch {
    showError('Failed to cancel settlement.')
  }
  finally {
    updating.value = null
  }
}

function showError(msg: string) {
  error.value = msg
  setTimeout(() => { error.value = '' }, 4000)
}

onMounted(() => {
  fetchSettlements()
})
</script>
