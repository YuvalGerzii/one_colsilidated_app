"""
Branding Manager

Custom branding for white-label tenants.
Allows partners to fully customize the platform appearance.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class ColorPalette:
    """Color scheme for branding"""
    primary: str = "#3b82f6"       # Primary brand color
    secondary: str = "#10b981"     # Secondary color
    accent: str = "#8b5cf6"        # Accent color
    background: str = "#0f172a"    # Background color
    surface: str = "#1e293b"       # Card/surface color
    text_primary: str = "#f8fafc"  # Primary text
    text_secondary: str = "#94a3b8" # Secondary text
    success: str = "#22c55e"
    warning: str = "#f59e0b"
    error: str = "#ef4444"
    info: str = "#3b82f6"


@dataclass
class Typography:
    """Typography settings"""
    font_family: str = "Inter, system-ui, sans-serif"
    heading_font: str = "Inter, system-ui, sans-serif"
    code_font: str = "JetBrains Mono, monospace"
    base_size: str = "16px"
    scale_ratio: float = 1.25


@dataclass
class LogoConfig:
    """Logo configuration"""
    primary_logo_url: Optional[str] = None
    favicon_url: Optional[str] = None
    logo_dark_url: Optional[str] = None  # For light backgrounds
    logo_height: str = "40px"
    show_company_name: bool = True


@dataclass
class BrandTheme:
    """Complete brand theme configuration"""
    theme_id: str
    tenant_id: str
    name: str

    # Visual identity
    colors: ColorPalette = field(default_factory=ColorPalette)
    typography: Typography = field(default_factory=Typography)
    logos: LogoConfig = field(default_factory=LogoConfig)

    # Company info
    company_name: str = "Platform"
    company_tagline: str = ""
    support_email: str = ""
    support_url: str = ""

    # Custom content
    login_title: str = "Welcome Back"
    login_subtitle: str = "Sign in to continue"
    dashboard_welcome: str = "Welcome to your dashboard"

    # Footer
    footer_text: str = ""
    footer_links: List[Dict[str, str]] = field(default_factory=list)

    # Meta
    page_title_template: str = "{page} | {company}"
    meta_description: str = ""

    # Custom CSS
    custom_css: str = ""

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


class BrandingManager:
    """
    Manages branding themes for white-label tenants.

    Features:
    - Theme creation and management
    - CSS generation
    - Asset management
    - Theme previews
    """

    def __init__(self):
        self.themes: Dict[str, BrandTheme] = {}

    async def create_theme(
        self,
        tenant_id: str,
        name: str,
        config: Optional[Dict[str, Any]] = None
    ) -> BrandTheme:
        """Create a new brand theme"""

        theme_id = f"theme_{tenant_id}_{datetime.now().timestamp()}"

        theme = BrandTheme(
            theme_id=theme_id,
            tenant_id=tenant_id,
            name=name
        )

        # Apply custom configuration
        if config:
            theme = self._apply_config(theme, config)

        self.themes[theme_id] = theme
        logger.info(f"Created theme {theme_id} for tenant {tenant_id}")

        return theme

    def _apply_config(
        self,
        theme: BrandTheme,
        config: Dict[str, Any]
    ) -> BrandTheme:
        """Apply configuration to theme"""

        # Colors
        if "colors" in config:
            for key, value in config["colors"].items():
                if hasattr(theme.colors, key):
                    setattr(theme.colors, key, value)

        # Typography
        if "typography" in config:
            for key, value in config["typography"].items():
                if hasattr(theme.typography, key):
                    setattr(theme.typography, key, value)

        # Logos
        if "logos" in config:
            for key, value in config["logos"].items():
                if hasattr(theme.logos, key):
                    setattr(theme.logos, key, value)

        # Company info
        for field in ["company_name", "company_tagline", "support_email",
                      "support_url", "login_title", "login_subtitle",
                      "dashboard_welcome", "footer_text", "page_title_template",
                      "meta_description", "custom_css"]:
            if field in config:
                setattr(theme, field, config[field])

        if "footer_links" in config:
            theme.footer_links = config["footer_links"]

        return theme

    async def get_theme(self, theme_id: str) -> Optional[BrandTheme]:
        """Get theme by ID"""
        return self.themes.get(theme_id)

    async def get_tenant_theme(self, tenant_id: str) -> Optional[BrandTheme]:
        """Get active theme for a tenant"""
        for theme in self.themes.values():
            if theme.tenant_id == tenant_id:
                return theme
        return None

    async def update_theme(
        self,
        theme_id: str,
        updates: Dict[str, Any]
    ) -> BrandTheme:
        """Update an existing theme"""

        if theme_id not in self.themes:
            raise ValueError(f"Theme {theme_id} not found")

        theme = self.themes[theme_id]
        theme = self._apply_config(theme, updates)
        theme.updated_at = datetime.now()

        return theme

    async def delete_theme(self, theme_id: str):
        """Delete a theme"""
        if theme_id in self.themes:
            del self.themes[theme_id]
            logger.info(f"Deleted theme {theme_id}")

    def generate_css(self, theme: BrandTheme) -> str:
        """Generate CSS variables from theme"""

        css = f"""
:root {{
    /* Colors */
    --color-primary: {theme.colors.primary};
    --color-secondary: {theme.colors.secondary};
    --color-accent: {theme.colors.accent};
    --color-background: {theme.colors.background};
    --color-surface: {theme.colors.surface};
    --color-text-primary: {theme.colors.text_primary};
    --color-text-secondary: {theme.colors.text_secondary};
    --color-success: {theme.colors.success};
    --color-warning: {theme.colors.warning};
    --color-error: {theme.colors.error};
    --color-info: {theme.colors.info};

    /* Typography */
    --font-family: {theme.typography.font_family};
    --font-heading: {theme.typography.heading_font};
    --font-code: {theme.typography.code_font};
    --font-size-base: {theme.typography.base_size};

    /* Logo */
    --logo-height: {theme.logos.logo_height};
}}

/* Custom CSS */
{theme.custom_css}
"""
        return css

    def generate_theme_config(self, theme: BrandTheme) -> Dict[str, Any]:
        """Generate theme configuration for frontend"""

        return {
            "theme_id": theme.theme_id,
            "company": {
                "name": theme.company_name,
                "tagline": theme.company_tagline,
                "support_email": theme.support_email,
                "support_url": theme.support_url
            },
            "logos": {
                "primary": theme.logos.primary_logo_url,
                "favicon": theme.logos.favicon_url,
                "dark": theme.logos.logo_dark_url,
                "height": theme.logos.logo_height,
                "show_name": theme.logos.show_company_name
            },
            "colors": {
                "primary": theme.colors.primary,
                "secondary": theme.colors.secondary,
                "accent": theme.colors.accent,
                "background": theme.colors.background,
                "surface": theme.colors.surface,
                "text": {
                    "primary": theme.colors.text_primary,
                    "secondary": theme.colors.text_secondary
                },
                "status": {
                    "success": theme.colors.success,
                    "warning": theme.colors.warning,
                    "error": theme.colors.error,
                    "info": theme.colors.info
                }
            },
            "typography": {
                "fontFamily": theme.typography.font_family,
                "headingFont": theme.typography.heading_font,
                "codeFont": theme.typography.code_font,
                "baseSize": theme.typography.base_size
            },
            "content": {
                "login": {
                    "title": theme.login_title,
                    "subtitle": theme.login_subtitle
                },
                "dashboard": {
                    "welcome": theme.dashboard_welcome
                }
            },
            "footer": {
                "text": theme.footer_text,
                "links": theme.footer_links
            },
            "meta": {
                "titleTemplate": theme.page_title_template,
                "description": theme.meta_description
            }
        }

    async def clone_theme(
        self,
        source_theme_id: str,
        target_tenant_id: str,
        new_name: str
    ) -> BrandTheme:
        """Clone a theme for another tenant"""

        if source_theme_id not in self.themes:
            raise ValueError(f"Source theme {source_theme_id} not found")

        source = self.themes[source_theme_id]

        # Create new theme with copied properties
        new_theme = await self.create_theme(target_tenant_id, new_name)

        # Copy all properties
        new_theme.colors = ColorPalette(
            primary=source.colors.primary,
            secondary=source.colors.secondary,
            accent=source.colors.accent,
            background=source.colors.background,
            surface=source.colors.surface,
            text_primary=source.colors.text_primary,
            text_secondary=source.colors.text_secondary,
            success=source.colors.success,
            warning=source.colors.warning,
            error=source.colors.error,
            info=source.colors.info
        )

        new_theme.typography = Typography(
            font_family=source.typography.font_family,
            heading_font=source.typography.heading_font,
            code_font=source.typography.code_font,
            base_size=source.typography.base_size,
            scale_ratio=source.typography.scale_ratio
        )

        return new_theme

    def get_preset_themes(self) -> List[Dict[str, Any]]:
        """Get list of preset themes"""

        return [
            {
                "id": "default_dark",
                "name": "Default Dark",
                "preview": {
                    "primary": "#3b82f6",
                    "background": "#0f172a"
                }
            },
            {
                "id": "professional_light",
                "name": "Professional Light",
                "preview": {
                    "primary": "#2563eb",
                    "background": "#ffffff"
                }
            },
            {
                "id": "emerald",
                "name": "Emerald",
                "preview": {
                    "primary": "#10b981",
                    "background": "#0f172a"
                }
            },
            {
                "id": "purple_haze",
                "name": "Purple Haze",
                "preview": {
                    "primary": "#8b5cf6",
                    "background": "#1e1b4b"
                }
            },
            {
                "id": "sunset",
                "name": "Sunset",
                "preview": {
                    "primary": "#f97316",
                    "background": "#1c1917"
                }
            }
        ]
