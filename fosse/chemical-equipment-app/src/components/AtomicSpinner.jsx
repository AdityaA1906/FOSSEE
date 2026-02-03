import React from 'react';
import './AtomicSpinner.css';

const AtomicSpinner = ({ size = 100 }) => {
    return (
        <div className="atomic-spinner-container" style={{ width: size, height: size }}>
            <div className="atomic-spinner">
                <div className="nucleus"></div>
                <div className="orbit orbit-1">
                    <div className="electron"></div>
                </div>
                <div className="orbit orbit-2">
                    <div className="electron"></div>
                </div>
                <div className="orbit orbit-3">
                    <div className="electron"></div>
                </div>
            </div>
            <p className="spinner-text">Processing Data...</p>
        </div>
    );
};

export default AtomicSpinner;
