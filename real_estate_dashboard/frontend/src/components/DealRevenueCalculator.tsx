import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Grid,
  TextField,
  Typography,
  Box,
  Paper,
  Divider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Stack,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import {
  Calculate as CalculateIcon,
  TrendingUp as TrendingUpIcon,
  AttachMoney as MoneyIcon,
  ExpandMore as ExpandMoreIcon,
  Info as InfoIcon,
} from '@mui/icons-material';

interface DealRevenueCalculatorProps {
  open: boolean;
  onClose: () => void;
  initialData?: {
    purchase_price?: number;
    asking_price?: number;
    property_type?: string;
  };
  onApplyToD eal?: (calculatedValues: CalculatedValues) => void;
}

interface CalculatedValues {
  purchase_price: number;
  estimated_revenue: number;
  net_profit: number;
  roi_percentage: number;
  hold_period_years: number;
}

interface CommissionCalculation {
  buyer_commission_rate: number;
  seller_commission_rate: number;
  buyer_commission_amount: number;
  seller_commission_amount: number;
  total_commission: number;
}

interface ResaleCalculation {
  future_sale_price: number;
  appreciation_rate: number;
  holding_costs: number;
  sale_costs: number;
  net_proceeds: number;
}

export const DealRevenueCalculator: React.FC<DealRevenueCalculatorProps> = ({
  open,
  onClose,
  initialData,
  onApplyToDeal,
}) => {
  // Input values
  const [purchasePrice, setPurchasePrice] = useState<number>(initialData?.purchase_price || 0);
  const [calculationType, setCalculationType] = useState<'commission' | 'resale' | 'both'>('both');

  // Commission inputs
  const [buyerCommissionRate, setBuyerCommissionRate] = useState<number>(2.5);
  const [sellerCommissionRate, setSellerCommissionRate] = useState<number>(2.5);

  // Resale inputs
  const [holdPeriodYears, setHoldPeriodYears] = useState<number>(5);
  const [appreciationRate, setAppreciationRate] = useState<number>(3.5);
  const [annualHoldingCosts, setAnnualHoldingCosts] = useState<number>(0);
  const [saleCommissionRate, setSaleCommissionRate] = useState<number>(5);
  const [closingCostsRate, setClosingCostsRate] = useState<number>(2);

  // Calculated values
  const [commission, setCommission] = useState<CommissionCalculation | null>(null);
  const [resale, setResale] = useState<ResaleCalculation | null>(null);
  const [totalROI, setTotalROI] = useState<number>(0);

  useEffect(() => {
    if (initialData?.purchase_price) {
      setPurchasePrice(initialData.purchase_price);
    }
  }, [initialData]);

  const calculateCommission = (): CommissionCalculation => {
    const buyerCommission = (purchasePrice * buyerCommissionRate) / 100;
    const sellerCommission = (purchasePrice * sellerCommissionRate) / 100;
    const totalCommission = buyerCommission + sellerCommission;

    return {
      buyer_commission_rate: buyerCommissionRate,
      seller_commission_rate: sellerCommissionRate,
      buyer_commission_amount: buyerCommission,
      seller_commission_amount: sellerCommission,
      total_commission: totalCommission,
    };
  };

  const calculateResale = (): ResaleCalculation => {
    // Calculate future value with compound appreciation
    const futureSalePrice = purchasePrice * Math.pow(1 + appreciationRate / 100, holdPeriodYears);

    // Calculate total holding costs
    const totalHoldingCosts = annualHoldingCosts * holdPeriodYears;

    // Calculate sale costs (commission + closing costs)
    const saleCommission = (futureSalePrice * saleCommissionRate) / 100;
    const closingCosts = (futureSalePrice * closingCostsRate) / 100;
    const totalSaleCosts = saleCommission + closingCosts;

    // Calculate net proceeds
    const netProceeds = futureSalePrice - purchasePrice - totalHoldingCosts - totalSaleCosts;

    return {
      future_sale_price: futureSalePrice,
      appreciation_rate: appreciationRate,
      holding_costs: totalHoldingCosts,
      sale_costs: totalSaleCosts,
      net_proceeds: netProceeds,
    };
  };

  const handleCalculate = () => {
    let totalRevenue = 0;
    let totalCosts = purchasePrice;

    if (calculationType === 'commission' || calculationType === 'both') {
      const commissionCalc = calculateCommission();
      setCommission(commissionCalc);
      totalRevenue += commissionCalc.total_commission;
    }

    if (calculationType === 'resale' || calculationType === 'both') {
      const resaleCalc = calculateResale();
      setResale(resaleCalc);
      totalRevenue += resaleCalc.net_proceeds;
    }

    // Calculate total ROI
    const roi = ((totalRevenue - totalCosts) / totalCosts) * 100;
    setTotalROI(roi);
  };

  const handleApplyToDeal = () => {
    if (resale && onApplyToDeal) {
      const calculatedValues: CalculatedValues = {
        purchase_price: purchasePrice,
        estimated_revenue: resale.future_sale_price,
        net_profit: resale.net_proceeds,
        roi_percentage: totalROI,
        hold_period_years: holdPeriodYears,
      };
      onApplyToDeal(calculatedValues);
    }
    onClose();
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        <Stack direction="row" alignItems="center" spacing={1}>
          <CalculateIcon />
          <Typography variant="h6">Deal Revenue Calculator</Typography>
        </Stack>
      </DialogTitle>

      <DialogContent dividers>
        <Grid container spacing={3}>
          {/* Calculation Type */}
          <Grid item xs={12}>
            <FormControl fullWidth>
              <InputLabel>Calculation Type</InputLabel>
              <Select
                value={calculationType}
                label="Calculation Type"
                onChange={(e) => setCalculationType(e.target.value as any)}
              >
                <MenuItem value="commission">Commission Only</MenuItem>
                <MenuItem value="resale">Resale/Future Sale Only</MenuItem>
                <MenuItem value="both">Both (Commission + Resale)</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          {/* Purchase Price */}
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Purchase Price"
              type="number"
              value={purchasePrice}
              onChange={(e) => setPurchasePrice(Number(e.target.value))}
              InputProps={{
                startAdornment: '$',
              }}
              required
            />
          </Grid>

          {/* Commission Section */}
          {(calculationType === 'commission' || calculationType === 'both') && (
            <>
              <Grid item xs={12}>
                <Typography variant="subtitle1" fontWeight={600} color="primary" gutterBottom>
                  <MoneyIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
                  Commission Calculator
                </Typography>
                <Divider />
              </Grid>

              <Grid item xs={6}>
                <TextField
                  fullWidth
                  label="Buyer Commission Rate (%)"
                  type="number"
                  value={buyerCommissionRate}
                  onChange={(e) => setBuyerCommissionRate(Number(e.target.value))}
                  inputProps={{ step: 0.1, min: 0, max: 10 }}
                />
              </Grid>

              <Grid item xs={6}>
                <TextField
                  fullWidth
                  label="Seller Commission Rate (%)"
                  type="number"
                  value={sellerCommissionRate}
                  onChange={(e) => setSellerCommissionRate(Number(e.target.value))}
                  inputProps={{ step: 0.1, min: 0, max: 10 }}
                />
              </Grid>
            </>
          )}

          {/* Resale Section */}
          {(calculationType === 'resale' || calculationType === 'both') && (
            <>
              <Grid item xs={12}>
                <Typography variant="subtitle1" fontWeight={600} color="primary" gutterBottom>
                  <TrendingUpIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
                  Future Sale Calculator
                </Typography>
                <Divider />
              </Grid>

              <Grid item xs={6}>
                <TextField
                  fullWidth
                  label="Hold Period (Years)"
                  type="number"
                  value={holdPeriodYears}
                  onChange={(e) => setHoldPeriodYears(Number(e.target.value))}
                  inputProps={{ min: 1, max: 30 }}
                />
              </Grid>

              <Grid item xs={6}>
                <TextField
                  fullWidth
                  label="Annual Appreciation Rate (%)"
                  type="number"
                  value={appreciationRate}
                  onChange={(e) => setAppreciationRate(Number(e.target.value))}
                  inputProps={{ step: 0.1, min: -10, max: 50 }}
                />
              </Grid>

              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Annual Holding Costs"
                  type="number"
                  value={annualHoldingCosts}
                  onChange={(e) => setAnnualHoldingCosts(Number(e.target.value))}
                  helperText="Property taxes, insurance, maintenance, etc."
                  InputProps={{
                    startAdornment: '$',
                  }}
                />
              </Grid>

              <Grid item xs={6}>
                <TextField
                  fullWidth
                  label="Sale Commission Rate (%)"
                  type="number"
                  value={saleCommissionRate}
                  onChange={(e) => setSaleCommissionRate(Number(e.target.value))}
                  inputProps={{ step: 0.1, min: 0, max: 10 }}
                />
              </Grid>

              <Grid item xs={6}>
                <TextField
                  fullWidth
                  label="Closing Costs Rate (%)"
                  type="number"
                  value={closingCostsRate}
                  onChange={(e) => setClosingCostsRate(Number(e.target.value))}
                  inputProps={{ step: 0.1, min: 0, max: 5 }}
                />
              </Grid>
            </>
          )}

          {/* Calculate Button */}
          <Grid item xs={12}>
            <Button
              fullWidth
              variant="contained"
              size="large"
              startIcon={<CalculateIcon />}
              onClick={handleCalculate}
              disabled={!purchasePrice}
            >
              Calculate Revenue & ROI
            </Button>
          </Grid>

          {/* Results Section */}
          {(commission || resale) && (
            <>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                  Results
                </Typography>
              </Grid>

              {/* Commission Results */}
              {commission && (
                <Grid item xs={12}>
                  <Paper variant="outlined" sx={{ p: 2, bgcolor: 'success.50' }}>
                    <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                      Commission Revenue
                    </Typography>
                    <Stack spacing={1}>
                      <Box display="flex" justifyContent="space-between">
                        <Typography variant="body2">Buyer Commission ({buyerCommissionRate}%):</Typography>
                        <Typography variant="body2" fontWeight={600}>
                          {formatCurrency(commission.buyer_commission_amount)}
                        </Typography>
                      </Box>
                      <Box display="flex" justifyContent="space-between">
                        <Typography variant="body2">Seller Commission ({sellerCommissionRate}%):</Typography>
                        <Typography variant="body2" fontWeight={600}>
                          {formatCurrency(commission.seller_commission_amount)}
                        </Typography>
                      </Box>
                      <Divider />
                      <Box display="flex" justifyContent="space-between">
                        <Typography variant="body1" fontWeight={700}>Total Commission:</Typography>
                        <Typography variant="body1" fontWeight={700} color="success.main">
                          {formatCurrency(commission.total_commission)}
                        </Typography>
                      </Box>
                    </Stack>
                  </Paper>
                </Grid>
              )}

              {/* Resale Results */}
              {resale && (
                <Grid item xs={12}>
                  <Paper variant="outlined" sx={{ p: 2, bgcolor: 'info.50' }}>
                    <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                      Future Sale Projection ({holdPeriodYears} years)
                    </Typography>
                    <Stack spacing={1}>
                      <Box display="flex" justifyContent="space-between">
                        <Typography variant="body2">Purchase Price:</Typography>
                        <Typography variant="body2">{formatCurrency(purchasePrice)}</Typography>
                      </Box>
                      <Box display="flex" justifyContent="space-between">
                        <Typography variant="body2">Future Sale Price:</Typography>
                        <Typography variant="body2" fontWeight={600} color="primary.main">
                          {formatCurrency(resale.future_sale_price)}
                        </Typography>
                      </Box>
                      <Box display="flex" justifyContent="space-between">
                        <Typography variant="body2">Holding Costs:</Typography>
                        <Typography variant="body2" color="error.main">
                          -{formatCurrency(resale.holding_costs)}
                        </Typography>
                      </Box>
                      <Box display="flex" justifyContent="space-between">
                        <Typography variant="body2">Sale Costs:</Typography>
                        <Typography variant="body2" color="error.main">
                          -{formatCurrency(resale.sale_costs)}
                        </Typography>
                      </Box>
                      <Divider />
                      <Box display="flex" justifyContent="space-between">
                        <Typography variant="body1" fontWeight={700}>Net Proceeds:</Typography>
                        <Typography
                          variant="body1"
                          fontWeight={700}
                          color={resale.net_proceeds >= 0 ? 'success.main' : 'error.main'}
                        >
                          {formatCurrency(resale.net_proceeds)}
                        </Typography>
                      </Box>
                    </Stack>
                  </Paper>
                </Grid>
              )}

              {/* Total ROI */}
              <Grid item xs={12}>
                <Alert
                  severity={totalROI >= 0 ? 'success' : 'error'}
                  icon={<TrendingUpIcon />}
                  sx={{ fontSize: '1.1rem' }}
                >
                  <Typography variant="h6" component="div">
                    Total ROI: {totalROI.toFixed(2)}%
                  </Typography>
                  <Typography variant="body2">
                    {totalROI >= 0
                      ? `Expected profit of ${formatCurrency(
                          (commission?.total_commission || 0) + (resale?.net_proceeds || 0)
                        )}`
                      : 'Expected loss - review your assumptions'}
                  </Typography>
                </Alert>
              </Grid>

              {/* Info Accordion */}
              <Grid item xs={12}>
                <Accordion>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <InfoIcon sx={{ mr: 1, color: 'info.main' }} />
                    <Typography variant="body2">How is this calculated?</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Typography variant="caption" component="div" color="text.secondary">
                      <strong>Commission:</strong> Calculated as a percentage of the purchase price.
                      <br />
                      <br />
                      <strong>Future Sale:</strong> Uses compound annual growth rate (CAGR) formula:
                      <br />
                      Future Value = Purchase Price × (1 + Appreciation Rate)^Years
                      <br />
                      <br />
                      <strong>Net Proceeds:</strong> Future Sale Price - Purchase Price - Total Holding Costs - Sale
                      Costs
                      <br />
                      <br />
                      <strong>ROI:</strong> (Total Revenue - Total Costs) / Total Costs × 100
                    </Typography>
                  </AccordionDetails>
                </Accordion>
              </Grid>
            </>
          )}
        </Grid>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>Close</Button>
        {resale && onApplyToDeal && (
          <Button variant="contained" onClick={handleApplyToDeal}>
            Apply to Deal
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
};

export default DealRevenueCalculator;
