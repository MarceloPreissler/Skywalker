import { useCallback, useEffect, useMemo, useState } from 'react';
import axios from 'axios';

import { Plan, Provider } from '../types';

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';

export interface Filters {
  providerIds: number[];
  terms: number[];
  renewableOnly: boolean;
  maxRate?: number;
}

export const usePlans = () => {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [providers, setProviders] = useState<Provider[]>([]);
  const [filters, setFilters] = useState<Filters>({
    providerIds: [],
    terms: [],
    renewableOnly: false,
  });
  const [selectedPlans, setSelectedPlans] = useState<number[]>([]);
  const [loading, setLoading] = useState(false);

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const [plansRes, providersRes] = await Promise.all([
        axios.get<Plan[]>(`${API_BASE}/plans`),
        axios.get<Provider[]>(`${API_BASE}/providers`),
      ]);
      setPlans(plansRes.data);
      setProviders(providersRes.data);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const filteredPlans = useMemo(() => {
    return plans.filter((plan) => {
      if (filters.providerIds.length && !filters.providerIds.includes(plan.provider_id)) {
        return false;
      }
      if (filters.terms.length && plan.term_months && !filters.terms.includes(plan.term_months)) {
        return false;
      }
      if (filters.renewableOnly && (plan.renewable_percentage ?? 0) < 50) {
        return false;
      }
      if (filters.maxRate && plan.rate_cents_kwh && plan.rate_cents_kwh > filters.maxRate) {
        return false;
      }
      return true;
    });
  }, [plans, filters]);

  return {
    plans: filteredPlans,
    providers,
    filters,
    setFilters,
    selectedPlans,
    setSelectedPlans,
    loading,
    reload: loadData,
  };
};
