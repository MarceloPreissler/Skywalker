import {
  Box,
  Checkbox,
  CircularProgress,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tooltip,
} from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';
import { Plan, Provider } from '../types';

interface Props {
  plans: Plan[];
  providers: Provider[];
  selectedPlans: number[];
  onToggleSelect: (id: number) => void;
  onShowDetails: (plan: Plan) => void;
  loading?: boolean;
}

export const PlanTable = ({
  plans,
  providers,
  selectedPlans,
  onToggleSelect,
  onShowDetails,
  loading = false,
}: Props) => {
  const providerLookup = Object.fromEntries(
    providers.map((provider) => [provider.id, provider.name])
  );

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight={200}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <TableContainer sx={{ maxHeight: 500 }}>
      <Table stickyHeader size="small">
        <TableHead>
          <TableRow>
            <TableCell>Select</TableCell>
            <TableCell>Plan</TableCell>
            <TableCell>Provider</TableCell>
            <TableCell align="right">Term (months)</TableCell>
            <TableCell align="right">Rate (¢/kWh)</TableCell>
            <TableCell align="right">Base Fee ($)</TableCell>
            <TableCell align="right">Renewable %</TableCell>
            <TableCell align="right">Estimated savings vs TXU ($/mo)</TableCell>
            <TableCell>Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {plans.map((plan) => (
            <TableRow hover key={plan.id}>
              <TableCell padding="checkbox">
                <Checkbox
                  color="primary"
                  checked={selectedPlans.includes(plan.id)}
                  onChange={() => onToggleSelect(plan.id)}
                  inputProps={{ 'aria-label': `Select ${plan.name}` }}
                />
              </TableCell>
              <TableCell>{plan.name}</TableCell>
              <TableCell>{providerLookup[plan.provider_id]}</TableCell>
              <TableCell align="right">{plan.term_months ?? '—'}</TableCell>
              <TableCell align="right">{plan.rate_cents_kwh?.toFixed(2)}</TableCell>
              <TableCell align="right">{plan.base_fee?.toFixed(2)}</TableCell>
              <TableCell align="right">{plan.renewable_percentage ?? '—'}</TableCell>
              <TableCell align="right">
                {plan.estimated_savings_vs_txu != null
                  ? `${plan.estimated_savings_vs_txu < 0 ? '-' : ''}$${Math.abs(
                      plan.estimated_savings_vs_txu
                    ).toFixed(2)}`
                  : '—'}
              </TableCell>
              <TableCell>
                <Tooltip title="View details">
                  <IconButton size="small" onClick={() => onShowDetails(plan)}>
                    <InfoIcon fontSize="small" />
                  </IconButton>
                </Tooltip>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
