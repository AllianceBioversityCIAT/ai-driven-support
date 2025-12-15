"""
AWS Bedrock AI Provider
Implements AI analysis using AWS Bedrock Claude models
"""
import logging
from typing import Optional, Dict, Any
import json
import boto3
import os
import re

logger = logging.getLogger(__name__)


class BedrockAIProvider:
    """AWS Bedrock AI provider for ticket analysis"""

    def __init__(self, aws_access_key: Optional[str] = None, aws_secret_key: Optional[str] = None):
        """
        Initialize AWS Bedrock client

        Args:
            aws_access_key: AWS Access Key (defaults to AWS_ACCESS_KEY env var)
            aws_secret_key: AWS Secret Key (defaults to AWS_SECRET_ACCESS_KEY env var)
        """
        self.aws_access_key = aws_access_key or os.getenv("AWS_ACCESS_KEY")
        self.aws_secret_key = aws_secret_key or os.getenv("AWS_SECRET_ACCESS_KEY")

        if not self.aws_access_key or not self.aws_secret_key:
            logger.warning("AWS credentials not configured")
            self.client = None
        else:
            try:
                self.client = boto3.client(
                    'bedrock-runtime',
                    region_name='us-east-1',
                    aws_access_key_id=self.aws_access_key,
                    aws_secret_access_key=self.aws_secret_key
                )
                logger.info("[AI] AWS Bedrock client initialized")
            except Exception as e:
                logger.error(f"[AI] Failed to initialize AWS Bedrock: {str(e)}")
                self.client = None

    def analyze(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """
        Analyze content using Bedrock Claude

        Args:
            system_prompt: System instructions
            user_prompt: User content to analyze

        Returns:
            Analysis result dictionary
        """
        if not self.client:
            raise ValueError("AWS Bedrock client not initialized")

        try:
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "system": system_prompt,
                "messages": [
                    {"role": "user", "content": user_prompt}
                ]
            }

            response = self.client.invoke_model(
                modelId="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                body=json.dumps(body)
            )

            response_body = json.loads(response['body'].read())
            response_text = response_body.get('content', [{}])[0].get('text', '').strip()
            
            if not response_text:
                logger.error(f"[AI] Empty response text. Full response: {response_body}")
                raise ValueError("Empty response text from Bedrock model")

            logger.info(f"[AI] Response text: {response_text[:200]}")
            
            # Extract JSON from markdown code blocks if present
            json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                json_str = response_text
            
            return json.loads(json_str)

        except json.JSONDecodeError as e:
            logger.error(f"[AI] JSON parsing error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"[AI] Error calling Bedrock: {str(e)}")
            raise
