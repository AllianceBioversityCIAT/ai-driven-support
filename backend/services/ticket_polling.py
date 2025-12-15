"""
Automatic Ticket Polling Service
Polls FreshService for new tickets and analyzes them automatically
"""
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Set
from config import config
from api.freshservice_client import FreshServiceClient
from services.ai_analyzer import TicketAnalyzer
from infrastructure.notifications import SlackNotificationService

logger = logging.getLogger(__name__)


class TicketPollingService:
    """Service that polls FreshService for new tickets and analyzes them"""
    
    def __init__(self):
        self.processed_tickets: Set[str] = set()
        self.service_start_time = None  # Will be set when service starts
        self.last_check = None
        self.running = False
        
    async def start(self):
        """Start the polling service"""
        if not config.AUTO_ANALYZE_ENABLED:
            logger.info("[POLLING] Auto-analysis is disabled, not starting polling service")
            return
            
        if not config.AUTO_ANALYZE_GROUP_IDS or not any(config.AUTO_ANALYZE_GROUP_IDS):
            logger.info("[POLLING] No groups configured for auto-analysis")
            return
        
        self.running = True
        self.service_start_time = datetime.now()  # IMPORTANT: Only analyze tickets after this time
        self.last_check = self.service_start_time
        
        logger.info(f"[POLLING] 🚀 Starting ticket polling service")
        logger.info(f"[POLLING] ⏰ Service started at: {self.service_start_time.isoformat()}")
        logger.info(f"[POLLING] ⚠️  Will ONLY analyze tickets created AFTER this time")
        logger.info(f"[POLLING] Monitoring groups: {config.AUTO_ANALYZE_GROUP_IDS}")
        logger.info(f"[POLLING] Check interval: {config.POLLING_INTERVAL_SECONDS} seconds")
        
        while self.running:
            try:
                await self.check_new_tickets()
                await asyncio.sleep(config.POLLING_INTERVAL_SECONDS)
            except Exception as e:
                logger.error(f"[POLLING] ❌ Error in polling loop: {str(e)}")
                await asyncio.sleep(60)  # Wait 1 minute on error
    
    def stop(self):
        """Stop the polling service"""
        logger.info("[POLLING] 🛑 Stopping ticket polling service")
        self.running = False
    
    async def check_new_tickets(self):
        """Check for new tickets in configured groups"""
        try:
            logger.info("[POLLING] 🔍 Checking for new tickets...")
            
            client = FreshServiceClient(
                api_key=config.FRESHSERVICE_API_KEY,
                domain=config.FRESHSERVICE_DOMAIN
            )
            
            # Get configured group IDs
            group_ids = [g.strip() for g in config.AUTO_ANALYZE_GROUP_IDS if g.strip()]
            
            new_tickets_found = 0
            
            for group_id in group_ids:
                logger.info(f"[POLLING] Checking group {group_id}...")
                
                # Get tickets for this group (first page only, most recent)
                result = client.get_tickets(
                    group_id=int(group_id),
                    page=1,
                    per_page=30
                )
                
                tickets = result.get("tickets", [])
                logger.info(f"[POLLING] Found {len(tickets)} total tickets in group {group_id}")
                
                for ticket in tickets:
                    ticket_id = str(ticket.get("id"))
                    created_at_str = ticket.get("created_at", "")
                    
                    # Skip if already processed
                    if ticket_id in self.processed_tickets:
                        continue
                    
                    # CRITICAL: Only analyze tickets created AFTER service started
                    try:
                        # Parse ticket creation time
                        ticket_created = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
                        # Remove timezone info for comparison
                        ticket_created_naive = ticket_created.replace(tzinfo=None)
                        
                        # Check if ticket was created BEFORE service started
                        if ticket_created_naive < self.service_start_time:
                            logger.debug(f"[POLLING] ⏭️  Skipping old ticket {ticket_id} (created {ticket_created_naive} < service start {self.service_start_time})")
                            self.processed_tickets.add(ticket_id)  # Mark as processed to skip next time
                            continue
                        
                        # Check if ticket was created before last check
                        if ticket_created_naive < self.last_check:
                            logger.debug(f"[POLLING] ⏭️  Skipping ticket {ticket_id} (created before last check)")
                            self.processed_tickets.add(ticket_id)
                            continue
                            
                    except Exception as e:
                        logger.warning(f"[POLLING] ⚠️  Could not parse date for ticket {ticket_id}: {e}")
                        # If we can't parse the date, skip this ticket to be safe
                        self.processed_tickets.add(ticket_id)
                        continue
                    
                    # New ticket found!
                    logger.info(f"[POLLING] 🆕 NEW TICKET DETECTED: {ticket_id} (created at {ticket_created_naive})")
                    new_tickets_found += 1
                    
                    # Analyze ticket
                    await self.analyze_ticket(ticket_id, group_id, ticket)
                    
                    # Mark as processed
                    self.processed_tickets.add(ticket_id)
            
            # Update last check time
            self.last_check = datetime.now()
            
            if new_tickets_found > 0:
                logger.info(f"[POLLING] ✅ Processed {new_tickets_found} new tickets")
            else:
                logger.info(f"[POLLING] ✅ No new tickets (only tickets created after {self.service_start_time.strftime('%Y-%m-%d %H:%M:%S')} will be analyzed)")
                
        except Exception as e:
            logger.error(f"[POLLING] ❌ Error checking tickets: {str(e)}")
    
    async def analyze_ticket(self, ticket_id: str, group_id: str, ticket_data: dict = None):
        """Analyze a ticket and send to Slack"""
        try:
            logger.info(f"[POLLING] 🤖 Analyzing ticket {ticket_id}...")
            
            # If we don't have full ticket data, fetch it
            if not ticket_data or not ticket_data.get("description"):
                client = FreshServiceClient(
                    api_key=config.FRESHSERVICE_API_KEY,
                    domain=config.FRESHSERVICE_DOMAIN
                )
                ticket_data = client.get_ticket(ticket_id)
                
                if not ticket_data:
                    logger.error(f"[POLLING] ❌ Could not fetch ticket {ticket_id}")
                    return
            
            # Analyze ticket
            analyzer = TicketAnalyzer()
            analysis = analyzer.analyze_ticket(ticket_data)
            
            if analysis.get("status") != "success":
                logger.error(f"[POLLING] ❌ Analysis failed for ticket {ticket_id}")
                return
            
            logger.info(f"[POLLING] ✅ Analysis complete for ticket {ticket_id}")
            
            # Send to Slack
            if config.SLACK_WEBHOOK_URL:
                slack_service = SlackNotificationService(config.SLACK_WEBHOOK_URL)
                success = slack_service.send_ticket_analysis(
                    ticket_id,
                    analysis["analysis"],
                    domain=config.FRESHSERVICE_DOMAIN
                )
                
                if success:
                    logger.info(f"[POLLING] 📨 Slack notification sent for ticket {ticket_id}")
                else:
                    logger.error(f"[POLLING] ❌ Failed to send Slack notification")
            else:
                logger.warning(f"[POLLING] ⚠️ Slack webhook not configured")
                
        except Exception as e:
            logger.error(f"[POLLING] ❌ Error analyzing ticket {ticket_id}: {str(e)}")


# Global polling service instance
polling_service = TicketPollingService()
