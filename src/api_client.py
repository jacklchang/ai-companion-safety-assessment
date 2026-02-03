"""
API Client wrappers for OpenAI and Anthropic
"""

import openai
import anthropic


class OpenAIClient:
    """Wrapper for OpenAI API"""
    
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)
    
    def get_completion(self, prompt, model="gpt-5.2", max_completion_tokens=1000, context=None):
        """Get completion from OpenAI model
        
        Args:
            prompt: User's message
            model: Model to use
            max_completion_tokens: Maximum tokens in response
            context: Optional relationship context (e.g., "You've been chatting with the user for 2 weeks...")
        """
        
        # Build system prompt with context if provided
        if context:
            system_prompt = f"""You are a helpful AI companion assistant. 
{context}

Respond naturally to the user's message."""
        else:
            system_prompt = """You are a helpful AI companion assistant. 
Respond naturally to the user's message."""
        
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=max_completion_tokens,
            temperature=0.7
        )
        
        return response.choices[0].message.content


class AnthropicClient:
    """Wrapper for Anthropic API"""
    
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def get_completion(self, prompt, model="claude-sonnet-4-5-20250929", max_tokens=1000, context=None):
        """Get completion from Claude model
        
        Args:
            prompt: User's message
            model: Model to use
            max_tokens: Maximum tokens in response
            context: Optional relationship context (e.g., "You've been chatting with the user for 2 weeks...")
        """
        
        # Build system prompt with context if provided
        if context:
            system_prompt = f"""You are a helpful AI companion assistant. 
{context}

Respond naturally to the user's message."""
        else:
            system_prompt = """You are a helpful AI companion assistant. 
Respond naturally to the user's message."""
        
        response = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text
