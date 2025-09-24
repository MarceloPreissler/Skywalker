import { useMemo, useState } from 'react';
import {
  AppBar,
  Box,
  Button,
  Container,
  CssBaseline,
  Toolbar,
  Typography,
} from '@mui/material';
import CompareIcon from '@mui/icons-material/Compare';

import { PlanTable } from './components/PlanTable';
import { FiltersPanel } from './components/Filters';
import { ComparisonDrawer } from './components/ComparisonDrawer';
import { PlanDetailsModal } from './components/PlanDetailsModal';
import { RateChart } from './components/RateChart';
import { usePlans } from './hooks/usePlans';
import { Plan } from './types';

const getBenchmarkRate = (plans: Plan[], benchmarkProviderSlug = 'txu') => {
  const txuPlans = plans.filter((plan) => plan.provider?.slug === benchmarkProviderSlug);
  if (!txuPlans.length) {
    return 1100;
  }
  const average =
    txuPlans.reduce((sum, plan) => sum + (plan.rate_cents_kwh ?? 0), 0) / txuPlans.length;
  return average;
};

export const App = () => {
  const {
    plans,
    providers,
    filters,
    setFilters,
    selectedPlans,
    setSelectedPlans,
    loading,
  } = usePlans();
  const [details, setDetails] = useState<Plan | null>(null);
  const [comparisonOpen, setComparisonOpen] = useState(false);

  const selectedPlanObjects = useMemo(
    () => plans.filter((plan) => selectedPlans.includes(plan.id)),
    [plans, selectedPlans]
  );

  const benchmarkRate = useMemo(() => getBenchmarkRate(plans), [plans]);

  const selectedProvider = providers.find((provider) => provider.id === details?.provider_id);

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <CssBaseline />
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Energy Plan Intelligence Dashboard
          </Typography>
          <Button
            color="inherit"
            startIcon={<CompareIcon />}
            onClick={() => setComparisonOpen(true)}
            disabled={!selectedPlans.length}
          >
            Compare ({selectedPlans.length})
          </Button>
        </Toolbar>
      </AppBar>

      <Container sx={{ py: 4, flexGrow: 1 }}>
        <Box display="flex" flexDirection="column" gap={3}>
          <FiltersPanel providers={providers} filters={filters} onChange={setFilters} />

          <PlanTable
            plans={plans}
            providers={providers}
            selectedPlans={selectedPlans}
            onToggleSelect={(id) =>
              setSelectedPlans((current) =>
                current.includes(id)
                  ? current.filter((planId) => planId !== id)
                  : [...current, id]
              )
            }
            onShowDetails={setDetails}
            loading={loading}
          />

          {!!plans.length && <RateChart plans={plans.slice(0, 5)} benchmarkRate={benchmarkRate} />}
        </Box>
      </Container>

      <ComparisonDrawer
        open={comparisonOpen}
        onClose={() => setComparisonOpen(false)}
        plans={selectedPlanObjects}
        providers={providers}
        benchmarkRate={benchmarkRate}
      />

      <PlanDetailsModal plan={details} provider={selectedProvider} onClose={() => setDetails(null)} />
    </Box>
  );
};

export default App;
