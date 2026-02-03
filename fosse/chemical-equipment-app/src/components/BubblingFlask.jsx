import React from 'react';
import './BubblingFlask.css';

const BubblingFlask = ({ size = 80 }) => {
    return (
        <div className="bubbling-flask-container" style={{ width: size, height: size }}>
            <svg
                viewBox="0 0 100 120"
                xmlns="http://www.w3.org/2000/svg"
                className="flask-svg"
            >
                {/* Flask body */}
                <defs>
                    <linearGradient id="flaskGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#3498db" />
                        <stop offset="100%" stopColor="#9b59b6" />
                    </linearGradient>
                </defs>

                {/* Flask outline */}
                <path
                    d="M 35 10 L 35 40 L 20 80 Q 20 100 30 105 L 70 105 Q 80 100 80 80 L 65 40 L 65 10 Z"
                    fill="none"
                    stroke="url(#flaskGradient)"
                    strokeWidth="3"
                    className="flask-outline"
                />

                {/* Flask neck */}
                <rect x="40" y="5" width="20" height="10" rx="2" fill="url(#flaskGradient)" opacity="0.3" />

                {/* Liquid */}
                <path
                    d="M 25 75 L 22 85 Q 22 95 30 98 L 70 98 Q 78 95 78 85 L 75 75 Z"
                    fill="url(#flaskGradient)"
                    opacity="0.2"
                    className="flask-liquid"
                />

                {/* Bubbles */}
                <circle cx="40" cy="85" r="4" fill="url(#flaskGradient)" opacity="0.6" className="bubble bubble-1" />
                <circle cx="55" cy="80" r="3" fill="url(#flaskGradient)" opacity="0.7" className="bubble bubble-2" />
                <circle cx="60" cy="90" r="3.5" fill="url(#flaskGradient)" opacity="0.5" className="bubble bubble-3" />
                <circle cx="45" cy="75" r="2.5" fill="url(#flaskGradient)" opacity="0.8" className="bubble bubble-4" />
            </svg>
            <p className="loading-text gradient-text">Loading...</p>
        </div>
    );
};

export default BubblingFlask;
