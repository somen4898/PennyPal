<template>
  <div class="space-y-10">
    <!-- ================================================================== -->
    <!-- 1. Welcome Header                                                   -->
    <!-- ================================================================== -->
    <header class="stagger-item" style="--i: 0">
      <h1 class="font-serif text-3xl tracking-tight text-[#efefef]">
        {{ greeting }}, {{ firstName }}
      </h1>
      <p class="mt-1 text-sm text-[#6a6a6a]">{{ formattedDate }}</p>
    </header>

    <!-- ================================================================== -->
    <!-- 2. Quick Stats Row                                                  -->
    <!-- ================================================================== -->
    <section class="grid grid-cols-1 gap-4 sm:grid-cols-3">
      <div
        class="stagger-item rounded-2xl border border-white/[0.04] bg-[#121212] p-6"
        style="--i: 1"
      >
        <p class="mb-2 text-sm uppercase tracking-wider text-[#6a6a6a]">
          Total Owed to You
        </p>
        <p v-if="loading" class="h-8 w-28 animate-pulse rounded-lg bg-white/[0.04]" />
        <p v-else class="font-mono text-2xl font-bold text-[#3bffad]">
          {{ formatMoney(totalOwed) }}
        </p>
      </div>

      <div
        class="stagger-item rounded-2xl border border-white/[0.04] bg-[#121212] p-6"
        style="--i: 2"
      >
        <p class="mb-2 text-sm uppercase tracking-wider text-[#6a6a6a]">
          Total You Owe
        </p>
        <p v-if="loading" class="h-8 w-28 animate-pulse rounded-lg bg-white/[0.04]" />
        <p v-else class="font-mono text-2xl font-bold text-[#ee4d37]">
          {{ formatMoney(totalDebt) }}
        </p>
      </div>

      <div
        class="stagger-item rounded-2xl border border-white/[0.04] bg-[#121212] p-6"
        style="--i: 3"
      >
        <p class="mb-2 text-sm uppercase tracking-wider text-[#6a6a6a]">
          Groups
        </p>
        <p v-if="loading" class="h-8 w-12 animate-pulse rounded-lg bg-white/[0.04]" />
        <p v-else class="font-mono text-2xl font-bold text-[#efefef]">
          {{ groups.length }}
        </p>
      </div>
    </section>

    <!-- ================================================================== -->
    <!-- 3. Quick Actions                                                    -->
    <!-- ================================================================== -->
    <section class="stagger-item flex gap-4" style="--i: 4">
      <NuxtLink
        to="/groups"
        class="btn-lime flex-1 rounded-xl py-3 text-center font-semibold transition-all"
      >
        Add Expense
      </NuxtLink>
      <NuxtLink
        to="/settlements"
        class="flex-1 rounded-xl border border-[#e5fe40]/30 py-3 text-center font-semibold text-[#e5fe40] transition-all hover:border-[#e5fe40]/50 hover:bg-[#e5fe40]/[0.04]"
      >
        Settle Up
      </NuxtLink>
    </section>

    <!-- ================================================================== -->
    <!-- 4. Recent Groups                                                    -->
    <!-- ================================================================== -->
    <section class="stagger-item space-y-5" style="--i: 5">
      <div class="flex items-center justify-between">
        <h2 class="font-serif text-xl text-[#efefef]">Your Groups</h2>
        <NuxtLink
          to="/groups"
          class="text-sm text-[#6a6a6a] transition-colors hover:text-[#b0b0b0]"
        >
          View all &rarr;
        </NuxtLink>
      </div>

      <!-- Loading skeleton -->
      <div v-if="loading" class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div
          v-for="n in 4"
          :key="n"
          class="h-28 animate-pulse rounded-2xl border border-white/[0.04] bg-[#121212]"
        />
      </div>

      <!-- Empty state -->
      <div
        v-else-if="groups.length === 0"
        class="rounded-2xl border border-white/[0.04] bg-[#121212] px-8 py-14 text-center"
      >
        <p class="text-[#6a6a6a]">No groups yet. Create one to start splitting expenses.</p>
        <NuxtLink
          to="/groups"
          class="mt-4 inline-block rounded-xl bg-[#e5fe40] px-5 py-2 text-sm font-semibold text-[#0d0d0d] transition-transform hover:scale-[1.02]"
        >
          Create Group
        </NuxtLink>
      </div>

      <!-- Group cards grid -->
      <div v-else class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <NuxtLink
          v-for="(group, gi) in groups.slice(0, 4)"
          :key="group.id"
          :to="`/groups/${group.id}`"
          class="stagger-item group rounded-2xl border border-white/[0.04] bg-[#121212] p-5 transition-all hover:border-white/[0.08] hover:bg-[#1a1a1a]"
          :style="{ '--i': 6 + gi }"
        >
          <p class="font-semibold text-[#efefef] transition-colors group-hover:text-[#e5fe40]">
            {{ group.name }}
          </p>
          <p v-if="group.description" class="mt-1 line-clamp-1 text-sm text-[#6a6a6a]">
            {{ group.description }}
          </p>
          <div class="mt-3 flex items-center gap-2">
            <!-- Member avatar circles -->
            <div class="flex -space-x-2">
              <span
                v-for="(member, mi) in group.members.slice(0, 5)"
                :key="member.id"
                class="flex h-7 w-7 items-center justify-center rounded-full border-2 border-[#121212] text-[10px] font-bold text-[#0d0d0d]"
                :style="{ backgroundColor: avatarColor(mi) }"
              >
                {{ memberInitial(member) }}
              </span>
              <span
                v-if="group.members.length > 5"
                class="flex h-7 w-7 items-center justify-center rounded-full border-2 border-[#121212] bg-[#2a2a2a] text-[10px] font-medium text-[#b0b0b0]"
              >
                +{{ group.members.length - 5 }}
              </span>
            </div>
            <span class="text-xs text-[#6a6a6a]">
              {{ group.members.length }} member{{ group.members.length !== 1 ? 's' : '' }}
            </span>
          </div>
        </NuxtLink>
      </div>
    </section>

    <!-- ================================================================== -->
    <!-- 5. Recent Activity                                                  -->
    <!-- ================================================================== -->
    <section class="stagger-item space-y-5" style="--i: 10">
      <h2 class="font-serif text-xl text-[#efefef]">Recent Settlements</h2>

      <!-- Loading skeleton -->
      <div v-if="loading" class="space-y-0">
        <div
          v-for="n in 3"
          :key="n"
          class="flex items-center gap-4 border-b border-white/[0.04] py-4"
        >
          <div class="h-5 w-40 animate-pulse rounded bg-white/[0.04]" />
          <div class="ml-auto h-5 w-20 animate-pulse rounded bg-white/[0.04]" />
        </div>
      </div>

      <!-- Empty state -->
      <div
        v-else-if="settlements.length === 0"
        class="rounded-2xl border border-white/[0.04] bg-[#121212] px-8 py-14 text-center"
      >
        <p class="text-[#6a6a6a]">No settlements yet. They will appear here once you start settling up.</p>
      </div>

      <!-- Settlement list -->
      <div v-else>
        <div
          v-for="(s, si) in settlements.slice(0, 6)"
          :key="s.id"
          class="stagger-item flex items-center gap-4 border-b border-white/[0.04] py-4 last:border-b-0"
          :style="{ '--i': 11 + si }"
        >
          <div class="min-w-0 flex-1">
            <p class="truncate text-sm font-medium text-[#efefef]">
              {{ s.description || 'Settlement' }}
            </p>
            <p class="mt-0.5 text-xs text-[#6a6a6a]">
              {{ formatDate(s.created_at) }}
              <span
                class="ml-2 inline-block rounded-full px-2 py-0.5 text-[10px] uppercase tracking-wider"
                :class="statusClasses(s.status)"
              >
                {{ s.status }}
              </span>
            </p>
          </div>
          <p class="shrink-0 font-mono text-lg font-bold text-[#ffcb45]">
            {{ formatMoney(s.amount) }}
          </p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import type { Group, Settlement } from '~/types'

definePageMeta({ middleware: 'auth' })

const auth = useAuthStore()
const api = useApi()

// ------------------------------------------------------------------
// Greeting
// ------------------------------------------------------------------
const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good morning'
  if (hour < 18) return 'Good afternoon'
  return 'Good evening'
})

const firstName = computed(() => {
  if (auth.user?.full_name) return auth.user.full_name.split(' ')[0]
  return auth.user?.username ?? 'there'
})

const formattedDate = computed(() => {
  return new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
    year: 'numeric',
  })
})

// ------------------------------------------------------------------
// Data
// ------------------------------------------------------------------
const groups = ref<Group[]>([])
const settlements = ref<Settlement[]>([])
const loading = ref(true)

const totalOwed = ref(0)
const totalDebt = ref(0)

async function fetchDashboardData() {
  loading.value = true
  try {
    const [groupsData, settlementsData] = await Promise.all([
      api.get<Group[]>('/v1/groups/'),
      api.get<Settlement[]>('/v1/settlements/'),
    ])
    groups.value = groupsData
    settlements.value = settlementsData

    // Compute balances from settlements
    const userId = auth.user?.id
    if (userId && settlementsData.length > 0) {
      let owed = 0
      let debt = 0
      for (const s of settlementsData) {
        if (s.status === 'pending') {
          if (s.payee_id === userId) owed += s.amount
          if (s.payer_id === userId) debt += s.amount
        }
      }
      totalOwed.value = owed
      totalDebt.value = debt
    }
  }
  catch (e) {
    console.error('Failed to fetch dashboard data', e)
  }
  finally {
    loading.value = false
  }
}

// ------------------------------------------------------------------
// Helpers
// ------------------------------------------------------------------
const AVATAR_COLORS = ['#e5fe40', '#3bffad', '#ffcb45', '#ee4d37', '#a78bfa', '#38bdf8']

function avatarColor(index: number): string {
  return AVATAR_COLORS[index % AVATAR_COLORS.length]
}

function memberInitial(member: { user_id: number }): string {
  // Without full user data on member, use a generic initial
  return `U${member.user_id}`.charAt(0).toUpperCase()
}

function formatMoney(amount: number): string {
  return `$${amount.toFixed(2)}`
}

function formatDate(dateStr: string | null): string {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

function statusClasses(status: string): string {
  switch (status) {
    case 'completed':
    case 'settled':
      return 'bg-[#3bffad]/10 text-[#3bffad]'
    case 'pending':
      return 'bg-[#ffcb45]/10 text-[#ffcb45]'
    case 'rejected':
    case 'cancelled':
      return 'bg-[#ee4d37]/10 text-[#ee4d37]'
    default:
      return 'bg-white/[0.06] text-[#b0b0b0]'
  }
}

// ------------------------------------------------------------------
// Fetch on mount (ensure user is loaded first)
// ------------------------------------------------------------------
onMounted(async () => {
  if (!auth.user) {
    await auth.fetchUser()
  }
  await fetchDashboardData()
})
</script>

<style scoped>
/* Stagger-enter animation */
.stagger-item {
  opacity: 0;
  transform: translateY(12px);
  animation: stagger-fade-in 0.5s ease-out forwards;
  animation-delay: calc(var(--i, 0) * 80ms);
}

@keyframes stagger-fade-in {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Lime CTA button with 3D press effect */
.btn-lime {
  background-color: #e5fe40;
  color: #0d0d0d;
  box-shadow:
    0 4px 0 0 #b8cc30,
    0 6px 12px rgba(229, 254, 64, 0.15);
  transform: translateY(0);
}

.btn-lime:hover {
  transform: translateY(-1px);
  box-shadow:
    0 5px 0 0 #b8cc30,
    0 8px 16px rgba(229, 254, 64, 0.2);
}

.btn-lime:active {
  transform: translateY(3px);
  box-shadow:
    0 1px 0 0 #b8cc30,
    0 2px 4px rgba(229, 254, 64, 0.1);
}
</style>
