"""
Integration Loader - Initialize all integrations based on configuration
"""

import logging
from typing import Dict
from app.settings import settings
from .manager import integration_manager
from .base import IntegrationConfig

# Import all integrations
from .market_data import CensusBureauIntegration, BLSIntegration, FREDIntegration
from .property_data import AttomDataIntegration, RealtorIntegration
from .banking import PlaidIntegration, StripeIntegration
from .tools import SlackIntegration, GoogleDriveIntegration
from .official_data import (
    DataGovUSIntegration,
    DataGovILIntegration,
    BankOfIsraelIntegration,
    HUDIntegration,
    FHFAIntegration
)

logger = logging.getLogger(__name__)


def initialize_integrations():
    """
    Initialize all third-party integrations based on configuration

    This function is called at application startup and will gracefully
    skip integrations that don't have API keys configured.
    """
    if not settings.ENABLE_INTEGRATIONS:
        logger.info("Third-party integrations are disabled")
        return

    logger.info("Initializing third-party integrations...")

    # ========================================
    # MARKET DATA INTEGRATIONS (FREE)
    # ========================================

    # Census Bureau
    if settings.ENABLE_CENSUS_INTEGRATION:
        try:
            census_config = IntegrationConfig(
                name="Census Bureau",
                category="market_data",
                is_free=True,
                requires_api_key=False,
                api_key=settings.CENSUS_API_KEY,
                enabled=True
            )
            census = CensusBureauIntegration(census_config)
            integration_manager.register("census", census)
            logger.info(f"Census Bureau integration: {census.status.value}")
        except Exception as e:
            logger.error(f"Failed to initialize Census Bureau integration: {e}")

    # Bureau of Labor Statistics
    if settings.ENABLE_BLS_INTEGRATION:
        try:
            bls_config = IntegrationConfig(
                name="BLS",
                category="market_data",
                is_free=True,
                requires_api_key=False,
                api_key=settings.BLS_API_KEY,
                enabled=True
            )
            bls = BLSIntegration(bls_config)
            integration_manager.register("bls", bls)
            logger.info(f"BLS integration: {bls.status.value}")
        except Exception as e:
            logger.error(f"Failed to initialize BLS integration: {e}")

    # FRED (Federal Reserve Economic Data)
    if settings.ENABLE_FRED_INTEGRATION:
        try:
            fred_config = IntegrationConfig(
                name="FRED",
                category="market_data",
                is_free=True,
                requires_api_key=True,
                api_key=settings.FRED_API_KEY,
                enabled=bool(settings.FRED_API_KEY)
            )
            fred = FREDIntegration(fred_config)
            integration_manager.register("fred", fred)
            logger.info(f"FRED integration: {fred.status.value}")
        except Exception as e:
            logger.error(f"Failed to initialize FRED integration: {e}")

    # ========================================
    # PROPERTY DATA INTEGRATIONS
    # ========================================

    # ATTOM Data
    if settings.ENABLE_ATTOM_INTEGRATION:
        try:
            attom_config = IntegrationConfig(
                name="ATTOM Data",
                category="property_data",
                is_free=False,
                requires_api_key=True,
                api_key=settings.ATTOM_API_KEY,
                enabled=bool(settings.ATTOM_API_KEY)
            )
            attom = AttomDataIntegration(attom_config)
            integration_manager.register("attom", attom)
            logger.info(f"ATTOM Data integration: {attom.status.value}")
        except Exception as e:
            logger.error(f"Failed to initialize ATTOM Data integration: {e}")

    # Realtor.com (via RapidAPI)
    if settings.ENABLE_REALTOR_INTEGRATION:
        try:
            realtor_config = IntegrationConfig(
                name="Realtor.com",
                category="property_data",
                is_free=True,
                requires_api_key=True,
                api_key=settings.REALTOR_RAPIDAPI_KEY,
                enabled=bool(settings.REALTOR_RAPIDAPI_KEY)
            )
            realtor = RealtorIntegration(realtor_config)
            integration_manager.register("realtor", realtor)
            logger.info(f"Realtor.com integration: {realtor.status.value}")
        except Exception as e:
            logger.error(f"Failed to initialize Realtor.com integration: {e}")

    # ========================================
    # BANKING & PAYMENT INTEGRATIONS
    # ========================================

    # Plaid
    if settings.ENABLE_PLAID_INTEGRATION:
        try:
            plaid_config = IntegrationConfig(
                name="Plaid",
                category="banking",
                is_free=True,
                requires_api_key=True,
                api_key=settings.PLAID_CLIENT_ID,  # Using client_id as primary key
                enabled=bool(settings.PLAID_CLIENT_ID and settings.PLAID_SECRET),
                additional_config={
                    "client_id": settings.PLAID_CLIENT_ID,
                    "secret": settings.PLAID_SECRET,
                    "environment": settings.PLAID_ENVIRONMENT
                }
            )
            plaid = PlaidIntegration(plaid_config)
            integration_manager.register("plaid", plaid)
            logger.info(f"Plaid integration: {plaid.status.value}")
        except Exception as e:
            logger.error(f"Failed to initialize Plaid integration: {e}")

    # Stripe
    if settings.ENABLE_STRIPE_INTEGRATION:
        try:
            stripe_config = IntegrationConfig(
                name="Stripe",
                category="banking",
                is_free=True,
                requires_api_key=True,
                api_key=settings.STRIPE_API_KEY,
                enabled=bool(settings.STRIPE_API_KEY)
            )
            stripe = StripeIntegration(stripe_config)
            integration_manager.register("stripe", stripe)
            logger.info(f"Stripe integration: {stripe.status.value}")
        except Exception as e:
            logger.error(f"Failed to initialize Stripe integration: {e}")

    # ========================================
    # TOOLS & AUTOMATION INTEGRATIONS
    # ========================================

    # Slack
    if settings.ENABLE_SLACK_INTEGRATION:
        try:
            slack_config = IntegrationConfig(
                name="Slack",
                category="tools",
                is_free=True,
                requires_api_key=True,
                api_key=settings.SLACK_BOT_TOKEN,
                enabled=bool(settings.SLACK_BOT_TOKEN)
            )
            slack = SlackIntegration(slack_config)
            integration_manager.register("slack", slack)
            logger.info(f"Slack integration: {slack.status.value}")
        except Exception as e:
            logger.error(f"Failed to initialize Slack integration: {e}")

    # Google Drive
    if settings.ENABLE_GOOGLE_DRIVE_INTEGRATION:
        try:
            google_drive_config = IntegrationConfig(
                name="Google Drive",
                category="tools",
                is_free=True,
                requires_api_key=True,
                api_key=settings.GOOGLE_DRIVE_ACCESS_TOKEN,
                enabled=bool(settings.GOOGLE_DRIVE_ACCESS_TOKEN)
            )
            google_drive = GoogleDriveIntegration(google_drive_config)
            integration_manager.register("google_drive", google_drive)
            logger.info(f"Google Drive integration: {google_drive.status.value}")
        except Exception as e:
            logger.error(f"Failed to initialize Google Drive integration: {e}")

    # ========================================
    # OFFICIAL GOVERNMENT DATA INTEGRATIONS
    # ========================================

    # Data.gov US
    if settings.ENABLE_DATAGOV_US_INTEGRATION:
        try:
            datagov_us_config = IntegrationConfig(
                name="Data.gov US",
                category="official_data",
                is_free=True,
                requires_api_key=False,
                enabled=True
            )
            datagov_us = DataGovUSIntegration(datagov_us_config)
            integration_manager.register("datagov_us", datagov_us)
            logger.info(f"Data.gov US integration: {datagov_us.status.value}")
        except Exception as e:
            logger.error(f"Failed to initialize Data.gov US integration: {e}")

    # Data.gov Israel
    if settings.ENABLE_DATAGOV_IL_INTEGRATION:
        try:
            datagov_il_config = IntegrationConfig(
                name="Data.gov IL",
                category="official_data",
                is_free=True,
                requires_api_key=False,
                enabled=True
            )
            datagov_il = DataGovILIntegration(datagov_il_config)
            integration_manager.register("datagov_il", datagov_il)
            logger.info(f"Data.gov IL integration: {datagov_il.status.value}")
        except Exception as e:
            logger.error(f"Failed to initialize Data.gov IL integration: {e}")

    # Bank of Israel
    if settings.ENABLE_BANK_OF_ISRAEL_INTEGRATION:
        try:
            boi_config = IntegrationConfig(
                name="Bank of Israel",
                category="official_data",
                is_free=True,
                requires_api_key=False,
                enabled=True
            )
            boi = BankOfIsraelIntegration(boi_config)
            integration_manager.register("bank_of_israel", boi)
            logger.info(f"Bank of Israel integration: {boi.status.value}")
        except Exception as e:
            logger.error(f"Failed to initialize Bank of Israel integration: {e}")

    # HUD (Housing and Urban Development)
    if settings.ENABLE_HUD_INTEGRATION:
        try:
            hud_config = IntegrationConfig(
                name="HUD",
                category="official_data",
                is_free=True,
                requires_api_key=False,
                enabled=True
            )
            hud = HUDIntegration(hud_config)
            integration_manager.register("hud", hud)
            logger.info(f"HUD integration: {hud.status.value}")
        except Exception as e:
            logger.error(f"Failed to initialize HUD integration: {e}")

    # FHFA (Federal Housing Finance Agency)
    if settings.ENABLE_FHFA_INTEGRATION:
        try:
            fhfa_config = IntegrationConfig(
                name="FHFA",
                category="official_data",
                is_free=True,
                requires_api_key=False,
                enabled=True
            )
            fhfa = FHFAIntegration(fhfa_config)
            integration_manager.register("fhfa", fhfa)
            logger.info(f"FHFA integration: {fhfa.status.value}")
        except Exception as e:
            logger.error(f"Failed to initialize FHFA integration: {e}")

    # ========================================
    # SUMMARY
    # ========================================
    summary = integration_manager.get_status_summary()
    active_count = sum(1 for v in summary.values() if v["available"])
    total_count = len(summary)

    logger.info(f"Integration initialization complete: {active_count}/{total_count} integrations active")

    # Log available integrations
    if active_count > 0:
        logger.info("Active integrations:")
        for key, info in summary.items():
            if info["available"]:
                free_indicator = "FREE" if info["is_free"] else "PAID"
                logger.info(f"  - {info['name']} ({info['category']}) [{free_indicator}]")

    return integration_manager


# Export for easy importing
__all__ = ["initialize_integrations", "integration_manager"]
