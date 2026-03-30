<template>
  <div class="landing" ref="landingRef">
    <!-- Fixed Nav -->
    <nav class="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-[5%] md:px-[8%] py-6">
      <span class="font-serif text-2xl tracking-tight text-white">SETTL</span>
      <div class="flex items-center gap-4">
        <NuxtLink to="/login" class="glass-btn text-xs font-semibold uppercase tracking-[3px] text-white px-6 py-3">
          Log in
        </NuxtLink>
        <NuxtLink to="/register" class="bg-[#e5fe40] text-black text-xs font-semibold uppercase tracking-[3px] px-6 py-3 transition-opacity hover:opacity-90">
          Get started
        </NuxtLink>
      </div>
    </nav>

    <!-- Section 1: Hero -->
    <section class="relative flex min-h-screen items-end pb-[15vh] md:items-center md:pb-0">
      <div class="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_60%_50%_at_50%_40%,rgba(229,254,64,0.05),transparent)]" />

      <div class="relative z-10 w-full px-[5%] md:px-[10%]">
        <div class="reveal" data-reveal>
          <p class="mb-6 text-xs font-semibold uppercase tracking-[6px] text-white/50">
            Expense splitting, reimagined
          </p>
        </div>
        <div class="reveal" data-reveal>
          <h1 class="font-serif text-[52px] leading-[1.02] text-white md:text-[90px] md:leading-[92px] max-w-[900px]">
            Split expenses.<br />
            Not friendships.
          </h1>
        </div>
        <div class="reveal" data-reveal>
          <p class="mt-8 max-w-[480px] text-base leading-[27px] text-white/70 md:text-[18px] md:leading-[30px]">
            Track shared expenses, optimize settlements, and let AI handle the
            math. Built for people who value clarity in every transaction.
          </p>
        </div>
        <div class="reveal mt-12 flex gap-4" data-reveal>
          <NuxtLink to="/register" class="glass-btn-lime px-8 py-4 text-sm font-semibold uppercase tracking-[3px] text-black">
            Start splitting
          </NuxtLink>
        </div>
      </div>
    </section>

    <!-- Gradient divider -->
    <div class="h-px w-full bg-gradient-to-r from-black via-[#222] to-black" />

    <!-- Section 2: The Problem -->
    <section class="flex min-h-[70vh] flex-col items-center justify-center px-[5%] md:px-[10%] py-24">
      <div class="reveal max-w-[700px] text-center" data-reveal>
        <p class="mb-6 text-xs font-semibold uppercase tracking-[6px] text-white/50">
          The problem
        </p>
      </div>
      <div class="reveal max-w-[700px] text-center" data-reveal>
        <h2 class="font-serif text-[36px] leading-[1.1] text-white md:text-[66px] md:leading-[72px]">
          Splitting bills shouldn't feel like solving equations
        </h2>
      </div>
      <div class="reveal mt-8 max-w-[500px] text-center" data-reveal>
        <p class="text-base leading-[27px] text-white/60">
          Awkward reminders. Uneven splits. Lost track of who paid what.
          We built SETTL to make shared finances frictionless.
        </p>
      </div>
    </section>

    <!-- Section 3: Features -->
    <section class="relative mt-12">
      <!-- Feature 1: Groups -->
      <div class="flex min-h-[80vh] flex-col justify-center px-[5%] md:flex-row md:items-center md:px-[10%] py-20">
        <div class="reveal md:w-1/2" data-reveal>
          <p class="mb-4 text-xs font-semibold uppercase tracking-[6px] text-[#e5fe40]">
            01
          </p>
          <h3 class="font-serif text-[32px] leading-[1.1] text-white md:text-[52px] md:leading-[58px]">
            Groups that<br />make sense
          </h3>
          <p class="mt-6 max-w-[400px] text-base leading-[27px] text-white/60">
            Create groups for trips, flatmates, dinners — anything.
            Add members, track expenses, see who owes what. Real-time.
          </p>
        </div>
        <div class="reveal mt-12 md:mt-0 md:w-1/2 md:pl-20" data-reveal>
          <div class="feature-card">
            <div class="flex items-center gap-3 mb-6">
              <div class="h-10 w-10 bg-[#e5fe40]/10 flex items-center justify-center">
                <span class="text-[#e5fe40] text-lg">G</span>
              </div>
              <div>
                <p class="text-sm font-semibold text-white">Goa Trip 2026</p>
                <p class="text-xs text-white/40">4 members</p>
              </div>
            </div>
            <div class="space-y-3">
              <div class="flex items-center justify-between border-t border-white/[0.06] pt-3">
                <span class="text-sm text-white/70">Hotel booking</span>
                <span class="font-mono text-sm font-semibold text-[#ffcb45]">₹12,400</span>
              </div>
              <div class="flex items-center justify-between border-t border-white/[0.06] pt-3">
                <span class="text-sm text-white/70">Dinner at Thalassa</span>
                <span class="font-mono text-sm font-semibold text-[#ffcb45]">₹3,200</span>
              </div>
              <div class="flex items-center justify-between border-t border-white/[0.06] pt-3">
                <span class="text-sm text-white/70">Cab to airport</span>
                <span class="font-mono text-sm font-semibold text-[#ffcb45]">₹1,800</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Feature 2: Smart Splits -->
      <div class="flex min-h-[80vh] flex-col justify-center px-[5%] md:flex-row-reverse md:items-center md:px-[10%] py-20">
        <div class="reveal md:w-1/2 md:pl-20" data-reveal>
          <p class="mb-4 text-xs font-semibold uppercase tracking-[6px] text-[#e5fe40]">
            02
          </p>
          <h3 class="font-serif text-[32px] leading-[1.1] text-white md:text-[52px] md:leading-[58px]">
            Split it<br />your way
          </h3>
          <p class="mt-6 max-w-[400px] text-base leading-[27px] text-white/60">
            Equal splits. Exact amounts. Percentages. Every expense is different — your splits should be too.
          </p>
        </div>
        <div class="reveal mt-12 md:mt-0 md:w-1/2" data-reveal>
          <div class="feature-card">
            <p class="mb-5 text-xs font-semibold uppercase tracking-[4px] text-white/40">Split type</p>
            <div class="flex gap-2 mb-6">
              <span class="bg-[#e5fe40] text-black text-xs font-semibold uppercase tracking-[2px] px-4 py-2">Equal</span>
              <span class="border border-white/20 text-white/60 text-xs font-semibold uppercase tracking-[2px] px-4 py-2">Exact</span>
              <span class="border border-white/20 text-white/60 text-xs font-semibold uppercase tracking-[2px] px-4 py-2">Percent</span>
            </div>
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="h-8 w-8 bg-[#3bffad]/10 flex items-center justify-center text-xs text-[#3bffad] font-semibold">A</div>
                  <span class="text-sm text-white/70">Alice</span>
                </div>
                <span class="font-mono text-sm text-white">₹500</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="h-8 w-8 bg-[#6a35ff]/10 flex items-center justify-center text-xs text-[#6a35ff] font-semibold">B</div>
                  <span class="text-sm text-white/70">Bob</span>
                </div>
                <span class="font-mono text-sm text-white">₹500</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="h-8 w-8 bg-[#ff8744]/10 flex items-center justify-center text-xs text-[#ff8744] font-semibold">C</div>
                  <span class="text-sm text-white/70">Charlie</span>
                </div>
                <span class="font-mono text-sm text-white">₹500</span>
              </div>
            </div>
            <div class="mt-5 border-t border-white/[0.06] pt-4 flex items-center justify-between">
              <span class="text-xs uppercase tracking-[3px] text-white/40">Total</span>
              <span class="font-mono text-lg font-bold text-[#ffcb45]">₹1,500</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Feature 3: AI -->
      <div class="flex min-h-[80vh] flex-col justify-center px-[5%] md:flex-row md:items-center md:px-[10%] py-20">
        <div class="reveal md:w-1/2" data-reveal>
          <p class="mb-4 text-xs font-semibold uppercase tracking-[6px] text-[#e5fe40]">
            03
          </p>
          <h3 class="font-serif text-[32px] leading-[1.1] text-white md:text-[52px] md:leading-[58px]">
            AI that<br />understands money
          </h3>
          <p class="mt-6 max-w-[400px] text-base leading-[27px] text-white/60">
            Ask in plain language. "How much do I owe Priya?" or "Add last night's dinner, split equally." Powered by Claude.
          </p>
        </div>
        <div class="reveal mt-12 md:mt-0 md:w-1/2 md:pl-20" data-reveal>
          <div class="feature-card">
            <div class="flex items-center gap-2 mb-5">
              <span class="text-[10px] font-semibold uppercase tracking-[3px] text-[#e5fe40]">SETTL AI</span>
            </div>
            <div class="space-y-4">
              <div class="flex justify-end">
                <div class="bg-white/[0.08] px-4 py-3 max-w-[80%]">
                  <p class="text-sm text-white/90">How much do I owe in the Goa trip group?</p>
                </div>
              </div>
              <div class="flex justify-start">
                <div class="border border-white/[0.06] px-4 py-3 max-w-[80%]">
                  <p class="text-sm text-white/70">You owe <span class="font-mono text-[#ee4d37]">₹4,350</span> in total. Priya paid for the hotel and dinner. I'd suggest settling with her first — she's owed the most.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Feature 4: Settlements -->
      <div class="flex min-h-[80vh] flex-col justify-center px-[5%] md:flex-row-reverse md:items-center md:px-[10%] py-20">
        <div class="reveal md:w-1/2 md:pl-20" data-reveal>
          <p class="mb-4 text-xs font-semibold uppercase tracking-[6px] text-[#e5fe40]">
            04
          </p>
          <h3 class="font-serif text-[32px] leading-[1.1] text-white md:text-[52px] md:leading-[58px]">
            Settle up.<br />Move on.
          </h3>
          <p class="mt-6 max-w-[400px] text-base leading-[27px] text-white/60">
            Smart algorithms minimize the number of transactions needed.
            Three people, one payment. Not three payments each way.
          </p>
        </div>
        <div class="reveal mt-12 md:mt-0 md:w-1/2" data-reveal>
          <div class="feature-card">
            <p class="mb-5 text-xs font-semibold uppercase tracking-[4px] text-white/40">Optimized settlements</p>
            <div class="space-y-4">
              <div class="flex items-center justify-between border border-white/[0.06] p-4">
                <div class="flex items-center gap-3">
                  <div class="h-8 w-8 bg-[#ee4d37]/10 flex items-center justify-center text-xs text-[#ee4d37] font-semibold">Y</div>
                  <span class="text-sm text-white/70">You</span>
                  <svg class="w-4 h-4 text-white/30" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                  <div class="h-8 w-8 bg-[#3bffad]/10 flex items-center justify-center text-xs text-[#3bffad] font-semibold">P</div>
                  <span class="text-sm text-white/70">Priya</span>
                </div>
                <span class="font-mono text-sm font-bold text-[#ffcb45]">₹4,350</span>
              </div>
              <div class="flex justify-center">
                <span class="glass-btn-lime px-6 py-2 text-[11px] font-semibold uppercase tracking-[3px] text-black cursor-pointer">
                  Settle now
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Section 4: CTA -->
    <section class="relative flex min-h-[60vh] flex-col items-center justify-center px-[5%] py-24">
      <div class="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_50%_50%_at_50%_50%,rgba(229,254,64,0.04),transparent)]" />
      <div class="reveal relative z-10 text-center" data-reveal>
        <h2 class="font-serif text-[40px] leading-[1.05] text-white md:text-[72px] md:leading-[78px]">
          Stop calculating.<br />Start settling.
        </h2>
      </div>
      <div class="reveal relative z-10 mt-10" data-reveal>
        <NuxtLink to="/register" class="glass-btn-lime px-10 py-5 text-sm font-semibold uppercase tracking-[4px] text-black">
          Create free account
        </NuxtLink>
      </div>
      <div class="reveal relative z-10 mt-5" data-reveal>
        <p class="text-xs text-white/30 uppercase tracking-[3px]">No credit card required</p>
      </div>
    </section>

    <!-- Footer -->
    <footer class="mt-24 border-t border-white/[0.1] px-[5%] md:px-[10%] py-12">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between">
        <div>
          <span class="font-serif text-xl text-white/80">SETTL</span>
          <p class="mt-2 text-sm text-white/50 tracking-wider">Split. Track. Settle.</p>
        </div>
        <div class="mt-8 md:mt-0 flex gap-8">
          <NuxtLink to="/login" class="text-sm uppercase tracking-[3px] text-white/70 hover:text-white transition-colors">Log in</NuxtLink>
          <NuxtLink to="/register" class="text-sm uppercase tracking-[3px] text-white/70 hover:text-white transition-colors">Sign up</NuxtLink>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: false })

const landingRef = ref<HTMLElement | null>(null)

onMounted(() => {
  const auth = useAuthStore()
  auth.loadToken()
  if (auth.isAuthenticated) {
    navigateTo('/')
    return
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed')
          observer.unobserve(entry.target)
        }
      })
    },
    { threshold: 0.15, rootMargin: '0px 0px -50px 0px' },
  )

  document.querySelectorAll('[data-reveal]').forEach((el) => {
    observer.observe(el)
  })
})
</script>

<style scoped>
.landing {
  background: #000;
  color: #fff;
  font-family: 'DM Sans', sans-serif;
  overflow-x: hidden;
}

.reveal {
  opacity: 0;
  transform: translate3d(0, 60px, 0);
  transition: opacity 0.8s cubic-bezier(0.47, 1.64, 0.41, 0.8),
              transform 1s cubic-bezier(0.47, 1.64, 0.41, 0.8);
}

.reveal.revealed {
  opacity: 1;
  transform: translate3d(0, 0, 0);
}

.reveal:nth-child(2) { transition-delay: 0.1s; }
.reveal:nth-child(3) { transition-delay: 0.2s; }
.reveal:nth-child(4) { transition-delay: 0.3s; }

.glass-btn {
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.glass-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.35);
}

.glass-btn-lime {
  background: #e5fe40;
  transition: all 0.3s ease;
}

.glass-btn-lime:hover {
  background: #d4ed3a;
}

.feature-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  padding: 32px;
}

.glass-btn,
.glass-btn-lime,
.feature-card,
.feature-card div {
  border-radius: 0 !important;
}

.font-serif {
  font-family: 'DM Serif Display', serif;
}

.font-mono {
  font-family: 'JetBrains Mono', monospace;
}

::selection {
  background: rgba(229, 254, 64, 0.3);
  color: #fff;
}

.landing::-webkit-scrollbar {
  display: none;
}
.landing {
  scrollbar-width: none;
}
</style>
