import React, { useState } from 'react';
import { motion } from 'framer-motion';
import './Sidebar.css';

const Sidebar = ({ activeView, onViewChange, onLogout }) => {
    const [isCollapsed, setIsCollapsed] = useState(false);

    const menuItems = [
        { id: 'dashboard', icon: '📊', label: 'Dashboard' },
        { id: 'history', icon: '🕐', label: 'History' },
        { id: 'reports', icon: '📄', label: 'Reports' },
    ];

    return (
        <motion.aside
            className={`sidebar ${isCollapsed ? 'collapsed' : ''}`}
        >
            <div className="sidebar-header">
                <motion.div
                    className="logo"
                    whileHover={{ scale: 1.05 }}
                >
                    <span className="logo-icon">⚗️</span>
                    {!isCollapsed && <span className="logo-text gradient-text">FOSSE</span>}
                </motion.div>

                <button
                    className="collapse-btn"
                    onClick={() => setIsCollapsed(!isCollapsed)}
                    aria-label="Toggle sidebar"
                >
                    {isCollapsed ? '→' : '←'}
                </button>
            </div>

            <nav className="sidebar-nav">
                {menuItems.map((item) => (
                    <motion.button
                        key={item.id}
                        className={`nav-item ${activeView === item.id ? 'active' : ''}`}
                        onClick={() => onViewChange(item.id)}
                        whileHover={{ x: 5 }}
                        whileTap={{ scale: 0.95 }}
                    >
                        <span className="nav-icon">{item.icon}</span>
                        {!isCollapsed && <span className="nav-label">{item.label}</span>}
                        {activeView === item.id && <div className="active-indicator"></div>}
                    </motion.button>
                ))}
            </nav>

            <div className="sidebar-footer">
                <motion.button
                    className="logout-btn"
                    onClick={onLogout}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                >
                    <span className="nav-icon">🚪</span>
                    {!isCollapsed && <span className="nav-label">Logout</span>}
                </motion.button>
            </div>
        </motion.aside>
    );
};

export default Sidebar;
