import { useState } from 'react';
import { useTickets } from '../hooks/useTickets';

export default function AIChatPanel() {
  const { fetchTickets, searchTickets } = useTickets();
  const [prompt, setPrompt] = useState('');

  const handleRun = async () => {
    // Extremely simple mock: run basic actions based on prompt keywords
    if (/open tickets|list tickets/i.test(prompt)) {
      await fetchTickets(1, 30);
    } else if (/search/i.test(prompt)) {
      const match = prompt.match(/search\s+(.+)/i);
      if (match) await searchTickets(match[1]);
    } else {
      alert('Tooling TBD: MCP tools will be wired here.');
    }
  };

  return (
    <div className="ai-chat-panel">
      <h3>AI Tools</h3>
      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Ask: 'list tickets' or 'search password'"
      />
      <button onClick={handleRun}>Run</button>
    </div>
  );
}
