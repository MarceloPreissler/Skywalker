import {
  Box,
  Divider,
  Drawer,
  IconButton,
  List,
  ListItem,
  ListItemText,
  Typography,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import BoltIcon from '@mui/icons-material/Bolt';

import { Plan, Provider } from '../types';

interface Props {
  open: boolean;
  onClose: () => void;
  plans: Plan[];
  providers: Provider[];
  benchmarkRate: number;
}

export const ComparisonDrawer = ({ open, onClose, plans, providers, benchmarkRate }: Props) => {
  const providerLookup = Object.fromEntries(
    providers.map((provider) => [provider.id, provider])
  );

  return (
    <Drawer anchor="right" open={open} onClose={onClose} keepMounted>
      <Box width={{ xs: 320, sm: 420 }} role="presentation" display="flex" flexDirection="column" height="100%">
        <Box display="flex" alignItems="center" justifyContent="space-between" p={2}>
          <Typography variant="h6">Plan Comparison</Typography>
          <IconButton onClick={onClose}>
            <CloseIcon />
          </IconButton>
        </Box>
        <Divider />
        <Box px={2} py={1} display="flex" alignItems="center" gap={1}>
          <BoltIcon color="primary" />
          <Typography variant="body2">
            TXU benchmark: {benchmarkRate.toFixed(2)} ¢/kWh
          </Typography>
        </Box>
        <Divider />
        <List sx={{ flexGrow: 1, overflowY: 'auto' }}>
          {plans.map((plan) => {
            const provider = providerLookup[plan.provider_id];
            return (
              <ListItem key={plan.id} alignItems="flex-start">
                <ListItemText
                  primary={`${plan.name} — ${provider?.name ?? ''}`}
                  secondary={
                    <>
                      <Typography component="span" variant="body2" color="text.primary">
                        {plan.rate_cents_kwh?.toFixed(2)} ¢/kWh · {plan.term_months} months
                      </Typography>
                      <br />
                      <Typography component="span" variant="caption" color="text.secondary">
                        Base fee ${plan.base_fee?.toFixed(2)} · Renewable {plan.renewable_percentage}%
                      </Typography>
                    </>
                  }
                />
              </ListItem>
            );
          })}
        </List>
      </Box>
    </Drawer>
  );
};
