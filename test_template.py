#!/usr/bin/env python3
"""
Test script to debug template rendering issue
"""
import os
import sys
sys.path.append('/Users/cuishaoyang/Desktop/KaiTeam/Mod_fixer/MCPs/myTarot')

from prompt_manager import prompt_manager

# Test data
test_question = "What should I focus on today?"
test_cards = [
    {'name': 'The Magician', 'orientation': 'Upright'},
    {'name': 'Three of Cups', 'orientation': 'Reversed'},
    {'name': 'The Star', 'orientation': 'Upright'}
]

print("Testing template rendering...")
print(f"Question: {test_question}")
print(f"Cards: {test_cards}")
print("\n" + "="*50)

try:
    # Test template rendering directly
    rendered_prompt = prompt_manager.render_prompt(
        'tarot_reading.md',
        question=test_question,
        cards=test_cards
    )
    
    if rendered_prompt:
        print("Template rendered successfully!")
        print("\nRendered prompt:")
        print("-" * 30)
        print(rendered_prompt)
    else:
        print("Template rendering returned empty string")
        
except Exception as e:
    print(f"Error during template rendering: {e}")
    import traceback
    traceback.print_exc()