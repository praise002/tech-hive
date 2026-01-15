export interface SubscriptionPlan {
  id: string;
  name: string;
  description: string;
  price: string;
  billing_cycle: 'MONTHLY' | 'YEARLY';
  features: Record<string, any>;
}

export interface Subscription {
  id: string;
  status:
    | 'TRIALING'
    | 'ACTIVE'
    | 'PAST_DUE'
    | 'CANCELLED'
    | 'EXPIRED'
    | 'UNPAID';
  plan: SubscriptionPlan;
  is_premium: boolean;
  is_trial: boolean;
  trial_start: string | null;
  trial_end: string | null;
  current_period_start: string | null;
  current_period_end: string | null;
  next_billing_date: string | null;
  days_remaining: number;
  cancelled_at: string | null;
  cancel_at_period_end: boolean;
  is_in_grace_period: boolean;
  grace_period_ends_at: string | null;
  card_details: {
    last4: string;
    type: string;
    bank: string;
  } | null;
}

export interface PaymentTransaction {
  id: string;
  reference: string;
  amount: string;
  status: 'PENDING' | 'SUCCESS' | 'FAILED';
  transaction_type: 'SUBSCRIPTION' | 'RENEWAL';
  initiated_at: string;
  paid_at: string | null;
  failed_at: string | null;
  failure_reason: string | null;
}

export interface SubscribeRequest {
  plan_id: string;
  start_trial: boolean;
}

export interface SubscribeResponse {
  authorization_url?: string;
  status?: string;
  trial_end?: string;
}

export interface CancelRequest {
  reason?: string;
}

export interface CancelResponse {
  access_until: string;
}
