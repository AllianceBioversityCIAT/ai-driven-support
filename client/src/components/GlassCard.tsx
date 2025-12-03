import React from 'react';
import styles from './GlassCard.module.css';

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
  onClick?: () => void;
}

export const GlassCard: React.FC<GlassCardProps> = ({
  children,
  className = '',
  hover = true,
  onClick,
}) => {
  return (
    <div
      className={`${styles.glassCard} ${hover ? styles.hover : ''} ${className}`}
      onClick={onClick}
    >
      {children}
    </div>
  );
};
