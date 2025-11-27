export interface Plan {
  id: number;
  provider_id: number;
  name: string;
  term_months?: number;
  rate_cents_kwh?: number;
  base_fee?: number;
  cancellation_fee?: number;
  renewable_percentage?: number;
  features?: string;
  url?: string;
  last_scraped_at: string;
  estimated_savings_vs_txu?: number;
  provider?: Provider;
}

export interface Provider {
  id: number;
  name: string;
  slug: string;
  website?: string;
}

export interface ApiResponse<T> {
  data: T;
}
