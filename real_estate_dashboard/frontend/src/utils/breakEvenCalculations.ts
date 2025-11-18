import { BreakEvenMetrics } from '../types/advancedAnalysisTypes';

// Generic binary search function for finding break-even points
function binarySearch(
  testFunction: (value: number) => boolean,
  min: number,
  max: number,
  tolerance: number = 0.0001
): number {
  let low = min;
  let high = max;
  let iterations = 0;
  const maxIterations = 100;

  while (high - low > tolerance && iterations < maxIterations) {
    const mid = (low + high) / 2;
    if (testFunction(mid)) {
      high = mid;
    } else {
      low = mid;
    }
    iterations++;
  }

  return (low + high) / 2;
}

// Calculate occupancy break-even (minimum occupancy to cover debt service)
export function calculateOccupancyBreakEven(
  calculateResults: (occupancy: number) => { noi: number; debtService: number },
  currentOccupancy: number,
  minOccupancy: number = 0.3,
  maxOccupancy: number = 1.0
): number {
  try {
    const breakEven = binarySearch(
      (occupancy) => {
        const result = calculateResults(occupancy);
        return result.noi >= result.debtService;
      },
      minOccupancy,
      maxOccupancy
    );

    // Return NaN if break-even is impossible within range
    if (breakEven >= maxOccupancy - 0.001) {
      return NaN;
    }

    return breakEven;
  } catch (error) {
    console.error('Error calculating occupancy break-even:', error);
    return NaN;
  }
}

// Calculate rent break-even (minimum rent to achieve target IRR)
export function calculateRentBreakEven(
  calculateResults: (rent: number) => { irr: number },
  targetIRR: number,
  currentRent: number,
  minRent: number = currentRent * 0.5,
  maxRent: number = currentRent * 2.0
): number {
  try {
    const breakEven = binarySearch(
      (rent) => {
        const result = calculateResults(rent);
        return result.irr >= targetIRR;
      },
      minRent,
      maxRent
    );

    // Return NaN if target IRR is impossible within range
    if (breakEven >= maxRent - 0.01) {
      return NaN;
    }

    return breakEven;
  } catch (error) {
    console.error('Error calculating rent break-even:', error);
    return NaN;
  }
}

// Calculate exit cap break-even (maximum exit cap for positive returns)
export function calculateExitCapBreakEven(
  calculateResults: (exitCap: number) => { irr: number; equityMultiple: number },
  minAcceptableIRR: number = 0.10, // 10% minimum
  currentExitCap: number,
  minExitCap: number = 0.03,
  maxExitCap: number = 0.15
): number {
  try {
    const breakEven = binarySearch(
      (exitCap) => {
        const result = calculateResults(exitCap);
        return result.irr >= minAcceptableIRR;
      },
      minExitCap,
      maxExitCap
    );

    // Return max cap if even highest cap still meets target
    if (breakEven >= maxExitCap - 0.0001) {
      return maxExitCap;
    }

    return breakEven;
  } catch (error) {
    console.error('Error calculating exit cap break-even:', error);
    return NaN;
  }
}

// Calculate years to break-even (when cumulative cash flow becomes positive)
export function calculateYearsToBreakEven(
  yearlyProjections: Array<{ year: number; cumulativeCashFlow: number }>
): number {
  for (let i = 0; i < yearlyProjections.length; i++) {
    if (yearlyProjections[i].cumulativeCashFlow >= 0) {
      // Linear interpolation for more accurate year
      if (i === 0) return yearlyProjections[i].year;

      const prev = yearlyProjections[i - 1];
      const curr = yearlyProjections[i];

      const fraction =
        -prev.cumulativeCashFlow /
        (curr.cumulativeCashFlow - prev.cumulativeCashFlow);

      return prev.year + fraction;
    }
  }

  // Never breaks even within projection period
  return NaN;
}

// Calculate safety margins (how far current values are from break-even)
export function calculateSafetyMargins(
  current: {
    occupancy?: number;
    rent?: number;
    exitCap?: number;
  },
  breakEven: {
    occupancy?: number;
    rent?: number;
    exitCap?: number;
  }
): {
  occupancy: number;
  rent: number;
  exitCap: number;
} {
  const occupancyMargin =
    current.occupancy && breakEven.occupancy && !isNaN(breakEven.occupancy)
      ? ((current.occupancy - breakEven.occupancy) / breakEven.occupancy) * 100
      : 0;

  const rentMargin =
    current.rent && breakEven.rent && !isNaN(breakEven.rent)
      ? ((current.rent - breakEven.rent) / breakEven.rent) * 100
      : 0;

  const exitCapMargin =
    current.exitCap && breakEven.exitCap && !isNaN(breakEven.exitCap)
      ? ((breakEven.exitCap - current.exitCap) / current.exitCap) * 100
      : 0;

  return {
    occupancy: occupancyMargin,
    rent: rentMargin,
    exitCap: exitCapMargin,
  };
}

// Main function to calculate all break-even metrics
export function calculateBreakEvenMetrics(
  baseInputs: any,
  baseResults: any,
  calculateResultsFunction: (inputs: any) => any,
  targetIRR: number = 0.15 // 15% default target
): BreakEvenMetrics {
  // Calculate occupancy break-even
  const occupancyBreakEven = calculateOccupancyBreakEven(
    (occupancy) => {
      const testInputs = {
        ...baseInputs,
        economicOccupancy: occupancy,
        physicalOccupancy: occupancy,
        occupancy: occupancy,
      };
      return calculateResultsFunction(testInputs);
    },
    baseInputs.economicOccupancy || baseInputs.occupancy || 0.95
  );

  // Calculate rent break-even (for target IRR)
  const currentRent =
    baseInputs.twoBedRent ||
    baseInputs.currentRentPerUnit ||
    baseInputs.adr ||
    baseInputs.arv ||
    0;

  const rentBreakEven = calculateRentBreakEven(
    (rent) => {
      const testInputs = {
        ...baseInputs,
        twoBedRent: rent,
        currentRentPerUnit: rent,
        targetRentPerUnit: rent,
        adr: rent,
      };
      return calculateResultsFunction(testInputs);
    },
    targetIRR,
    currentRent
  );

  // Calculate exit cap break-even
  const currentExitCap = baseInputs.exitCapRate || 0.05;
  const exitCapBreakEven = calculateExitCapBreakEven(
    (exitCap) => {
      const testInputs = { ...baseInputs, exitCapRate: exitCap };
      return calculateResultsFunction(testInputs);
    },
    targetIRR,
    currentExitCap
  );

  // Calculate years to break-even
  const yearlyProjections = baseResults.projections || baseResults.yearlyProjections || [];
  const yearsToBreakEven = calculateYearsToBreakEven(yearlyProjections);

  // Calculate safety margins
  const safetyMargins = calculateSafetyMargins(
    {
      occupancy: baseInputs.economicOccupancy || baseInputs.occupancy,
      rent: currentRent,
      exitCap: currentExitCap,
    },
    {
      occupancy: occupancyBreakEven,
      rent: rentBreakEven,
      exitCap: exitCapBreakEven,
    }
  );

  return {
    occupancyBreakEven,
    rentBreakEven,
    exitCapBreakEven,
    yearsToBreakEven,
    currentOccupancy: baseInputs.economicOccupancy || baseInputs.occupancy,
    currentRent,
    currentExitCap,
    safetyMargins,
  };
}

// Helper function to format break-even results for display
export function formatBreakEvenMetric(
  value: number,
  type: 'percent' | 'currency' | 'years'
): string {
  if (isNaN(value) || !isFinite(value)) {
    return 'N/A';
  }

  switch (type) {
    case 'percent':
      return `${(value * 100).toFixed(1)}%`;
    case 'currency':
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
      }).format(value);
    case 'years':
      return `${value.toFixed(1)} years`;
    default:
      return value.toFixed(2);
  }
}

// Helper to determine risk level based on safety margin
export function getRiskLevel(safetyMargin: number): 'safe' | 'moderate' | 'risk' {
  if (safetyMargin > 20) return 'safe'; // >20% above break-even
  if (safetyMargin > 10) return 'moderate'; // 10-20% above break-even
  return 'risk'; // <10% above break-even
}
