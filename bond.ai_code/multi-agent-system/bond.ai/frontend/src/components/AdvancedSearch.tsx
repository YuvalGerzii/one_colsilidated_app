import React, { useState, useEffect, useCallback } from 'react';
import { Search, Filter, X, Sparkles, TrendingUp, Clock } from 'lucide-react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { api } from '../lib/api';
import { debounce } from 'lodash';

/**
 * Advanced Search Component
 *
 * Features:
 * - Hybrid search (keyword + semantic)
 * - Real-time autocomplete suggestions
 * - Personalized search history
 * - Advanced filters
 * - Search analytics
 */

interface SearchResult {
  id: string;
  type: 'user' | 'match' | 'need' | 'offering';
  title: string;
  description: string;
  score: number;
  keywordScore?: number;
  semanticScore?: number;
  metadata: Record<string, any>;
  highlights?: string[];
}

export function AdvancedSearch() {
  const [query, setQuery] = useState('');
  const [searchMode, setSearchMode] = useState<'keyword' | 'semantic' | 'hybrid'>('hybrid');
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState<any>({});
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);

  // Search mutation
  const searchMutation = useMutation({
    mutationFn: async (searchQuery: string) => {
      const response = await api.post('/api/search', {
        query: searchQuery,
        searchMode,
        filters,
        fuzzyMatch: true,
        limit: 50
      });
      return response.data;
    }
  });

  // Get autocomplete suggestions
  const { data: autocompleteSuggestions } = useQuery({
    queryKey: ['search-suggestions', query],
    queryFn: async () => {
      if (query.length < 2) return { suggestions: [] };
      const response = await api.get(`/api/search/suggestions?q=${encodeURIComponent(query)}`);
      return response.data;
    },
    enabled: query.length >= 2
  });

  // Get personalized suggestions
  const { data: personalizedSuggestions } = useQuery({
    queryKey: ['personalized-suggestions'],
    queryFn: async () => {
      const response = await api.get('/api/search/personalized-suggestions');
      return response.data;
    }
  });

  // Get popular searches
  const { data: popularSearches } = useQuery({
    queryKey: ['popular-searches'],
    queryFn: async () => {
      const response = await api.get('/api/search/popular');
      return response.data;
    }
  });

  // Get analytics
  const { data: analytics } = useQuery({
    queryKey: ['search-analytics'],
    queryFn: async () => {
      const response = await api.get('/api/search/analytics');
      return response.data;
    }
  });

  // Track click mutation
  const trackClickMutation = useMutation({
    mutationFn: async (data: { resultId: string; resultType: string }) => {
      await api.post('/api/search/track-click', {
        query,
        resultId: data.resultId,
        resultType: data.resultType
      });
    }
  });

  // Update suggestions when autocomplete data changes
  useEffect(() => {
    if (autocompleteSuggestions?.suggestions) {
      setSuggestions(autocompleteSuggestions.suggestions.map((s: any) => s.suggestion));
    }
  }, [autocompleteSuggestions]);

  // Debounced search
  const debouncedSearch = useCallback(
    debounce((searchQuery: string) => {
      if (searchQuery.trim().length >= 2) {
        searchMutation.mutate(searchQuery);
      }
    }, 500),
    [searchMode, filters]
  );

  const handleQueryChange = (value: string) => {
    setQuery(value);
    setShowSuggestions(true);

    if (value.trim().length >= 2) {
      debouncedSearch(value);
    }
  };

  const handleSearch = () => {
    if (query.trim().length >= 2) {
      searchMutation.mutate(query);
      setShowSuggestions(false);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setQuery(suggestion);
    searchMutation.mutate(suggestion);
    setShowSuggestions(false);
  };

  const handleResultClick = (result: SearchResult) => {
    trackClickMutation.mutate({
      resultId: result.id,
      resultType: result.type
    });

    // TODO: Navigate to result details
    console.log('Clicked result:', result);
  };

  const updateFilter = (key: string, value: any) => {
    setFilters((prev: any) => ({
      ...prev,
      [key]: value
    }));
  };

  const clearFilters = () => {
    setFilters({});
  };

  const results = searchMutation.data?.results || [];
  const took = searchMutation.data?.took || 0;

  return (
    <div className="space-y-6">
      {/* Search Header */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex items-center gap-4 mb-4">
          <div className="flex-1 relative">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                value={query}
                onChange={(e) => handleQueryChange(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    handleSearch();
                  }
                }}
                onFocus={() => setShowSuggestions(true)}
                placeholder="Search users, matches, needs, or offerings..."
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Autocomplete Suggestions */}
            {showSuggestions && suggestions.length > 0 && (
              <div className="absolute z-10 w-full mt-2 bg-white rounded-lg shadow-lg border border-gray-200 max-h-64 overflow-y-auto">
                {suggestions.map((suggestion, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSuggestionClick(suggestion)}
                    className="w-full text-left px-4 py-2 hover:bg-gray-50 flex items-center gap-2"
                  >
                    <Search className="w-4 h-4 text-gray-400" />
                    <span>{suggestion}</span>
                  </button>
                ))}
              </div>
            )}
          </div>

          <button
            onClick={handleSearch}
            disabled={query.trim().length < 2}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center gap-2"
          >
            <Search className="w-4 h-4" />
            Search
          </button>

          <button
            onClick={() => setShowFilters(!showFilters)}
            className="px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2"
          >
            <Filter className="w-4 h-4" />
            Filters
            {Object.keys(filters).length > 0 && (
              <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-0.5 rounded-full">
                {Object.keys(filters).length}
              </span>
            )}
          </button>
        </div>

        {/* Search Mode Toggle */}
        <div className="flex items-center gap-4">
          <span className="text-sm text-gray-600">Search mode:</span>
          <div className="flex gap-2">
            {(['keyword', 'semantic', 'hybrid'] as const).map((mode) => (
              <button
                key={mode}
                onClick={() => setSearchMode(mode)}
                className={`px-3 py-1 text-sm rounded-full ${
                  searchMode === mode
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {mode === 'hybrid' && <Sparkles className="w-3 h-3 inline mr-1" />}
                {mode.charAt(0).toUpperCase() + mode.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Filters Panel */}
        {showFilters && (
          <div className="mt-4 p-4 bg-gray-50 rounded-lg space-y-4">
            <div className="flex items-center justify-between">
              <h4 className="font-medium">Advanced Filters</h4>
              {Object.keys(filters).length > 0 && (
                <button
                  onClick={clearFilters}
                  className="text-sm text-gray-600 hover:text-gray-700 flex items-center gap-1"
                >
                  <X className="w-3 h-3" />
                  Clear All
                </button>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Industries */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Industries
                </label>
                <select
                  multiple
                  value={filters.industries || []}
                  onChange={(e) => {
                    const selected = Array.from(e.target.selectedOptions, option => option.value);
                    updateFilter('industries', selected);
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                >
                  <option value="technology">Technology</option>
                  <option value="finance">Finance</option>
                  <option value="healthcare">Healthcare</option>
                  <option value="education">Education</option>
                </select>
              </div>

              {/* Match Types */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Match Types
                </label>
                <select
                  multiple
                  value={filters.matchTypes || []}
                  onChange={(e) => {
                    const selected = Array.from(e.target.selectedOptions, option => option.value);
                    updateFilter('matchTypes', selected);
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                >
                  <option value="investor-startup">Investor-Startup</option>
                  <option value="partnership">Partnership</option>
                  <option value="mentor-mentee">Mentor-Mentee</option>
                </select>
              </div>

              {/* Min Score */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Minimum Score
                </label>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={(filters.minScore || 0) * 100}
                  onChange={(e) => updateFilter('minScore', parseInt(e.target.value) / 100)}
                  className="w-full"
                />
                <div className="text-sm text-gray-600 text-center">
                  {Math.round((filters.minScore || 0) * 100)}%
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Sidebar: Popular & Personalized */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-1 space-y-4">
          {/* Personalized Suggestions */}
          {personalizedSuggestions?.suggestions && personalizedSuggestions.suggestions.length > 0 && (
            <div className="bg-white rounded-lg shadow p-4">
              <h3 className="font-semibold mb-3 flex items-center gap-2">
                <Clock className="w-4 h-4 text-gray-600" />
                Recent Searches
              </h3>
              <div className="space-y-2">
                {personalizedSuggestions.suggestions.map((s: any, idx: number) => (
                  <button
                    key={idx}
                    onClick={() => handleSuggestionClick(s.suggestion)}
                    className="w-full text-left text-sm text-gray-700 hover:text-blue-600 flex items-center justify-between"
                  >
                    <span>{s.suggestion}</span>
                    <span className="text-xs text-gray-400">({s.frequency})</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Popular Searches */}
          {popularSearches?.popular && popularSearches.popular.length > 0 && (
            <div className="bg-white rounded-lg shadow p-4">
              <h3 className="font-semibold mb-3 flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-gray-600" />
                Trending Searches
              </h3>
              <div className="space-y-2">
                {popularSearches.popular.slice(0, 5).map((s: any, idx: number) => (
                  <button
                    key={idx}
                    onClick={() => handleSuggestionClick(s.query)}
                    className="w-full text-left text-sm text-gray-700 hover:text-blue-600"
                  >
                    {s.query}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Analytics */}
          {analytics?.analytics && (
            <div className="bg-white rounded-lg shadow p-4">
              <h3 className="font-semibold mb-3">Your Search Stats</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Total Searches:</span>
                  <span className="font-medium">{analytics.analytics.totalSearches}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Avg Response:</span>
                  <span className="font-medium">{analytics.analytics.avgResponseTime}ms</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Click Rate:</span>
                  <span className="font-medium">{analytics.analytics.clickThroughRate}%</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Search Results */}
        <div className="md:col-span-2">
          {searchMutation.isLoading && (
            <div className="bg-white rounded-lg shadow p-8 text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">Searching...</p>
            </div>
          )}

          {searchMutation.isSuccess && (
            <div className="bg-white rounded-lg shadow">
              <div className="p-4 border-b">
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold">
                    {results.length} results
                  </h3>
                  <span className="text-sm text-gray-500">
                    {took}ms
                  </span>
                </div>
              </div>

              <div className="divide-y">
                {results.map((result: SearchResult) => (
                  <button
                    key={result.id}
                    onClick={() => handleResultClick(result)}
                    className="w-full text-left p-4 hover:bg-gray-50 transition-colors"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <h4 className="font-medium text-gray-900">{result.title}</h4>
                          <span className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">
                            {result.type}
                          </span>
                        </div>
                        {result.highlights && result.highlights.length > 0 ? (
                          <p
                            className="text-sm text-gray-600"
                            dangerouslySetInnerHTML={{ __html: result.highlights[0] }}
                          />
                        ) : (
                          <p className="text-sm text-gray-600">{result.description}</p>
                        )}
                      </div>
                      <div className="ml-4 text-right">
                        <div className="text-lg font-semibold text-blue-600">
                          {Math.round(result.score * 100)}%
                        </div>
                        {result.keywordScore !== undefined && result.semanticScore !== undefined && (
                          <div className="text-xs text-gray-500 mt-1">
                            <div>K: {Math.round(result.keywordScore * 100)}%</div>
                            <div>S: {Math.round(result.semanticScore * 100)}%</div>
                          </div>
                        )}
                      </div>
                    </div>
                  </button>
                ))}
              </div>

              {results.length === 0 && (
                <div className="p-8 text-center text-gray-500">
                  No results found. Try adjusting your search query or filters.
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
