import React from 'react';
import styles from './Navigation.module.css';

interface NavigationProps {
  title?: string;
}

export const Navigation: React.FC<NavigationProps> = ({ title = 'FreshAI' }) => {
  return (
    <nav className={styles.navbar}>
      <div className={styles.container}>
        <div className={styles.logo}>
          <span className={styles.logoText}>{title}</span>
        </div>
        <ul className={styles.menu}>
          <li>
            <a href="#dashboard">Dashboard</a>
          </li>
          <li>
            <a href="#tickets">Tickets</a>
          </li>
          <li>
            <a href="#analytics">Analytics</a>
          </li>
          <li>
            <a href="#settings">Settings</a>
          </li>
        </ul>
      </div>
    </nav>
  );
};
