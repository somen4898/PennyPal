<template>
  <div class="flex flex-col" :style="{ height: 'calc(100vh - 96px)' }">
    <!-- Group selector bar -->
    <div class="mb-4 flex items-center justify-between">
      <h1 class="font-serif text-2xl tracking-tight text-[#efefef]">SETTL AI</h1>
      <div class="relative">
        <select
          v-model="selectedGroupId"
          class="appearance-none rounded-xl border border-white/[0.06] bg-[#121212] py-2 pl-4 pr-10 text-sm text-[#b0b0b0] outline-none transition-colors focus:border-[#e5fe40]/30 focus:text-[#efefef]"
        >
          <option :value="null">No group selected</option>
          <option v-for="g in groups" :key="g.id" :value="g.id">{{ g.name }}</option>
        </select>
        <svg class="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[#6a6a6a]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
        </svg>
      </div>
    </div>

    <!-- Chat area -->
    <div ref="chatContainer" class="flex-1 overflow-y-auto scroll-smooth rounded-2xl border border-white/[0.04] bg-[#0a0a0a]">
      <!-- Empty state -->
      <div v-if="messages.length === 0 && !chatLoading" class="flex h-full flex-col items-center justify-center px-6">
        <div class="mb-8 text-center">
          <h2 class="font-serif text-2xl text-[#efefef]">Ask me anything about your expenses</h2>
          <p class="mt-2 text-sm text-[#6a6a6a]">I can help you track balances, settle debts, and manage splits.</p>
        </div>
        <div class="flex flex-wrap justify-center gap-2">
          <button
            v-for="chip in quickActions"
            :key="chip"
            class="rounded-full border border-white/[0.06] bg-[#161616] px-4 py-2 text-sm text-[#b0b0b0] transition-all hover:border-[#e5fe40]/30 hover:text-[#efefef] active:scale-95"
            @click="sendMessage(chip)"
          >
            {{ chip }}
          </button>
        </div>
      </div>

      <!-- Messages -->
      <div v-else class="space-y-4 p-5">
        <TransitionGroup
          enter-active-class="transition duration-300 ease-out"
          enter-from-class="translate-y-2 opacity-0"
          enter-to-class="translate-y-0 opacity-100"
        >
          <div
            v-for="(msg, i) in messages"
            :key="i"
            :class="msg.role === 'user' ? 'flex justify-end' : 'flex justify-start'"
          >
            <div :class="msg.role === 'user' ? 'max-w-[75%]' : 'max-w-[80%]'">
              <!-- Assistant label -->
              <span
                v-if="msg.role === 'assistant'"
                class="mb-1.5 block text-[11px] font-semibold uppercase tracking-[0.15em] text-[#e5fe40]"
              >
                SETTL AI
              </span>

              <div
                :class="[
                  'whitespace-pre-wrap rounded-2xl p-4 text-sm leading-relaxed',
                  msg.role === 'user'
                    ? 'rounded-br-sm bg-[#1e1e1e] text-[#efefef]'
                    : 'rounded-bl-sm bg-[#121212] text-[#d0d0d0]',
                ]"
              >
                {{ msg.content }}
              </div>
            </div>
          </div>
        </TransitionGroup>

        <!-- Typing indicator -->
        <Transition
          enter-active-class="transition duration-200 ease-out"
          enter-from-class="opacity-0"
          enter-to-class="opacity-100"
          leave-active-class="transition duration-150 ease-in"
          leave-from-class="opacity-100"
          leave-to-class="opacity-0"
        >
          <div v-if="chatLoading" class="flex justify-start">
            <div class="max-w-[80%]">
              <span class="mb-1.5 block text-[11px] font-semibold uppercase tracking-[0.15em] text-[#e5fe40]">
                SETTL AI
              </span>
              <div class="flex items-center gap-1.5 rounded-2xl rounded-bl-sm bg-[#121212] px-5 py-4">
                <span class="typing-dot h-2 w-2 rounded-full bg-[#e5fe40]/60" style="animation-delay: 0ms" />
                <span class="typing-dot h-2 w-2 rounded-full bg-[#e5fe40]/60" style="animation-delay: 150ms" />
                <span class="typing-dot h-2 w-2 rounded-full bg-[#e5fe40]/60" style="animation-delay: 300ms" />
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </div>

    <!-- Input area -->
    <div class="mt-4">
      <form class="flex items-end gap-3" @submit.prevent="sendMessage(input)">
        <div class="relative flex-1">
          <textarea
            ref="inputEl"
            v-model="input"
            rows="1"
            placeholder="Ask about your expenses..."
            class="block w-full resize-none rounded-xl border border-white/[0.06] bg-[#121212] px-4 py-3 pr-12 text-sm text-[#efefef] placeholder-[#4a4a4a] outline-none transition-colors focus:border-[#e5fe40]/30"
            :disabled="chatLoading"
            @keydown.enter.exact.prevent="sendMessage(input)"
            @input="autoGrow"
          />
        </div>
        <button
          type="submit"
          :disabled="!input.trim() || chatLoading"
          class="flex h-[44px] w-[44px] flex-shrink-0 items-center justify-center rounded-xl bg-[#e5fe40] text-[#0d0d0d] transition-all hover:brightness-110 active:scale-95 disabled:opacity-30 disabled:hover:brightness-100"
          style="box-shadow: 0 4px 0 0 #b5cc30"
        >
          <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
          </svg>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ChatMessage, Group } from '~/types'

definePageMeta({ middleware: 'auth' })

const api = useApi()

const messages = ref<ChatMessage[]>([])
const input = ref('')
const selectedGroupId = ref<number | null>(null)
const chatLoading = ref(false)
const groups = ref<Group[]>([])

const chatContainer = ref<HTMLElement | null>(null)
const inputEl = ref<HTMLTextAreaElement | null>(null)

const quickActions = ['What do I owe?', 'Show my balances', 'Help me settle up']

// Fetch groups for selector
async function fetchGroups() {
  try {
    groups.value = await api.get<Group[]>('/v1/groups/')
  }
  catch {
    // Silently fail; group selector will just show "No group selected"
  }
}

function autoGrow() {
  const el = inputEl.value
  if (!el) return
  el.style.height = 'auto'
  el.style.height = `${Math.min(el.scrollHeight, 120)}px`
}

function scrollToBottom() {
  nextTick(() => {
    const container = chatContainer.value
    if (container) {
      container.scrollTo({ top: container.scrollHeight, behavior: 'smooth' })
    }
  })
}

async function sendMessage(text: string) {
  const trimmed = text.trim()
  if (!trimmed || chatLoading.value) return

  // Add user message
  messages.value.push({ role: 'user', content: trimmed })
  input.value = ''

  // Reset textarea height
  if (inputEl.value) {
    inputEl.value.style.height = 'auto'
  }

  scrollToBottom()
  chatLoading.value = true

  try {
    const res = await api.post<{ response: string, actions_taken?: string[], suggested_actions?: string[] }>(
      '/v1/chatbot/chat',
      { message: trimmed, group_id: selectedGroupId.value },
    )
    messages.value.push({ role: 'assistant', content: res.response })
  }
  catch {
    messages.value.push({
      role: 'assistant',
      content: 'Sorry, something went wrong. Please try again.',
    })
  }
  finally {
    chatLoading.value = false
    scrollToBottom()
  }
}

onMounted(() => {
  fetchGroups()
})
</script>

<style scoped>
@keyframes typingBounce {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.4;
  }
  30% {
    transform: translateY(-6px);
    opacity: 1;
  }
}

.typing-dot {
  animation: typingBounce 1.2s ease-in-out infinite;
}

/* Custom scrollbar for chat */
div::-webkit-scrollbar {
  width: 4px;
}

div::-webkit-scrollbar-track {
  background: transparent;
}

div::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 2px;
}

div::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.15);
}
</style>
