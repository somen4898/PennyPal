export interface User {
  id: number
  email: string
  username: string
  full_name: string
  is_active: boolean
  created_at: string | null
  updated_at: string | null
}

export interface Group {
  id: number
  name: string
  description: string | null
  created_by_id: number
  created_at: string | null
  updated_at: string | null
  members: GroupMember[]
}

export interface GroupMember {
  id: number
  user_id: number
  group_id: number
  is_admin: boolean
  joined_at: string | null
}

export interface Expense {
  id: number
  title: string
  description: string | null
  amount: number
  currency: string
  split_type: string
  group_id: number
  created_by_id: number
  created_at: string | null
  updated_at: string | null
  splits: ExpenseSplit[]
}

export interface ExpenseSplit {
  id: number
  expense_id: number
  user_id: number
  amount: number
  percentage: number | null
  created_at: string | null
}

export interface Settlement {
  id: number
  payer_id: number
  payee_id: number
  amount: number
  currency: string
  status: string
  description: string | null
  group_id: number | null
  settled_at: string | null
  created_at: string | null
  updated_at: string | null
}

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}
