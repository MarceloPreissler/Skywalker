import {
  Box,
  Dialog,
  DialogContent,
  DialogTitle,
  Link,
  Typography,
} from '@mui/material';
import { Plan, Provider } from '../types';

interface Props {
  plan: Plan | null;
  provider?: Provider;
  onClose: () => void;
}

export const PlanDetailsModal = ({ plan, provider, onClose }: Props) => {
  return (
    <Dialog open={Boolean(plan)} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>{plan?.name}</DialogTitle>
      <DialogContent dividers>
        {plan && (
          <Box display="flex" flexDirection="column" gap={2}>
            <Typography variant="subtitle1">Provider: {provider?.name}</Typography>
            <Typography variant="body2">
              Rate: {plan.rate_cents_kwh?.toFixed(2)} ¢/kWh | Term: {plan.term_months} months
            </Typography>
            <Typography variant="body2">
              Base fee: ${plan.base_fee?.toFixed(2)} | Cancellation fee: ${plan.cancellation_fee?.toFixed(2)}
            </Typography>
            <Typography variant="body2">
              Renewable content: {plan.renewable_percentage}%
            </Typography>
            {plan.features && (
              <Typography variant="body2">Features: {plan.features}</Typography>
            )}
            {plan.url && (
              <Link href={plan.url} target="_blank" rel="noopener">
                View official plan details
              </Link>
            )}
          </Box>
        )}
      </DialogContent>
    </Dialog>
  );
};
