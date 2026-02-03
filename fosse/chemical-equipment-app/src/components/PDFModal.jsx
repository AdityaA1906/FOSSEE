import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './PDFModal.css';

const PDFModal = ({ isOpen, onClose, pdfContent }) => {
    if (!isOpen) return null;

    return (
        <AnimatePresence>
            <motion.div
                className="pdf-modal-overlay"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={onClose}
            >
                <motion.div
                    className="pdf-modal-content glass-card"
                    initial={{ scale: 0.9, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    exit={{ scale: 0.9, opacity: 0 }}
                    onClick={(e) => e.stopPropagation()}
                >
                    <div className="pdf-modal-header">
                        <h2 className="gradient-text">Equipment Report</h2>
                        <button className="close-button" onClick={onClose}>✕</button>
                    </div>

                    <div className="pdf-modal-body">
                        <iframe
                            src={pdfContent}
                            width="100%"
                            height="100%"
                            style={{ border: 'none', borderRadius: '8px', background: 'white' }}
                            title="PDF Report"
                        />
                    </div>

                    <div className="pdf-modal-footer">
                        <button
                            className="neon-button"
                            onClick={() => {
                                const link = document.createElement('a');
                                link.href = pdfContent;
                                link.download = `Equipment_Report_${new Date().getTime()}.pdf`;
                                link.click();
                            }}
                        >
                            📥 Download PDF
                        </button>
                    </div>
                </motion.div>
            </motion.div>
        </AnimatePresence>
    );
};

export default PDFModal;
