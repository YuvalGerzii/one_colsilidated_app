import React, { useState, useEffect } from 'react';
import {
  Search,
  Network,
  User,
  Building2,
  Home,
  Briefcase,
  Star,
  ChevronRight,
  Filter,
  Plus,
  Link2,
  ArrowRight,
  Layers,
  Eye,
  Edit,
  Trash2,
  GitBranch,
  Maximize2
} from 'lucide-react';

interface Entity {
  id: string;
  type: 'person' | 'company' | 'property' | 'skill' | 'opportunity';
  name: string;
  platform: string;
  properties: Record<string, any>;
  connections: number;
  confidence: number;
}

interface Relationship {
  id: string;
  type: string;
  sourceId: string;
  targetId: string;
  sourceName: string;
  targetName: string;
  weight: number;
  platform: string;
}

export default function EntityExplorer() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedType, setSelectedType] = useState<string>('all');
  const [selectedEntity, setSelectedEntity] = useState<Entity | null>(null);
  const [viewMode, setViewMode] = useState<'list' | 'graph'>('list');

  const entityTypes = [
    { id: 'all', name: 'All Types', icon: Layers },
    { id: 'person', name: 'People', icon: User },
    { id: 'company', name: 'Companies', icon: Building2 },
    { id: 'property', name: 'Properties', icon: Home },
    { id: 'skill', name: 'Skills', icon: Star },
    { id: 'opportunity', name: 'Opportunities', icon: Briefcase },
  ];

  const entities: Entity[] = [
    {
      id: 'ent_1',
      type: 'person',
      name: 'John Smith',
      platform: 'Bond.AI',
      properties: {
        title: 'Managing Director',
        company: 'Blackstone Real Estate',
        location: 'New York, NY',
        expertise: ['Real Estate', 'Private Equity', 'M&A']
      },
      connections: 156,
      confidence: 0.95
    },
    {
      id: 'ent_2',
      type: 'company',
      name: 'Blackstone Real Estate',
      platform: 'Finance',
      properties: {
        type: 'Investment Firm',
        aum: '$298B',
        focus: ['Multifamily', 'Logistics', 'Office'],
        location: 'New York, NY'
      },
      connections: 342,
      confidence: 0.98
    },
    {
      id: 'ent_3',
      type: 'property',
      name: 'Parkview Apartments',
      platform: 'Real Estate',
      properties: {
        type: 'Multifamily',
        units: 250,
        value: '$45M',
        location: 'Austin, TX',
        capRate: '6.2%'
      },
      connections: 28,
      confidence: 0.92
    },
    {
      id: 'ent_4',
      type: 'skill',
      name: 'Machine Learning',
      platform: 'Labor',
      properties: {
        category: 'Technical',
        demandGrowth: '+35%',
        avgSalary: '$155K',
        relatedSkills: ['Python', 'TensorFlow', 'Data Science']
      },
      connections: 1250,
      confidence: 0.88
    },
    {
      id: 'ent_5',
      type: 'opportunity',
      name: 'Series B Investment',
      platform: 'Bond.AI',
      properties: {
        type: 'Investment',
        amount: '$25M',
        sector: 'PropTech',
        stage: 'Due Diligence'
      },
      connections: 15,
      confidence: 0.85
    },
    {
      id: 'ent_6',
      type: 'person',
      name: 'Sarah Chen',
      platform: 'Labor',
      properties: {
        title: 'Data Scientist',
        company: 'TechCorp',
        skills: ['Python', 'ML', 'NLP'],
        experience: '5 years'
      },
      connections: 89,
      confidence: 0.91
    }
  ];

  const relationships: Relationship[] = [
    {
      id: 'rel_1',
      type: 'WORKS_AT',
      sourceId: 'ent_1',
      targetId: 'ent_2',
      sourceName: 'John Smith',
      targetName: 'Blackstone Real Estate',
      weight: 1.0,
      platform: 'Bond.AI'
    },
    {
      id: 'rel_2',
      type: 'INVESTED_IN',
      sourceId: 'ent_2',
      targetId: 'ent_3',
      sourceName: 'Blackstone Real Estate',
      targetName: 'Parkview Apartments',
      weight: 0.85,
      platform: 'Finance'
    },
    {
      id: 'rel_3',
      type: 'HAS_SKILL',
      sourceId: 'ent_6',
      targetId: 'ent_4',
      sourceName: 'Sarah Chen',
      targetName: 'Machine Learning',
      weight: 0.92,
      platform: 'Labor'
    },
    {
      id: 'rel_4',
      type: 'INTERESTED_IN',
      sourceId: 'ent_1',
      targetId: 'ent_5',
      sourceName: 'John Smith',
      targetName: 'Series B Investment',
      weight: 0.78,
      platform: 'Bond.AI'
    }
  ];

  const getEntityIcon = (type: string) => {
    switch (type) {
      case 'person': return User;
      case 'company': return Building2;
      case 'property': return Home;
      case 'skill': return Star;
      case 'opportunity': return Briefcase;
      default: return Layers;
    }
  };

  const getEntityColor = (type: string) => {
    switch (type) {
      case 'person': return 'bg-blue-100 text-blue-600 dark:bg-blue-900 dark:text-blue-400';
      case 'company': return 'bg-purple-100 text-purple-600 dark:bg-purple-900 dark:text-purple-400';
      case 'property': return 'bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-400';
      case 'skill': return 'bg-yellow-100 text-yellow-600 dark:bg-yellow-900 dark:text-yellow-400';
      case 'opportunity': return 'bg-orange-100 text-orange-600 dark:bg-orange-900 dark:text-orange-400';
      default: return 'bg-gray-100 text-gray-600';
    }
  };

  const filteredEntities = entities.filter(e => {
    const matchesSearch = e.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      e.platform.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesType = selectedType === 'all' || e.type === selectedType;
    return matchesSearch && matchesType;
  });

  const entityRelationships = selectedEntity
    ? relationships.filter(r => r.sourceId === selectedEntity.id || r.targetId === selectedEntity.id)
    : [];

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 bg-indigo-100 dark:bg-indigo-900 rounded-lg">
            <Network className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Entity Explorer
          </h1>
        </div>
        <p className="text-gray-600 dark:text-gray-400">
          Explore and manage entities across the unified knowledge graph
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
        {entityTypes.slice(1).map((type) => {
          const count = entities.filter(e => e.type === type.id).length;
          return (
            <button
              key={type.id}
              onClick={() => setSelectedType(type.id === selectedType ? 'all' : type.id)}
              className={`p-4 rounded-xl border transition-all ${
                selectedType === type.id
                  ? 'bg-indigo-50 dark:bg-indigo-900/30 border-indigo-500'
                  : 'bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 hover:border-indigo-300'
              }`}
            >
              <type.icon className={`w-5 h-5 mb-2 ${
                selectedType === type.id ? 'text-indigo-600 dark:text-indigo-400' : 'text-gray-400'
              }`} />
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{count}</p>
              <p className="text-xs text-gray-500">{type.name}</p>
            </button>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Entity List */}
        <div className="lg:col-span-2">
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
              <div className="flex items-center gap-4">
                <div className="flex-1 relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search entities..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => setViewMode('list')}
                    className={`p-2 rounded-lg ${viewMode === 'list' ? 'bg-indigo-100 dark:bg-indigo-900 text-indigo-600' : 'text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'}`}
                  >
                    <Layers className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => setViewMode('graph')}
                    className={`p-2 rounded-lg ${viewMode === 'graph' ? 'bg-indigo-100 dark:bg-indigo-900 text-indigo-600' : 'text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'}`}
                  >
                    <GitBranch className="w-4 h-4" />
                  </button>
                </div>
                <button className="flex items-center gap-2 px-3 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-lg">
                  <Plus className="w-4 h-4" />
                  Add Entity
                </button>
              </div>
            </div>

            {viewMode === 'list' ? (
              <div className="divide-y divide-gray-200 dark:divide-gray-700 max-h-[600px] overflow-y-auto">
                {filteredEntities.map((entity) => {
                  const Icon = getEntityIcon(entity.type);
                  return (
                    <div
                      key={entity.id}
                      onClick={() => setSelectedEntity(entity)}
                      className={`p-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 cursor-pointer transition-colors ${
                        selectedEntity?.id === entity.id ? 'bg-indigo-50 dark:bg-indigo-900/20' : ''
                      }`}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex items-start gap-3">
                          <div className={`p-2 rounded-lg ${getEntityColor(entity.type)}`}>
                            <Icon className="w-4 h-4" />
                          </div>
                          <div>
                            <p className="font-medium text-gray-900 dark:text-white">{entity.name}</p>
                            <div className="flex items-center gap-2 mt-1">
                              <span className="text-xs text-gray-500">{entity.platform}</span>
                              <span className="text-xs text-gray-400">•</span>
                              <span className="text-xs text-gray-500">{entity.connections} connections</span>
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-gray-500">
                            {(entity.confidence * 100).toFixed(0)}% confidence
                          </span>
                          <ChevronRight className="w-4 h-4 text-gray-400" />
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="p-8 flex items-center justify-center h-[600px] bg-gray-50 dark:bg-gray-900">
                <div className="text-center">
                  <GitBranch className="w-16 h-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
                  <p className="text-gray-500 mb-2">Graph Visualization</p>
                  <p className="text-sm text-gray-400">Interactive force-directed graph coming soon</p>
                  <button className="mt-4 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm rounded-lg">
                    <Maximize2 className="w-4 h-4 inline mr-2" />
                    Open Full Screen
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Entity Details */}
        <div className="space-y-6">
          {selectedEntity ? (
            <>
              <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-4">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-semibold text-gray-900 dark:text-white">Entity Details</h3>
                  <div className="flex gap-1">
                    <button className="p-1.5 hover:bg-gray-100 dark:hover:bg-gray-700 rounded">
                      <Eye className="w-4 h-4 text-gray-400" />
                    </button>
                    <button className="p-1.5 hover:bg-gray-100 dark:hover:bg-gray-700 rounded">
                      <Edit className="w-4 h-4 text-gray-400" />
                    </button>
                    <button className="p-1.5 hover:bg-red-100 dark:hover:bg-red-900/20 rounded">
                      <Trash2 className="w-4 h-4 text-red-400" />
                    </button>
                  </div>
                </div>

                <div className="flex items-center gap-3 mb-4">
                  {(() => {
                    const Icon = getEntityIcon(selectedEntity.type);
                    return (
                      <div className={`p-3 rounded-lg ${getEntityColor(selectedEntity.type)}`}>
                        <Icon className="w-6 h-6" />
                      </div>
                    );
                  })()}
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">{selectedEntity.name}</p>
                    <p className="text-sm text-gray-500 capitalize">{selectedEntity.type}</p>
                  </div>
                </div>

                <div className="space-y-3">
                  {Object.entries(selectedEntity.properties).map(([key, value]) => (
                    <div key={key} className="flex justify-between text-sm">
                      <span className="text-gray-500 capitalize">{key.replace(/([A-Z])/g, ' $1').trim()}</span>
                      <span className="text-gray-900 dark:text-white font-medium">
                        {Array.isArray(value) ? value.join(', ') : value}
                      </span>
                    </div>
                  ))}
                </div>

                <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                  <div className="grid grid-cols-2 gap-4 text-center">
                    <div>
                      <p className="text-2xl font-bold text-gray-900 dark:text-white">
                        {selectedEntity.connections}
                      </p>
                      <p className="text-xs text-gray-500">Connections</p>
                    </div>
                    <div>
                      <p className="text-2xl font-bold text-gray-900 dark:text-white">
                        {(selectedEntity.confidence * 100).toFixed(0)}%
                      </p>
                      <p className="text-xs text-gray-500">Confidence</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Relationships */}
              <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-4">
                <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Relationships</h3>
                {entityRelationships.length > 0 ? (
                  <div className="space-y-3">
                    {entityRelationships.map((rel) => (
                      <div key={rel.id} className="p-3 bg-gray-50 dark:bg-gray-900 rounded-lg">
                        <div className="flex items-center gap-2 text-sm">
                          <span className="font-medium text-gray-900 dark:text-white">
                            {rel.sourceId === selectedEntity.id ? selectedEntity.name : rel.sourceName}
                          </span>
                          <ArrowRight className="w-4 h-4 text-gray-400" />
                          <span className="px-2 py-0.5 bg-indigo-100 dark:bg-indigo-900 text-indigo-600 dark:text-indigo-400 text-xs rounded">
                            {rel.type.replace(/_/g, ' ')}
                          </span>
                          <ArrowRight className="w-4 h-4 text-gray-400" />
                          <span className="font-medium text-gray-900 dark:text-white">
                            {rel.targetId === selectedEntity.id ? selectedEntity.name : rel.targetName}
                          </span>
                        </div>
                        <div className="flex items-center justify-between mt-2 text-xs text-gray-500">
                          <span>{rel.platform}</span>
                          <span>Weight: {(rel.weight * 100).toFixed(0)}%</span>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-gray-500 text-center py-4">No relationships found</p>
                )}
                <button className="w-full mt-3 flex items-center justify-center gap-2 px-3 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 text-sm rounded-lg">
                  <Link2 className="w-4 h-4" />
                  Add Relationship
                </button>
              </div>
            </>
          ) : (
            <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-8 text-center">
              <Network className="w-12 h-12 text-gray-300 dark:text-gray-600 mx-auto mb-3" />
              <p className="text-gray-500">Select an entity to view details</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
