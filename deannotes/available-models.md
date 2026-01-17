# Models to Consider for v0.5 and beyond.

Here's answers from Claude on which models to consider for v0.5 and later versions.

The goal here is to support less expensive models for when we're smoke-testing functionality, and then use more expensive and advanced models for when we want to interrogate the transcript corpi.

## Claude Models (Recommended)

**claude-haiku-4-5-20251001** (Already using in v0.1)
- **Cost**: Input $0.80/M tokens, Output $4.00/M tokens
- **Use case**: Cheap testing, high volume queries
- **Keep as default**

**claude-sonnet-4-20250514**
- **Cost**: Input $3/M tokens, Output $15/M tokens (~4x Haiku)
- **Use case**: Better quality answers, balanced cost/quality
- **Recommended for most production use**

**claude-sonnet-4.5** (if needed)
- **Cost**: TBD (likely higher than Sonnet 4)
- **Use case**: Best quality
- **Maybe defer to v0.6 - keep v0.5 simple**

## OpenAI Models (For comparison)

**gpt-4o-mini**
- **Cost**: Input $0.15/M tokens, Output $0.60/M tokens (cheaper than Haiku!)
- **Use case**: Cost-conscious users who want OpenAI
- **Good option for high volume**

**gpt-4o**
- **Cost**: Input $2.50/M tokens, Output $10/M tokens (similar to Sonnet 4)
- **Use case**: Standard OpenAI quality
- **Direct competitor to Sonnet 4**

**Skip for v0.5:**
- GPT-4 Turbo (older, being phased out)
- o1/o1-mini (expensive reasoning models, overkill for RAG)

## Recommended v0.5 Model List

Keep it tight - **4 models total**:

1. **claude-haiku-4.5** (default, cheapest)
2. **claude-sonnet-4** (recommended, balanced)
3. **gpt-4o-mini** (cheapest OpenAI)
4. **gpt-4o** (quality OpenAI)

## CLI Implementation

```bash
# Default (Haiku)
python explore.py "What does Lenny say about pricing?"

# Specify model
python explore.py --model sonnet-4 "What does Lenny say about pricing?"
python explore.py --model gpt-4o "What does Lenny say about pricing?"
```

## Cost Comparison Table (for docs)

| Model | Per Query (est) | Quality | Speed | Use When |
|-------|----------------|---------|-------|----------|
| haiku-4.5 | $0.001 | Good | Fast | Testing, high volume |
| sonnet-4 | $0.004 | Better | Medium | Production, most use |
| gpt-4o-mini | $0.0008 | Good | Fast | Cost optimization |
| gpt-4o | $0.003 | Better | Medium | OpenAI preference |

## Why Not More?

**Discipline.** v0.5 is "model switching." Not "every model ever."

- 4 models covers the use cases
- More = decision paralysis
- Easy to add more in v0.6+ if users request

## Implementation Notes for v0.5

```python
MODELS = {
    'haiku': 'claude-haiku-4-5-20251001',
    'sonnet-4': 'claude-sonnet-4-20250514',
    'gpt-4o-mini': 'gpt-4o-mini',
    'gpt-4o': 'gpt-4o'
}
```

Simple mapping. Clear names. Done.

**ONE FEATURE: Choose your model.** Ship it. 🚀

Sleep on it. Decide in the morning if you want to adjust the list. But this gives you cheap → premium across both providers.