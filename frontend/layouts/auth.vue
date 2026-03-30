<template>
  <div class="flex min-h-screen items-center justify-center bg-[#0d0d0d] grain">
    <!-- Subtle gradient glow behind the form -->
    <div class="pointer-events-none fixed left-1/2 top-1/3 h-[500px] w-[500px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-[#e5fe40]/[0.03] blur-[120px]" />

    <div class="relative z-10 w-full max-w-md px-6">
      <!-- Logo -->
      <div class="mb-12 text-center">
        <h1 class="font-serif text-5xl tracking-tight text-[#e5fe40]">SETTL</h1>
        <p class="mt-3 text-sm tracking-[0.15em] text-[#6a6a6a]">SPLIT. TRACK. SETTLE.</p>
      </div>

      <slot />
    </div>
  </div>
</template>
