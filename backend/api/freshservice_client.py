"""
FreshService API Client
Legacy adapter - use infrastructure.integrations.FreshServiceIntegration for new code
"""
import logging
from typing import Optional, List, Dict, Any
from infrastructure.integrations import FreshServiceIntegration

logger = logging.getLogger(__name__)


class FreshServiceClient(FreshServiceIntegration):
    """
    FreshService API Client - Legacy adapter
    Extends FreshServiceIntegration for backward compatibility
    """
    pass
