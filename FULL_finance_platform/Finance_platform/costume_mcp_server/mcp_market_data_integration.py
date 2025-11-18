"""
Market Data Integration Module for Portfolio Dashboard
Uses Financial Datasets MCP server to enhance valuation models

This module provides:
1. Automatic comparable company data retrieval
2. Market multiples calculation
3. Industry benchmark analysis
4. Exit multiple validation
"""

import asyncio
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import httpx


class MCPMarketDataIntegrator:
    """
    Integrates Financial Datasets MCP server with Portfolio Dashboard
    to provide real-time market data for valuation models
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the MCP Market Data Integrator
        
        Args:
            api_key: Financial Datasets API key
        """
        self.api_key = api_key
        self.base_url = "https://api.financialdatasets.ai"
        self.headers = {"X-API-KEY": api_key}
    
    async def get_comparable_companies_data(
        self, 
        ticker_list: List[str], 
        period: str = "ttm"
    ) -> Dict:
        """
        Fetch financial data for comparable companies
        
        Args:
            ticker_list: List of public company tickers for comparison
            period: 'ttm' (trailing twelve months), 'annual', or 'quarterly'
            
        Returns:
            Dictionary with financial metrics for each comparable
        """
        comparables_data = {}
        
        async with httpx.AsyncClient() as client:
            for ticker in ticker_list:
                try:
                    # Get income statement
                    income_url = f"{self.base_url}/financials/income-statements/"
                    income_params = {
                        "ticker": ticker,
                        "period": period,
                        "limit": 1
                    }
                    income_response = await client.get(
                        income_url, 
                        headers=self.headers, 
                        params=income_params,
                        timeout=30.0
                    )
                    income_data = income_response.json()
                    
                    # Get balance sheet
                    balance_url = f"{self.base_url}/financials/balance-sheets/"
                    balance_params = {
                        "ticker": ticker,
                        "period": period,
                        "limit": 1
                    }
                    balance_response = await client.get(
                        balance_url,
                        headers=self.headers,
                        params=balance_params,
                        timeout=30.0
                    )
                    balance_data = balance_response.json()
                    
                    # Get current stock price
                    price_url = f"{self.base_url}/prices/snapshot/"
                    price_params = {"ticker": ticker}
                    price_response = await client.get(
                        price_url,
                        headers=self.headers,
                        params=price_params,
                        timeout=30.0
                    )
                    price_data = price_response.json()
                    
                    comparables_data[ticker] = {
                        "income_statement": income_data.get("income_statements", [{}])[0],
                        "balance_sheet": balance_data.get("balance_sheets", [{}])[0],
                        "current_price": price_data.get("snapshot", {})
                    }
                    
                except Exception as e:
                    print(f"Error fetching data for {ticker}: {str(e)}")
                    comparables_data[ticker] = {"error": str(e)}
        
        return comparables_data
    
    def calculate_trading_multiples(self, comparables_data: Dict) -> Dict:
        """
        Calculate key valuation multiples from comparable company data
        
        Args:
            comparables_data: Output from get_comparable_companies_data()
            
        Returns:
            Dictionary with calculated multiples for each comparable
        """
        multiples = {}
        
        for ticker, data in comparables_data.items():
            if "error" in data:
                continue
                
            try:
                income = data["income_statement"]
                balance = data["balance_sheet"]
                price_info = data["current_price"]
                
                # Extract key metrics
                revenue = income.get("revenue", 0)
                ebitda = income.get("ebitda", 0)
                net_income = income.get("net_income", 0)
                shares_outstanding = balance.get("shares_outstanding", 0)
                total_debt = balance.get("total_debt", 0)
                cash = balance.get("cash_and_equivalents", 0)
                
                # Current market cap
                current_price = price_info.get("price", 0)
                market_cap = current_price * shares_outstanding if shares_outstanding else 0
                
                # Enterprise Value
                enterprise_value = market_cap + total_debt - cash
                
                # Calculate multiples
                multiples[ticker] = {
                    "market_cap": market_cap,
                    "enterprise_value": enterprise_value,
                    "ev_revenue": enterprise_value / revenue if revenue else None,
                    "ev_ebitda": enterprise_value / ebitda if ebitda else None,
                    "pe_ratio": market_cap / net_income if net_income else None,
                    "price_per_share": current_price,
                    "revenue": revenue,
                    "ebitda": ebitda,
                    "ebitda_margin": (ebitda / revenue * 100) if revenue else None
                }
                
            except Exception as e:
                print(f"Error calculating multiples for {ticker}: {str(e)}")
                multiples[ticker] = {"error": str(e)}
        
        return multiples
    
    def get_industry_benchmarks(self, multiples: Dict) -> Dict:
        """
        Calculate industry benchmark statistics from comparable multiples
        
        Args:
            multiples: Output from calculate_trading_multiples()
            
        Returns:
            Dictionary with median, mean, min, max for each multiple
        """
        # Extract all valid multiples
        ev_revenues = [m["ev_revenue"] for m in multiples.values() 
                      if "ev_revenue" in m and m["ev_revenue"] is not None]
        ev_ebitdas = [m["ev_ebitda"] for m in multiples.values() 
                     if "ev_ebitda" in m and m["ev_ebitda"] is not None]
        pe_ratios = [m["pe_ratio"] for m in multiples.values() 
                    if "pe_ratio" in m and m["pe_ratio"] is not None]
        ebitda_margins = [m["ebitda_margin"] for m in multiples.values()
                         if "ebitda_margin" in m and m["ebitda_margin"] is not None]
        
        def calc_stats(values: List[float]) -> Dict:
            if not values:
                return {"median": None, "mean": None, "min": None, "max": None}
            
            sorted_values = sorted(values)
            n = len(sorted_values)
            median = (sorted_values[n//2] if n % 2 else 
                     (sorted_values[n//2-1] + sorted_values[n//2]) / 2)
            
            return {
                "median": round(median, 2),
                "mean": round(sum(values) / len(values), 2),
                "min": round(min(values), 2),
                "max": round(max(values), 2),
                "count": len(values)
            }
        
        return {
            "ev_revenue": calc_stats(ev_revenues),
            "ev_ebitda": calc_stats(ev_ebitdas),
            "pe_ratio": calc_stats(pe_ratios),
            "ebitda_margin": calc_stats(ebitda_margins)
        }
    
    async def validate_portfolio_company_valuation(
        self,
        portfolio_company_metrics: Dict,
        comparable_tickers: List[str]
    ) -> Dict:
        """
        Validate portfolio company valuation against public market comparables
        
        Args:
            portfolio_company_metrics: Dict with revenue, ebitda, enterprise_value
            comparable_tickers: List of public company tickers
            
        Returns:
            Validation report comparing portfolio company to market
        """
        # Get comparable company data
        comp_data = await self.get_comparable_companies_data(comparable_tickers)
        
        # Calculate multiples
        comp_multiples = self.calculate_trading_multiples(comp_data)
        
        # Get industry benchmarks
        benchmarks = self.get_industry_benchmarks(comp_multiples)
        
        # Calculate portfolio company multiples
        portfolio_revenue = portfolio_company_metrics.get("revenue", 0)
        portfolio_ebitda = portfolio_company_metrics.get("ebitda", 0)
        portfolio_ev = portfolio_company_metrics.get("enterprise_value", 0)
        
        portfolio_ev_revenue = portfolio_ev / portfolio_revenue if portfolio_revenue else None
        portfolio_ev_ebitda = portfolio_ev / portfolio_ebitda if portfolio_ebitda else None
        
        # Compare to benchmarks
        validation = {
            "portfolio_company": {
                "revenue": portfolio_revenue,
                "ebitda": portfolio_ebitda,
                "enterprise_value": portfolio_ev,
                "ev_revenue": portfolio_ev_revenue,
                "ev_ebitda": portfolio_ev_ebitda
            },
            "market_benchmarks": benchmarks,
            "comparable_companies": comp_multiples,
            "valuation_assessment": self._assess_valuation(
                portfolio_ev_revenue,
                portfolio_ev_ebitda,
                benchmarks
            )
        }
        
        return validation
    
    def _assess_valuation(
        self,
        portfolio_ev_revenue: Optional[float],
        portfolio_ev_ebitda: Optional[float],
        benchmarks: Dict
    ) -> Dict:
        """
        Assess if portfolio company valuation is above/below market
        
        Returns:
            Assessment with flags and commentary
        """
        assessment = {
            "ev_revenue_vs_median": None,
            "ev_ebitda_vs_median": None,
            "overall_assessment": "Insufficient data"
        }
        
        if portfolio_ev_revenue and benchmarks["ev_revenue"]["median"]:
            median_ev_rev = benchmarks["ev_revenue"]["median"]
            diff = ((portfolio_ev_revenue - median_ev_rev) / median_ev_rev) * 100
            
            assessment["ev_revenue_vs_median"] = {
                "portfolio": portfolio_ev_revenue,
                "market_median": median_ev_rev,
                "difference_pct": round(diff, 1),
                "flag": "Above Market" if diff > 10 else ("Below Market" if diff < -10 else "At Market")
            }
        
        if portfolio_ev_ebitda and benchmarks["ev_ebitda"]["median"]:
            median_ev_ebitda = benchmarks["ev_ebitda"]["median"]
            diff = ((portfolio_ev_ebitda - median_ev_ebitda) / median_ev_ebitda) * 100
            
            assessment["ev_ebitda_vs_median"] = {
                "portfolio": portfolio_ev_ebitda,
                "market_median": median_ev_ebitda,
                "difference_pct": round(diff, 1),
                "flag": "Above Market" if diff > 10 else ("Below Market" if diff < -10 else "At Market")
            }
        
        # Overall assessment
        if assessment["ev_revenue_vs_median"] or assessment["ev_ebitda_vs_median"]:
            flags = []
            if assessment["ev_revenue_vs_median"]:
                flags.append(assessment["ev_revenue_vs_median"]["flag"])
            if assessment["ev_ebitda_vs_median"]:
                flags.append(assessment["ev_ebitda_vs_median"]["flag"])
            
            if all(f == "Above Market" for f in flags):
                assessment["overall_assessment"] = "Premium Valuation - Above market multiples"
            elif all(f == "Below Market" for f in flags):
                assessment["overall_assessment"] = "Discount Valuation - Below market multiples"
            else:
                assessment["overall_assessment"] = "Mixed Valuation - Some multiples above/below market"
        
        return assessment


# Example usage function
async def example_usage():
    """
    Example: How to use the MCPMarketDataIntegrator
    """
    # Initialize with your API key
    integrator = MCPMarketDataIntegrator(api_key="your-api-key-here")
    
    # Example 1: Get comparable company data
    print("=" * 60)
    print("EXAMPLE 1: Fetch Comparable Company Data")
    print("=" * 60)
    
    tech_comparables = ["AAPL", "MSFT", "GOOGL", "META"]
    comp_data = await integrator.get_comparable_companies_data(tech_comparables)
    print(json.dumps(comp_data, indent=2))
    
    # Example 2: Calculate trading multiples
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Calculate Trading Multiples")
    print("=" * 60)
    
    multiples = integrator.calculate_trading_multiples(comp_data)
    print(json.dumps(multiples, indent=2))
    
    # Example 3: Get industry benchmarks
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Industry Benchmarks")
    print("=" * 60)
    
    benchmarks = integrator.get_industry_benchmarks(multiples)
    print(json.dumps(benchmarks, indent=2))
    
    # Example 4: Validate portfolio company valuation
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Validate Portfolio Company")
    print("=" * 60)
    
    portfolio_metrics = {
        "revenue": 500_000_000,  # $500M
        "ebitda": 100_000_000,   # $100M (20% margin)
        "enterprise_value": 800_000_000  # $800M
    }
    
    validation = await integrator.validate_portfolio_company_valuation(
        portfolio_metrics,
        tech_comparables
    )
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    # Run example
    asyncio.run(example_usage())
