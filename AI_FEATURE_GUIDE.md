# FreshAI - AI Ticket Analysis Feature

## Overview

The AI Ticket Analysis feature provides intelligent analysis of support tickets without hallucination or unfounded assumptions. It analyzes tickets based **only on explicitly stated information** and provides:

- **Summary**: Concise overview of the ticket issue
- **Possible Categories**: Categories based on ticket content with confidence levels
- **Possible Automations**: Actionable automation suggestions with feasibility assessment
- **User Sentiment**: Emotional analysis and urgency detection based on language indicators

## 🎯 Key Principles

1. **No Hallucination**: AI only analyzes what's explicitly written
2. **Conservative Assessment**: Low confidence when information is ambiguous
3. **Factual Analysis**: Based solely on ticket content
4. **Actionable Insights**: Practical suggestions for support teams

## 🚀 Getting Started

### Backend Setup

1. **Add OpenAI API Key** to your `.env` file:

```env
OPENAI_API_KEY=sk-proj-your-key-here
```

Get your OpenAI API key from: https://platform.openai.com/api-keys

2. **The AI Analyzer** uses `gpt-4o-mini` model (cost-effective and fast)

### Frontend Usage

The AI Analysis button appears in the ticket detail view. Click it to analyze the current ticket.

## 📋 API Endpoint

### Analyze Single Ticket

**Request:**

```
POST /api/tickets/{ticket_id}/analyze
```

**Response:**

```json
{
  "status": "success",
  "ticket_id": 123,
  "analysis": {
    "status": "success",
    "analysis": {
      "summary": "User experiencing network connectivity issues with intermittent disconnections occurring every 30 minutes",
      "possible_categories": [
        {
          "category": "Network Issues",
          "confidence": "high",
          "reason": "Ticket explicitly mentions network connectivity and disconnections"
        },
        {
          "category": "Hardware Problem",
          "confidence": "medium",
          "reason": "Intermittent nature could suggest hardware issues, but not explicitly stated"
        }
      ],
      "possible_automations": [
        {
          "automation": "Automatic Network Diagnostics",
          "description": "Run automated network tests and provide results to support team",
          "feasibility": "high"
        },
        {
          "automation": "Device Restart Suggestion",
          "description": "Suggest user restart their device with automated follow-up",
          "feasibility": "high"
        }
      ],
      "user_sentiment": {
        "overall_feeling": "frustrated",
        "indicators": [
          "This is getting really frustrating",
          "I've tried everything",
          "happening constantly"
        ],
        "urgency_level": "high"
      }
    }
  }
}
```

## 🔧 Configuration

### Environment Variables

| Variable               | Required | Description              |
| ---------------------- | -------- | ------------------------ |
| `OPENAI_API_KEY`       | Yes      | Your OpenAI API key      |
| `FRESHSERVICE_API_KEY` | Yes      | FreshService API key     |
| `FRESHSERVICE_DOMAIN`  | Yes      | Your FreshService domain |

### Backend Files

- **`services/ai_analyzer.py`**: Core AI analysis logic
- **`api/routes/tickets.py`**: API endpoint for analysis

### Frontend Files

- **`src/components/AIAnalysisPanel.tsx`**: UI component
- **`src/components/AIAnalysisPanel.module.css`**: Styling
- **`src/services/api.ts`**: API client method

## 📊 Analysis Output Explained

### Summary

- **What**: Concise description of the issue
- **How**: Extracted directly from ticket content
- **Confidence**: Always 100% accurate (directly from ticket text)

### Possible Categories

- **Category**: Suggested ticket category
- **Confidence Levels**:
  - **High**: Clearly mentioned or heavily implied in ticket
  - **Medium**: Related keywords present, but not explicit
  - **Low**: Tangentially related, uncertain connection
- **Reason**: Explanation of why this category was suggested

### Possible Automations

- **Automation**: What could be automated
- **Description**: How the automation would work
- **Feasibility Levels**:
  - **High**: Technically straightforward, high success rate
  - **Medium**: Possible but may require configuration
  - **Low**: Complex or uncertain effectiveness

### User Sentiment

- **Overall Feeling**:

  - `positive`: Satisfied, happy, complimentary tone
  - `neutral`: Factual, without emotion
  - `negative`: Dissatisfied, critical
  - `frustrated`: Irritated, exasperated
  - `urgent`: Time-sensitive, demanding quick action

- **Indicators**: Text snippets showing this sentiment
- **Urgency Level**:
  - `low`: Can wait, routine matter
  - `medium`: Should be addressed soon
  - `high`: Time-sensitive issue
  - `critical`: Severe impact, immediate attention needed

## 🔐 Privacy & Security

- ✅ Tickets are sent to OpenAI API for analysis
- ✅ No data is stored by FreshAI beyond the analysis result
- ✅ OpenAI processes data according to their privacy policy
- ✅ Use your own API keys (never shared)

## 💰 Cost Considerations

Using `gpt-4o-mini`:

- Average ticket analysis: ~0.002-0.005 USD
- Batch processing 1000 tickets: ~2-5 USD
- See [OpenAI Pricing](https://openai.com/pricing/) for current rates

## 🛠️ Advanced Usage

### Manual Analysis in Python

```python
from services.ai_analyzer import TicketAnalyzer

analyzer = TicketAnalyzer()

ticket = {
    "id": 123,
    "subject": "Cannot connect to VPN",
    "description": "I cannot access the VPN from home..."
}

result = analyzer.analyze_ticket(ticket)
print(result)
```

### Batch Analysis

```python
tickets = [ticket1, ticket2, ticket3]
batch_result = analyzer.analyze_multiple_tickets(tickets)
print(f"Analyzed: {batch_result['successful']}/{batch_result['total']}")
```

## 🐛 Troubleshooting

### "OpenAI API key not configured"

**Solution**: Add `OPENAI_API_KEY` to your `.env` file

```env
OPENAI_API_KEY=sk-proj-your-key-here
```

### "Failed to parse AI response"

**Possible causes**:

- API rate limit exceeded
- Invalid API key
- Network connectivity issue

**Solution**: Wait a moment and try again

### Analysis takes too long

- OpenAI API is processing (typically 2-5 seconds)
- Check your internet connection
- Verify API key is valid

### "Analysis failed" error

Check backend logs:

```bash
cd backend
python main.py  # Look for error messages
```

## 📈 Performance Tips

1. **Batch Processing**: Analyze multiple tickets at once for better throughput
2. **Caching**: Cache analysis results to avoid re-analyzing identical tickets
3. **Scheduling**: Run analyses during off-peak hours for faster response

## 🚀 Future Enhancements

Potential improvements:

- Multi-language support
- Custom analysis templates
- Analysis result caching
- Bulk analysis scheduling
- Integration with automation workflows
- Custom sentiment dictionaries

## 📚 Related Documentation

- [OpenAI API Docs](https://platform.openai.com/docs/api-reference)
- [GPT-4 Model Card](https://openai.com/research/gpt-4)
- [FreshService API](https://api.freshservice.com/)

## 🤝 Support

For issues or questions:

1. Check the troubleshooting section above
2. Review backend logs: `backend.log`
3. Open an issue on [GitHub](https://github.com/SantiagoSC1999/FreshAI-Service/issues)

---

**Version**: 1.0  
**Last Updated**: December 2, 2025
