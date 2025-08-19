"""
Prompt management system for Tarot Reading
Simple template loading and OpenAI API integration
"""

import os
from typing import Dict, List
from jinja2 import Template
import openai

def load_prompt_from_template(template_path, params):
    """Simple template loading function"""
    with open(template_path, 'r', encoding='utf-8') as file:
        template_content = file.read()
    template = Template(template_content)
    return template.render(params)

class PromptManager:
    """Simple prompt manager for OpenAI API calls"""
    
    def __init__(self, prompts_dir: str = None):
        if prompts_dir is None:
            prompts_dir = os.path.join(os.path.dirname(__file__), 'prompts')
        self.prompts_dir = prompts_dir
        
        # Check for OpenAI API key
        if not os.getenv('OPENAI_API_KEY'):
            print("Warning: OPENAI_API_KEY not found in environment variables")
    
    def get_tarot_reading_sync(self, question: str, cards: List[Dict[str, str]]) -> str:
        """Get tarot reading using simple template loading"""
        try:
            # Load and render template
            # print(f"Cards: {cards}")
            template_path = os.path.join(self.prompts_dir, 'tarot_reading.md')
            params = {
                'question': question,
                'cards': cards
            }
            
            prompt = load_prompt_from_template(template_path, params)
            # print(f"Rendered Prompt:\n{prompt}\n{'-'*40}")
            
            if not prompt:
                return self._get_fallback_reading()
            
            # Initialize OpenAI client
            client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            
            # Call OpenAI API
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=1400,
                temperature=0.8
            )
            
            reading = response.choices[0].message.content.strip()
            return reading
            
        except Exception as e:
            print(f"Error getting tarot reading: {e}")
            return self._get_fallback_reading()
    
    def _get_fallback_reading(self) -> str:
        """Fallback reading when API fails"""
        return """Trust in your intuition and follow your heart. The cards have spoken through the ancient wisdom that flows within you.

相信你的直觉，跟随你的内心。卡牌已通过你内心流淌的古老智慧为你指引。"""


# Global instance
prompt_manager = PromptManager()


if __name__ == "__main__":
    # Example usage
    # question = "What does my future hold?"
    # cards = [
    #     {"name": "The Fool", "meaning": "New beginnings, adventure"},
    #     {"name": "The Magician", "meaning": "Manifestation, resourcefulness"},
    #     {"name": "The High Priestess", "meaning": "Intuition, unconscious knowledge"}
    # ]
    # params = {
    #     "question": question,
    #     "cards": cards
    # }
    
    # reading = load_prompt_from_template('prompts/tarot_reading.md', params)

    # print(f"Tarot Reading:\n{reading}")
    pass