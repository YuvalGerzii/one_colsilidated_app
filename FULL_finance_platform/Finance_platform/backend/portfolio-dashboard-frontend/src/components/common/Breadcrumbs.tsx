// src/components/common/Breadcrumbs.tsx
import React from 'react';
import { Breadcrumbs as MuiBreadcrumbs, Link, Typography, Box } from '@mui/material';
import { NavigateNext as NavigateNextIcon, Home as HomeIcon } from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

interface BreadcrumbItem {
  label: string;
  path?: string;
}

export const Breadcrumbs: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const getBreadcrumbs = (): BreadcrumbItem[] => {
    const pathnames = location.pathname.split('/').filter((x) => x);
    const breadcrumbs: BreadcrumbItem[] = [{ label: 'Home', path: '/dashboard' }];

    let currentPath = '';
    pathnames.forEach((segment, index) => {
      currentPath += `/${segment}`;

      // Create readable labels
      let label = segment.charAt(0).toUpperCase() + segment.slice(1);
      label = label.replace(/-/g, ' ');

      // Map specific routes to better labels
      const labelMap: Record<string, string> = {
        'companies': 'Portfolio Companies',
        'models': 'Model Generator',
        'real-estate': 'Real Estate Models',
        'finance-models': 'Corporate Finance Models',
        'market-data': 'Market Data',
        'documents': 'Documents',
        'upload': 'Document Extraction',
        'library': 'Documents Library',
        'financials': 'Financials',
        'data-entry': 'Data Entry',
        'reports': 'Reports',
        'settings': 'Settings',
      };

      label = labelMap[segment] || label;

      // Don't add path for the last item (current page)
      breadcrumbs.push({
        label,
        path: index === pathnames.length - 1 ? undefined : currentPath,
      });
    });

    return breadcrumbs;
  };

  const breadcrumbs = getBreadcrumbs();

  // Don't show breadcrumbs if we're on the home page
  if (breadcrumbs.length <= 1) {
    return null;
  }

  return (
    <Box sx={{ mb: 2 }}>
      <MuiBreadcrumbs
        separator={<NavigateNextIcon fontSize="small" />}
        aria-label="breadcrumb"
      >
        {breadcrumbs.map((crumb, index) => {
          const isLast = index === breadcrumbs.length - 1;
          const isFirst = index === 0;

          if (isLast) {
            return (
              <Typography key={crumb.label} color="text.primary" variant="body2">
                {crumb.label}
              </Typography>
            );
          }

          return (
            <Link
              key={crumb.label}
              component="button"
              variant="body2"
              onClick={() => crumb.path && navigate(crumb.path)}
              sx={{
                display: 'flex',
                alignItems: 'center',
                textDecoration: 'none',
                color: 'text.secondary',
                '&:hover': {
                  textDecoration: 'underline',
                  color: 'primary.main',
                },
              }}
            >
              {isFirst && <HomeIcon sx={{ mr: 0.5, fontSize: 18 }} />}
              {crumb.label}
            </Link>
          );
        })}
      </MuiBreadcrumbs>
    </Box>
  );
};
