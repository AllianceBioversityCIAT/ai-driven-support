import { useEffect, useState } from 'react';
import { useTickets } from '../hooks/useTickets';
import { useTicketStore } from '../store';
import type { Ticket } from '../store';

export default function Dashboard() {
  const { fetchTickets } = useTickets();
  const { tickets, isLoading, error } = useTicketStore();
  const [query, setQuery] = useState('');

  useEffect(() => {
    fetchTickets(1, 30);
  }, [fetchTickets]);

  return (
    <div className="container">
      <h2>FreshService Tickets</h2>
      <div className="toolbar">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search tickets..."
        />
        {/* Search handler wired via useTickets in a future iteration */}
      </div>

      {isLoading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}

      <table className="tickets-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Subject</th>
            <th>Type</th>
            <th>Status</th>
            <th>Priority</th>
          </tr>
        </thead>
        <tbody>
          {tickets.map((t: Ticket) => (
            <tr key={t.id}>
              <td>{t.id}</td>
              <td>{t.subject} muhca loca vos</td>
              <td>{t.type}</td>
              <td>{t.status}</td>
              <td>{t.priority}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
