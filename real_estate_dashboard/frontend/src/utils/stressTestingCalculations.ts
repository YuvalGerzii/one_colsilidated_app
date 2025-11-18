import { StressScenario, ScenarioResult, StressTestResults, TornadoChartData } from '../types/advancedAnalysisTypes';

/**
 * Apply scenario adjustments to base inputs
 * @param baseInputs Original calculator inputs
 * @param scenario Stress scenario to apply
 * @returns Adjusted inputs with scenario modifications
 */
export function applyScenarioAdjustments(baseInputs: any, scenario: StressScenario): any {
  const adjustedInputs = { ...baseInputs };
  const adj = scenario.adjustments;

  // Rent growth adjustment (additive)
  if (adj.rentGrowth !== undefined) {
    const currentRentGrowth = baseInputs.rentGrowth || baseInputs.adrGrowthRate || 0;
    adjustedInputs.rentGrowth = currentRentGrowth + adj.rentGrowth * 100; // Convert to percentage
    adjustedInputs.adrGrowthRate = currentRentGrowth + adj.rentGrowth; // For hotel calculator
  }

  // Vacancy rate adjustment (additive)
  if (adj.vacancyRate !== undefined) {
    const currentVacancy = baseInputs.vacancyRate || (1 - (baseInputs.economicOccupancy || 95) / 100);
    const newVacancy = Math.max(0, Math.min(0.95, currentVacancy + adj.vacancyRate));
    adjustedInputs.vacancyRate = newVacancy * 100; // Convert to percentage
    adjustedInputs.economicOccupancy = (1 - newVacancy) * 100; // For multifamily
    adjustedInputs.year1Occupancy = Math.max(0.3, (1 - newVacancy)); // For hotel
    adjustedInputs.stabilizedOccupancy = Math.max(0.5, (1 - newVacancy)); // For hotel
  }

  // Exit cap rate adjustment (additive)
  if (adj.exitCapRate !== undefined) {
    const currentExitCap = baseInputs.exitCapRate || 0.055;
    adjustedInputs.exitCapRate = Math.max(0.03, currentExitCap + adj.exitCapRate);
  }

  // Expense growth adjustment (additive)
  if (adj.expenseGrowth !== undefined) {
    const currentExpenseGrowth = baseInputs.expenseGrowth || 0.025;
    adjustedInputs.expenseGrowth = currentExpenseGrowth + adj.expenseGrowth * 100; // Convert to percentage
  }

  // Interest rate adjustment (additive)
  if (adj.interestRate !== undefined) {
    const currentRate = baseInputs.interestRate || 0.065;
    adjustedInputs.interestRate = Math.max(0.02, currentRate + adj.interestRate);
  }

  // Property value adjustment (multiplicative) - applied in results calculation
  // This will be handled separately when calculating exit values

  return adjustedInputs;
}

/**
 * Calculate stress test results for all scenarios
 * @param baseInputs Original calculator inputs
 * @param baseResults Original calculator results
 * @param calculateFunction Function to recalculate results with modified inputs
 * @param scenarios List of stress scenarios to test
 * @returns Complete stress test results with all scenarios
 */
export function calculateStressTestResults(
  baseInputs: any,
  baseResults: any,
  calculateFunction: (inputs: any) => any,
  scenarios: StressScenario[]
): StressTestResults {
  const scenarioResults: ScenarioResult[] = [];

  // Calculate results for each scenario
  for (const scenario of scenarios) {
    const adjustedInputs = applyScenarioAdjustments(baseInputs, scenario);
    const results = calculateFunction(adjustedInputs);

    // Apply property value adjustment to exit value if specified
    let exitValue = results.exitValue || 0;
    if (scenario.adjustments.propertyValueAdjustment !== undefined) {
      exitValue = exitValue * (1 + scenario.adjustments.propertyValueAdjustment);
    }

    // Extract key metrics
    const irr = results.irr || 0;
    const equityMultiple = results.equityMultiple || 0;
    const noi = results.noi || results.stabilizedNoi || results.year1Noi || 0;
    const cashFlow = results.cashFlow || results.stabilizedCashFlow || results.year1CashFlow || 0;
    const dscr = results.dscr || results.year1Dscr || 0;

    scenarioResults.push({
      scenarioId: scenario.id,
      scenarioName: scenario.name,
      irr,
      equityMultiple,
      exitValue,
      noi,
      cashFlow,
      dscr,
      metrics: {
        irr,
        equityMultiple,
        exitValue,
        noi,
        cashFlow,
        dscr,
      },
    });
  }

  // Find base case
  const baseCase = scenarioResults.find(r => r.scenarioId === 'base-case');

  // Find worst and best cases by IRR
  const sortedByIrr = [...scenarioResults]
    .filter(r => r.scenarioId !== 'base-case')
    .sort((a, b) => a.irr - b.irr);

  const worstCase = sortedByIrr[0];
  const bestCase = sortedByIrr[sortedByIrr.length - 1];

  // Calculate sensitivity ranking
  const sensitivityRanking = calculateSensitivityRanking(
    baseInputs,
    baseResults,
    calculateFunction
  );

  return {
    baseCase: baseCase || scenarioResults[0],
    scenarios: scenarioResults,
    worstCase,
    bestCase,
    sensitivityRanking,
  };
}

/**
 * Calculate sensitivity ranking by testing each variable independently
 * Uses tornado chart methodology: one-at-a-time sensitivity analysis
 */
export function calculateSensitivityRanking(
  baseInputs: any,
  baseResults: any,
  calculateFunction: (inputs: any) => any
): TornadoChartData[] {
  const baseIrr = baseResults.irr || 0;
  const sensitivities: TornadoChartData[] = [];

  // Define variables to test with their adjustment ranges
  const variablesToTest = [
    {
      name: 'rentGrowth',
      displayName: 'Rent Growth',
      baseValue: baseInputs.rentGrowth || baseInputs.adrGrowthRate || 3,
      range: 0.02, // +/- 2%
      isPercentage: true,
    },
    {
      name: 'vacancyRate',
      displayName: 'Vacancy Rate',
      baseValue: baseInputs.vacancyRate || (100 - (baseInputs.economicOccupancy || 95)),
      range: 0.10, // +/- 10%
      isPercentage: true,
    },
    {
      name: 'exitCapRate',
      displayName: 'Exit Cap Rate',
      baseValue: (baseInputs.exitCapRate || 0.055) * 100,
      range: 0.01, // +/- 100 bps
      isPercentage: true,
    },
    {
      name: 'expenseGrowth',
      displayName: 'Expense Growth',
      baseValue: baseInputs.expenseGrowth || 2.5,
      range: 0.02, // +/- 2%
      isPercentage: true,
    },
    {
      name: 'interestRate',
      displayName: 'Interest Rate',
      baseValue: (baseInputs.interestRate || 0.065) * 100,
      range: 0.01, // +/- 100 bps
      isPercentage: true,
    },
  ];

  for (const variable of variablesToTest) {
    // Test low value
    const lowScenario: StressScenario = {
      id: `${variable.name}-low`,
      name: `${variable.displayName} Low`,
      description: '',
      color: '#3b82f6',
      adjustments: {
        [variable.name]: -variable.range,
      },
    };

    const lowInputs = applyScenarioAdjustments(baseInputs, lowScenario);
    const lowResults = calculateFunction(lowInputs);
    const lowIrr = lowResults.irr || 0;

    // Test high value
    const highScenario: StressScenario = {
      id: `${variable.name}-high`,
      name: `${variable.displayName} High`,
      description: '',
      color: '#3b82f6',
      adjustments: {
        [variable.name]: variable.range,
      },
    };

    const highInputs = applyScenarioAdjustments(baseInputs, highScenario);
    const highResults = calculateFunction(highInputs);
    const highIrr = highResults.irr || 0;

    // Calculate impact
    const range = Math.abs(highIrr - lowIrr);
    const impact = range / Math.abs(baseIrr) * 100; // Percentage impact on IRR

    sensitivities.push({
      variable: variable.name,
      displayName: variable.displayName,
      lowValue: lowIrr,
      baseValue: baseIrr,
      highValue: highIrr,
      range,
      impact,
    });
  }

  // Sort by impact (descending)
  return sensitivities.sort((a, b) => b.impact - a.impact);
}

/**
 * Format scenario result for display
 */
export function formatScenarioMetric(value: number, type: 'irr' | 'multiple' | 'currency' | 'ratio'): string {
  switch (type) {
    case 'irr':
      return `${(value * 100).toFixed(2)}%`;
    case 'multiple':
      return `${value.toFixed(2)}x`;
    case 'currency':
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
      }).format(value);
    case 'ratio':
      return `${value.toFixed(2)}x`;
    default:
      return value.toFixed(2);
  }
}

/**
 * Calculate percentage change from base case
 */
export function calculatePercentageChange(current: number, base: number): number {
  if (base === 0) return 0;
  return ((current - base) / Math.abs(base)) * 100;
}

/**
 * Get risk level based on IRR threshold
 */
export function getScenarioRiskLevel(irr: number, targetIrr: number = 0.15): 'excellent' | 'strong' | 'acceptable' | 'weak' | 'unacceptable' {
  if (irr >= targetIrr * 1.3) return 'excellent'; // 30% above target
  if (irr >= targetIrr) return 'strong'; // Meets target
  if (irr >= targetIrr * 0.7) return 'acceptable'; // 70% of target
  if (irr >= 0) return 'weak'; // Positive but below threshold
  return 'unacceptable'; // Negative returns
}
