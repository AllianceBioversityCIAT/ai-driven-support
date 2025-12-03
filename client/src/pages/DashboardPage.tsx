import React, { useEffect, useState } from 'react';
import { Navigation } from '../components/Navigation';
import { SearchBar } from '../components/SearchBar';
import { TicketCard } from '../components/TicketCard';
import { GlassCard } from '../components/GlassCard';
import { Button } from '../components/Button';
import { TicketFilters } from '../components/TicketFilters';
import { useTickets } from '../hooks/useTickets';
import { useTicketStore } from '../store';
import styles from './DashboardPage.module.css';

interface TicketStats {
  openTickets: number;
  inProgressTickets: number;
  resolvedToday: number;
  avgResponse: string;
}

export const DashboardPage: React.FC = () => {
  const { loading, fetchTickets } = useTickets();
  const { tickets, appendTickets, pagination } = useTicketStore();
  const [stats, setStats] = useState<TicketStats>({
    openTickets: 0,
    inProgressTickets: 0,
    resolvedToday: 0,
    avgResponse: '0h',
  });
  const [filteredTickets, setFilteredTickets] = useState<any[]>([]);
  const [selectedGroup, setSelectedGroup] = useState<number | null>(null);
  const [selectedStatus, setSelectedStatus] = useState<number | null>(null);
  const [isLoadingMore, setIsLoadingMore] = useState(false);

  // Calculate statistics based on tickets
  const calculateStats = (ticketsList: any[]) => {
    if (!Array.isArray(ticketsList) || ticketsList.length === 0) {
      setStats({
        openTickets: 0,
        inProgressTickets: 0,
        resolvedToday: 0,
        avgResponse: '0h',
      });
      return;
    }

    const openTickets = ticketsList.filter((t) => t.status === 2 || t.status === 3).length;
    const inProgressTickets = ticketsList.filter((t) => t.status === 3).length;

    const now = new Date();
    const yesterday = new Date(now.getTime() - 24 * 60 * 60 * 1000);
    const resolvedToday = ticketsList.filter((t) => {
      if (t.status === 4 || t.status === 5) {
        const updatedAt = new Date(t.updated_at);
        return updatedAt > yesterday;
      }
      return false;
    }).length;

    let totalResponseTime = 0;
    let respondedTickets = 0;

    ticketsList.forEach((ticket) => {
      if (ticket.created_at && ticket.updated_at) {
        const createdAt = new Date(ticket.created_at).getTime();
        const updatedAt = new Date(ticket.updated_at).getTime();
        const responseTime = updatedAt - createdAt;

        if (responseTime > 0) {
          totalResponseTime += responseTime;
          respondedTickets++;
        }
      }
    });

    const avgResponseMs = respondedTickets > 0 ? totalResponseTime / respondedTickets : 0;
    const avgResponseHours = Math.round((avgResponseMs / (1000 * 60 * 60)) * 10) / 10;
    const avgResponse = avgResponseHours > 0 ? `${avgResponseHours}h` : '0h';

    const newStats: TicketStats = {
      openTickets,
      inProgressTickets,
      resolvedToday,
      avgResponse,
    };

    setStats(newStats);
  };

  // Apply filters and recalculate stats
  useEffect(() => {
    if (tickets && Array.isArray(tickets)) {
      let filtered = tickets;

      // Only apply status filter client-side (group is filtered server-side)
      if (selectedStatus) {
        filtered = filtered.filter((t) => Number(t.status) === selectedStatus);
      }

      setFilteredTickets(filtered);
      calculateStats(filtered);
    }
  }, [tickets, selectedStatus]);

  const handleFilterChange = (groupId: number | null, status: number | null) => {
    setSelectedGroup(groupId);
    setSelectedStatus(status);

    // When filter changes, reload tickets from page 1 with the group filter
    // Pass group_id to backend for server-side filtering
    if (groupId !== null) {
      fetchTickets(1, 30, groupId);
    } else {
      fetchTickets(1, 30);
    }
  };

  const handleSearch = (query: string) => {
    if (query.trim()) {
      const filtered = tickets.filter(
        (ticket: any) =>
          ticket.subject?.toLowerCase().includes(query.toLowerCase()) ||
          ticket.id?.toString().includes(query) ||
          ticket.description?.toLowerCase().includes(query.toLowerCase())
      );
      setFilteredTickets(filtered);
    } else {
      setFilteredTickets(tickets);
    }
  };

  const loadMoreTickets = async () => {
    try {
      setIsLoadingMore(true);
      const nextPage = pagination.page + 1;
      // Fetch next page with group filter if active
      await fetchTickets(nextPage, pagination.per_page, selectedGroup || undefined);
    } catch (err: any) {
      console.error('Error loading more tickets:', err);
    } finally {
      setIsLoadingMore(false);
    }
  };

  return (
    <div className={styles.dashboard}>
      <Navigation title="FreshAI Service" />

      <main className={styles.container}>
        {/* Header Section */}
        <section className={styles.header}>
          <div>
            <h1 className={styles.title}>Welcome Back</h1>
            <p className={styles.subtitle}>Manage your support tickets with AI-powered insights</p>
          </div>
          <Button variant="primary">+ New Ticket</Button>
        </section>

        {/* Filters Section */}
        <section className={styles.filterSection}>
          <TicketFilters onFilterChange={handleFilterChange} />
        </section>

        {/* Stats Section */}
        <section className={styles.statsGrid}>
          <GlassCard>
            <div className={styles.statCard}>
              <div className={styles.statNumber}>{stats.openTickets}</div>
              <div className={styles.statLabel}>Open Tickets</div>
            </div>
          </GlassCard>
          <GlassCard>
            <div className={styles.statCard}>
              <div className={styles.statNumber}>{stats.inProgressTickets}</div>
              <div className={styles.statLabel}>In Progress</div>
            </div>
          </GlassCard>
          <GlassCard>
            <div className={styles.statCard}>
              <div className={styles.statNumber}>{stats.resolvedToday}</div>
              <div className={styles.statLabel}>Resolved Today</div>
            </div>
          </GlassCard>
          <GlassCard>
            <div className={styles.statCard}>
              <div className={styles.statNumber}>{stats.avgResponse}</div>
              <div className={styles.statLabel}>Avg Response</div>
            </div>
          </GlassCard>
        </section>

        {/* Search Section */}
        <section className={styles.searchSection}>
          <SearchBar
            onSearch={handleSearch}
            placeholder="Search tickets by ID, subject, or status..."
          />
        </section>

        {/* Tickets Section */}
        <section className={styles.ticketsSection}>
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle}>Recent Tickets ({filteredTickets.length})</h2>
            <Button variant="secondary" size="sm">
              View All
            </Button>
          </div>

          {loading ? (
            <div className={styles.loading}>
              <div className={styles.spinner}></div>
              <p>Loading tickets...</p>
            </div>
          ) : filteredTickets && Array.isArray(filteredTickets) && filteredTickets.length > 0 ? (
            <>
              <div className={styles.ticketsGrid}>
                {filteredTickets.map((ticket: any) => (
                  <TicketCard key={ticket.id} ticket={ticket} />
                ))}
              </div>

              {/* Load More Button - show if there are more tickets to load */}
              {pagination.has_more && (
                <div className={styles.loadMoreContainer}>
                  <Button variant="secondary" onClick={loadMoreTickets} disabled={isLoadingMore}>
                    {isLoadingMore ? 'Loading...' : 'Load More Tickets'}
                  </Button>
                </div>
              )}

              {/* Pagination Info */}
              <div className={styles.paginationInfo}>
                <p>
                  {selectedGroup || selectedStatus ? (
                    <>
                      Showing {filteredTickets.length} filtered tickets (from {tickets.length}{' '}
                      total)
                    </>
                  ) : (
                    <>
                      Showing {tickets.length} of {pagination.total} tickets
                    </>
                  )}
                </p>
              </div>
            </>
          ) : (
            <GlassCard>
              <div className={styles.emptyState}>
                <p>No tickets found</p>
              </div>
            </GlassCard>
          )}
        </section>
      </main>
    </div>
  );
};
