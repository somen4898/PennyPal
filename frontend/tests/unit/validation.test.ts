import { describe, it, expect } from 'vitest'
import {
  validateField,
  passwordRules,
  usernameRules,
  emailRules,
  fullNameRules,
} from '~/composables/useValidation'

describe('password validation', () => {
  it('rejects passwords shorter than 8 characters', () => {
    const result = validateField('Ab1', passwordRules)
    expect(result.valid).toBe(false)
    expect(result.errors).toContain('At least 8 characters')
  })

  it('rejects passwords without uppercase', () => {
    const result = validateField('abcdefg1', passwordRules)
    expect(result.valid).toBe(false)
    expect(result.errors).toContain('One uppercase letter')
  })

  it('rejects passwords without lowercase', () => {
    const result = validateField('ABCDEFG1', passwordRules)
    expect(result.valid).toBe(false)
    expect(result.errors).toContain('One lowercase letter')
  })

  it('rejects passwords without a number', () => {
    const result = validateField('Abcdefgh', passwordRules)
    expect(result.valid).toBe(false)
    expect(result.errors).toContain('One number')
  })

  it('accepts valid passwords', () => {
    const result = validateField('Abcdefg1', passwordRules)
    expect(result.valid).toBe(true)
    expect(result.errors).toHaveLength(0)
  })

  it('rejects empty passwords with all errors', () => {
    const result = validateField('', passwordRules)
    expect(result.valid).toBe(false)
    expect(result.errors).toHaveLength(4)
  })
})

describe('username validation', () => {
  it('rejects usernames shorter than 3 characters', () => {
    const result = validateField('ab', usernameRules)
    expect(result.valid).toBe(false)
    expect(result.errors).toContain('At least 3 characters')
  })

  it('rejects usernames longer than 30 characters', () => {
    const result = validateField('a'.repeat(31), usernameRules)
    expect(result.valid).toBe(false)
    expect(result.errors).toContain('At most 30 characters')
  })

  it('rejects usernames with spaces', () => {
    const result = validateField('bad name', usernameRules)
    expect(result.valid).toBe(false)
    expect(result.errors).toContain('Only letters, numbers, underscores, hyphens')
  })

  it('rejects usernames with special characters', () => {
    const result = validateField('user@name!', usernameRules)
    expect(result.valid).toBe(false)
  })

  it('accepts valid usernames with letters, numbers, underscores, hyphens', () => {
    expect(validateField('john_doe', usernameRules).valid).toBe(true)
    expect(validateField('user-123', usernameRules).valid).toBe(true)
    expect(validateField('ABC', usernameRules).valid).toBe(true)
  })
})

describe('email validation', () => {
  it('rejects empty email', () => {
    const result = validateField('', emailRules)
    expect(result.valid).toBe(false)
  })

  it('rejects invalid email format', () => {
    expect(validateField('notanemail', emailRules).valid).toBe(false)
    expect(validateField('missing@domain', emailRules).valid).toBe(false)
    expect(validateField('@no-local.com', emailRules).valid).toBe(false)
  })

  it('accepts valid emails', () => {
    expect(validateField('user@example.com', emailRules).valid).toBe(true)
    expect(validateField('test.user@domain.co', emailRules).valid).toBe(true)
  })
})

describe('full name validation', () => {
  it('rejects empty full name', () => {
    const result = validateField('', fullNameRules)
    expect(result.valid).toBe(false)
  })

  it('rejects whitespace-only full name', () => {
    const result = validateField('   ', fullNameRules)
    expect(result.valid).toBe(false)
  })

  it('rejects names longer than 100 characters', () => {
    const result = validateField('A'.repeat(101), fullNameRules)
    expect(result.valid).toBe(false)
  })

  it('accepts valid full names', () => {
    expect(validateField('John Doe', fullNameRules).valid).toBe(true)
    expect(validateField('A', fullNameRules).valid).toBe(true)
  })
})
