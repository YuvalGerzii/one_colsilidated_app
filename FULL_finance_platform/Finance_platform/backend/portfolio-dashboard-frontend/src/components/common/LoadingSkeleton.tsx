// src/components/common/LoadingSkeleton.tsx
import React from 'react';
import { Box, Card, CardContent, Skeleton, Grid, Stack } from '@mui/material';

export const KPICardSkeleton: React.FC = () => (
  <Card>
    <CardContent>
      <Skeleton variant="text" width="60%" height={20} />
      <Skeleton variant="text" width="80%" height={48} sx={{ mt: 1 }} />
      <Skeleton variant="text" width="40%" height={16} sx={{ mt: 0.5 }} />
    </CardContent>
  </Card>
);

export const TableSkeleton: React.FC<{ rows?: number }> = ({ rows = 5 }) => (
  <Stack spacing={1}>
    {Array.from({ length: rows }).map((_, index) => (
      <Skeleton key={index} variant="rectangular" height={52} />
    ))}
  </Stack>
);

export const ChartSkeleton: React.FC<{ height?: number }> = ({ height = 300 }) => (
  <Card>
    <CardContent>
      <Skeleton variant="text" width="40%" height={28} sx={{ mb: 2 }} />
      <Skeleton variant="rectangular" height={height} />
    </CardContent>
  </Card>
);

export const DashboardSkeleton: React.FC = () => (
  <Stack spacing={3}>
    <Box>
      <Skeleton variant="text" width="30%" height={48} />
      <Skeleton variant="text" width="50%" height={24} sx={{ mt: 1 }} />
    </Box>

    <Grid container spacing={3}>
      {[1, 2, 3, 4].map((item) => (
        <Grid item xs={12} md={3} key={item}>
          <KPICardSkeleton />
        </Grid>
      ))}
    </Grid>

    <Grid container spacing={3}>
      <Grid item xs={12} md={8}>
        <ChartSkeleton />
      </Grid>
      <Grid item xs={12} md={4}>
        <ChartSkeleton />
      </Grid>
    </Grid>
  </Stack>
);

export const FormSkeleton: React.FC<{ fields?: number }> = ({ fields = 5 }) => (
  <Stack spacing={3}>
    {Array.from({ length: fields }).map((_, index) => (
      <Skeleton key={index} variant="rectangular" height={56} />
    ))}
  </Stack>
);

interface PageSkeletonProps {
  type?: 'dashboard' | 'table' | 'form' | 'detail';
}

export const PageSkeleton: React.FC<PageSkeletonProps> = ({ type = 'table' }) => {
  if (type === 'dashboard') {
    return <DashboardSkeleton />;
  }

  if (type === 'form') {
    return (
      <Box sx={{ maxWidth: 800, mx: 'auto' }}>
        <Skeleton variant="text" width="40%" height={48} sx={{ mb: 3 }} />
        <FormSkeleton />
      </Box>
    );
  }

  if (type === 'detail') {
    return (
      <Stack spacing={3}>
        <Skeleton variant="text" width="40%" height={48} />
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Stack spacing={2}>
              <Skeleton variant="rectangular" height={200} />
              <Skeleton variant="rectangular" height={300} />
            </Stack>
          </Grid>
          <Grid item xs={12} md={4}>
            <Skeleton variant="rectangular" height={508} />
          </Grid>
        </Grid>
      </Stack>
    );
  }

  return (
    <Stack spacing={3}>
      <Box>
        <Skeleton variant="text" width="30%" height={48} />
        <Skeleton variant="text" width="50%" height={24} sx={{ mt: 1 }} />
      </Box>
      <Skeleton variant="rectangular" height={56} />
      <Skeleton variant="rectangular" height={500} />
    </Stack>
  );
};
