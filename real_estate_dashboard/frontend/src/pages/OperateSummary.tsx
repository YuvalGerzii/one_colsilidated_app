import { useState } from 'react';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import {
  Building2, Home, Users, DollarSign, Calendar, AlertCircle,
  CheckCircle2, Clock, Wrench, FileText, TrendingUp, TrendingDown,
  MapPin, Search, Download, Filter
} from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';
import { useCompany } from '../context/CompanyContext';

interface Property {
  id: string;
  name: string;
  type: string;
  location: string;
  units: number;
  occupancy: number;
  revenue: number;
  expenses: number;
  noi: number;
  maintenanceIssues: number;
  leasesExpiring: number;
  status: 'excellent' | 'good' | 'warning' | 'critical';
}

interface Lease {
  id: string;
  tenant: string;
  property: string;
  unit: string;
  rent: number;
  startDate: string;
  endDate: string;
  status: 'active' | 'expiring-soon' | 'expired' | 'pending';
}

interface MaintenanceTicket {
  id: string;
  property: string;
  unit: string;
  issue: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  status: 'open' | 'in-progress' | 'completed';
  createdDate: string;
  assignedTo?: string;
}

export function OperateSummary() {
  const { theme, colors } = useTheme();
  const { selectedCompany } = useCompany();
  const [activeView, setActiveView] = useState<'properties' | 'leases' | 'maintenance'>('properties');
  const [searchTerm, setSearchTerm] = useState('');

  // Mock data - would come from API
  // TODO: Connect to backend API to fetch real property data for selectedCompany
  const properties: Property[] = selectedCompany ? [] : [];

  // TODO: Connect to backend API to fetch real lease data for selectedCompany
  const leases: Lease[] = selectedCompany ? [] : [];

  // TODO: Connect to backend API to fetch real maintenance data for selectedCompany
  const maintenanceTickets: MaintenanceTicket[] = selectedCompany ? [] : [];

  const getStatusColor = (status: Property['status']) => {
    const colors = {
      excellent: { bg: 'bg-green-500/10', text: 'text-green-400', border: 'border-green-500/20' },
      good: { bg: 'bg-blue-500/10', text: 'text-blue-400', border: 'border-blue-500/20' },
      warning: { bg: 'bg-amber-500/10', text: 'text-amber-400', border: 'border-amber-500/20' },
      critical: { bg: 'bg-red-500/10', text: 'text-red-400', border: 'border-red-500/20' }
    };
    return theme === 'dark' ? colors[status] : {
      excellent: { bg: 'bg-green-100', text: 'text-green-700', border: 'border-green-300' },
      good: { bg: 'bg-blue-100', text: 'text-blue-700', border: 'border-blue-300' },
      warning: { bg: 'bg-amber-100', text: 'text-amber-700', border: 'border-amber-300' },
      critical: { bg: 'bg-red-100', text: 'text-red-700', border: 'border-red-300' }
    }[status];
  };

  const getPriorityColor = (priority: MaintenanceTicket['priority']) => {
    const colors = {
      low: theme === 'dark' ? 'text-slate-400' : 'text-slate-600',
      medium: theme === 'dark' ? 'text-blue-400' : 'text-blue-600',
      high: theme === 'dark' ? 'text-amber-400' : 'text-amber-600',
      urgent: theme === 'dark' ? 'text-red-400' : 'text-red-600'
    };
    return colors[priority];
  };

  const getLeaseStatusColor = (status: Lease['status']) => {
    const colors = {
      active: theme === 'dark' ? 'text-green-400' : 'text-green-600',
      'expiring-soon': theme === 'dark' ? 'text-amber-400' : 'text-amber-600',
      expired: theme === 'dark' ? 'text-red-400' : 'text-red-600',
      pending: theme === 'dark' ? 'text-blue-400' : 'text-blue-600'
    };
    return colors[status];
  };

  const filteredProperties = properties.filter(p =>
    p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.location.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className={`${colors.bg.primary}`}>
      {/* Header */}
      <div className={`${theme === 'dark' ? 'bg-slate-900/40 border-slate-700/50' : 'bg-white/60 border-slate-200/80'} border-b px-8 py-5 backdrop-blur-sm`}>
        <div className="flex items-center justify-between">
          <div>
            <h1 className={`text-2xl font-bold mb-1 ${colors.text.primary}`}>
              Operations Summary
            </h1>
            <p className={`text-sm ${colors.text.secondary}`}>
              {selectedCompany?.name || 'All Properties'} · Portfolio Overview
            </p>
          </div>
          <div className="flex items-center gap-3">
            <div className={`relative ${theme === 'dark' ? 'bg-slate-800/50' : 'bg-slate-100'} rounded-lg`}>
              <Search className={`absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 ${colors.text.tertiary}`} />
              <input
                type="text"
                placeholder="Search properties..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className={`pl-10 pr-4 py-2 text-sm ${theme === 'dark' ? 'bg-slate-800/50 text-white placeholder-slate-500' : 'bg-slate-100 text-slate-900 placeholder-slate-400'} rounded-lg border-0 focus:outline-none focus:ring-2 focus:ring-blue-500/50`}
              />
            </div>
            <Button variant="outline" size="sm" className={`${theme === 'dark' ? 'border-slate-700 text-slate-300 bg-slate-800/50 hover:bg-slate-800' : 'border-slate-300 text-slate-700 bg-white hover:bg-slate-50'}`}>
              <Filter className="w-4 h-4 mr-2" />
              Filter
            </Button>
            <Button variant="outline" size="sm" className={`${theme === 'dark' ? 'border-slate-700 text-slate-300 bg-slate-800/50 hover:bg-slate-800' : 'border-slate-300 text-slate-700 bg-white hover:bg-slate-50'}`}>
              <Download className="w-4 h-4 mr-2" />
              Export
            </Button>
          </div>
        </div>

        {/* View Tabs */}
        <div className="flex gap-2 mt-4">
          {(['properties', 'leases', 'maintenance'] as const).map((view) => (
            <button
              key={view}
              onClick={() => setActiveView(view)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                activeView === view
                  ? theme === 'dark'
                    ? 'bg-blue-600 text-white'
                    : 'bg-blue-600 text-white'
                  : theme === 'dark'
                    ? 'bg-slate-800/50 text-slate-400 hover:text-white hover:bg-slate-800'
                    : 'bg-slate-100 text-slate-600 hover:text-slate-900 hover:bg-slate-200'
              }`}
            >
              {view === 'properties' && <Building2 className="w-4 h-4 inline-block mr-2" />}
              {view === 'leases' && <FileText className="w-4 h-4 inline-block mr-2" />}
              {view === 'maintenance' && <Wrench className="w-4 h-4 inline-block mr-2" />}
              {view.charAt(0).toUpperCase() + view.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Table Content */}
      <div className="p-8">
        <Card className={`${theme === 'dark' ? 'bg-slate-800/40 border-slate-700/50' : 'bg-white border-slate-200'}`}>
          {/* Properties Table */}
          {activeView === 'properties' && (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className={`${theme === 'dark' ? 'border-slate-700' : 'border-slate-200'} border-b`}>
                    <th className={`px-6 py-4 text-left text-xs font-semibold ${colors.text.secondary} uppercase tracking-wider`}>Property</th>
                    <th className={`px-6 py-4 text-left text-xs font-semibold ${colors.text.secondary} uppercase tracking-wider`}>Type</th>
                    <th className={`px-6 py-4 text-left text-xs font-semibold ${colors.text.secondary} uppercase tracking-wider`}>Location</th>
                    <th className={`px-6 py-4 text-right text-xs font-semibold ${colors.text.secondary} uppercase tracking-wider`}>Units</th>
                    <th className={`px-6 py-4 text-right text-xs font-semibold ${colors.text.secondary} uppercase tracking-wider`}>Occupancy</th>
                    <th className={`px-6 py-4 text-right text-xs font-semibold ${colors.text.secondary} uppercase tracking-wider`}>Revenue</th>
                    <th className={`px-6 py-4 text-right text-xs font-semibold ${colors.text.secondary} uppercase tracking-wider`}>NOI</th>
                    <th className={`px-6 py-4 text-center text-xs font-semibold ${colors.text.secondary} uppercase tracking-wider`}>Issues</th>
                    <th className={`px-6 py-4 text-center text-xs font-semibold ${colors.text.secondary} uppercase tracking-wider`}>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredProperties.map((property) => {
                    const statusColors = getStatusColor(property.status);
                    return (
                      <tr key={property.id} className={`${theme === 'dark' ? 'border-slate-700 hover:bg-slate-800/30' : 'border-slate-200 hover:bg-slate-50'} border-b transition-colors`}>
                        <td className={`px-6 py-4 ${colors.text.primary} font-medium`}>{property.name}</td>
                        <td className={`px-6 py-4 ${colors.text.secondary} text-sm`}>{property.type}</td>
                        <td className={`px-6 py-4 ${colors.text.secondary} text-sm`}>
                          <div className="flex items-center gap-1">
                            <MapPin className="w-3 h-3" />
                            {property.location}
                          </div>
                        </td>
                        <td className={`px-6 py-4 ${colors.text.primary} text-sm text-right`}>{property.units}</td>
                        <td className={`px-6 py-4 text-sm text-right`}>
                          <div className="flex items-center justify-end gap-2">
                            <span className={property.occupancy >= 95 ? (theme === 'dark' ? 'text-green-400' : 'text-green-600') : (theme === 'dark' ? 'text-amber-400' : 'text-amber-600')}>
                              {property.occupancy}%
                            </span>
                          </div>
                        </td>
                        <td className={`px-6 py-4 ${colors.text.primary} text-sm text-right font-medium`}>
                          ${property.revenue.toLocaleString()}
                        </td>
                        <td className={`px-6 py-4 ${theme === 'dark' ? 'text-green-400' : 'text-green-600'} text-sm text-right font-semibold`}>
                          ${property.noi.toLocaleString()}
                        </td>
                        <td className={`px-6 py-4 text-center`}>
                          <div className="flex items-center justify-center gap-3">
                            <div className={`flex items-center gap-1 ${property.maintenanceIssues > 0 ? (theme === 'dark' ? 'text-amber-400' : 'text-amber-600') : colors.text.tertiary}`}>
                              <Wrench className="w-4 h-4" />
                              <span className="text-sm">{property.maintenanceIssues}</span>
                            </div>
                            <div className={`flex items-center gap-1 ${property.leasesExpiring > 0 ? (theme === 'dark' ? 'text-blue-400' : 'text-blue-600') : colors.text.tertiary}`}>
                              <Calendar className="w-4 h-4" />
                              <span className="text-sm">{property.leasesExpiring}</span>
                            </div>
                          </div>
                        </td>
                        <td className={`px-6 py-4 text-center`}>
                          <span className={`inline-flex px-3 py-1 text-xs font-medium rounded-full ${statusColors.bg} ${statusColors.text} ${statusColors.border} border`}>
                            {property.status}
                          </span>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}

          {/* Leases Table */}
          {activeView === 'leases' && (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className={`${theme === 'dark' ? 'border-slate-700' : 'border-slate-200'} border-b`}>
                    <th className={`px-6 py-4 text-left text-xs font-semibold ${colors.text.secondary} uppercase tracking-wider`}>Tenant</th>
                    <th className={`px-6 py-4 text-left text-xs font-semibold ${colors.text.secondary} uppercase tracking-wider`}>Property</th>
                    <th className={`px-6 py-4 text-left text-xs font-semibold ${colors.text.secondary} uppercase tracking-wider`}>Unit</th>
                    <th className={`px-6 py-4 text-right text-xs font-semibold ${colors.text.secondary} uppercase tracking-wider`}>Rent</th>
                    <th className={`px-6 py-4 text-left text-xs font-semibold ${colors.text.secondary} uppercase tracking-wider`}>Start Date</th>
                    <th className={`px-6 py-4 text-left text-xs font-semibold ${colors.text.secondary} uppercase tracking-wider`}>End Date</th>
                    <th className={`px-6 py-4 text-center text-xs font-semibold ${colors.text.secondary} uppercase tracking-wider`}>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {leases.map((lease) => (
                    <tr key={lease.id} className={`${theme === 'dark' ? 'border-slate-700 hover:bg-slate-800/30' : 'border-slate-200 hover:bg-slate-50'} border-b transition-colors`}>
                      <td className={`px-6 py-4 ${colors.text.primary} font-medium`}>
                        <div className="flex items-center gap-2">
                          <Users className="w-4 h-4" />
                          {lease.tenant}
                        </div>
                      </td>
                      <td className={`px-6 py-4 ${colors.text.secondary} text-sm`}>{lease.property}</td>
                      <td className={`px-6 py-4 ${colors.text.secondary} text-sm`}>{lease.unit}</td>
                      <td className={`px-6 py-4 ${colors.text.primary} text-sm text-right font-medium`}>
                        ${lease.rent.toLocaleString()}
                      </td>
                      <td className={`px-6 py-4 ${colors.text.secondary} text-sm`}>{lease.startDate}</td>
                      <td className={`px-6 py-4 ${colors.text.secondary} text-sm`}>{lease.endDate}</td>
                      <td className={`px-6 py-4 text-center`}>
                        <span className={`inline-flex items-center gap-1 text-sm font-medium ${getLeaseStatusColor(lease.status)}`}>
                          {lease.status === 'active' && <CheckCircle2 className="w-4 h-4" />}
                          {lease.status === 'expiring-soon' && <Clock className="w-4 h-4" />}
                          {lease.status === 'expired' && <AlertCircle className="w-4 h-4" />}
                          {lease.status.replace('-', ' ')}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Maintenance Table */}
          {activeView === 'maintenance' && (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className={`${theme === 'dark' ? 'border-slate-700' : 'border-slate-200'} border-b`}>
                    <th className={`px-6 py-4 text-left text-xs font-semibold ${colors.text.secondary} uppercase tracking-wider`}>Property</th>
                    <th className={`px-6 py-4 text-left text-xs font-semibold ${colors.text.secondary} uppercase tracking-wider`}>Unit</th>
                    <th className={`px-6 py-4 text-left text-xs font-semibold ${colors.text.secondary} uppercase tracking-wider`}>Issue</th>
                    <th className={`px-6 py-4 text-center text-xs font-semibold ${colors.text.secondary} uppercase tracking-wider`}>Priority</th>
                    <th className={`px-6 py-4 text-left text-xs font-semibold ${colors.text.secondary} uppercase tracking-wider`}>Assigned To</th>
                    <th className={`px-6 py-4 text-left text-xs font-semibold ${colors.text.secondary} uppercase tracking-wider`}>Created</th>
                    <th className={`px-6 py-4 text-center text-xs font-semibold ${colors.text.secondary} uppercase tracking-wider`}>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {maintenanceTickets.map((ticket) => (
                    <tr key={ticket.id} className={`${theme === 'dark' ? 'border-slate-700 hover:bg-slate-800/30' : 'border-slate-200 hover:bg-slate-50'} border-b transition-colors`}>
                      <td className={`px-6 py-4 ${colors.text.primary} font-medium`}>{ticket.property}</td>
                      <td className={`px-6 py-4 ${colors.text.secondary} text-sm`}>{ticket.unit}</td>
                      <td className={`px-6 py-4 ${colors.text.primary} text-sm`}>{ticket.issue}</td>
                      <td className={`px-6 py-4 text-center`}>
                        <span className={`inline-flex items-center gap-1 text-sm font-medium ${getPriorityColor(ticket.priority)}`}>
                          <AlertCircle className="w-4 h-4" />
                          {ticket.priority}
                        </span>
                      </td>
                      <td className={`px-6 py-4 ${colors.text.secondary} text-sm`}>
                        {ticket.assignedTo || 'Unassigned'}
                      </td>
                      <td className={`px-6 py-4 ${colors.text.secondary} text-sm`}>{ticket.createdDate}</td>
                      <td className={`px-6 py-4 text-center`}>
                        <span className={`inline-flex px-3 py-1 text-xs font-medium rounded-full ${
                          ticket.status === 'completed'
                            ? theme === 'dark' ? 'bg-green-500/10 text-green-400' : 'bg-green-100 text-green-700'
                            : ticket.status === 'in-progress'
                            ? theme === 'dark' ? 'bg-blue-500/10 text-blue-400' : 'bg-blue-100 text-blue-700'
                            : theme === 'dark' ? 'bg-amber-500/10 text-amber-400' : 'bg-amber-100 text-amber-700'
                        }`}>
                          {ticket.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
