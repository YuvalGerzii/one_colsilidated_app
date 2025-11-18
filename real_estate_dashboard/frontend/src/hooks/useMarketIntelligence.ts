/**
 * React Query Hooks for Market Intelligence
 *
 * Custom hooks for fetching market intelligence data including
 * gentrification scores, market summaries, and trends.
 */

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../services/apiClient';
import { queryKeys } from '../config/react-query';

// Types
interface ComponentScore {
  score: number;
  weight: string;
  value: string;
  indicator: string;
}

interface GentrificationData {
  score: number;
  risk_level: string;
  risk_description: string;
  recommendation: string;
  confidence: string;
  component_scores: {
    price_growth: ComponentScore;
    market_velocity: ComponentScore;
    employment: ComponentScore;
    interest_rates: ComponentScore;
    affordability: ComponentScore;
  };
  market_indicators: {
    price_growth_yoy: number;
    months_supply: number;
    unemployment_rate: number;
    mortgage_rate_30y: number;
    median_price: number;
  };
  location: string;
  timestamp: string;
  data_quality: {
    sources_available: number;
    confidence_level: string;
    employment_source: string;
    housing_source: string;
    rates_source: string;
  };
}

interface MarketSummary {
  overview: any;
  trends: any;
  forecasts: any;
}

// ============================================================================
// Query Hooks
// ============================================================================

/**
 * Fetch gentrification risk score for a location
 *
 * Usage:
 *   const { data: score, isLoading } = useGentrificationScore('New York, NY');
 *   // Or for national data:
 *   const { data: score } = useGentrificationScore();
 */
export const useGentrificationScore = (location?: string) => {
  return useQuery({
    queryKey: queryKeys.marketIntelligence.gentrification(location),
    queryFn: async () => {
      const params = location ? { location } : {};
      const response = await apiClient.instance.get(
        '/market-intelligence/analysis/gentrification-score',
        { params }
      );
      return response.data as GentrificationData;
    },
    staleTime: 15 * 60 * 1000, // 15 minutes - market data doesn't change frequently
    retry: 2,
  });
};

/**
 * Fetch market intelligence summary
 *
 * Usage:
 *   const { data: summary, isLoading } = useMarketSummary();
 */
export const useMarketSummary = () => {
  return useQuery({
    queryKey: queryKeys.marketIntelligence.summary(),
    queryFn: async () => {
      const response = await apiClient.instance.get('/market-intelligence/data/summary');
      return response.data as MarketSummary;
    },
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
};

/**
 * Fetch market data for a specific indicator
 *
 * Usage:
 *   const { data } = useMarketData('housing_prices', { location: 'CA' });
 */
export const useMarketData = (
  indicator: string,
  params?: Record<string, any>
) => {
  return useQuery({
    queryKey: [...queryKeys.marketIntelligence.all, 'data', indicator, params],
    queryFn: async () => {
      const response = await apiClient.instance.get(
        `/market-intelligence/data/${indicator}`,
        { params }
      );
      return response.data;
    },
    enabled: !!indicator,
    staleTime: 15 * 60 * 1000,
  });
};

// ============================================================================
// YFinance Hooks
// ============================================================================

/**
 * Fetch stock data from Yahoo Finance
 *
 * Usage:
 *   const { data, isLoading } = useStockData('AAPL', '1mo', '1d');
 */
export const useStockData = (
  ticker: string,
  period: string = '1mo',
  interval: string = '1d',
  useCache: boolean = true
) => {
  return useQuery({
    queryKey: [...queryKeys.marketIntelligence.all, 'yfinance', 'stock', ticker, period, interval],
    queryFn: async () => {
      const response = await apiClient.instance.get(
        `/market-intelligence/yfinance/stock/${ticker}`,
        { params: { period, interval, use_cache: useCache } }
      );
      return response.data;
    },
    enabled: !!ticker,
    staleTime: 15 * 60 * 1000, // 15 minutes
  });
};

/**
 * Fetch REIT data from Yahoo Finance
 *
 * Usage:
 *   const { data, isLoading } = useREITData();
 *   // Or for specific REIT:
 *   const { data } = useREITData('VNQ');
 */
export const useREITData = (ticker?: string, useCache: boolean = true) => {
  return useQuery({
    queryKey: [...queryKeys.marketIntelligence.all, 'yfinance', 'reits', ticker],
    queryFn: async () => {
      const params: any = { use_cache: useCache };
      if (ticker) params.ticker = ticker;
      const response = await apiClient.instance.get(
        '/market-intelligence/yfinance/reits',
        { params }
      );
      return response.data;
    },
    staleTime: 15 * 60 * 1000,
  });
};

/**
 * Fetch market indices from Yahoo Finance
 *
 * Usage:
 *   const { data, isLoading } = useMarketIndices();
 */
export const useMarketIndices = (useCache: boolean = true) => {
  return useQuery({
    queryKey: [...queryKeys.marketIntelligence.all, 'yfinance', 'indices'],
    queryFn: async () => {
      const response = await apiClient.instance.get(
        '/market-intelligence/yfinance/indices',
        { params: { use_cache: useCache } }
      );
      return response.data;
    },
    staleTime: 15 * 60 * 1000,
  });
};

/**
 * Fetch treasury rates from Yahoo Finance
 *
 * Usage:
 *   const { data, isLoading } = useTreasuryRates();
 */
export const useTreasuryRates = (useCache: boolean = true) => {
  return useQuery({
    queryKey: [...queryKeys.marketIntelligence.all, 'yfinance', 'treasury'],
    queryFn: async () => {
      const response = await apiClient.instance.get(
        '/market-intelligence/yfinance/treasury-rates',
        { params: { use_cache: useCache } }
      );
      return response.data;
    },
    staleTime: 15 * 60 * 1000,
  });
};

/**
 * Fetch comprehensive market summary from Yahoo Finance
 *
 * Usage:
 *   const { data, isLoading } = useYFinanceMarketSummary();
 */
export const useYFinanceMarketSummary = (useCache: boolean = true) => {
  return useQuery({
    queryKey: [...queryKeys.marketIntelligence.all, 'yfinance', 'summary'],
    queryFn: async () => {
      const response = await apiClient.instance.get(
        '/market-intelligence/yfinance/market-summary',
        { params: { use_cache: useCache } }
      );
      return response.data;
    },
    staleTime: 15 * 60 * 1000,
  });
};

// ============================================================================
// Economics API Hooks
// ============================================================================

/**
 * Fetch country economic overview from Economics API
 *
 * Usage:
 *   const { data, isLoading } = useCountryOverview('united-states');
 */
export const useCountryOverview = (
  country: string,
  related?: string,
  useCache: boolean = true
) => {
  return useQuery({
    queryKey: [...queryKeys.marketIntelligence.all, 'economics', 'overview', country, related],
    queryFn: async () => {
      const params: any = { use_cache: useCache };
      if (related) params.related = related;
      const response = await apiClient.instance.get(
        `/market-intelligence/economics/country/${country}/overview`,
        { params }
      );
      return response.data;
    },
    enabled: !!country,
    staleTime: 60 * 60 * 1000, // 1 hour - economic data changes less frequently
  });
};

/**
 * Fetch economic indicator by category
 *
 * Usage:
 *   const { data, isLoading } = useEconomicIndicator('united-states', 'gdp');
 */
export const useEconomicIndicator = (
  country: string,
  category: string,
  related?: string,
  useCache: boolean = true
) => {
  return useQuery({
    queryKey: [...queryKeys.marketIntelligence.all, 'economics', category, country, related],
    queryFn: async () => {
      const params: any = { use_cache: useCache };
      if (related) params.related = related;
      const response = await apiClient.instance.get(
        `/market-intelligence/economics/country/${country}/${category}`,
        { params }
      );
      return response.data;
    },
    enabled: !!country && !!category,
    staleTime: 60 * 60 * 1000,
  });
};

/**
 * Fetch housing data for a country
 *
 * Usage:
 *   const { data, isLoading } = useHousingData('united-states');
 */
export const useHousingData = (country: string, useCache: boolean = true) => {
  return useQuery({
    queryKey: [...queryKeys.marketIntelligence.all, 'economics', 'housing', country],
    queryFn: async () => {
      const response = await apiClient.instance.get(
        `/market-intelligence/economics/housing/${country}`,
        { params: { use_cache: useCache } }
      );
      return response.data;
    },
    enabled: !!country,
    staleTime: 60 * 60 * 1000,
  });
};

/**
 * Fetch economic calendar
 *
 * Usage:
 *   const { data, isLoading } = useEconomicCalendar();
 */
export const useEconomicCalendar = (useCache: boolean = true) => {
  return useQuery({
    queryKey: [...queryKeys.marketIntelligence.all, 'economics', 'calendar'],
    queryFn: async () => {
      const response = await apiClient.instance.get(
        '/market-intelligence/economics/calendar',
        { params: { use_cache: useCache } }
      );
      return response.data;
    },
    staleTime: 30 * 60 * 1000, // 30 minutes
  });
};

/**
 * Fetch comprehensive economic summary for key countries
 *
 * Usage:
 *   const { data, isLoading } = useEconomicSummary(['united-states', 'israel']);
 */
export const useEconomicSummary = (
  countries?: string[],
  useCache: boolean = true
) => {
  return useQuery({
    queryKey: [...queryKeys.marketIntelligence.all, 'economics', 'summary', countries],
    queryFn: async () => {
      const params: any = { use_cache: useCache };
      if (countries) params.countries = countries;
      const response = await apiClient.instance.get(
        '/market-intelligence/economics/summary',
        { params }
      );
      return response.data;
    },
    staleTime: 60 * 60 * 1000,
  });
};

/**
 * Fetch comprehensive market intelligence from all sources
 *
 * Usage:
 *   const { data, isLoading } = useComprehensiveMarketIntelligence();
 */
export const useComprehensiveMarketIntelligence = (
  countries?: string[],
  useCache: boolean = true
) => {
  return useQuery({
    queryKey: [...queryKeys.marketIntelligence.all, 'comprehensive', countries],
    queryFn: async () => {
      const params: any = { use_cache: useCache };
      if (countries) params.countries = countries;
      const response = await apiClient.instance.get(
        '/market-intelligence/market-intelligence/comprehensive',
        { params }
      );
      return response.data;
    },
    staleTime: 15 * 60 * 1000,
  });
};
