<template>
  <div class="min-h-screen bg-[#0d0d0d] px-4 py-8 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-5xl">
      <!-- Header -->
      <div
        class="stagger-enter mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"
        :style="{ animationDelay: '0ms' }"
      >
        <h1 class="font-serif text-3xl text-[#efefef] sm:text-4xl">Groups</h1>
        <button
          class="settl-btn-primary flex items-center gap-2 text-sm"
          @click="showCreateModal = true"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
          Create Group
        </button>
      </div>

      <!-- Create Group Modal Overlay -->
      <Teleport to="body">
        <Transition name="modal">
          <div
            v-if="showCreateModal"
            class="fixed inset-0 z-50 flex items-center justify-center p-4"
            @click.self="closeModal"
          >
            <div class="fixed inset-0 bg-black/60 backdrop-blur-sm" @click="closeModal" />
            <div class="relative z-10 w-full max-w-md">
              <div class="settl-card p-6">
                <div class="mb-6 flex items-center justify-between">
                  <h2 class="font-serif text-xl text-[#efefef]">New Group</h2>
                  <button
                    class="rounded-lg p-1 text-[#6a6a6a] transition-colors hover:bg-white/5 hover:text-[#efefef]"
                    @click="closeModal"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>

                <form @submit.prevent="createGroup">
                  <div class="mb-4">
                    <label class="mb-1.5 block text-sm font-medium text-[#b0b0b0]">Group Name</label>
                    <input
                      v-model="newGroup.name"
                      type="text"
                      required
                      placeholder="Weekend trip, Flatmates..."
                      class="w-full rounded-xl border border-white/[0.06] bg-[#1e1e1e] px-4 py-3 text-sm text-[#efefef] placeholder-[#6a6a6a] outline-none transition-colors focus:border-[#e5fe40]/30 focus:ring-1 focus:ring-[#e5fe40]/20"
                    />
                  </div>

                  <div class="mb-6">
                    <label class="mb-1.5 block text-sm font-medium text-[#b0b0b0]">Description</label>
                    <textarea
                      v-model="newGroup.description"
                      rows="3"
                      placeholder="What's this group for?"
                      class="w-full resize-none rounded-xl border border-white/[0.06] bg-[#1e1e1e] px-4 py-3 text-sm text-[#efefef] placeholder-[#6a6a6a] outline-none transition-colors focus:border-[#e5fe40]/30 focus:ring-1 focus:ring-[#e5fe40]/20"
                    />
                  </div>

                  <div class="flex gap-3">
                    <button
                      type="button"
                      class="flex-1 rounded-xl border border-white/[0.06] bg-[#1e1e1e] px-4 py-3 text-sm font-medium text-[#b0b0b0] transition-colors hover:bg-[#252525] hover:text-[#efefef]"
                      @click="closeModal"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      class="settl-btn-primary flex-1 text-sm"
                      :disabled="creating"
                    >
                      {{ creating ? 'Creating...' : 'Create Group' }}
                    </button>
                  </div>

                  <p v-if="createError" class="mt-3 text-center text-sm text-[#ee4d37]">
                    {{ createError }}
                  </p>
                </form>
              </div>
            </div>
          </div>
        </Transition>
      </Teleport>

      <!-- Loading State -->
      <div v-if="loading" class="grid gap-4 sm:grid-cols-2">
        <div v-for="n in 4" :key="n" class="settl-card animate-pulse p-6">
          <div class="mb-3 h-5 w-2/3 rounded-lg bg-white/[0.06]" />
          <div class="mb-4 h-4 w-full rounded-lg bg-white/[0.04]" />
          <div class="flex gap-1">
            <div v-for="a in 3" :key="a" class="h-7 w-7 rounded-full bg-white/[0.06]" />
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="stagger-enter settl-card p-8 text-center" :style="{ animationDelay: '100ms' }">
        <div class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-[#ee4d37]/10">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-[#ee4d37]" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
        </div>
        <p class="mb-1 text-[#efefef]">Failed to load groups</p>
        <p class="mb-4 text-sm text-[#6a6a6a]">{{ error }}</p>
        <button class="settl-btn-primary text-sm" @click="fetchGroups">Try Again</button>
      </div>

      <!-- Empty State -->
      <div
        v-else-if="groups.length === 0"
        class="stagger-enter settl-card p-12 text-center"
        :style="{ animationDelay: '100ms' }"
      >
        <div class="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-[#e5fe40]/10">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-[#e5fe40]" viewBox="0 0 20 20" fill="currentColor">
            <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z" />
          </svg>
        </div>
        <h3 class="mb-2 font-serif text-xl text-[#efefef]">No groups yet</h3>
        <p class="mb-6 text-sm text-[#6a6a6a]">Create your first group to start splitting expenses with friends.</p>
        <button class="settl-btn-primary text-sm" @click="showCreateModal = true">
          Create Your First Group
        </button>
      </div>

      <!-- Groups Grid -->
      <div v-else class="grid gap-4 sm:grid-cols-2">
        <div
          v-for="(group, index) in groups"
          :key="group.id"
          class="stagger-enter settl-card cursor-pointer p-6"
          :style="{ animationDelay: `${(index + 1) * 80}ms` }"
          @click="navigateTo(`/groups/${group.id}`)"
        >
          <div class="mb-1 flex items-start justify-between">
            <h3 class="text-lg font-semibold text-[#efefef]">{{ group.name }}</h3>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 shrink-0 text-[#6a6a6a]" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
            </svg>
          </div>

          <p v-if="group.description" class="mb-4 line-clamp-2 text-sm text-[#6a6a6a]">
            {{ group.description }}
          </p>
          <div v-else class="mb-4" />

          <div class="flex items-center gap-2">
            <div class="flex -space-x-2">
              <div
                v-for="(member, mIndex) in group.members.slice(0, 5)"
                :key="member.id"
                class="flex h-7 w-7 items-center justify-center rounded-full border-2 border-[#121212] text-[10px] font-bold"
                :class="avatarColor(mIndex)"
              >
                {{ memberInitial(member.user_id) }}
              </div>
              <div
                v-if="group.members.length > 5"
                class="flex h-7 w-7 items-center justify-center rounded-full border-2 border-[#121212] bg-[#252525] text-[10px] font-medium text-[#b0b0b0]"
              >
                +{{ group.members.length - 5 }}
              </div>
            </div>
            <span class="text-xs text-[#6a6a6a]">
              {{ group.members.length }} member{{ group.members.length !== 1 ? 's' : '' }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Group } from '~/types'

definePageMeta({ middleware: 'auth' })

const api = useApi()

const groups = ref<Group[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

const showCreateModal = ref(false)
const creating = ref(false)
const createError = ref<string | null>(null)
const newGroup = ref({ name: '', description: '' })

const avatarColors = [
  'bg-[#e5fe40]/20 text-[#e5fe40]',
  'bg-[#3bffad]/20 text-[#3bffad]',
  'bg-[#ffcb45]/20 text-[#ffcb45]',
  'bg-[#6a35ff]/20 text-[#6a35ff]',
  'bg-[#ee4d37]/20 text-[#ee4d37]',
]

function avatarColor(index: number) {
  return avatarColors[index % avatarColors.length]
}

function memberInitial(userId: number) {
  return `U${userId}`
}

async function fetchGroups() {
  loading.value = true
  error.value = null
  try {
    groups.value = await api.get<Group[]>('/v1/groups/')
  }
  catch (e: any) {
    error.value = e?.data?.detail || e?.message || 'Something went wrong'
  }
  finally {
    loading.value = false
  }
}

function closeModal() {
  showCreateModal.value = false
  createError.value = null
  newGroup.value = { name: '', description: '' }
}

async function createGroup() {
  creating.value = true
  createError.value = null
  try {
    const created = await api.post<Group>('/v1/groups/', {
      name: newGroup.value.name,
      description: newGroup.value.description || null,
    })
    groups.value.unshift(created)
    closeModal()
  }
  catch (e: any) {
    createError.value = e?.data?.detail || e?.message || 'Failed to create group'
  }
  finally {
    creating.value = false
  }
}

onMounted(() => {
  fetchGroups()
})
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-active .settl-card,
.modal-leave-active .settl-card {
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .settl-card {
  transform: scale(0.95) translateY(10px);
  opacity: 0;
}

.modal-leave-to .settl-card {
  transform: scale(0.95) translateY(10px);
  opacity: 0;
}
</style>
