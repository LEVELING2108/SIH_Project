import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { analyticsAPI, performanceAPI } from '../api';

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [seeding, setSeeding] = useState(false);
  const [seedMessage, setSeedMessage] = useState(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await analyticsAPI.getStats();
      setStats(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to load analytics');
      setLoading(false);
    }
  };

  const handleSeedData = async () => {
    if (!window.confirm('This will add 20 sample vendors with their track equipment. Continue?')) {
      return;
    }

    setSeeding(true);
    setSeedMessage(null);

    try {
      const response = await performanceAPI.seedData();
      setSeedMessage({
        type: 'success',
        text: `✅ Seeded ${response.data.vendors_created} vendors, ${response.data.track_items_created} track items, and ${response.data.inspections_created} inspections!`
      });
      fetchStats();
    } catch (err) {
      console.error('Seed error:', err);
      const errorMsg = err.response?.data?.message || err.response?.data?.error || 'Failed to seed data. Make sure you are logged in as admin.';
      setSeedMessage({
        type: 'error',
        text: `Error: ${errorMsg} (Status: ${err.response?.status})`
      });
    } finally {
      setSeeding(false);
    }
  };

  if (loading) {
    return (
      <div className="text-center" style={{ padding: '4rem 2rem' }}>
        <div className="spinner"></div>
        <p style={{ color: 'var(--slate-600)', marginTop: '1rem', fontSize: '1.1rem' }}>Loading dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-danger">
        <span>⚠️</span> {error}
      </div>
    );
  }

  return (
    <div>
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ 
          fontSize: '2.25rem', 
          fontWeight: '800', 
          background: 'var(--gradient-primary)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          marginBottom: '0.5rem'
        }}>
          Dashboard
        </h1>
        <p style={{ color: 'var(--slate-500)', fontSize: '1.1rem' }}>
          Welcome back! Here's your vendor verification overview
        </p>
      </div>

      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{stats?.total_vendors || 0}</div>
          <div className="stat-label">🏢 Total Vendors</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ background: 'var(--gradient-success)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}>
            {stats?.risk_distribution?.low || 0}
          </div>
          <div className="stat-label">✅ Low Risk</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ background: 'var(--gradient-warning)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}>
            {stats?.risk_distribution?.medium || 0}
          </div>
          <div className="stat-label">⚠️ Medium Risk</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ background: 'var(--gradient-danger)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}>
            {stats?.risk_distribution?.high || 0}
          </div>
          <div className="stat-label">🚨 High Risk</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ background: 'linear-gradient(135deg, #64748b 0%, #475569 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text', fontSize: '2rem' }}>
            {stats?.average_risk_score || 0}
          </div>
          <div className="stat-label">📊 Avg Risk Score</div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card">
        <div className="card-header">
          <span>⚡</span> Quick Actions
        </div>
        <div className="grid grid-3">
          <Link to="/add" className="btn btn-primary">
            <span>➕</span> Add New Vendor
          </Link>
          <Link to="/scan" className="btn btn-success">
            <span>📷</span> Scan QR Code
          </Link>
          <Link to="/vendors" className="btn btn-secondary">
            <span>📋</span> View All Vendors
          </Link>
        </div>
      </div>

      {/* Seed Data */}
      <div className="card">
        <div className="card-header">
          <span>📦</span> Sample Data
        </div>
        <div className="text-center p-3">
          <p style={{ color: 'var(--slate-600)', marginBottom: '1.5rem', fontSize: '1rem', lineHeight: '1.6' }}>
            Load 20 sample vendors with track equipment for testing and performance analysis
          </p>
          {seedMessage && (
            <div className={`alert alert-${seedMessage.type} mb-2`} style={{ marginBottom: '1rem' }}>
              {seedMessage.text}
            </div>
          )}
          <button
            onClick={handleSeedData}
            disabled={seeding}
            className="btn btn-primary btn-lg"
            style={{
              background: seeding ? 'var(--slate-400)' : 'var(--gradient-ocean)',
              cursor: seeding ? 'not-allowed' : 'pointer',
              opacity: seeding ? 0.7 : 1
            }}
          >
            {seeding ? (
              <>
                <span className="spinner" style={{ width: '20px', height: '20px', borderWidth: '2px', marginRight: '0.5rem', display: 'inline-block', verticalAlign: 'middle' }}></span>
                Loading...
              </>
            ) : (
              <>🚀 Load Sample Data</>
            )}
          </button>
        </div>
      </div>

      {/* Info Card */}
      <div className="card">
        <div className="card-header">
          <span>📌</span> Welcome to RailTrack Pro
        </div>
        <div className="alert alert-info" style={{ background: 'linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%)', border: '1px solid rgba(14, 165, 233, 0.3)' }}>
          <strong style={{ display: 'block', marginBottom: '0.75rem', fontSize: '1.05rem' }}>🔐 How it works:</strong>
          <ul style={{ paddingLeft: '1.5rem', lineHeight: '1.8', color: 'var(--slate-700)' }}>
            <li>Add vendor details with complete information</li>
            <li>Generate unique QR codes for each vendor</li>
            <li>Scan QR codes to verify vendors and get AI-powered risk insights</li>
            <li>Review risk scores, flags, and recommendations for each vendor</li>
          </ul>
        </div>
      </div>

      {/* Features */}
      <div className="grid grid-3">
        <div className="card" style={{ transition: 'all 0.3s ease' }}>
          <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem', color: 'var(--slate-800)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontSize: '1.5rem' }}>🔐</span> Secure Verification
          </h3>
          <p style={{ color: 'var(--slate-600)', lineHeight: '1.7' }}>
            Each vendor gets a unique QR code linked to their database record for instant verification.
          </p>
        </div>
        <div className="card" style={{ transition: 'all 0.3s ease' }}>
          <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem', color: 'var(--slate-800)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontSize: '1.5rem' }}>🤖</span> AI Risk Assessment
          </h3>
          <p style={{ color: 'var(--slate-600)', lineHeight: '1.7' }}>
            Advanced algorithms analyze vendor data to detect potential risks and flag suspicious patterns.
          </p>
        </div>
        <div className="card" style={{ transition: 'all 0.3s ease' }}>
          <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem', color: 'var(--slate-800)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontSize: '1.5rem' }}>📊</span> Real-time Analytics
          </h3>
          <p style={{ color: 'var(--slate-600)', lineHeight: '1.7' }}>
            Monitor vendor risk distribution and get insights into your vendor ecosystem.
          </p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
