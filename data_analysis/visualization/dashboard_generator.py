"""
Dashboard Generator Module
===========================

Generate comprehensive dashboards and reports for data analysis.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path
from datetime import datetime
import json
import warnings

warnings.filterwarnings('ignore')


class DashboardGenerator:
    """
    Generate dashboards and summary reports for data analysis.
    """

    def __init__(self, title: str = 'Data Analysis Dashboard'):
        """
        Initialize dashboard generator.

        Args:
            title: Dashboard title
        """
        self.title = title
        self.sections = []
        self.metrics = {}
        self.charts = []

    def add_section(
        self,
        title: str,
        content: Union[str, Dict, pd.DataFrame],
        section_type: str = 'text'
    ) -> None:
        """
        Add a section to the dashboard.

        Args:
            title: Section title
            content: Section content
            section_type: 'text', 'table', 'metrics', or 'chart'
        """
        self.sections.append({
            'title': title,
            'content': content,
            'type': section_type
        })

    def add_metrics(
        self,
        metrics: Dict[str, Union[float, int, str]],
        title: str = 'Key Metrics'
    ) -> None:
        """
        Add key metrics to dashboard.

        Args:
            metrics: Dictionary of metric name to value
            title: Metrics section title
        """
        self.metrics[title] = metrics
        self.add_section(title, metrics, 'metrics')

    def add_table(
        self,
        df: pd.DataFrame,
        title: str = 'Data Table'
    ) -> None:
        """
        Add data table to dashboard.

        Args:
            df: DataFrame to display
            title: Table title
        """
        self.add_section(title, df, 'table')

    def add_chart_reference(
        self,
        chart_path: str,
        title: str = 'Chart'
    ) -> None:
        """
        Add chart reference to dashboard.

        Args:
            chart_path: Path to chart image
            title: Chart title
        """
        self.charts.append({
            'title': title,
            'path': chart_path
        })
        self.add_section(title, chart_path, 'chart')

    def generate_html_dashboard(
        self,
        output_path: str,
        include_styles: bool = True
    ) -> str:
        """
        Generate HTML dashboard.

        Args:
            output_path: Output HTML file path
            include_styles: Include CSS styles

        Returns:
            HTML content
        """
        styles = """
        <style>
            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .dashboard {
                max-width: 1400px;
                margin: 0 auto;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            .header h1 {
                margin: 0;
                font-size: 2.5em;
            }
            .header .timestamp {
                opacity: 0.8;
                margin-top: 10px;
            }
            .section {
                background: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .section h2 {
                color: #333;
                border-bottom: 2px solid #667eea;
                padding-bottom: 10px;
                margin-top: 0;
            }
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
            }
            .metric-card {
                background: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                border-left: 4px solid #667eea;
            }
            .metric-value {
                font-size: 2em;
                font-weight: bold;
                color: #333;
            }
            .metric-label {
                color: #666;
                font-size: 0.9em;
                margin-top: 5px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #667eea;
                color: white;
            }
            tr:hover {
                background-color: #f5f5f5;
            }
            .chart-container {
                text-align: center;
            }
            .chart-container img {
                max-width: 100%;
                border-radius: 8px;
            }
            .text-content {
                line-height: 1.6;
                color: #444;
            }
        </style>
        """ if include_styles else ""

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{self.title}</title>
            {styles}
        </head>
        <body>
            <div class="dashboard">
                <div class="header">
                    <h1>{self.title}</h1>
                    <div class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
                </div>
        """

        for section in self.sections:
            html += f"""
                <div class="section">
                    <h2>{section['title']}</h2>
            """

            if section['type'] == 'metrics':
                html += '<div class="metrics-grid">'
                for name, value in section['content'].items():
                    formatted_value = f"{value:.4f}" if isinstance(value, float) else str(value)
                    html += f"""
                        <div class="metric-card">
                            <div class="metric-value">{formatted_value}</div>
                            <div class="metric-label">{name}</div>
                        </div>
                    """
                html += '</div>'

            elif section['type'] == 'table':
                df = section['content']
                html += '<table>'
                html += '<thead><tr>'
                for col in df.columns:
                    html += f'<th>{col}</th>'
                html += '</tr></thead>'
                html += '<tbody>'
                for _, row in df.iterrows():
                    html += '<tr>'
                    for val in row:
                        formatted = f"{val:.4f}" if isinstance(val, float) else str(val)
                        html += f'<td>{formatted}</td>'
                    html += '</tr>'
                html += '</tbody></table>'

            elif section['type'] == 'chart':
                html += f"""
                    <div class="chart-container">
                        <img src="{section['content']}" alt="{section['title']}">
                    </div>
                """

            else:  # text
                html += f'<div class="text-content">{section["content"]}</div>'

            html += '</div>'

        html += """
            </div>
        </body>
        </html>
        """

        # Save HTML
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(html)

        return html

    def generate_markdown_report(
        self,
        output_path: str
    ) -> str:
        """
        Generate Markdown report.

        Args:
            output_path: Output file path

        Returns:
            Markdown content
        """
        md = f"# {self.title}\n\n"
        md += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
        md += "---\n\n"

        for section in self.sections:
            md += f"## {section['title']}\n\n"

            if section['type'] == 'metrics':
                md += "| Metric | Value |\n"
                md += "|--------|-------|\n"
                for name, value in section['content'].items():
                    formatted = f"{value:.4f}" if isinstance(value, float) else str(value)
                    md += f"| {name} | {formatted} |\n"
                md += "\n"

            elif section['type'] == 'table':
                df = section['content']
                md += df.to_markdown(index=False)
                md += "\n\n"

            elif section['type'] == 'chart':
                md += f"![{section['title']}]({section['content']})\n\n"

            else:
                md += f"{section['content']}\n\n"

        # Save
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(md)

        return md

    def generate_json_summary(
        self,
        output_path: str = None
    ) -> Dict:
        """
        Generate JSON summary of dashboard.

        Args:
            output_path: Optional output path

        Returns:
            Summary dictionary
        """
        summary = {
            'title': self.title,
            'generated_at': datetime.now().isoformat(),
            'metrics': self.metrics,
            'sections': []
        }

        for section in self.sections:
            section_data = {
                'title': section['title'],
                'type': section['type']
            }

            if section['type'] == 'metrics':
                section_data['content'] = section['content']
            elif section['type'] == 'table':
                section_data['content'] = section['content'].to_dict()
            elif section['type'] == 'chart':
                section_data['content'] = section['content']
            else:
                section_data['content'] = str(section['content'])

            summary['sections'].append(section_data)

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(summary, f, indent=2, default=str)

        return summary

    def create_executive_summary(
        self,
        data_summary: Dict,
        model_metrics: Dict,
        forecast_results: Dict = None
    ) -> str:
        """
        Create executive summary section.

        Args:
            data_summary: Data quality summary
            model_metrics: Model performance metrics
            forecast_results: Forecast results

        Returns:
            Summary text
        """
        summary = "### Executive Summary\n\n"

        # Data overview
        summary += "**Data Overview:**\n"
        if 'total_rows' in data_summary:
            summary += f"- Total records: {data_summary['total_rows']:,}\n"
        if 'total_columns' in data_summary:
            summary += f"- Total features: {data_summary['total_columns']}\n"

        # Model performance
        summary += "\n**Model Performance:**\n"
        for model, metrics in model_metrics.items():
            if 'RMSE' in metrics:
                summary += f"- {model}: RMSE = {metrics['RMSE']:.4f}"
                if 'R2' in metrics:
                    summary += f", R² = {metrics['R2']:.4f}"
                summary += "\n"

        # Forecast insights
        if forecast_results:
            summary += "\n**Forecast Insights:**\n"
            if 'forecast' in forecast_results:
                forecast = forecast_results['forecast']
                summary += f"- Forecast horizon: {len(forecast)} periods\n"
                summary += f"- Average forecast value: {np.mean(forecast):.2f}\n"

        return summary

    def create_full_analysis_dashboard(
        self,
        data_quality: Dict,
        trend_analysis: Dict,
        forecast_results: Dict,
        model_comparison: pd.DataFrame,
        output_path: str
    ) -> str:
        """
        Create comprehensive analysis dashboard.

        Args:
            data_quality: Data quality report
            trend_analysis: Trend analysis results
            forecast_results: Forecast results
            model_comparison: Model comparison DataFrame
            output_path: Output HTML path

        Returns:
            HTML content
        """
        # Executive summary
        exec_summary = "This dashboard presents a comprehensive analysis of the data, "
        exec_summary += "including data quality assessment, trend analysis, and forecasting results."
        self.add_section('Executive Summary', exec_summary, 'text')

        # Data quality metrics
        quality_metrics = {
            'Total Records': data_quality.get('total_rows', 0),
            'Total Features': data_quality.get('total_columns', 0),
            'Memory Usage (MB)': round(data_quality.get('memory_usage_mb', 0), 2)
        }
        self.add_metrics(quality_metrics, 'Data Overview')

        # Trend analysis
        if trend_analysis:
            trend_text = f"**Trend Direction:** {trend_analysis.get('trend', 'Unknown')}\n"
            if 'slope' in trend_analysis:
                trend_text += f"**Slope:** {trend_analysis['slope']:.6f}\n"
            if 'r_squared' in trend_analysis:
                trend_text += f"**R²:** {trend_analysis['r_squared']:.4f}\n"
            self.add_section('Trend Analysis', trend_text, 'text')

        # Model comparison
        if model_comparison is not None and not model_comparison.empty:
            self.add_table(model_comparison, 'Model Comparison')

        # Forecast metrics
        if forecast_results:
            forecast_metrics = {}
            if 'forecast' in forecast_results:
                forecast = forecast_results['forecast']
                forecast_metrics['Forecast Periods'] = len(forecast)
                forecast_metrics['Mean Forecast'] = round(np.mean(forecast), 2)
                forecast_metrics['Min Forecast'] = round(np.min(forecast), 2)
                forecast_metrics['Max Forecast'] = round(np.max(forecast), 2)
            self.add_metrics(forecast_metrics, 'Forecast Summary')

        return self.generate_html_dashboard(output_path)
