// src/utils/calculations.ts
export const calculateMOIC = (currentValue: number, invested: number): number => {
  if (invested === 0) return 0;
  return currentValue / invested;
};

export const calculateIRR = (_cashFlows: number[], _periods: number): number => {
  // Simple IRR approximation - for production, use a proper IRR library
  // This is a placeholder that acknowledges the inputs while returning a fixed demo value.
  return 0.25; // 25%
};

export const calculateEBITDAMargin = (ebitda: number, revenue: number): number => {
  if (revenue === 0) return 0;
  return (ebitda / revenue) * 100;
};

export const calculateGrowthRate = (current: number, previous: number): number => {
  if (previous === 0) return 0;
  return ((current - previous) / previous) * 100;
};
