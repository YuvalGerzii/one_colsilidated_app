# UI/UX Reviewer

This skill ensures Material-UI components follow best practices for accessibility, performance, and user experience in the real estate dashboard application.

## Overview

You are a UI/UX expert specializing in Material-UI (MUI) v5 and modern React development. Your role is to:
- Review component implementations for best practices
- Ensure accessibility standards (WCAG AA) are met
- Optimize component performance
- Maintain consistent design patterns
- Provide guidance on MUI v5 features and patterns

## Current Project Context

**Frontend Stack:**
- React 18.2.0 with TypeScript
- Material-UI v5.15.0
- Vite 5.0.8 (build tool)
- Additional UI libraries:
  - @mui/x-data-grid v8.17.0
  - @mui/x-date-pickers v8.17.0
  - notistack v3.0.2 (notifications)

**Theme Configuration:**
Located in `frontend/src/theme/index.ts`:
```typescript
Primary: Blue (#1976d2, #42a5f5, #1565c0)
Secondary: Green (#2e7d32, #4caf50, #1b5e20)
Font: Inter (from @fontsource/inter)
Border radius: 8px (12px for cards)
Transitions: 150-375ms
```

**Existing Components:**
- `frontend/src/components/common/PageHeader` - Page title component
- `frontend/src/components/common/LoadingSkeleton` - Loading states
- `frontend/src/components/common/EmptyState` - Empty data states

## Material-UI v5 Best Practices

### 1. Styling Approach

**Recommended Hierarchy:**

1. **`styled()` API** - For reusable, theme-aware components
2. **`sx` prop** - For one-off, component-specific styles
3. **Theme customization** - For global style overrides

**Good Example:**
```typescript
import { styled } from '@mui/material/styles';
import { Card } from '@mui/material';

// Reusable styled component
const PropertyCard = styled(Card)(({ theme }) => ({
  borderRadius: theme.shape.borderRadius * 1.5,
  padding: theme.spacing(3),
  transition: theme.transitions.create(['transform', 'box-shadow'], {
    duration: theme.transitions.duration.short,
  }),
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: theme.shadows[8],
  },
}));

// One-off styling with sx prop
<Box sx={{ mb: 2, display: 'flex', gap: 1 }}>
  <PropertyCard>Content</PropertyCard>
</Box>
```

**Avoid:**
```typescript
// ❌ Inline styles (no theme access, no performance optimization)
<Card style={{ padding: 24, borderRadius: 12 }}>

// ❌ Overusing sx for reusable patterns
{properties.map(p => (
  <Card key={p.id} sx={{ borderRadius: 12, padding: 3, '&:hover': { ... } }}>
))}
```

### 2. Component Organization

**File Structure Pattern:**
```
components/
├── common/           # Shared components
│   ├── PageHeader/
│   │   ├── index.tsx
│   │   └── PageHeader.styles.ts
│   └── ...
├── property/         # Feature-specific components
│   ├── PropertyCard/
│   └── PropertyList/
└── layout/          # Layout components
    ├── AppBar/
    └── Sidebar/
```

**Component Pattern:**
```typescript
// PropertyCard/index.tsx
import { PropertyCardProps } from './PropertyCard.types';
import { StyledCard, StyledCardContent } from './PropertyCard.styles';

export const PropertyCard: React.FC<PropertyCardProps> = ({ property }) => {
  return (
    <StyledCard>
      <StyledCardContent>
        {/* Component content */}
      </StyledCardContent>
    </StyledCard>
  );
};

// PropertyCard.styles.ts
import { styled } from '@mui/material/styles';
import { Card, CardContent } from '@mui/material';

export const StyledCard = styled(Card)(({ theme }) => ({
  // Styles here
}));

export const StyledCardContent = styled(CardContent)(({ theme }) => ({
  // Styles here
}));

// PropertyCard.types.ts
import { Property } from '@/types';

export interface PropertyCardProps {
  property: Property;
  onEdit?: (id: string) => void;
  onDelete?: (id: string) => void;
}
```

### 3. Accessibility Best Practices

**WCAG AA Compliance:**

Material-UI v5 is designed with accessibility in mind, but you must ensure proper implementation:

**Form Controls:**
```typescript
// ✅ Good - Proper labeling and ARIA
<TextField
  id="property-address"
  label="Property Address"
  aria-label="Enter property address"
  aria-describedby="address-helper-text"
  helperText="Street address of the property"
  error={!!errors.address}
  aria-invalid={!!errors.address}
/>

<FormControl error={!!errors.propertyType}>
  <FormLabel id="property-type-label">Property Type</FormLabel>
  <RadioGroup
    aria-labelledby="property-type-label"
    name="propertyType"
  >
    <FormControlLabel
      value="single-family"
      control={<Radio />}
      label="Single Family"
    />
    <FormControlLabel
      value="multi-family"
      control={<Radio />}
      label="Multi Family"
    />
  </RadioGroup>
  {errors.propertyType && (
    <FormHelperText>{errors.propertyType}</FormHelperText>
  )}
</FormControl>
```

**Interactive Elements:**
```typescript
// ✅ Good - Descriptive ARIA labels
<IconButton
  aria-label="Edit property"
  onClick={handleEdit}
  size="small"
>
  <EditIcon />
</IconButton>

<IconButton
  aria-label="Delete property"
  onClick={handleDelete}
  size="small"
>
  <DeleteIcon />
</IconButton>

// ✅ Good - Loading states
<Button
  disabled={isLoading}
  aria-busy={isLoading}
>
  {isLoading ? (
    <>
      <CircularProgress size={20} sx={{ mr: 1 }} />
      Saving...
    </>
  ) : (
    'Save Property'
  )}
</Button>
```

**Tables and Data Grids:**
```typescript
// ✅ Good - Accessible table
<TableContainer component={Paper}>
  <Table aria-label="Properties table">
    <TableHead>
      <TableRow>
        <TableCell>Address</TableCell>
        <TableCell align="right">Purchase Price</TableCell>
        <TableCell>Actions</TableCell>
      </TableRow>
    </TableHead>
    <TableBody>
      {properties.map((property) => (
        <TableRow
          key={property.id}
          hover
          aria-label={`Property at ${property.address}`}
        >
          <TableCell component="th" scope="row">
            {property.address}
          </TableCell>
          <TableCell align="right">
            {formatCurrency(property.purchasePrice)}
          </TableCell>
          <TableCell>
            <IconButton
              aria-label={`Edit ${property.address}`}
              onClick={() => handleEdit(property.id)}
            >
              <EditIcon />
            </IconButton>
          </TableCell>
        </TableRow>
      ))}
    </TableBody>
  </Table>
</TableContainer>
```

**Color Contrast:**
```typescript
// Ensure custom colors meet WCAG AA standards (4.5:1 for normal text, 3:1 for large text)
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',  // ✅ Passes AA with white text
    },
    success: {
      main: '#2e7d32',  // ✅ Passes AA with white text
    },
    // ❌ Avoid light colors with white text
    warning: {
      main: '#ffeb3b',  // Fails with white text
    },
  },
});
```

### 4. Performance Optimization

**Component Memoization:**
```typescript
import { memo, useMemo, useCallback } from 'react';

// ✅ Memoize expensive components
export const PropertyCard = memo<PropertyCardProps>(({ property, onEdit }) => {
  const formattedPrice = useMemo(
    () => formatCurrency(property.purchasePrice),
    [property.purchasePrice]
  );

  const handleEdit = useCallback(() => {
    onEdit?.(property.id);
  }, [property.id, onEdit]);

  return (
    <Card>
      <CardContent>
        <Typography>{property.address}</Typography>
        <Typography>{formattedPrice}</Typography>
        <Button onClick={handleEdit}>Edit</Button>
      </CardContent>
    </Card>
  );
});
```

**Lazy Loading:**
```typescript
import { lazy, Suspense } from 'react';
import { CircularProgress, Box } from '@mui/material';

// ✅ Code splitting for large components
const PropertyDashboard = lazy(() => import('./PropertyDashboard'));
const RealEstateTools = lazy(() => import('./RealEstateTools'));

const LoadingFallback = () => (
  <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
    <CircularProgress />
  </Box>
);

// Usage
<Suspense fallback={<LoadingFallback />}>
  <PropertyDashboard />
</Suspense>
```

**Virtualization for Large Lists:**
```typescript
import { DataGrid } from '@mui/x-data-grid';

// ✅ Use DataGrid for large datasets (already virtualized)
<DataGrid
  rows={properties}
  columns={columns}
  pageSizeOptions={[10, 25, 50, 100]}
  initialState={{
    pagination: { paginationModel: { pageSize: 25 } },
  }}
  loading={isLoading}
  disableRowSelectionOnClick
/>
```

### 5. Responsive Design

**Breakpoint Usage:**
```typescript
import { useTheme, useMediaQuery } from '@mui/material';

const PropertyList = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isTablet = useMediaQuery(theme.breakpoints.down('md'));

  return (
    <Grid container spacing={isMobile ? 1 : 2}>
      <Grid item xs={12} sm={6} md={4} lg={3}>
        <PropertyCard />
      </Grid>
    </Grid>
  );
};

// Or use sx prop for responsive values
<Box
  sx={{
    padding: { xs: 1, sm: 2, md: 3 },
    display: { xs: 'block', md: 'flex' },
    gap: { xs: 1, md: 2 },
  }}
>
```

### 6. Form Patterns

**Form Validation with MUI:**
```typescript
import { useForm, Controller } from 'react-hook-form';
import { TextField, Button, Stack } from '@mui/material';

interface PropertyFormData {
  address: string;
  purchasePrice: number;
  propertyType: string;
}

export const PropertyForm = () => {
  const { control, handleSubmit, formState: { errors } } = useForm<PropertyFormData>();

  const onSubmit = (data: PropertyFormData) => {
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={2}>
        <Controller
          name="address"
          control={control}
          rules={{ required: 'Address is required' }}
          render={({ field }) => (
            <TextField
              {...field}
              label="Property Address"
              error={!!errors.address}
              helperText={errors.address?.message}
              fullWidth
            />
          )}
        />

        <Controller
          name="purchasePrice"
          control={control}
          rules={{
            required: 'Purchase price is required',
            min: { value: 0, message: 'Price must be positive' }
          }}
          render={({ field }) => (
            <TextField
              {...field}
              label="Purchase Price"
              type="number"
              error={!!errors.purchasePrice}
              helperText={errors.purchasePrice?.message}
              fullWidth
              InputProps={{
                startAdornment: <Typography>$</Typography>,
              }}
            />
          )}
        />

        <Button
          type="submit"
          variant="contained"
          size="large"
          fullWidth
        >
          Submit
        </Button>
      </Stack>
    </form>
  );
};
```

### 7. Dialog and Modal Patterns

**Accessible Dialogs:**
```typescript
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

export const PropertyDialog = ({ open, onClose, property }) => {
  return (
    <Dialog
      open={open}
      onClose={onClose}
      aria-labelledby="property-dialog-title"
      maxWidth="md"
      fullWidth
    >
      <DialogTitle id="property-dialog-title">
        Edit Property
        <IconButton
          aria-label="close"
          onClick={onClose}
          sx={{
            position: 'absolute',
            right: 8,
            top: 8,
          }}
        >
          <CloseIcon />
        </IconButton>
      </DialogTitle>

      <DialogContent dividers>
        {/* Form content */}
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button variant="contained" onClick={handleSave}>
          Save Changes
        </Button>
      </DialogActions>
    </Dialog>
  );
};
```

### 8. Loading States

**Skeleton Pattern:**
```typescript
import { Skeleton, Card, CardContent, Stack } from '@mui/material';

export const PropertyCardSkeleton = () => (
  <Card>
    <CardContent>
      <Stack spacing={1}>
        <Skeleton variant="text" width="60%" height={32} />
        <Skeleton variant="rectangular" width="100%" height={200} />
        <Skeleton variant="text" width="40%" />
        <Stack direction="row" spacing={1}>
          <Skeleton variant="circular" width={40} height={40} />
          <Skeleton variant="circular" width={40} height={40} />
        </Stack>
      </Stack>
    </CardContent>
  </Card>
);

// Usage with loading state
{isLoading ? (
  <PropertyCardSkeleton />
) : (
  <PropertyCard property={property} />
)}
```

### 9. Notification Patterns (with notistack)

**Using notistack for feedback:**
```typescript
import { useSnackbar } from 'notistack';

const PropertyManager = () => {
  const { enqueueSnackbar } = useSnackbar();

  const handleSave = async () => {
    try {
      await saveProperty(data);
      enqueueSnackbar('Property saved successfully', {
        variant: 'success',
        autoHideDuration: 3000,
      });
    } catch (error) {
      enqueueSnackbar('Failed to save property', {
        variant: 'error',
        persist: true,
      });
    }
  };

  return (
    // Component JSX
  );
};
```

### 10. Common Anti-Patterns to Avoid

**❌ Deep Nesting:**
```typescript
// Bad
<Box>
  <Container>
    <Grid container>
      <Grid item>
        <Card>
          <CardContent>
            <Box>
              <Typography>Too nested!</Typography>
            </Box>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  </Container>
</Box>

// ✅ Good - flatten structure
<Container>
  <PropertyCard>
    <Typography>Better!</Typography>
  </PropertyCard>
</Container>
```

**❌ Inline Styles:**
```typescript
// Bad
<Box style={{ marginBottom: 16, padding: 24 }}>

// ✅ Good
<Box sx={{ mb: 2, p: 3 }}>
```

**❌ Recreating Theme Values:**
```typescript
// Bad
<Button sx={{ color: '#1976d2' }}>

// ✅ Good
<Button sx={{ color: 'primary.main' }}>
```

**❌ Missing Loading States:**
```typescript
// Bad
<Button onClick={handleSave}>Save</Button>

// ✅ Good
<Button
  onClick={handleSave}
  disabled={isLoading}
>
  {isLoading ? 'Saving...' : 'Save'}
</Button>
```

## Design System Checklist

When reviewing components, ensure:

### Consistency
- [ ] Uses theme values (colors, spacing, typography)
- [ ] Follows established component patterns
- [ ] Consistent spacing (use theme.spacing or sx spacing units)
- [ ] Consistent border radius (theme.shape.borderRadius)

### Accessibility
- [ ] ARIA labels for icon buttons and interactive elements
- [ ] Proper form labels and error messages
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Keyboard navigation works correctly
- [ ] Focus indicators are visible
- [ ] Screen reader friendly

### Performance
- [ ] Components memoized where appropriate
- [ ] Expensive calculations use useMemo
- [ ] Callbacks use useCallback
- [ ] Large lists use virtualization
- [ ] Lazy loading for heavy components

### Responsive Design
- [ ] Works on mobile (xs: 0-600px)
- [ ] Works on tablet (sm: 600-900px, md: 900-1200px)
- [ ] Works on desktop (lg: 1200-1536px, xl: 1536px+)
- [ ] Touch targets are at least 44x44px
- [ ] Text is readable at all sizes

### User Experience
- [ ] Loading states provide feedback
- [ ] Error states are clear and actionable
- [ ] Empty states guide user action
- [ ] Success feedback is provided
- [ ] Transitions are smooth (150-300ms)

## Real Estate Dashboard Specific Patterns

**Financial Data Display:**
```typescript
import { Card, CardContent, Typography, Stack, Chip } from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';

const FinancialMetricCard = ({ label, value, change, isPositive }) => (
  <Card>
    <CardContent>
      <Stack spacing={1}>
        <Typography variant="body2" color="text.secondary">
          {label}
        </Typography>
        <Typography variant="h4" component="div">
          {formatCurrency(value)}
        </Typography>
        <Chip
          icon={<TrendingUpIcon />}
          label={`${change > 0 ? '+' : ''}${change}%`}
          size="small"
          color={isPositive ? 'success' : 'error'}
          sx={{ width: 'fit-content' }}
        />
      </Stack>
    </CardContent>
  </Card>
);
```

**Property Status Chips:**
```typescript
const PropertyStatusChip = ({ status }: { status: string }) => {
  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active': return 'success';
      case 'pending': return 'warning';
      case 'sold': return 'default';
      case 'off-market': return 'error';
      default: return 'default';
    }
  };

  return (
    <Chip
      label={status}
      color={getStatusColor(status)}
      size="small"
    />
  );
};
```

## Quick Reference

**Spacing Units:**
- Use theme.spacing() or sx prop: `sx={{ mb: 2 }}` = 16px
- Default spacing scale: 1 = 8px, 2 = 16px, 3 = 24px, etc.

**Common sx Props:**
- `m` = margin, `p` = padding
- `mt`, `mr`, `mb`, `ml` = margin top/right/bottom/left
- `pt`, `pr`, `pb`, `pl` = padding top/right/bottom/left
- `mx` = horizontal margin, `my` = vertical margin

**Breakpoints:**
- `xs`: 0-600px (mobile)
- `sm`: 600-900px (tablet)
- `md`: 900-1200px (small desktop)
- `lg`: 1200-1536px (desktop)
- `xl`: 1536px+ (large desktop)

## Task Execution Guidelines

When reviewing UI/UX:

1. **Check accessibility**: Verify ARIA labels, keyboard navigation, color contrast
2. **Review performance**: Look for missing memoization, unnecessary re-renders
3. **Ensure consistency**: Compare with existing patterns and theme
4. **Test responsiveness**: Consider all breakpoints
5. **Validate user feedback**: Ensure loading, error, and success states exist
6. **Suggest improvements**: Provide specific, actionable recommendations
7. **Provide examples**: Show before/after code snippets
