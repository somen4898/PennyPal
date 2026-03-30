<template>
  <div class="min-h-screen bg-[#0d0d0d] px-4 py-8 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-4xl">
      <!-- Loading State -->
      <div v-if="loading" class="space-y-6">
        <div class="h-4 w-24 animate-pulse rounded bg-white/[0.06]" />
        <div class="h-8 w-64 animate-pulse rounded-lg bg-white/[0.06]" />
        <div class="h-4 w-96 animate-pulse rounded bg-white/[0.04]" />
        <div class="flex gap-2">
          <div v-for="n in 4" :key="n" class="h-8 w-20 animate-pulse rounded-full bg-white/[0.06]" />
        </div>
        <div class="settl-card animate-pulse p-8">
          <div class="space-y-4">
            <div class="h-4 w-full rounded bg-white/[0.04]" />
            <div class="h-4 w-3/4 rounded bg-white/[0.04]" />
            <div class="h-4 w-1/2 rounded bg-white/[0.04]" />
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
        <p class="mb-1 text-[#efefef]">Failed to load group</p>
        <p class="mb-4 text-sm text-[#6a6a6a]">{{ error }}</p>
        <button class="settl-btn-primary text-sm" @click="fetchGroup">Try Again</button>
      </div>

      <!-- Group Content -->
      <template v-else-if="group">
        <!-- Back Link -->
        <button
          class="stagger-enter mb-6 flex items-center gap-1.5 text-sm text-[#6a6a6a] transition-colors hover:text-[#efefef]"
          :style="{ animationDelay: '0ms' }"
          @click="navigateTo('/groups')"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
          </svg>
          Groups
        </button>

        <!-- Group Header -->
        <div class="stagger-enter mb-2" :style="{ animationDelay: '60ms' }">
          <h1 class="font-serif text-2xl text-[#efefef] sm:text-3xl">{{ group.name }}</h1>
        </div>
        <p
          v-if="group.description"
          class="stagger-enter mb-5 text-sm text-[#6a6a6a]"
          :style="{ animationDelay: '120ms' }"
        >
          {{ group.description }}
        </p>

        <!-- Member Pills -->
        <div class="stagger-enter mb-8 flex flex-wrap gap-2" :style="{ animationDelay: '180ms' }">
          <div
            v-for="(member, mIndex) in group.members"
            :key="member.id"
            class="flex items-center gap-1.5 rounded-full border border-white/[0.06] bg-[#1e1e1e] px-3 py-1.5"
          >
            <div
              class="flex h-5 w-5 items-center justify-center rounded-full text-[9px] font-bold"
              :class="avatarColor(mIndex)"
            >
              {{ memberInitial(member.user_id) }}
            </div>
            <span class="text-xs text-[#b0b0b0]">User {{ member.user_id }}</span>
            <span
              v-if="member.is_admin"
              class="rounded-full bg-[#e5fe40]/15 px-1.5 py-0.5 text-[9px] font-semibold text-[#e5fe40]"
            >
              Admin
            </span>
          </div>
        </div>

        <!-- Tab Navigation -->
        <div class="stagger-enter mb-6 border-b border-white/[0.06]" :style="{ animationDelay: '240ms' }">
          <nav class="-mb-px flex gap-6">
            <button
              v-for="tab in tabs"
              :key="tab.key"
              class="relative pb-3 text-sm font-medium transition-colors"
              :class="
                activeTab === tab.key
                  ? 'text-[#efefef]'
                  : 'text-[#6a6a6a] hover:text-[#b0b0b0]'
              "
              @click="activeTab = tab.key"
            >
              {{ tab.label }}
              <div
                v-if="activeTab === tab.key"
                class="absolute bottom-0 left-0 right-0 h-0.5 rounded-full bg-[#e5fe40]"
              />
            </button>
          </nav>
        </div>

        <!-- Tab Content -->
        <div class="stagger-enter" :style="{ animationDelay: '300ms' }">
          <!-- ==================== EXPENSES TAB ==================== -->
          <div v-if="activeTab === 'expenses'">
            <div class="mb-4 flex items-center justify-between">
              <h2 class="text-sm font-medium text-[#b0b0b0]">
                {{ expenses.length }} expense{{ expenses.length !== 1 ? 's' : '' }}
              </h2>
              <button
                class="settl-btn-primary flex items-center gap-1.5 px-4 py-2 text-xs"
                @click="showExpenseForm = !showExpenseForm"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
                </svg>
                Add Expense
              </button>
            </div>

            <!-- Add Expense Form -->
            <Transition name="slide">
              <div v-if="showExpenseForm" class="settl-card mb-6 p-6">
                <div class="mb-5 flex items-center justify-between">
                  <h3 class="font-serif text-lg text-[#efefef]">New Expense</h3>
                  <button
                    class="rounded-lg p-1 text-[#6a6a6a] transition-colors hover:bg-white/5 hover:text-[#efefef]"
                    @click="resetExpenseForm"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>

                <form @submit.prevent="submitExpense">
                  <!-- Title -->
                  <div class="mb-4">
                    <label class="mb-1.5 block text-sm font-medium text-[#b0b0b0]">Title</label>
                    <input
                      v-model="expenseForm.title"
                      type="text"
                      required
                      placeholder="Dinner, Groceries, Taxi..."
                      class="w-full rounded-xl border border-white/[0.06] bg-[#1e1e1e] px-4 py-3 text-sm text-[#efefef] placeholder-[#6a6a6a] outline-none transition-colors focus:border-[#e5fe40]/30 focus:ring-1 focus:ring-[#e5fe40]/20"
                    />
                  </div>

                  <!-- Amount -->
                  <div class="mb-5">
                    <label class="mb-1.5 block text-sm font-medium text-[#b0b0b0]">Amount</label>
                    <div class="relative">
                      <span class="absolute left-4 top-1/2 -translate-y-1/2 font-mono text-lg text-[#ffcb45]">&#8377;</span>
                      <input
                        v-model.number="expenseForm.amount"
                        type="number"
                        required
                        min="0.01"
                        step="0.01"
                        placeholder="0.00"
                        class="w-full rounded-xl border border-white/[0.06] bg-[#1e1e1e] py-3 pl-10 pr-4 font-mono text-2xl text-[#ffcb45] placeholder-[#6a6a6a]/50 outline-none transition-colors focus:border-[#e5fe40]/30 focus:ring-1 focus:ring-[#e5fe40]/20"
                      />
                    </div>
                  </div>

                  <!-- Split Type -->
                  <div class="mb-5">
                    <label class="mb-2 block text-sm font-medium text-[#b0b0b0]">Split Type</label>
                    <div class="flex gap-2">
                      <button
                        v-for="st in splitTypes"
                        :key="st.value"
                        type="button"
                        class="rounded-xl px-4 py-2 text-sm font-medium transition-all"
                        :class="
                          expenseForm.splitType === st.value
                            ? 'bg-[#e5fe40] text-[#0d0d0d] shadow-[0_3px_0_0_#b5cc30]'
                            : 'border border-white/[0.06] bg-[#1e1e1e] text-[#6a6a6a] hover:border-white/[0.1] hover:text-[#b0b0b0]'
                        "
                        @click="expenseForm.splitType = st.value"
                      >
                        {{ st.label }}
                      </button>
                    </div>
                  </div>

                  <!-- Member Selection -->
                  <div class="mb-5">
                    <label class="mb-2 block text-sm font-medium text-[#b0b0b0]">Split Between</label>
                    <div class="space-y-2">
                      <label
                        v-for="(member, mIndex) in group.members"
                        :key="member.id"
                        class="flex cursor-pointer items-center gap-3 rounded-xl border border-white/[0.06] bg-[#1e1e1e] p-3 transition-colors hover:border-white/[0.1]"
                        :class="{ 'border-[#e5fe40]/30 bg-[#e5fe40]/5': selectedMembers.includes(member.user_id) }"
                      >
                        <input
                          v-model="selectedMembers"
                          type="checkbox"
                          :value="member.user_id"
                          class="sr-only"
                        />
                        <div
                          class="flex h-5 w-5 items-center justify-center rounded-md border transition-colors"
                          :class="
                            selectedMembers.includes(member.user_id)
                              ? 'border-[#e5fe40] bg-[#e5fe40]'
                              : 'border-white/[0.12] bg-transparent'
                          "
                        >
                          <svg
                            v-if="selectedMembers.includes(member.user_id)"
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-3 w-3 text-[#0d0d0d]"
                            viewBox="0 0 20 20"
                            fill="currentColor"
                          >
                            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                          </svg>
                        </div>
                        <div
                          class="flex h-6 w-6 items-center justify-center rounded-full text-[9px] font-bold"
                          :class="avatarColor(mIndex)"
                        >
                          {{ memberInitial(member.user_id) }}
                        </div>
                        <span class="flex-1 text-sm text-[#efefef]">User {{ member.user_id }}</span>

                        <!-- Per-member input for exact / percentage -->
                        <input
                          v-if="expenseForm.splitType === 'exact' && selectedMembers.includes(member.user_id)"
                          v-model.number="memberAmounts[member.user_id]"
                          type="number"
                          min="0"
                          step="0.01"
                          placeholder="0.00"
                          class="w-24 rounded-lg border border-white/[0.06] bg-[#252525] px-3 py-1.5 text-right font-mono text-sm text-[#ffcb45] placeholder-[#6a6a6a]/50 outline-none focus:border-[#e5fe40]/30"
                          @click.stop
                        />
                        <input
                          v-if="expenseForm.splitType === 'percentage' && selectedMembers.includes(member.user_id)"
                          v-model.number="memberPercentages[member.user_id]"
                          type="number"
                          min="0"
                          max="100"
                          step="0.1"
                          placeholder="0%"
                          class="w-20 rounded-lg border border-white/[0.06] bg-[#252525] px-3 py-1.5 text-right font-mono text-sm text-[#b0b0b0] placeholder-[#6a6a6a]/50 outline-none focus:border-[#e5fe40]/30"
                          @click.stop
                        />
                      </label>
                    </div>
                  </div>

                  <!-- Validation hints for exact/percentage -->
                  <div v-if="expenseForm.splitType === 'exact' && selectedMembers.length > 0" class="mb-4">
                    <p class="text-xs" :class="exactTotal === expenseForm.amount ? 'text-[#3bffad]' : 'text-[#ee4d37]'">
                      Total: <span class="font-mono">{{ formatMoney(exactTotal) }}</span> / <span class="font-mono">{{ formatMoney(expenseForm.amount || 0) }}</span>
                      <span v-if="exactTotal === expenseForm.amount"> -- Balanced</span>
                    </p>
                  </div>
                  <div v-if="expenseForm.splitType === 'percentage' && selectedMembers.length > 0" class="mb-4">
                    <p class="text-xs" :class="percentageTotal === 100 ? 'text-[#3bffad]' : 'text-[#ee4d37]'">
                      Total: <span class="font-mono">{{ percentageTotal }}%</span> / <span class="font-mono">100%</span>
                      <span v-if="percentageTotal === 100"> -- Balanced</span>
                    </p>
                  </div>

                  <div class="flex gap-3">
                    <button
                      type="button"
                      class="flex-1 rounded-xl border border-white/[0.06] bg-[#1e1e1e] px-4 py-3 text-sm font-medium text-[#b0b0b0] transition-colors hover:bg-[#252525] hover:text-[#efefef]"
                      @click="resetExpenseForm"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      class="settl-btn-primary flex-1 text-sm"
                      :disabled="submittingExpense || !canSubmitExpense"
                    >
                      {{ submittingExpense ? 'Adding...' : 'Add Expense' }}
                    </button>
                  </div>

                  <p v-if="expenseError" class="mt-3 text-center text-sm text-[#ee4d37]">
                    {{ expenseError }}
                  </p>
                </form>
              </div>
            </Transition>

            <!-- Expense List -->
            <div v-if="loadingExpenses" class="space-y-3">
              <div v-for="n in 3" :key="n" class="settl-card animate-pulse p-4">
                <div class="flex items-center justify-between">
                  <div class="space-y-2">
                    <div class="h-4 w-32 rounded bg-white/[0.06]" />
                    <div class="h-3 w-24 rounded bg-white/[0.04]" />
                  </div>
                  <div class="h-6 w-20 rounded bg-white/[0.06]" />
                </div>
              </div>
            </div>

            <div v-else-if="expenses.length === 0" class="settl-card p-10 text-center">
              <div class="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-2xl bg-[#ffcb45]/10">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-[#ffcb45]" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M4 4a2 2 0 00-2 2v1h16V6a2 2 0 00-2-2H4z" />
                  <path fill-rule="evenodd" d="M18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9zM4 13a1 1 0 011-1h1a1 1 0 110 2H5a1 1 0 01-1-1zm5-1a1 1 0 100 2h1a1 1 0 100-2H9z" clip-rule="evenodd" />
                </svg>
              </div>
              <p class="text-sm text-[#6a6a6a]">No expenses yet. Add one to get started.</p>
            </div>

            <div v-else class="space-y-3">
              <div
                v-for="(expense, eIndex) in expenses"
                :key="expense.id"
                class="stagger-enter settl-card group p-4"
                :style="{ animationDelay: `${eIndex * 60}ms` }"
              >
                <div class="flex items-center justify-between">
                  <div class="min-w-0 flex-1">
                    <div class="flex items-center gap-2">
                      <h4 class="truncate text-sm font-semibold text-[#efefef]">{{ expense.title }}</h4>
                      <span class="shrink-0 rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase" :class="splitBadgeClass(expense.split_type)">
                        {{ expense.split_type }}
                      </span>
                    </div>
                    <p class="mt-0.5 text-xs text-[#6a6a6a]">
                      {{ formatDate(expense.created_at) }}
                      <span class="mx-1">--</span>
                      {{ expense.splits.length }} split{{ expense.splits.length !== 1 ? 's' : '' }}
                    </p>
                  </div>
                  <div class="flex items-center gap-3">
                    <span class="money text-lg">{{ formatMoney(expense.amount) }}</span>
                    <button
                      v-if="expense.created_by_id === authStore.user?.id"
                      class="rounded-lg p-1.5 text-[#6a6a6a] opacity-0 transition-all hover:bg-[#ee4d37]/10 hover:text-[#ee4d37] group-hover:opacity-100"
                      title="Delete expense"
                      @click.stop="deleteExpense(expense.id)"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                      </svg>
                    </button>
                  </div>
                </div>

                <!-- Expanded splits (click to toggle) -->
                <button
                  class="mt-2 text-xs text-[#6a6a6a] transition-colors hover:text-[#b0b0b0]"
                  @click="toggleExpense(expense.id)"
                >
                  {{ expandedExpenses.includes(expense.id) ? 'Hide splits' : 'View splits' }}
                </button>
                <Transition name="slide">
                  <div v-if="expandedExpenses.includes(expense.id)" class="mt-3 space-y-1.5 border-t border-white/[0.04] pt-3">
                    <div
                      v-for="split in expense.splits"
                      :key="split.id"
                      class="flex items-center justify-between rounded-lg bg-white/[0.02] px-3 py-2"
                    >
                      <span class="text-xs text-[#b0b0b0]">User {{ split.user_id }}</span>
                      <span class="font-mono text-xs text-[#ffcb45]">{{ formatMoney(split.amount) }}</span>
                    </div>
                  </div>
                </Transition>
              </div>
            </div>
          </div>

          <!-- ==================== BALANCES TAB ==================== -->
          <div v-else-if="activeTab === 'balances'">
            <!-- Balance List -->
            <div v-if="loadingBalances" class="space-y-3">
              <div v-for="n in 4" :key="n" class="settl-card animate-pulse p-4">
                <div class="flex items-center justify-between">
                  <div class="h-4 w-28 rounded bg-white/[0.06]" />
                  <div class="h-5 w-20 rounded bg-white/[0.06]" />
                </div>
              </div>
            </div>

            <template v-else>
              <div v-if="Object.keys(balances).length === 0" class="settl-card p-10 text-center">
                <div class="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-2xl bg-[#3bffad]/10">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-[#3bffad]" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                </div>
                <p class="text-sm text-[#6a6a6a]">All balanced. No outstanding amounts.</p>
              </div>

              <div v-else class="space-y-3">
                <div
                  v-for="(amount, userId, bIndex) in balances"
                  :key="userId"
                  class="stagger-enter settl-card flex items-center justify-between p-4"
                  :style="{ animationDelay: `${Number(bIndex) * 60}ms` }"
                >
                  <div class="flex items-center gap-3">
                    <div
                      class="flex h-8 w-8 items-center justify-center rounded-full text-[10px] font-bold"
                      :class="Number(amount) >= 0 ? 'bg-[#3bffad]/15 text-[#3bffad]' : 'bg-[#ee4d37]/15 text-[#ee4d37]'"
                    >
                      {{ memberInitial(Number(userId)) }}
                    </div>
                    <span class="text-sm text-[#efefef]">User {{ userId }}</span>
                  </div>
                  <span
                    class="font-mono text-base font-semibold"
                    :class="Number(amount) >= 0 ? 'text-[#3bffad]' : 'text-[#ee4d37]'"
                  >
                    {{ Number(amount) >= 0 ? '+' : '' }}{{ formatMoney(Number(amount)) }}
                  </span>
                </div>
              </div>

              <!-- Suggestions Section -->
              <div class="mt-8">
                <div class="mb-4 flex items-center justify-between">
                  <h3 class="font-serif text-lg text-[#efefef]">Settlement Suggestions</h3>
                  <button
                    class="settl-btn-primary px-4 py-2 text-xs"
                    :disabled="loadingSuggestions"
                    @click="fetchSuggestions"
                  >
                    {{ loadingSuggestions ? 'Loading...' : 'Get Suggestions' }}
                  </button>
                </div>

                <div v-if="suggestions.length === 0 && !loadingSuggestions" class="settl-card p-6 text-center">
                  <p class="text-sm text-[#6a6a6a]">Click "Get Suggestions" to see optimal settlement paths.</p>
                </div>

                <div v-else class="space-y-3">
                  <div
                    v-for="(suggestion, sIndex) in suggestions"
                    :key="sIndex"
                    class="stagger-enter settl-card flex items-center justify-between p-4"
                    :style="{ animationDelay: `${sIndex * 80}ms` }"
                  >
                    <div class="flex items-center gap-2">
                      <div class="flex h-7 w-7 items-center justify-center rounded-full bg-[#ee4d37]/15 text-[9px] font-bold text-[#ee4d37]">
                        {{ memberInitial(suggestion.from_user_id) }}
                      </div>
                      <span class="text-sm text-[#b0b0b0]">pays</span>
                      <div class="flex h-7 w-7 items-center justify-center rounded-full bg-[#3bffad]/15 text-[9px] font-bold text-[#3bffad]">
                        {{ memberInitial(suggestion.to_user_id) }}
                      </div>
                    </div>
                    <div class="flex items-center gap-3">
                      <span class="money text-base">{{ formatMoney(suggestion.amount) }}</span>
                      <button
                        class="rounded-lg bg-[#3bffad]/10 px-3 py-1.5 text-xs font-semibold text-[#3bffad] transition-colors hover:bg-[#3bffad]/20"
                        @click="settleUp(suggestion)"
                      >
                        Settle
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </template>
          </div>

          <!-- ==================== MEMBERS TAB ==================== -->
          <div v-else-if="activeTab === 'members'">
            <div class="mb-6 space-y-3">
              <div
                v-for="(member, mIndex) in group.members"
                :key="member.id"
                class="stagger-enter settl-card flex items-center gap-4 p-4"
                :style="{ animationDelay: `${mIndex * 60}ms` }"
              >
                <div
                  class="flex h-10 w-10 items-center justify-center rounded-full text-sm font-bold"
                  :class="avatarColor(mIndex)"
                >
                  {{ memberInitial(member.user_id) }}
                </div>
                <div class="flex-1">
                  <p class="text-sm font-medium text-[#efefef]">User {{ member.user_id }}</p>
                  <p class="text-xs text-[#6a6a6a]">
                    Joined {{ member.joined_at ? formatDate(member.joined_at) : 'recently' }}
                  </p>
                </div>
                <span
                  v-if="member.is_admin"
                  class="rounded-full bg-[#e5fe40]/15 px-2.5 py-1 text-[10px] font-semibold text-[#e5fe40]"
                >
                  Admin
                </span>
              </div>
            </div>

            <!-- Invite Form -->
            <div class="settl-card p-5">
              <h3 class="mb-4 font-serif text-lg text-[#efefef]">Invite Member</h3>
              <form class="flex gap-3" @submit.prevent="inviteMember">
                <input
                  v-model.number="inviteUserId"
                  type="number"
                  min="1"
                  required
                  placeholder="User ID"
                  class="flex-1 rounded-xl border border-white/[0.06] bg-[#1e1e1e] px-4 py-3 text-sm text-[#efefef] placeholder-[#6a6a6a] outline-none transition-colors focus:border-[#e5fe40]/30 focus:ring-1 focus:ring-[#e5fe40]/20"
                />
                <button
                  type="submit"
                  class="settl-btn-primary shrink-0 px-5 py-3 text-sm"
                  :disabled="inviting"
                >
                  {{ inviting ? 'Inviting...' : 'Invite' }}
                </button>
              </form>
              <p v-if="inviteError" class="mt-2 text-sm text-[#ee4d37]">{{ inviteError }}</p>
              <p v-if="inviteSuccess" class="mt-2 text-sm text-[#3bffad]">{{ inviteSuccess }}</p>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Expense, Group } from '~/types'

definePageMeta({ middleware: 'auth' })

const route = useRoute()
const api = useApi()
const authStore = useAuthStore()
const groupId = route.params.id as string

// ── Group State ──
const group = ref<Group | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

// ── Tabs ──
const tabs = [
  { key: 'expenses', label: 'Expenses' },
  { key: 'balances', label: 'Balances' },
  { key: 'members', label: 'Members' },
] as const
type TabKey = (typeof tabs)[number]['key']
const activeTab = ref<TabKey>('expenses')

// ── Expenses State ──
const expenses = ref<Expense[]>([])
const loadingExpenses = ref(false)
const expandedExpenses = ref<number[]>([])
const showExpenseForm = ref(false)
const submittingExpense = ref(false)
const expenseError = ref<string | null>(null)

const splitTypes = [
  { value: 'equal', label: 'Equal' },
  { value: 'exact', label: 'Exact' },
  { value: 'percentage', label: 'Percentage' },
]

const expenseForm = ref({
  title: '',
  amount: null as number | null,
  splitType: 'equal',
})

const selectedMembers = ref<number[]>([])
const memberAmounts = ref<Record<number, number>>({})
const memberPercentages = ref<Record<number, number>>({})

const exactTotal = computed(() => {
  return selectedMembers.value.reduce((sum, uid) => sum + (memberAmounts.value[uid] || 0), 0)
})

const percentageTotal = computed(() => {
  return selectedMembers.value.reduce((sum, uid) => sum + (memberPercentages.value[uid] || 0), 0)
})

const canSubmitExpense = computed(() => {
  if (!expenseForm.value.title || !expenseForm.value.amount || selectedMembers.value.length === 0) return false
  if (expenseForm.value.splitType === 'exact' && exactTotal.value !== expenseForm.value.amount) return false
  if (expenseForm.value.splitType === 'percentage' && percentageTotal.value !== 100) return false
  return true
})

// ── Balances State ──
const balances = ref<Record<string, number>>({})
const loadingBalances = ref(false)

// ── Suggestions State ──
interface Suggestion {
  from_user_id: number
  to_user_id: number
  amount: number
}
const suggestions = ref<Suggestion[]>([])
const loadingSuggestions = ref(false)

// ── Members State ──
const inviteUserId = ref<number | null>(null)
const inviting = ref(false)
const inviteError = ref<string | null>(null)
const inviteSuccess = ref<string | null>(null)

// ── Helpers ──
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

function formatMoney(amount: number) {
  return new Intl.NumberFormat('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(amount)
}

function formatDate(dateStr: string | null) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
}

function splitBadgeClass(splitType: string) {
  switch (splitType) {
    case 'equal': return 'bg-[#3bffad]/15 text-[#3bffad]'
    case 'exact': return 'bg-[#ffcb45]/15 text-[#ffcb45]'
    case 'percentage': return 'bg-[#6a35ff]/15 text-[#6a35ff]'
    default: return 'bg-white/10 text-[#b0b0b0]'
  }
}

function toggleExpense(id: number) {
  const idx = expandedExpenses.value.indexOf(id)
  if (idx === -1) expandedExpenses.value.push(id)
  else expandedExpenses.value.splice(idx, 1)
}

// ── API Calls ──
async function fetchGroup() {
  loading.value = true
  error.value = null
  try {
    group.value = await api.get<Group>(`/v1/groups/${groupId}`)
    // Pre-select all members for expense splitting
    if (group.value) {
      selectedMembers.value = group.value.members.map(m => m.user_id)
    }
  }
  catch (e: any) {
    error.value = e?.data?.detail || e?.message || 'Failed to load group'
  }
  finally {
    loading.value = false
  }
}

async function fetchExpenses() {
  loadingExpenses.value = true
  try {
    expenses.value = await api.get<Expense[]>(`/v1/expenses/group/${groupId}`)
  }
  catch {
    // Silently handle -- expenses section will just be empty
  }
  finally {
    loadingExpenses.value = false
  }
}

async function fetchBalances() {
  loadingBalances.value = true
  try {
    balances.value = await api.get<Record<string, number>>(`/v1/settlements/group/${groupId}/balances`)
  }
  catch {
    balances.value = {}
  }
  finally {
    loadingBalances.value = false
  }
}

async function fetchSuggestions() {
  loadingSuggestions.value = true
  try {
    suggestions.value = await api.get<Suggestion[]>(`/v1/settlements/group/${groupId}/suggestions`)
  }
  catch {
    suggestions.value = []
  }
  finally {
    loadingSuggestions.value = false
  }
}

function resetExpenseForm() {
  showExpenseForm.value = false
  expenseError.value = null
  expenseForm.value = { title: '', amount: null, splitType: 'equal' }
  memberAmounts.value = {}
  memberPercentages.value = {}
  if (group.value) {
    selectedMembers.value = group.value.members.map(m => m.user_id)
  }
}

async function submitExpense() {
  if (!canSubmitExpense.value) return
  submittingExpense.value = true
  expenseError.value = null

  try {
    // Build splits payload based on split type
    let splits: { user_id: number; amount?: number; percentage?: number }[] = []

    if (expenseForm.value.splitType === 'equal') {
      const perPerson = (expenseForm.value.amount || 0) / selectedMembers.value.length
      splits = selectedMembers.value.map(uid => ({ user_id: uid, amount: perPerson }))
    }
    else if (expenseForm.value.splitType === 'exact') {
      splits = selectedMembers.value.map(uid => ({ user_id: uid, amount: memberAmounts.value[uid] || 0 }))
    }
    else if (expenseForm.value.splitType === 'percentage') {
      splits = selectedMembers.value.map(uid => ({
        user_id: uid,
        percentage: memberPercentages.value[uid] || 0,
        amount: ((memberPercentages.value[uid] || 0) / 100) * (expenseForm.value.amount || 0),
      }))
    }

    const body = {
      title: expenseForm.value.title,
      amount: expenseForm.value.amount,
      split_type: expenseForm.value.splitType,
      group_id: Number(groupId),
      splits,
    }

    const created = await api.post<Expense>('/v1/expenses/', body)
    expenses.value.unshift(created)
    resetExpenseForm()
  }
  catch (e: any) {
    expenseError.value = e?.data?.detail || e?.message || 'Failed to add expense'
  }
  finally {
    submittingExpense.value = false
  }
}

async function deleteExpense(expenseId: number) {
  try {
    await api.del(`/v1/expenses/${expenseId}`)
    expenses.value = expenses.value.filter(e => e.id !== expenseId)
  }
  catch {
    // Could show a toast here
  }
}

async function settleUp(suggestion: Suggestion) {
  try {
    await api.post('/v1/settlements/', {
      payer_id: suggestion.from_user_id,
      payee_id: suggestion.to_user_id,
      amount: suggestion.amount,
      group_id: Number(groupId),
    })
    // Refresh balances and suggestions
    await Promise.all([fetchBalances(), fetchSuggestions()])
  }
  catch {
    // Could show a toast here
  }
}

async function inviteMember() {
  if (!inviteUserId.value) return
  inviting.value = true
  inviteError.value = null
  inviteSuccess.value = null

  try {
    await api.post(`/v1/groups/${groupId}/members`, { user_id: inviteUserId.value })
    inviteSuccess.value = `User ${inviteUserId.value} added to the group`
    inviteUserId.value = null
    // Refresh group data
    await fetchGroup()
  }
  catch (e: any) {
    inviteError.value = e?.data?.detail || e?.message || 'Failed to invite member'
  }
  finally {
    inviting.value = false
  }
}

// ── Watchers ──
watch(activeTab, (tab) => {
  if (tab === 'balances') {
    fetchBalances()
  }
})

// ── Init ──
onMounted(async () => {
  await fetchGroup()
  if (!error.value) {
    fetchExpenses()
  }
})
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: all 0.25s ease-out;
  overflow: hidden;
}

.slide-enter-from {
  opacity: 0;
  max-height: 0;
  transform: translateY(-8px);
}

.slide-enter-to {
  opacity: 1;
  max-height: 800px;
}

.slide-leave-from {
  opacity: 1;
  max-height: 800px;
}

.slide-leave-to {
  opacity: 0;
  max-height: 0;
  transform: translateY(-8px);
}
</style>
