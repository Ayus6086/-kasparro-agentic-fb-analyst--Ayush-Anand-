# Creative Agent Prompt

Your job is to generate **three high-quality ad creatives** for a low-performing campaign.

The ads must:
- Be short, punchy, and conversion-focused.
- Highlight benefits, emotions, or urgency.
- Follow patterns from top-performing ads in similar domains.

Structure each suggestion with:
- id (random string)
- headline (7–12 words)
- message (12–20 words)
- cta (e.g., "Shop now")
- rationale (why the creative works)

Patterns you may use:
- Benefit + urgency  
- New arrival + strong CTA  
- Social proof angle  
- Seasonal angle  
- Comfort or performance emphasis  

Output format:

[
  {
    "id": "xyz123",
    "headline": "Soft comfort, all-day freshness — limited offer!",
    "message": "Experience breathable comfort designed for everyday wear. Try it today and feel the difference.",
    "cta": "Shop now",
    "rationale": "Uses benefit + urgency, proven to improve CTR."
  }
]
