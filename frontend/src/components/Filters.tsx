import {
  Box,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  SelectChangeEvent,
  Slider,
  Switch,
  Typography,
} from '@mui/material';
import { Provider } from '../types';
import { Filters } from '../hooks/usePlans';

interface Props {
  providers: Provider[];
  filters: Filters;
  onChange: (filters: Filters) => void;
}

const termOptions = [6, 12, 24, 36];

export const FiltersPanel = ({ providers, filters, onChange }: Props) => {
  const handleProviderChange = (event: SelectChangeEvent<number[]>) => {
    const value = event.target.value as unknown as number[];
    onChange({ ...filters, providerIds: value });
  };

  const handleTermChange = (event: SelectChangeEvent<number[]>) => {
    const value = event.target.value as unknown as number[];
    onChange({ ...filters, terms: value });
  };

  return (
    <Box display="flex" flexWrap="wrap" gap={2} alignItems="center">
      <FormControl sx={{ minWidth: 160 }} size="small">
        <InputLabel id="provider-filter">Providers</InputLabel>
        <Select
          labelId="provider-filter"
          multiple
          value={filters.providerIds}
          label="Providers"
          onChange={handleProviderChange}
          renderValue={(selected) =>
            selected
              .map((id) => providers.find((p) => p.id === id)?.name ?? id)
              .join(', ')
          }
        >
          {providers.map((provider) => (
            <MenuItem key={provider.id} value={provider.id}>
              {provider.name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <FormControl sx={{ minWidth: 160 }} size="small">
        <InputLabel id="term-filter">Term</InputLabel>
        <Select
          labelId="term-filter"
          multiple
          value={filters.terms}
          label="Term"
          onChange={handleTermChange}
        >
          {termOptions.map((term) => (
            <MenuItem key={term} value={term}>
              {term} months
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      <Box display="flex" alignItems="center" gap={1}>
        <Switch
          checked={filters.renewableOnly}
          onChange={(event) =>
            onChange({ ...filters, renewableOnly: event.target.checked })
          }
        />
        <Typography variant="body2">50%+ renewable</Typography>
      </Box>

      <Box flexGrow={1} minWidth={200}>
        <Typography gutterBottom variant="body2">
          Max Rate (¢/kWh)
        </Typography>
        <Slider
          min={800}
          max={2000}
          step={50}
          value={filters.maxRate ?? 2000}
          onChange={(_, value) =>
            onChange({ ...filters, maxRate: value as number })
          }
          valueLabelDisplay="auto"
        />
      </Box>
    </Box>
  );
};
