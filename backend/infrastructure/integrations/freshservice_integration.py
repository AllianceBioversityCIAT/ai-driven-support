"""
FreshService Integration Client
Handles all communication with FreshService API
"""
import logging
import requests
from typing import Optional, List, Dict, Any
import base64

logger = logging.getLogger(__name__)


class FreshServiceIntegration:
    """FreshService API Integration"""
    
    def __init__(self, api_key: str, domain: str):
        """
        Initialize FreshService client
        
        Args:
            api_key: FreshService API key
            domain: FreshService domain (e.g., 'alliance')
        """
        self.api_key = api_key
        self.domain = domain
        self.base_url = f"https://{domain}.freshservice.com/api/v2"
        
        auth_string = f"{api_key}:X"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        
        self.headers = {
            "Authorization": f"Basic {auth_b64}",
            "Content-Type": "application/json"
        }
        
        logger.info(f"[CLIENT] FreshService client initialized for domain: {domain}")
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request with logging"""
        url = f"{self.base_url}{endpoint}"
        
        logger.info(f"[API] {method} {url}")
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                timeout=10,
                **kwargs
            )
            
            logger.info(f"[API] Response: {response.status_code}")
            logger.debug(f"[API] Response body: {response.text[:500]}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError as e:
            logger.error(f"[API] Connection error: {str(e)}")
            raise
        except requests.exceptions.Timeout as e:
            logger.error(f"[API] Timeout error: {str(e)}")
            raise
        except requests.exceptions.HTTPError as e:
            logger.error(f"[API] HTTP error {response.status_code}: {response.text}")
            raise
        except Exception as e:
            logger.error(f"[API] Error: {str(e)}")
            raise
    
    def get_tickets(self, status: Optional[str] = None, priority: Optional[str] = None, group_id: Optional[int] = None, page: int = 1, per_page: int = 100) -> Dict[str, Any]:
        """Get tickets with pagination support"""
        try:
            logger.info(f"[TICKETS] Fetching tickets: status={status}, priority={priority}, group_id={group_id}, page={page}, per_page={per_page}")
            params = {
                "page": page,
                "per_page": per_page
            }
            
            endpoint = "/tickets"
            if group_id:
                params['query'] = f'"group_id:{group_id}"'
                endpoint = "/tickets/filter"
            
            if status:
                params['status'] = status
            if priority:
                params['priority'] = priority

            response = self._request("GET", endpoint, params=params)
            tickets = response.get("tickets", [])

            total_count = response.get("total", None)
            
            logger.info(f"[TICKETS] Found {len(tickets)} tickets on page {page}, total: {total_count}")

            if total_count is not None:
                has_more = (page * per_page) < total_count
            else:
                has_more = len(tickets) >= per_page
            
            return {
                "tickets": tickets,
                "page": page,
                "per_page": per_page,
                "total": total_count or len(tickets),
                "has_more": has_more
            }
        except Exception as e:
            logger.error(f"[TICKETS] Error getting tickets: {str(e)}")
            return {
                "tickets": [],
                "page": page,
                "per_page": per_page,
                "total": 0,
                "has_more": False
            }

    def get_all_tickets(self, status: Optional[str] = None, priority: Optional[str] = None, per_page: int = 100) -> List[Dict]:
        """Get all tickets by fetching all pages"""
        try:
            logger.info(f"[TICKETS] Fetching ALL tickets: status={status}, priority={priority}")
            all_tickets = []
            page = 1
            
            while True:
                result = self.get_tickets(status=status, priority=priority, page=page, per_page=per_page)
                tickets = result.get("tickets", [])
                
                if not tickets:
                    break
                
                all_tickets.extend(tickets)
                logger.info(f"[TICKETS] Fetched {len(all_tickets)} tickets total so far...")
                
                if not result.get("has_more", False):
                    break
                    
                page += 1
            
            logger.info(f"[TICKETS] Total tickets fetched: {len(all_tickets)}")
            return all_tickets
        except Exception as e:
            logger.error(f"[TICKETS] Error fetching all tickets: {str(e)}")
            return []

    def get_ticket(self, ticket_id: str) -> Optional[Dict]:
        """Get single ticket"""
        try:
            logger.info(f"[TICKET] Fetching ticket: {ticket_id}")
            response = self._request("GET", f"/tickets/{ticket_id}")
            ticket = response.get("ticket")
            
            if ticket:
                logger.info(f"[TICKET] Ticket {ticket_id} fetched successfully")
                logger.info(f"[TICKET] Ticket keys available: {list(ticket.keys())}")
                logger.info(f"[TICKET] Ticket ID: {ticket.get('id')}")
                logger.info(f"[TICKET] Subject: {ticket.get('subject', 'NO SUBJECT')[:100]}")
                logger.info(f"[TICKET] Description present: {bool(ticket.get('description'))}")
                logger.info(f"[TICKET] Description_text present: {bool(ticket.get('description_text'))}")
            else:
                logger.warning(f"[TICKET] Ticket {ticket_id} not found in response")
            return ticket
        except requests.exceptions.HTTPError as e:
            logger.error(f"[TICKET] HTTP error fetching ticket {ticket_id}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"[TICKET] Error fetching ticket {ticket_id}: {str(e)}")
            return None
    
    def search_tickets(self, query: str) -> List[Dict]:
        """Search tickets"""
        try:
            logger.info(f"[SEARCH] Searching tickets: {query}")
            params = {"query": f'"{query}"'}
            response = self._request("GET", "/search/tickets", params=params)
            results = response.get("results", [])
            logger.info(f"[SEARCH] Found {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"[SEARCH] Error searching tickets: {str(e)}")
            return []
    
    def get_ticket_conversations(self, ticket_id: str) -> List[Dict]:
        """Get ticket conversations"""
        try:
            logger.info(f"[CONVERSATIONS] Fetching conversations for ticket: {ticket_id}")
            response = self._request("GET", f"/tickets/{ticket_id}/conversations")
            conversations = response.get("conversations", [])
            logger.info(f"[CONVERSATIONS] Found {len(conversations)} conversations")
            return conversations
        except Exception as e:
            logger.error(f"[CONVERSATIONS] Error fetching conversations: {str(e)}")
            return []
    
    def create_ticket(self, subject: str, description: str, **kwargs) -> Optional[Dict]:
        """Create new ticket"""
        try:
            logger.info(f"[CREATE] Creating ticket: {subject}")
            data = {
                "subject": subject,
                "description": description,
                **kwargs
            }
            response = self._request("POST", "/tickets", json=data)
            ticket = response.get("ticket")
            if ticket:
                logger.info(f"[CREATE] Ticket created with ID: {ticket.get('id')}")
            return ticket
        except Exception as e:
            logger.error(f"[CREATE] Error creating ticket: {str(e)}")
            return None
    
    def update_ticket(self, ticket_id: str, **kwargs) -> Optional[Dict]:
        """Update ticket"""
        try:
            logger.info(f"[UPDATE] Updating ticket: {ticket_id}")
            response = self._request("PUT", f"/tickets/{ticket_id}", json=kwargs)
            ticket = response.get("ticket")
            if ticket:
                logger.info(f"[UPDATE] Ticket {ticket_id} updated")
            return ticket
        except Exception as e:
            logger.error(f"[UPDATE] Error updating ticket {ticket_id}: {str(e)}")
            return None
    
    def get_groups(self) -> List[Dict]:
        """Get all agent groups"""
        try:
            logger.info(f"[GROUPS] Fetching groups")
            response = self._request("GET", "/groups")
            groups = response.get("groups", [])
            logger.info(f"[GROUPS] Found {len(groups)} groups")
            return groups
        except Exception as e:
            logger.error(f"[GROUPS] Error fetching groups: {str(e)}")
            return []
