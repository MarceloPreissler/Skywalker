import { Card, CardContent, Typography } from '@mui/material';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Legend,
  Tooltip,
} from 'chart.js';
import { Plan } from '../types';

ChartJS.register(CategoryScale, LinearScale, BarElement, Legend, Tooltip);

interface Props {
  plans: Plan[];
  benchmarkRate: number;
}

export const RateChart = ({ plans, benchmarkRate }: Props) => {
  const labels = plans.map((plan) => plan.name);
  const data = {
    labels,
    datasets: [
      {
        label: 'Rate (¢/kWh)',
        data: plans.map((plan) => plan.rate_cents_kwh ?? 0),
        backgroundColor: 'rgba(25, 118, 210, 0.6)',
      },
      {
        label: 'TXU Benchmark',
        data: plans.map(() => benchmarkRate),
        backgroundColor: 'rgba(0, 150, 136, 0.4)',
      },
    ],
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Rate Comparison
        </Typography>
        <Bar data={data} />
      </CardContent>
    </Card>
  );
};
