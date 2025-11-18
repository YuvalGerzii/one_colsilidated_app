/**
 * Utility to clear old localStorage data that isn't company-specific
 *
 * Run this once to clean up legacy data from before company-based isolation was implemented
 */

export function clearLegacyLocalStorage() {
  const legacyKeys = [
    'portfolioProperties',      // Old non-company-specific key
    'savedReports',             // Old non-company-specific key
    // Add any other legacy keys here
  ];

  let clearedCount = 0;
  legacyKeys.forEach(key => {
    if (localStorage.getItem(key) !== null) {
      localStorage.removeItem(key);
      clearedCount++;
      console.log(`[Cleanup] Removed legacy localStorage key: ${key}`);
    }
  });

  if (clearedCount > 0) {
    console.log(`[Cleanup] Cleared ${clearedCount} legacy localStorage keys`);
  }

  return clearedCount;
}

/**
 * Get all company-specific localStorage keys
 */
export function getCompanyLocalStorageKeys(companyId: string) {
  return {
    properties: `portfolioProperties_${companyId}`,
    reports: `savedReports_${companyId}`,
  };
}

/**
 * Clear all data for a specific company
 */
export function clearCompanyData(companyId: string) {
  const keys = getCompanyLocalStorageKeys(companyId);
  Object.values(keys).forEach(key => {
    localStorage.removeItem(key);
  });
  console.log(`[Cleanup] Cleared all data for company: ${companyId}`);
}

/**
 * List all localStorage keys to help debug
 */
export function debugLocalStorage() {
  console.log('[Debug] All localStorage keys:');
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (key) {
      const value = localStorage.getItem(key);
      console.log(`  ${key}:`, value?.substring(0, 100));
    }
  }
}
