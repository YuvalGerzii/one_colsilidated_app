import React from 'react';
import { Box, Paper, Typography, Divider, alpha } from '@mui/material';
import { useAppTheme } from '../../contexts/ThemeContext';
import {
  CheckCircle as CheckCircleIcon,
  Cancel as CancelIcon,
  TrendingUp as TrendingUpIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
} from '@mui/icons-material';

interface MarkdownViewerProps {
  content: string;
}

export const MarkdownViewer: React.FC<MarkdownViewerProps> = ({ content }) => {
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';

  // Enhanced markdown parsing with better visual styling
  const parseMarkdown = (text: string) => {
    const lines = text.split('\n');
    const elements: JSX.Element[] = [];
    let inCodeBlock = false;
    let codeBlockContent: string[] = [];
    let inTable = false;
    let tableRows: string[][] = [];
    let listItems: string[] = [];
    let inList = false;
    let listType: 'ul' | 'ol' = 'ul';
    let currentKey = 0;

    const flushList = () => {
      if (inList && listItems.length > 0) {
        const ListComponent = listType === 'ol' ? 'ol' : 'ul';
        elements.push(
          <Box
            key={`list-${currentKey++}`}
            component={ListComponent}
            sx={{
              pl: 3,
              my: 2,
              '& li': {
                mb: 1,
                lineHeight: 1.8,
                '&::marker': {
                  color: isDark ? '#60a5fa' : '#2563eb',
                  fontWeight: 600,
                },
              },
            }}
          >
            {listItems.map((item, idx) => (
              <li key={idx}>
                <Typography variant="body2" component="span" sx={{ color: isDark ? 'rgba(255,255,255,0.87)' : 'rgba(0,0,0,0.87)' }}>
                  {parseInlineMarkdown(item)}
                </Typography>
              </li>
            ))}
          </Box>
        );
        listItems = [];
        inList = false;
      }
    };

    const flushCodeBlock = () => {
      if (inCodeBlock && codeBlockContent.length > 0) {
        elements.push(
          <Paper
            key={`code-${currentKey++}`}
            elevation={0}
            sx={{
              my: 3,
              p: 3,
              bgcolor: isDark ? 'rgba(0, 0, 0, 0.4)' : 'rgba(0, 0, 0, 0.04)',
              border: `1px solid ${isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)'}`,
              borderRadius: 2,
              overflow: 'auto',
            }}
          >
            <Typography
              component="pre"
              sx={{
                fontFamily: '"Fira Code", "JetBrains Mono", "SF Mono", Monaco, Consolas, monospace',
                fontSize: '0.875rem',
                lineHeight: 1.7,
                margin: 0,
                color: isDark ? '#93c5fd' : '#1e40af',
                whiteSpace: 'pre',
              }}
            >
              {codeBlockContent.join('\n')}
            </Typography>
          </Paper>
        );
        codeBlockContent = [];
        inCodeBlock = false;
      }
    };

    const flushTable = () => {
      if (inTable && tableRows.length > 0) {
        elements.push(
          <Box
            key={`table-${currentKey++}`}
            sx={{
              my: 3,
              overflowX: 'auto',
              borderRadius: 2,
              border: `1px solid ${isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)'}`,
            }}
          >
            <Box
              component="table"
              sx={{
                width: '100%',
                borderCollapse: 'collapse',
                '& th': {
                  bgcolor: isDark ? 'rgba(59, 130, 246, 0.15)' : 'rgba(59, 130, 246, 0.08)',
                  color: isDark ? '#93c5fd' : '#1e40af',
                  fontWeight: 700,
                  fontSize: '0.875rem',
                  textAlign: 'left',
                  p: 2,
                  borderBottom: `2px solid ${isDark ? 'rgba(59, 130, 246, 0.3)' : 'rgba(59, 130, 246, 0.2)'}`,
                },
                '& td': {
                  p: 2,
                  fontSize: '0.875rem',
                  borderBottom: `1px solid ${isDark ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)'}`,
                  color: isDark ? 'rgba(255,255,255,0.87)' : 'rgba(0,0,0,0.87)',
                },
                '& tr:hover td': {
                  bgcolor: isDark ? 'rgba(255, 255, 255, 0.02)' : 'rgba(0, 0, 0, 0.02)',
                },
              }}
            >
              <thead>
                <tr>
                  {tableRows[0].map((cell, idx) => (
                    <th key={idx}>{parseInlineMarkdown(cell.trim())}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {tableRows.slice(2).map((row, rowIdx) => (
                  <tr key={rowIdx}>
                    {row.map((cell, cellIdx) => (
                      <td key={cellIdx}>{parseInlineMarkdown(cell.trim())}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </Box>
          </Box>
        );
        tableRows = [];
        inTable = false;
      }
    };

    const parseInlineMarkdown = (text: string): React.ReactNode => {
      // Bold
      text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
      // Italic
      text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');
      // Inline code
      text = text.replace(/`(.+?)`/g, `<code style="background: ${isDark ? 'rgba(59, 130, 246, 0.2)' : 'rgba(59, 130, 246, 0.1)'}; color: ${isDark ? '#93c5fd' : '#1e40af'}; padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 0.875em;">$1</code>`);

      return <span dangerouslySetInnerHTML={{ __html: text }} />;
    };

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const trimmed = line.trim();

      // Code blocks
      if (trimmed.startsWith('```')) {
        if (inCodeBlock) {
          flushCodeBlock();
        } else {
          flushList();
          flushTable();
          inCodeBlock = true;
        }
        continue;
      }

      if (inCodeBlock) {
        codeBlockContent.push(line);
        continue;
      }

      // Tables
      if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
        if (!inTable) {
          flushList();
          inTable = true;
        }
        const cells = trimmed.split('|').filter(cell => cell.trim());
        tableRows.push(cells);
        continue;
      } else if (inTable) {
        flushTable();
      }

      // Headings
      if (trimmed.startsWith('#')) {
        flushList();
        const level = trimmed.match(/^#+/)?.[0].length || 1;
        const text = trimmed.replace(/^#+\s*/, '').replace(/\*\*/g, '');

        const headingProps = {
          1: { variant: 'h3' as const, mt: 5, mb: 3, fontWeight: 800, color: isDark ? '#60a5fa' : '#1e40af' },
          2: { variant: 'h4' as const, mt: 4, mb: 2.5, fontWeight: 700, color: isDark ? '#93c5fd' : '#2563eb' },
          3: { variant: 'h5' as const, mt: 3.5, mb: 2, fontWeight: 700, color: isDark ? '#bfdbfe' : '#3b82f6' },
          4: { variant: 'h6' as const, mt: 3, mb: 1.5, fontWeight: 600, color: isDark ? '#dbeafe' : '#60a5fa' },
        };

        const props = headingProps[Math.min(level, 4) as keyof typeof headingProps];

        elements.push(
          <Typography
            key={`heading-${currentKey++}`}
            {...props}
            sx={{
              mt: props.mt,
              mb: props.mb,
              fontWeight: props.fontWeight,
              color: props.color,
              letterSpacing: '-0.02em',
              display: 'flex',
              alignItems: 'center',
              gap: 1.5,
              '&::before': level === 1 ? {
                content: '""',
                display: 'block',
                width: 4,
                height: '1.2em',
                bgcolor: isDark ? '#60a5fa' : '#2563eb',
                borderRadius: 1,
              } : {},
            }}
          >
            {text}
          </Typography>
        );
        continue;
      }

      // Horizontal rule
      if (trimmed === '---' || trimmed === '___') {
        flushList();
        elements.push(
          <Divider
            key={`hr-${currentKey++}`}
            sx={{
              my: 4,
              borderColor: isDark ? 'rgba(59, 130, 246, 0.2)' : 'rgba(59, 130, 246, 0.15)',
              borderWidth: 2,
            }}
          />
        );
        continue;
      }

      // Lists
      const bulletMatch = trimmed.match(/^[-•\*]\s+(.+)/);
      const numberMatch = trimmed.match(/^\d+\.\s+(.+)/);

      if (bulletMatch || numberMatch) {
        if (!inList) {
          inList = true;
          listType = numberMatch ? 'ol' : 'ul';
        }
        const content = (bulletMatch || numberMatch)![1];

        // Handle checkboxes
        if (content.startsWith('[ ]')) {
          listItems.push(content.replace('[ ]', '☐'));
        } else if (content.startsWith('[x]') || content.startsWith('[X]')) {
          listItems.push(content.replace(/\[(x|X)\]/, '✓'));
        } else {
          listItems.push(content);
        }
        continue;
      } else if (inList && trimmed) {
        // Continue list item on new line
        if (listItems.length > 0) {
          listItems[listItems.length - 1] += ' ' + trimmed;
          continue;
        }
      } else if (inList) {
        flushList();
      }

      // Special callout boxes
      if (trimmed.startsWith('**') && (
        trimmed.includes('DO:') || trimmed.includes('DON\'T:') ||
        trimmed.includes('IMPORTANT:') || trimmed.includes('NOTE:') ||
        trimmed.includes('WARNING:') || trimmed.includes('TIP:')
      )) {
        flushList();
        const isPositive = trimmed.includes('DO:') || trimmed.includes('TIP:');
        const isNegative = trimmed.includes('DON\'T:') || trimmed.includes('WARNING:');
        const isInfo = trimmed.includes('NOTE:') || trimmed.includes('IMPORTANT:');

        const icon = isPositive ? <CheckCircleIcon /> : isNegative ? <CancelIcon /> : <InfoIcon />;
        const color = isPositive ? '#10b981' : isNegative ? '#ef4444' : '#3b82f6';

        elements.push(
          <Paper
            key={`callout-${currentKey++}`}
            elevation={0}
            sx={{
              my: 3,
              p: 2.5,
              bgcolor: isDark ? alpha(color, 0.1) : alpha(color, 0.05),
              border: `2px solid ${alpha(color, 0.3)}`,
              borderRadius: 2,
              display: 'flex',
              gap: 2,
              alignItems: 'flex-start',
            }}
          >
            <Box sx={{ color, mt: 0.5 }}>{icon}</Box>
            <Typography variant="body2" sx={{ fontWeight: 600, color: isDark ? 'rgba(255,255,255,0.9)' : 'rgba(0,0,0,0.87)' }}>
              {parseInlineMarkdown(trimmed.replace(/\*\*/g, ''))}
            </Typography>
          </Paper>
        );
        continue;
      }

      // Regular paragraphs
      if (trimmed) {
        flushList();
        elements.push(
          <Typography
            key={`para-${currentKey++}`}
            variant="body2"
            sx={{
              mb: 2,
              lineHeight: 1.8,
              color: isDark ? 'rgba(255,255,255,0.87)' : 'rgba(0,0,0,0.87)',
            }}
          >
            {parseInlineMarkdown(trimmed)}
          </Typography>
        );
      } else if (!inList && !inCodeBlock && !inTable) {
        // Empty line adds spacing
        elements.push(<Box key={`space-${currentKey++}`} sx={{ height: 8 }} />);
      }
    }

    // Flush any remaining content
    flushList();
    flushCodeBlock();
    flushTable();

    return elements;
  };

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', px: 2 }}>
      <Paper
        elevation={0}
        sx={{
          p: { xs: 3, sm: 4, md: 5 },
          bgcolor: isDark ? 'rgba(17, 24, 39, 0.8)' : 'rgba(255, 255, 255, 0.95)',
          border: `1px solid ${isDark ? 'rgba(59, 130, 246, 0.2)' : 'rgba(59, 130, 246, 0.15)'}`,
          borderRadius: 3,
          backdropFilter: 'blur(10px)',
          boxShadow: isDark
            ? '0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2)'
            : '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        }}
      >
        <Box
          sx={{
            '& > *:first-of-type': {
              mt: 0,
            },
            '& strong': {
              fontWeight: 700,
              color: isDark ? '#93c5fd' : '#1e40af',
            },
            '& em': {
              fontStyle: 'italic',
              color: isDark ? '#bfdbfe' : '#3b82f6',
            },
          }}
        >
          {parseMarkdown(content)}
        </Box>
      </Paper>
    </Box>
  );
};
