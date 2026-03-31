export interface ValidationRule {
  test: (value: string) => boolean
  message: string
}

export interface FieldValidation {
  valid: boolean
  errors: string[]
  dirty: boolean
}

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const usernameRegex = /^[a-zA-Z0-9_-]+$/

export const passwordRules: ValidationRule[] = [
  { test: (v) => v.length >= 8, message: 'At least 8 characters' },
  { test: (v) => v.length <= 128, message: 'At most 128 characters' },
  { test: (v) => /[A-Z]/.test(v), message: 'One uppercase letter' },
  { test: (v) => /[a-z]/.test(v), message: 'One lowercase letter' },
  { test: (v) => /[0-9]/.test(v), message: 'One number' },
]

export const usernameRules: ValidationRule[] = [
  { test: (v) => v.length >= 3, message: 'At least 3 characters' },
  { test: (v) => v.length <= 30, message: 'At most 30 characters' },
  { test: (v) => usernameRegex.test(v), message: 'Only letters, numbers, underscores, hyphens' },
]

export const emailRules: ValidationRule[] = [
  { test: (v) => v.length > 0, message: 'Email is required' },
  { test: (v) => emailRegex.test(v), message: 'Must be a valid email' },
]

export const fullNameRules: ValidationRule[] = [
  { test: (v) => v.trim().length >= 1, message: 'Full name is required' },
  { test: (v) => v.length <= 100, message: 'At most 100 characters' },
]

export function validateField(value: string, rules: ValidationRule[]): Omit<FieldValidation, 'dirty'> {
  const errors = rules.filter((r) => !r.test(value)).map((r) => r.message)
  return { valid: errors.length === 0, errors }
}

export function useFieldValidation(rules: ValidationRule[]) {
  const value = ref('')
  const dirty = ref(false)

  const validation = computed(() => {
    const result = validateField(value.value, rules)
    return { ...result, dirty: dirty.value }
  })

  function touch() {
    dirty.value = true
  }

  return { value, dirty, validation, touch }
}
