// src/pages/Auth/LoginPage.tsx
import React from 'react';
import {
  Avatar,
  Box,
  Button,
  Card,
  CardContent,
  Link,
  Stack,
  TextField,
  Typography,
} from '@mui/material';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';

export const LoginPage: React.FC = () => {
  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: (theme) => theme.palette.background.default,
        px: 2,
      }}
    >
      <Card
        elevation={6}
        sx={{
          width: '100%',
          maxWidth: 420,
          borderRadius: 4,
        }}
      >
        <CardContent>
          <Stack spacing={4} alignItems="center">
            <Stack spacing={1} alignItems="center">
              <Avatar sx={{ bgcolor: 'primary.main', width: 64, height: 64 }}>
                <LockOutlinedIcon fontSize="large" />
              </Avatar>
              <Typography variant="h4" component="h1" textAlign="center">
                Finance Platform
              </Typography>
              <Typography color="text.secondary" textAlign="center">
                Sign in to access your portfolio analytics suite.
              </Typography>
            </Stack>

            <Stack component="form" spacing={3} width="100%">
              <TextField
                fullWidth
                type="email"
                label="Email address"
                placeholder="you@company.com"
                autoComplete="email"
              />
              <TextField
                fullWidth
                type="password"
                label="Password"
                placeholder="••••••••"
                autoComplete="current-password"
              />
              <Button
                fullWidth
                size="large"
                variant="contained"
                sx={{ py: 1.5 }}
              >
                Login
              </Button>
            </Stack>

            <Stack direction="row" justifyContent="space-between" width="100%">
              <Link href="#" variant="body2" underline="hover">
                Forgot password?
              </Link>
              <Link href="#" variant="body2" underline="hover">
                Create an account
              </Link>
            </Stack>
          </Stack>
        </CardContent>
      </Card>
    </Box>
  );
};

