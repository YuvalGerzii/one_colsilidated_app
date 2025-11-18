// src/utils/formatters.ts
import numeral from 'numeral';

export const formatCurrency = (value: number | undefined | null): string => {
  if (value === undefined || value === null) return '$0';
  return numeral(value).format('$0,0');
};

export const formatCurrencyCompact = (value: number | undefined | null): string => {
  if (value === undefined || value === null) return '$0';
  return numeral(value).format('$0.0a').toUpperCase();
};

export const formatPercent = (value: number | undefined | null, decimals = 1): string => {
  if (value === undefined || value === null) return '0%';
  return numeral(value / 100).format(`0,0.${'0'.repeat(decimals)}%`);
};

export const formatMultiple = (value: number | undefined | null): string => {
  if (value === undefined || value === null) return '0.0x';
  return `${value.toFixed(1)}x`;
};

export const formatNumber = (value: number | undefined | null): string => {
  if (value === undefined || value === null) return '0';
  return numeral(value).format('0,0');
};
