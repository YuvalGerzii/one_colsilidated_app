import { ReactNode } from 'react';
import { ArrowLeft, LucideIcon, Download, Share2, Save } from 'lucide-react';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Calculator, FileCheck, BarChart, FileText } from 'lucide-react';
import { useTheme } from '../../contexts/ThemeContext';

interface CalculatorLayoutProps {
  title: string;
  description: string;
  icon: LucideIcon;
  gradient: string;
  badge?: string;
  badgeColor?: string;
  onBack: () => void;
  children: {
    calculator: ReactNode;
    results?: ReactNode;
    charts?: ReactNode;
    documentation?: ReactNode;
  };
}

export function CalculatorLayout({
  title,
  description,
  icon: Icon,
  gradient,
  badge,
  badgeColor = 'bg-green-600',
  onBack,
  children,
}: CalculatorLayoutProps) {
  const { theme, colors } = useTheme();

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <header className={`sticky top-0 z-20 ${theme === 'dark' ? 'bg-[#0f1419]/80' : 'bg-white/80'} backdrop-blur-xl border-b ${colors.border.primary}`}>
        <div className="px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={onBack}
                className={`${theme === 'dark' ? 'hover:bg-slate-800/50 text-slate-400 hover:text-white' : 'hover:bg-slate-100 text-slate-600 hover:text-slate-900'}`}
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                All Models
              </Button>
              <div className={`w-px h-6 ${theme === 'dark' ? 'bg-slate-700/50' : 'bg-slate-300'}`} />
              <div className="flex items-center gap-3">
                <div className={`w-10 h-10 bg-gradient-to-br ${gradient} rounded-xl flex items-center justify-center shadow-lg relative`}>
                  <div className="absolute inset-0 bg-gradient-to-t from-white/20 to-transparent rounded-xl" />
                  <Icon className="w-5 h-5 text-white relative z-10" />
                </div>
                <div>
                  <h1 className={`text-lg ${colors.text.primary}`}>{title}</h1>
                  <p className={`text-xs ${colors.text.secondary}`}>Financial Model</p>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-3">
              {badge && (
                <Badge className={`${badgeColor} text-white px-4 py-1.5 text-sm border-0 shadow-lg`}>
                  {badge}
                </Badge>
              )}
              <Button 
                variant="outline" 
                size="sm" 
                className={`border ${colors.border.secondary} ${theme === 'dark' ? 'hover:bg-slate-800/50' : 'hover:bg-slate-100'} ${colors.text.primary}`}
              >
                <Save className="w-4 h-4 mr-2" />
                Save
              </Button>
              <Button 
                variant="outline" 
                size="sm" 
                className={`border ${colors.border.secondary} ${theme === 'dark' ? 'hover:bg-slate-800/50' : 'hover:bg-slate-100'} ${colors.text.primary}`}
              >
                <Share2 className="w-4 h-4 mr-2" />
                Share
              </Button>
              <Button size="sm" className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 shadow-lg shadow-blue-500/20 text-white">
                <Download className="w-4 h-4 mr-2" />
                Export PDF
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <div className="p-8 max-w-[1800px] mx-auto">
          {/* Description */}
          <div className={`mb-8 p-6 ${colors.card} border ${colors.border.secondary} rounded-2xl backdrop-blur-sm`}>
            <p className={`${colors.text.secondary} leading-relaxed`}>
              {description}
            </p>
          </div>

          {/* Tabs */}
          <Tabs defaultValue="calculator" className="w-full">
            <TabsList className={`mb-8 ${theme === 'dark' ? 'bg-gradient-to-r from-slate-800/40 to-slate-900/40' : 'bg-white'} border ${colors.border.secondary} p-1.5 rounded-2xl backdrop-blur-sm inline-flex`}>
              <TabsTrigger
                value="calculator"
                className={`flex items-center gap-2 rounded-xl px-6 py-3 transition-all data-[state=active]:bg-gradient-to-r data-[state=active]:from-blue-600 data-[state=active]:to-blue-700 data-[state=active]:text-white data-[state=active]:shadow-lg data-[state=active]:shadow-blue-500/20 ${colors.text.secondary}`}
              >
                <Calculator className="w-4 h-4" />
                Calculator
              </TabsTrigger>
              {children.results && (
                <TabsTrigger
                  value="results"
                  className={`flex items-center gap-2 rounded-xl px-6 py-3 transition-all data-[state=active]:bg-gradient-to-r data-[state=active]:from-blue-600 data-[state=active]:to-blue-700 data-[state=active]:text-white data-[state=active]:shadow-lg data-[state=active]:shadow-blue-500/20 ${colors.text.secondary}`}
                >
                  <FileCheck className="w-4 h-4" />
                  Results
                </TabsTrigger>
              )}
              {children.charts && (
                <TabsTrigger
                  value="charts"
                  className={`flex items-center gap-2 rounded-xl px-6 py-3 transition-all data-[state=active]:bg-gradient-to-r data-[state=active]:from-blue-600 data-[state=active]:to-blue-700 data-[state=active]:text-white data-[state=active]:shadow-lg data-[state=active]:shadow-blue-500/20 ${colors.text.secondary}`}
                >
                  <BarChart className="w-4 h-4" />
                  Analytics
                </TabsTrigger>
              )}
              {children.documentation && (
                <TabsTrigger
                  value="documentation"
                  className={`flex items-center gap-2 rounded-xl px-6 py-3 transition-all data-[state=active]:bg-gradient-to-r data-[state=active]:from-blue-600 data-[state=active]:to-blue-700 data-[state=active]:text-white data-[state=active]:shadow-lg data-[state=active]:shadow-blue-500/20 ${colors.text.secondary}`}
                >
                  <FileText className="w-4 h-4" />
                  Documentation
                </TabsTrigger>
              )}
            </TabsList>

            <TabsContent value="calculator" className="m-0">
              {children.calculator}
            </TabsContent>

            {children.results && (
              <TabsContent value="results" className="m-0">
                {children.results}
              </TabsContent>
            )}

            {children.charts && (
              <TabsContent value="charts" className="m-0">
                {children.charts}
              </TabsContent>
            )}

            {children.documentation && (
              <TabsContent value="documentation" className="m-0">
                {children.documentation}
              </TabsContent>
            )}
          </Tabs>
        </div>
      </div>
    </div>
  );
}