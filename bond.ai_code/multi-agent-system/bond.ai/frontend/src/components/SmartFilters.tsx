import React, { useState, useEffect } from 'react';
import { Filter, X, Save, Sparkles, TrendingUp } from 'lucide-react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../lib/api';

/**
 * Smart Match Filters Component
 *
 * Features:
 * - Auto-apply filters for immediate feedback
 * - ML-based filter suggestions
 * - Save and load filter presets
 * - Real-time result count
 * - Transparent match scoring
 */

interface FilterCriteria {
  location?: {
    cities?: string[];
    countries?: string[];
    radius?: number;
    remote?: boolean;
  };
  industries?: string[];
  expertiseAreas?: string[];
  matchTypes?: string[];
  minCompatibilityScore?: number;
  needCategories?: string[];
  offeringCategories?: string[];
  degreeOfSeparation?: number;
  trustLevel?: number;
  companySize?: string[];
  fundingStage?: string[];
  communicationStyle?: string[];
}

interface FilterSuggestion {
  filterKey: string;
  filterValue: any;
  reason: string;
  confidence: number;
  basedOn: string;
}

interface SmartFiltersProps {
  onFilterChange: (criteria: FilterCriteria) => void;
  autoApply?: boolean;
}

export function SmartFilters({ onFilterChange, autoApply = true }: SmartFiltersProps) {
  const [criteria, setCriteria] = useState<FilterCriteria>({});
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [filterName, setFilterName] = useState('');
  const queryClient = useQueryClient();

  // Load saved preferences
  const { data: preferences } = useQuery({
    queryKey: ['filter-preferences'],
    queryFn: async () => {
      const response = await api.get('/api/filters/preferences');
      return response.data;
    }
  });

  // Load ML suggestions
  const { data: suggestions } = useQuery({
    queryKey: ['filter-suggestions'],
    queryFn: async () => {
      const response = await api.get('/api/filters/suggestions');
      return response.data.suggestions as FilterSuggestion[];
    },
    enabled: showSuggestions
  });

  // Load saved filters
  const { data: savedFilters } = useQuery({
    queryKey: ['saved-filters'],
    queryFn: async () => {
      const response = await api.get('/api/filters/saved');
      return response.data.filters;
    }
  });

  // Apply filters mutation
  const applyFiltersMutation = useMutation({
    mutationFn: async (newCriteria: FilterCriteria) => {
      const response = await api.post('/api/filters/apply', {
        criteria: newCriteria,
        limit: 50
      });
      return response.data;
    },
    onSuccess: (data) => {
      // Trigger parent component update
      onFilterChange(criteria);
    }
  });

  // Save preferences mutation
  const savePreferencesMutation = useMutation({
    mutationFn: async (data: { criteria: FilterCriteria; name?: string }) => {
      const response = await api.post('/api/filters/preferences', {
        criteria: data.criteria,
        name: data.name,
        autoApply: true,
        saveAsDefault: false
      });
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['filter-preferences'] });
    }
  });

  // Save filter set mutation
  const saveFilterMutation = useMutation({
    mutationFn: async (data: { name: string; criteria: FilterCriteria }) => {
      const response = await api.post('/api/filters/saved', {
        name: data.name,
        description: `Custom filter: ${data.name}`,
        criteria: data.criteria
      });
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['saved-filters'] });
      setFilterName('');
    }
  });

  // Auto-apply filters when criteria changes
  useEffect(() => {
    if (autoApply && Object.keys(criteria).length > 0) {
      const timer = setTimeout(() => {
        applyFiltersMutation.mutate(criteria);
      }, 500); // Debounce 500ms

      return () => clearTimeout(timer);
    }
  }, [criteria, autoApply]);

  // Load preferences on mount
  useEffect(() => {
    if (preferences?.preferences?.criteria) {
      setCriteria(preferences.preferences.criteria);
    }
  }, [preferences]);

  const updateCriteria = (key: string, value: any) => {
    const newCriteria = { ...criteria, [key]: value };
    if (value === undefined || value === null || value === '' ||
        (Array.isArray(value) && value.length === 0)) {
      delete newCriteria[key];
    }
    setCriteria(newCriteria);
  };

  const applySuggestion = (suggestion: FilterSuggestion) => {
    updateCriteria(suggestion.filterKey, suggestion.filterValue);
  };

  const clearFilters = () => {
    setCriteria({});
    onFilterChange({});
  };

  const loadSavedFilter = async (filter: any) => {
    setCriteria(filter.criteria);

    // Track usage
    await api.put(`/api/filters/saved/${filter.id}/use`);
    queryClient.invalidateQueries({ queryKey: ['saved-filters'] });
  };

  const activeFilterCount = Object.keys(criteria).length;

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Filter className="w-5 h-5 text-blue-600" />
          <h3 className="text-lg font-semibold">Smart Filters</h3>
          {activeFilterCount > 0 && (
            <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded">
              {activeFilterCount} active
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowSuggestions(!showSuggestions)}
            className="flex items-center gap-1 text-sm text-purple-600 hover:text-purple-700"
          >
            <Sparkles className="w-4 h-4" />
            {showSuggestions ? 'Hide' : 'Show'} AI Suggestions
          </button>
          {activeFilterCount > 0 && (
            <button
              onClick={clearFilters}
              className="flex items-center gap-1 text-sm text-gray-600 hover:text-gray-700"
            >
              <X className="w-4 h-4" />
              Clear All
            </button>
          )}
        </div>
      </div>

      {/* AI Suggestions */}
      {showSuggestions && suggestions && suggestions.length > 0 && (
        <div className="bg-purple-50 rounded-lg p-4 space-y-2">
          <div className="flex items-center gap-2 mb-3">
            <Sparkles className="w-4 h-4 text-purple-600" />
            <h4 className="text-sm font-semibold text-purple-900">AI-Powered Suggestions</h4>
          </div>
          <div className="space-y-2">
            {suggestions.map((suggestion, idx) => (
              <div
                key={idx}
                className="bg-white rounded p-3 flex items-center justify-between hover:shadow-md transition-shadow"
              >
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">{suggestion.reason}</p>
                  <p className="text-xs text-gray-500 mt-1">
                    Confidence: {Math.round(suggestion.confidence * 100)}% • Based on {suggestion.basedOn.replace(/_/g, ' ')}
                  </p>
                </div>
                <button
                  onClick={() => applySuggestion(suggestion)}
                  className="ml-4 px-3 py-1 bg-purple-600 text-white text-xs rounded hover:bg-purple-700"
                >
                  Apply
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Saved Filters */}
      {savedFilters && savedFilters.length > 0 && (
        <div className="border-t pt-4">
          <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
            <TrendingUp className="w-4 h-4" />
            Saved Filter Sets
          </h4>
          <div className="flex flex-wrap gap-2">
            {savedFilters.map((filter: any) => (
              <button
                key={filter.id}
                onClick={() => loadSavedFilter(filter)}
                className="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-full hover:bg-gray-200 flex items-center gap-1"
              >
                {filter.name}
                {filter.usage_count > 0 && (
                  <span className="text-xs text-gray-500">({filter.usage_count})</span>
                )}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Filter Controls */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Compatibility Score */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Minimum Compatibility Score
          </label>
          <input
            type="range"
            min="0"
            max="100"
            value={(criteria.minCompatibilityScore || 0) * 100}
            onChange={(e) => updateCriteria('minCompatibilityScore', parseInt(e.target.value) / 100)}
            className="w-full"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>0%</span>
            <span className="font-medium text-gray-900">
              {Math.round((criteria.minCompatibilityScore || 0) * 100)}%
            </span>
            <span>100%</span>
          </div>
        </div>

        {/* Degree of Separation */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Degree of Separation
          </label>
          <select
            value={criteria.degreeOfSeparation || ''}
            onChange={(e) => updateCriteria('degreeOfSeparation', e.target.value ? parseInt(e.target.value) : undefined)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">Any</option>
            <option value="1">1st degree (Direct connections)</option>
            <option value="2">Up to 2nd degree</option>
            <option value="3">Up to 3rd degree</option>
          </select>
        </div>

        {/* Industries */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Industries
          </label>
          <select
            multiple
            value={criteria.industries || []}
            onChange={(e) => {
              const selected = Array.from(e.target.selectedOptions, option => option.value);
              updateCriteria('industries', selected);
            }}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="technology">Technology</option>
            <option value="finance">Finance</option>
            <option value="healthcare">Healthcare</option>
            <option value="education">Education</option>
            <option value="retail">Retail</option>
            <option value="manufacturing">Manufacturing</option>
          </select>
        </div>

        {/* Match Types */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Match Types
          </label>
          <select
            multiple
            value={criteria.matchTypes || []}
            onChange={(e) => {
              const selected = Array.from(e.target.selectedOptions, option => option.value);
              updateCriteria('matchTypes', selected);
            }}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="investor-startup">Investor-Startup</option>
            <option value="partnership">Partnership</option>
            <option value="mentor-mentee">Mentor-Mentee</option>
            <option value="talent-acquisition">Talent Acquisition</option>
            <option value="collaboration">Collaboration</option>
          </select>
        </div>

        {/* Company Size */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Company Size
          </label>
          <select
            multiple
            value={criteria.companySize || []}
            onChange={(e) => {
              const selected = Array.from(e.target.selectedOptions, option => option.value);
              updateCriteria('companySize', selected);
            }}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="startup">Startup (1-10)</option>
            <option value="small">Small (11-50)</option>
            <option value="medium">Medium (51-200)</option>
            <option value="enterprise">Enterprise (200+)</option>
          </select>
        </div>

        {/* Funding Stage */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Funding Stage
          </label>
          <select
            multiple
            value={criteria.fundingStage || []}
            onChange={(e) => {
              const selected = Array.from(e.target.selectedOptions, option => option.value);
              updateCriteria('fundingStage', selected);
            }}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="pre-seed">Pre-seed</option>
            <option value="seed">Seed</option>
            <option value="series-a">Series A</option>
            <option value="series-b+">Series B+</option>
            <option value="public">Public</option>
          </select>
        </div>
      </div>

      {/* Save Filter */}
      <div className="border-t pt-4">
        <div className="flex items-center gap-2">
          <input
            type="text"
            placeholder="Filter name (e.g., 'Tech Startups')"
            value={filterName}
            onChange={(e) => setFilterName(e.target.value)}
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          />
          <button
            onClick={() => {
              if (filterName && Object.keys(criteria).length > 0) {
                saveFilterMutation.mutate({ name: filterName, criteria });
              }
            }}
            disabled={!filterName || Object.keys(criteria).length === 0}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center gap-2"
          >
            <Save className="w-4 h-4" />
            Save Filter
          </button>
        </div>
      </div>

      {/* Results Info */}
      {applyFiltersMutation.data && (
        <div className="bg-blue-50 rounded-lg p-4">
          <p className="text-sm text-blue-900">
            <span className="font-semibold">{applyFiltersMutation.data.count} matches</span> found with current filters
          </p>
          {autoApply && (
            <p className="text-xs text-blue-700 mt-1">
              Results update automatically as you adjust filters
            </p>
          )}
        </div>
      )}
    </div>
  );
}
