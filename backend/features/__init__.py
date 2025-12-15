"""
FreshAI Features
Screaming Architecture - Features module
"""

# This file makes it clear what this application does
# by exposing all available features

from .ticket_analysis import (
    AnalyzeTicketUseCase,
    TicketAnalysisResult,
    TicketData
)

from .ticket_management import (
    ListTicketsUseCase,
    GetTicketDetailsUseCase,
    SearchTicketsUseCase,
    Ticket,
    TicketConversation,
    TicketSearchCriteria
)

__all__ = [
    # Ticket Analysis Feature
    "AnalyzeTicketUseCase",
    "TicketAnalysisResult",
    "TicketData",
    
    # Ticket Management Feature
    "ListTicketsUseCase",
    "GetTicketDetailsUseCase",
    "SearchTicketsUseCase",
    "Ticket",
    "TicketConversation",
    "TicketSearchCriteria"
]
