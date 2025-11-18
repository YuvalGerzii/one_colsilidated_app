import { useState } from 'react';
import { Wrench, DollarSign, Plus, Trash2 } from 'lucide-react';
import { CalculatorLayout } from './CalculatorLayout';
import { Card } from '../ui/card';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Button } from '../ui/button';
import { useTheme } from '../../contexts/ThemeContext';

interface BudgetItem {
  category: string;
  cost: number;
}

export function RenovationBudget({ onBack }: { onBack: () => void }) {
  const { theme, colors } = useTheme();
  const [items, setItems] = useState<BudgetItem[]>([
    { category: 'Kitchen', cost: 15000 },
    { category: 'Bathrooms', cost: 8000 },
    { category: 'Flooring', cost: 5000 },
    { category: 'Paint & Finishes', cost: 3000 },
    { category: 'HVAC', cost: 6000 },
  ]);

  const [contingency, setContingency] = useState(10);
  const [squareFeet, setSquareFeet] = useState(1500);

  const addItem = () => {
    setItems([...items, { category: 'New Category', cost: 0 }]);
  };

  const removeItem = (index: number) => {
    setItems(items.filter((_, i) => i !== index));
  };

  const updateItem = (index: number, field: keyof BudgetItem, value: string | number) => {
    const newItems = [...items];
    newItems[index] = { ...newItems[index], [field]: value };
    setItems(newItems);
  };

  const subtotal = items.reduce((sum, item) => sum + item.cost, 0);
  const contingencyAmount = subtotal * (contingency / 100);
  const total = subtotal + contingencyAmount;
  const costPerSqFt = squareFeet > 0 ? total / squareFeet : 0;

  const formatCurrency = (value: number) =>
    new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0 }).format(value);

  return (
    <CalculatorLayout
      title="Renovation Budget"
      description="Comprehensive construction cost estimation with line-item budgeting, contingency planning, and per-square-foot cost analysis. Track renovation expenses across multiple categories with built-in buffers for unforeseen costs."
      icon={Wrench}
      gradient="from-amber-600 to-amber-700"
      badge={`Total: ${formatCurrency(total)}`}
      badgeColor="bg-amber-600"
      onBack={onBack}
    >
      {{
        calculator: (
          <div className="grid grid-cols-12 gap-6">
            <div className="col-span-8 space-y-6">
              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-amber-500/10 rounded-xl flex items-center justify-center border border-amber-500/20">
                      <Wrench className="w-5 h-5 text-amber-400" />
                    </div>
                    <h3 className={`text-lg ${colors.text.primary}`}>Budget Line Items</h3>
                  </div>
                  <Button
                    onClick={addItem}
                    size="sm"
                    className="bg-gradient-to-r from-amber-600 to-amber-700 hover:from-amber-700 hover:to-amber-800 text-white"
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    Add Item
                  </Button>
                </div>

                <div className="space-y-3">
                  {items.map((item, index) => (
                    <div key={index} className="grid grid-cols-12 gap-3 items-center">
                      <div className="col-span-7">
                        <Input
                          value={item.category}
                          onChange={(e) => updateItem(index, 'category', e.target.value)}
                          placeholder="Category"
                          className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                        />
                      </div>
                      <div className="col-span-4">
                        <Input
                          type="number"
                          value={item.cost}
                          onChange={(e) => updateItem(index, 'cost', Number(e.target.value))}
                          placeholder="Cost"
                          className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                        />
                      </div>
                      <div className="col-span-1">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => removeItem(index)}
                          className="text-red-400 hover:text-red-300 hover:bg-red-500/10"
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </Card>

              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <h3 className={`text-lg ${colors.text.primary} mb-6`}>Project Settings</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Contingency %</Label>
                    <Input
                      type="number"
                      step="0.1"
                      value={contingency}
                      onChange={(e) => setContingency(Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                    <p className={`text-xs ${colors.text.tertiary} mt-1`}>
                      Recommended: 10-20% for unforeseen costs
                    </p>
                  </div>
                  <div>
                    <Label className={`${colors.text.secondary} mb-2 text-sm`}>Total Square Feet</Label>
                    <Input
                      type="number"
                      value={squareFeet}
                      onChange={(e) => setSquareFeet(Number(e.target.value))}
                      className={`h-11 ${colors.input} border ${colors.border.secondary} ${colors.text.primary}`}
                    />
                    <p className={`text-xs ${colors.text.tertiary} mt-1`}>
                      For cost per SF calculation
                    </p>
                  </div>
                </div>
              </Card>
            </div>

            <div className="col-span-4 space-y-6">
              <Card className="p-8 bg-gradient-to-br from-amber-600 via-amber-700 to-amber-800 border-0 shadow-2xl shadow-amber-500/20 relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent" />
                <div className="absolute top-0 right-0 w-48 h-48 bg-white/5 rounded-full blur-3xl -mr-24 -mt-24" />
                <div className="relative z-10">
                  <div className="flex items-center gap-2 mb-3">
                    <DollarSign className="w-5 h-5 text-amber-200" />
                    <h3 className="text-sm uppercase tracking-wider text-amber-200">Total Budget</h3>
                  </div>
                  <div className="text-5xl text-white mb-3">{formatCurrency(total)}</div>
                  <p className="text-sm text-amber-100">Including {contingency}% contingency</p>
                </div>
              </Card>

              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <h3 className={`text-lg ${colors.text.primary} mb-6`}>Budget Summary</h3>
                <div className="space-y-4">
                  <div className={`flex justify-between pb-3 border-b ${theme === 'dark' ? 'border-slate-700/50' : 'border-blue-100'}`}>
                    <span className={`text-sm ${colors.text.secondary}`}>Subtotal</span>
                    <span className={colors.text.primary}>{formatCurrency(subtotal)}</span>
                  </div>
                  <div className={`flex justify-between pb-3 border-b ${theme === 'dark' ? 'border-slate-700/50' : 'border-blue-100'}`}>
                    <span className={`text-sm ${colors.text.secondary}`}>Contingency ({contingency}%)</span>
                    <span className="text-amber-400">{formatCurrency(contingencyAmount)}</span>
                  </div>
                  <div className={`pt-3 border-t-2 ${theme === 'dark' ? 'border-slate-600' : 'border-blue-200'} flex justify-between`}>
                    <span className={`${colors.text.primary}`}>Total Budget</span>
                    <span className="text-lg text-green-400">{formatCurrency(total)}</span>
                  </div>
                </div>
              </Card>

              <Card className={`p-6 ${colors.card} border ${colors.border.secondary} ${theme === 'light' ? 'shadow-md' : ''}`}>
                <h3 className={`text-lg ${colors.text.primary} mb-6`}>Cost Analysis</h3>
                <div className="space-y-4">
                  <div>
                    <div className={`text-sm ${colors.text.secondary} mb-2`}>Cost Per Square Foot</div>
                    <div className="text-3xl text-amber-400">{formatCurrency(costPerSqFt)}</div>
                  </div>
                  <div>
                    <div className={`text-sm ${colors.text.secondary} mb-2`}>Number of Categories</div>
                    <div className={`text-2xl ${colors.text.primary}`}>{items.length}</div>
                  </div>
                </div>
              </Card>

              <Card className={`p-6 ${theme === 'dark' ? 'bg-gradient-to-br from-amber-900/20 to-amber-800/20 border-amber-700/30' : 'bg-amber-50 border-amber-200'}`}>
                <h3 className={`text-sm ${colors.text.primary} mb-3`}>Budget Tips</h3>
                <ul className="text-xs space-y-2 text-amber-200">
                  <li className={theme === 'light' ? 'text-amber-900' : ''}>• Always include 10-20% contingency</li>
                  <li className={theme === 'light' ? 'text-amber-900' : ''}>• Get multiple contractor quotes</li>
                  <li className={theme === 'light' ? 'text-amber-900' : ''}>• Plan for permits and inspections</li>
                  <li className={theme === 'light' ? 'text-amber-900' : ''}>• Factor in timeline delays</li>
                </ul>
              </Card>
            </div>
          </div>
        ),
        documentation: (
          <Card className={`p-8 ${colors.card} border ${colors.border.secondary} max-w-5xl`}>
            <h2 className={`text-3xl ${colors.text.primary} mb-6`}>Renovation Budget Documentation</h2>
            <div className={`${colors.text.secondary} space-y-4 leading-relaxed`}>
              <p>Track and manage renovation costs with detailed line-item budgeting and contingency planning for construction projects.</p>
            </div>
          </Card>
        ),
      }}
    </CalculatorLayout>
  );
}
