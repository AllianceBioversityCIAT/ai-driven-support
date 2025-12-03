import React, { useState } from 'react';
import { GlassCard } from './GlassCard';
import styles from './TicketFilters.module.css';

interface TicketFiltersProps {
  onFilterChange: (groupId: number | null, status: number | null) => void;
}

const groups = [
  { id: null, name: 'All Groups' },
  { id: 26000250424, name: 'IT Innovation and Business Development' },
  { id: 26000171555, name: 'IT Network Infrastructure and Security' },
  { id: 26000171552, name: 'IT Operations and Service Desk' },
];

const statuses = [
  { id: null, name: 'All Status' },
  { id: 2, name: 'Open' },
  { id: 3, name: 'Pending' },
  { id: 4, name: 'Resolved' },
  { id: 5, name: 'Closed' },
];

export const TicketFilters: React.FC<TicketFiltersProps> = ({ onFilterChange }) => {
  const [selectedGroup, setSelectedGroup] = useState<number | null>(null);
  const [selectedStatus, setSelectedStatus] = useState<number | null>(null);

  const handleGroupChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const groupId = e.target.value ? parseInt(e.target.value) : null;
    setSelectedGroup(groupId);
    onFilterChange(groupId, selectedStatus);
    console.log(`🔍 Filtering by group:`, groupId);
  };

  const handleStatusChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const statusId = e.target.value ? parseInt(e.target.value) : null;
    setSelectedStatus(statusId);
    onFilterChange(selectedGroup, statusId);
    console.log(`🔍 Filtering by status:`, statusId);
  };

  return (
    <GlassCard className={styles.filterCard}>
      <div className={styles.filterContainer}>
        <div className={styles.filterGroup}>
          <label htmlFor="group-filter" className={styles.filterLabel}>
            Filter by Group
          </label>

          <select
            id="group-filter"
            value={selectedGroup || ''}
            onChange={handleGroupChange}
            className={styles.filterSelect}
          >
            {groups.map((group) => (
              <option key={group.id || 'all'} value={group.id || ''}>
                {group.name}
              </option>
            ))}
          </select>
        </div>

        <div className={styles.filterGroup}>
          <label htmlFor="status-filter" className={styles.filterLabel}>
            Filter by Status
          </label>

          <select
            id="status-filter"
            value={selectedStatus || ''}
            onChange={handleStatusChange}
            className={styles.filterSelect}
          >
            {statuses.map((status) => (
              <option key={status.id || 'all'} value={status.id || ''}>
                {status.name}
              </option>
            ))}
          </select>
        </div>
      </div>
    </GlassCard>
  );
};
