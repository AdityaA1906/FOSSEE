import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Plot from 'react-plotly.js';
import confetti from 'canvas-confetti';
import Sidebar from '../components/Sidebar';
import AtomicSpinner from '../components/AtomicSpinner';
import PDFModal from '../components/PDFModal';
import { authAPI, dataAPI } from '../services/api';
import './Dashboard.css';

const Dashboard = ({ user, onLogout }) => {
    const [activeView, setActiveView] = useState('dashboard');
    const [equipmentData, setEquipmentData] = useState([]);
    const [statistics, setStatistics] = useState(null);
    const [uploadHistory, setUploadHistory] = useState([]);
    const [loading, setLoading] = useState(false);
    const [uploadLoading, setUploadLoading] = useState(false);
    const [pdfModalOpen, setPdfModalOpen] = useState(false);
    const [pdfContent, setPdfContent] = useState('');
    const [currentDatasetId, setCurrentDatasetId] = useState(null);
    const fileInputRef = useRef(null);

    useEffect(() => {
        fetchHistory();
        loadLocalData();
    }, []);

    const fetchHistory = async () => {
        try {
            const history = await dataAPI.getUploadHistory();
            setUploadHistory(history);
        } catch (error) {
            console.error("Failed to fetch history:", error);
        }
    };

    const loadLocalData = () => {
        const storedData = localStorage.getItem('equipmentData');
        const storedId = localStorage.getItem('currentDatasetId');
        if (storedData) {
            const data = JSON.parse(storedData);
            setEquipmentData(data);
            setCurrentDatasetId(storedId);
            calculateStatistics(data);
        }
    };

    const calculateStatistics = (data) => {
        if (!data || data.length === 0) return;
        const flowrates = data.map(d => d.flowrate);
        const pressures = data.map(d => d.pressure);
        const temperatures = data.map(d => d.temperature);

        setStatistics({
            total_count: data.length,
            flowrate: {
                mean: flowrates.reduce((a, b) => a + b, 0) / flowrates.length,
                min: Math.min(...flowrates),
                max: Math.max(...flowrates),
            },
            pressure: {
                mean: pressures.reduce((a, b) => a + b, 0) / pressures.length,
                min: Math.min(...pressures),
                max: Math.max(...pressures),
            },
            temperature: {
                mean: temperatures.reduce((a, b) => a + b, 0) / temperatures.length,
                min: Math.min(...temperatures),
                max: Math.max(...temperatures),
            },
        });
    };

    const handleFileUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        setUploadLoading(true);
        try {
            const result = await dataAPI.uploadCSV(file);
            // Fetch the actual data and stats for the new dataset
            const data = await dataAPI.getEquipmentData(result.dataset_id);
            const stats = await dataAPI.getStatistics(result.dataset_id);

            setEquipmentData(data);
            setStatistics(stats);
            setCurrentDatasetId(result.dataset_id);
            localStorage.setItem('equipmentData', JSON.stringify(data));
            localStorage.setItem('currentDatasetId', result.dataset_id);
            fetchHistory();
            confetti({ particleCount: 150, spread: 70, origin: { y: 0.6 } });
        } catch (error) {
            console.error("Upload failed details:", error.response?.data || error.message);
            alert(`Upload failed: ${error.response?.data?.error || error.message}`);
        } finally {
            setUploadLoading(false);
            e.target.value = '';
        }
    };

    const loadFromHistory = async (dataset) => {
        setLoading(true);
        try {
            const data = await dataAPI.getEquipmentData(dataset.id);
            const stats = await dataAPI.getStatistics(dataset.id);
            setEquipmentData(data);
            setStatistics(stats);
            setCurrentDatasetId(dataset.id);
            localStorage.setItem('equipmentData', JSON.stringify(data));
            localStorage.setItem('currentDatasetId', dataset.id);
            setActiveView('dashboard');
            confetti({ particleCount: 100, spread: 60, origin: { y: 0.7 } });
        } catch (error) {
            console.error("Failed to load history:", error);
        } finally {
            setLoading(false);
        }
    };

    const generatePDF = async () => {
        if (!equipmentData || equipmentData.length === 0) return;
        setLoading(true);
        try {
            const blob = await dataAPI.generatePDF(currentDatasetId);
            const url = URL.createObjectURL(blob);
            setPdfContent(url); // Now storing Blob URL
            setPdfModalOpen(true);
        } catch (error) {
            console.error("PDF generation failed:", error);
            alert("Failed to generate PDF. Please ensure the backend is running.");
        } finally {
            setLoading(false);
        }
    };

    // Helper components
    const AnimatedCounter = ({ value, suffix = '' }) => {
        const [count, setCount] = useState(0);
        useEffect(() => {
            let start = 0;
            const end = parseFloat(value) || 0;
            if (start === end) return;
            const totalSteps = 60;
            const increment = (end - start) / totalSteps;
            let currentStep = 0;

            const timer = setInterval(() => {
                currentStep++;
                if (currentStep >= totalSteps) {
                    setCount(end);
                    clearInterval(timer);
                } else {
                    setCount(prev => prev + increment);
                }
            }, 16);
            return () => clearInterval(timer);
        }, [value]);

        return <span>{count.toFixed(suffix ? 0 : 2)}{suffix}</span>;
    };

    // Plot Data Helpers
    const get3DScatterData = () => [{
        x: equipmentData.map(d => d.flowrate),
        y: equipmentData.map(d => d.pressure),
        z: equipmentData.map(d => d.temperature),
        text: equipmentData.map(d => d.equipment_name),
        mode: 'markers',
        type: 'scatter3d',
        marker: {
            size: equipmentData.map(d => 5 + (d.pressure / 2)),
            color: equipmentData.map(d => d.temperature),
            colorscale: 'Viridis',
            opacity: 0.8,
            line: { color: 'rgba(255, 255, 255, 0.2)', width: 1 }
        },
        projection: {
            z: { show: true, opacity: 0.5, scale: 0.8, color: '#00d4ff' }
        }
    }];

    const get3DScatterLayout = () => ({
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#e6f1ff', family: 'Inter, sans-serif' },
        margin: { l: 0, r: 0, b: 0, t: 0 },
        scene: {
            xaxis: { title: 'Flowrate', gridcolor: 'rgba(0, 212, 255, 0.1)', backgroundcolor: 'rgba(10, 25, 47, 0.4)' },
            yaxis: { title: 'Pressure', gridcolor: 'rgba(0, 212, 255, 0.1)', backgroundcolor: 'rgba(10, 25, 47, 0.4)' },
            zaxis: { title: 'Temperature', gridcolor: 'rgba(0, 212, 255, 0.1)', backgroundcolor: 'rgba(10, 25, 47, 0.4)' },
            camera: { eye: { x: 1.5, y: 1.5, z: 1.5 } }
        }
    });

    const get3DPieData = () => {
        const counts = {};
        equipmentData.forEach(d => counts[d.equipment_type] = (counts[d.equipment_type] || 0) + 1);
        return [{
            values: Object.values(counts),
            labels: Object.keys(counts),
            type: 'pie',
            hole: 0.4,
            pull: [0.1, 0, 0, 0, 0],
            marker: { colors: ['#00d4ff', '#b794f6', '#00ff88', '#ff006e'] },
            textinfo: 'label+percent',
            hoverinfo: 'label+value'
        }];
    };

    const get3DPieLayout = () => ({
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#e6f1ff' },
        showlegend: false,
        margin: { l: 20, r: 20, b: 20, t: 20 }
    });

    const getBarChartData = () => {
        const types = [...new Set(equipmentData.map(d => d.equipment_type))];
        return types.map(type => {
            const temp = equipmentData.filter(d => d.equipment_type === type).map(d => d.temperature);
            return {
                x: [type],
                y: [temp.reduce((a, b) => a + b, 0) / temp.length],
                name: type,
                type: 'bar',
                marker: {
                    color: type === types[0] ? '#00d4ff' : '#b794f6',
                    opacity: 0.8,
                    line: { width: 1, color: '#fff' }
                }
            };
        });
    };

    const getBarChartLayout = () => ({
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#e6f1ff' },
        yaxis: { title: 'Avg Temperature (°C)', gridcolor: 'rgba(255,255,255,0.1)' },
        xaxis: { gridcolor: 'rgba(255,255,255,0.1)' },
        margin: { l: 50, r: 20, b: 50, t: 20 },
        barmode: 'group'
    });

    return (
        <div className="dashboard-page">
            <Sidebar activeView={activeView} onViewChange={setActiveView} onLogout={onLogout} user={user} />

            <div className="dashboard-content">
                <AnimatePresence>
                    {loading && (
                        <motion.div
                            className="modal-overlay"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                        >
                            <AtomicSpinner size={120} />
                        </motion.div>
                    )}
                </AnimatePresence>

                <motion.header
                    className="dashboard-header"
                >
                    <div className="header-content">
                        <div>
                            <h1 className="gradient-text">Command Center</h1>
                            <p className="header-subtitle">Chemical Equipment Parameter Visualizer</p>
                        </div>
                        <div className="header-actions">
                            <span className="user-info neon-text">👤 {user?.username || 'User'}</span>
                        </div>
                    </div>
                </motion.header>

                {activeView === 'dashboard' && (
                    <div className="bento-grid">
                        <motion.div
                            className="bento-item upload-section"
                        >
                            <h2 className="section-title">
                                <span className="title-icon">📤</span>
                                Upload Data
                            </h2>
                            {uploadLoading ? (
                                <div className="flex-center" style={{ minHeight: '150px' }}>
                                    <AtomicSpinner size={80} />
                                </div>
                            ) : (
                                <div className="upload-area" onClick={() => fileInputRef.current?.click()}>
                                    <input
                                        ref={fileInputRef}
                                        type="file"
                                        accept=".csv"
                                        onChange={handleFileUpload}
                                        style={{ display: 'none' }}
                                    />
                                    <div className="upload-content">
                                        <div className="upload-icon">📄</div>
                                        <p className="upload-text">Drop CSV file or click to browse</p>
                                        <p className="upload-hint">Supports standard formats</p>
                                    </div>
                                </div>
                            )}
                        </motion.div>

                        {statistics && (
                            <>
                                <motion.div className="bento-item metric-card" whileHover={{ scale: 1.05 }}>
                                    <div className="metric-icon">📊</div>
                                    <h3 className="metric-label">Total Units</h3>
                                    <p className="metric-value gradient-text">
                                        <AnimatedCounter value={statistics.total_count} suffix="" />
                                    </p>
                                </motion.div>
                                <motion.div className="bento-item metric-card" whileHover={{ scale: 1.05 }}>
                                    <div className="metric-icon">💧</div>
                                    <h3 className="metric-label">Flowrate</h3>
                                    <p className="metric-value neon-text">
                                        <AnimatedCounter value={statistics.flowrate.mean} />
                                    </p>
                                </motion.div>
                                <motion.div className="bento-item metric-card" whileHover={{ scale: 1.05 }}>
                                    <div className="metric-icon">⚡</div>
                                    <h3 className="metric-label">Pressure</h3>
                                    <p className="metric-value neon-text">
                                        <AnimatedCounter value={statistics.pressure.mean} />
                                    </p>
                                </motion.div>
                                <motion.div className="bento-item metric-card" whileHover={{ scale: 1.05 }}>
                                    <div className="metric-icon">🌡️</div>
                                    <h3 className="metric-label">Temperature</h3>
                                    <p className="metric-value neon-text">
                                        <AnimatedCounter value={statistics.temperature.mean} suffix="°C" />
                                    </p>
                                </motion.div>
                            </>
                        )}

                        <motion.div
                            className="bento-item bento-item-large graph-container"
                        >
                            <h2 className="section-title"><span className="title-icon">🎯</span> 3D Analysis</h2>
                            {equipmentData.length > 0 ? (
                                <Plot data={get3DScatterData()} layout={get3DScatterLayout()} config={{ responsive: true }} style={{ width: '100%', height: '500px' }} />
                            ) : <div className="empty-state">No data</div>}
                        </motion.div>

                        <motion.div className="bento-item graph-container">
                            <h2 className="section-title"><span className="title-icon">🥧</span> Distribution</h2>
                            {equipmentData.length > 0 ? (
                                <Plot data={get3DPieData()} layout={get3DPieLayout()} config={{ responsive: true }} style={{ width: '100%', height: '300px' }} />
                            ) : <div className="empty-state">No data</div>}
                        </motion.div>

                        <motion.div className="bento-item bento-item-large graph-container">
                            <h2 className="section-title"><span className="title-icon">📊</span> Parameter Ranges</h2>
                            {equipmentData.length > 0 ? (
                                <Plot data={getBarChartData()} layout={getBarChartLayout()} config={{ responsive: true }} style={{ width: '100%', height: '400px' }} />
                            ) : <div className="empty-state">No data</div>}
                        </motion.div>
                    </div>
                )}

                {activeView === 'history' && (
                    <div className="view-content">
                        <h2 className="section-title">Upload Archive</h2>
                        <div className="history-bento-grid">
                            {uploadHistory.map((item, idx) => (
                                <motion.div
                                    key={item.id}
                                    className={`history-tile glass-card ${idx === 0 ? 'latest-glow' : ''}`}
                                    onClick={() => loadFromHistory(item)}
                                >
                                    <div className="tile-header">
                                        <span className="file-name">{item.filename}</span>
                                        <span className="upload-date">{new Date(item.uploaded_at).toLocaleDateString()}</span>
                                    </div>
                                    <div className="tile-stats">
                                        <div className="mini-stat"><span className="label">Rows</span><span className="value">{item.row_count}</span></div>
                                    </div>
                                    <div className="tile-actions">
                                        <button className="action-btn load">⚡ Restore</button>
                                    </div>
                                </motion.div>
                            ))}
                        </div>
                    </div>
                )}

                {activeView === 'reports' && (
                    <div className="view-content" style={{ paddingBottom: '4rem' }}>
                        <div className="report-header glass-card" style={{ marginBottom: '2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <div>
                                <h1 className="gradient-text" style={{ fontSize: '1.8rem', marginBottom: '0.5rem' }}>Report Center</h1>
                                <p style={{ opacity: 0.8 }}>Generate professional PDF reports for the current dataset.</p>
                            </div>
                            <button className="neon-button" onClick={generatePDF} disabled={equipmentData.length === 0}>
                                GENERATE PDF REPORT
                            </button>
                        </div>

                        {equipmentData.length > 0 ? (
                            <div className="data-preview-section glass-card">
                                <h2 className="section-title"><span className="title-icon">🔍</span> Dataset Preview ({equipmentData.length} records)</h2>
                                <div className="table-container" style={{ overflowX: 'auto', marginTop: '1rem' }}>
                                    <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                                        <thead>
                                            <tr style={{ borderBottom: '1px solid var(--glass-border)', color: 'var(--neon-cyan)' }}>
                                                <th style={{ padding: '1rem' }}>Equipment Name</th>
                                                <th style={{ padding: '1rem' }}>Type</th>
                                                <th style={{ padding: '1rem' }}>Flowrate</th>
                                                <th style={{ padding: '1rem' }}>Pressure</th>
                                                <th style={{ padding: '1rem' }}>Temp</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {equipmentData.map((item, idx) => (
                                                <tr key={idx} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)', background: idx % 2 === 0 ? 'rgba(255,255,255,0.02)' : 'transparent' }}>
                                                    <td style={{ padding: '0.8rem 1rem', fontWeight: 500 }}>{item.equipment_name}</td>
                                                    <td style={{ padding: '0.8rem 1rem' }}><span className="badge-3d" style={{ padding: '2px 8px', fontSize: '0.7rem' }}>{item.equipment_type}</span></td>
                                                    <td style={{ padding: '0.8rem 1rem' }}>{item.flowrate.toFixed(2)}</td>
                                                    <td style={{ padding: '0.8rem 1rem' }}>{item.pressure.toFixed(2)}</td>
                                                    <td style={{ padding: '0.8rem 1rem' }}>{item.temperature.toFixed(2)}°C</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        ) : (
                            <div className="flex-center" style={{ minHeight: '40vh' }}>
                                <div className="glass-card" style={{ padding: '3rem', textAlign: 'center' }}>
                                    <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📁</div>
                                    <h3 style={{ marginBottom: '1rem' }}>No Data Selected</h3>
                                    <p>Please upload a CSV or select one from History to generate a report.</p>
                                    <button className="action-btn load" style={{ marginTop: '2rem', padding: '10px 20px' }} onClick={() => setActiveView('dashboard')}>Go to Dashboard</button>
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </div>
            <PDFModal isOpen={pdfModalOpen} onClose={() => setPdfModalOpen(false)} pdfContent={pdfContent} />
        </div>
    );
};

export default Dashboard;
