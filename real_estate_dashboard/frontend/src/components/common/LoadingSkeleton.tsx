import React from 'react';
import { Box, Card, CardContent, Grid, Skeleton, Stack } from '@mui/material';

interface LoadingSkeletonProps {
  variant?: 'dashboard' | 'table' | 'cards' | 'chart';
  count?: number;
}

export const LoadingSkeleton: React.FC<LoadingSkeletonProps> = ({
  variant = 'dashboard',
  count = 3
}) => {
  if (variant === 'dashboard') {
    return (
      <Box>
        <Stack spacing={3}>
          {/* Header Skeleton */}
          <Skeleton variant="rectangular" height={120} sx={{ borderRadius: 2 }} />

          {/* Stats Cards */}
          <Grid container spacing={2}>
            {[1, 2, 3, 4].map((item) => (
              <Grid item xs={12} sm={6} md={3} key={item}>
                <Skeleton variant="rectangular" height={100} sx={{ borderRadius: 2 }} />
              </Grid>
            ))}
          </Grid>

          {/* Charts */}
          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <Skeleton variant="rectangular" height={350} sx={{ borderRadius: 2 }} />
            </Grid>
            <Grid item xs={12} md={4}>
              <Skeleton variant="rectangular" height={350} sx={{ borderRadius: 2 }} />
            </Grid>
          </Grid>
        </Stack>
      </Box>
    );
  }

  if (variant === 'table') {
    return (
      <Box>
        <Stack spacing={2}>
          <Skeleton variant="rectangular" height={56} sx={{ borderRadius: 2 }} />
          {[...Array(count)].map((_, index) => (
            <Skeleton key={index} variant="rectangular" height={72} sx={{ borderRadius: 1 }} />
          ))}
        </Stack>
      </Box>
    );
  }

  if (variant === 'cards') {
    return (
      <Grid container spacing={3}>
        {[...Array(count)].map((_, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card>
              <CardContent>
                <Skeleton variant="circular" width={60} height={60} sx={{ mb: 2 }} />
                <Skeleton variant="text" width="80%" height={32} />
                <Skeleton variant="text" width="60%" />
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    );
  }

  if (variant === 'chart') {
    return (
      <Box sx={{ p: 3 }}>
        <Skeleton variant="text" width={200} height={32} sx={{ mb: 3 }} />
        <Skeleton variant="rectangular" height={300} sx={{ borderRadius: 2 }} />
      </Box>
    );
  }

  return <Skeleton variant="rectangular" height={400} sx={{ borderRadius: 2 }} />;
};
