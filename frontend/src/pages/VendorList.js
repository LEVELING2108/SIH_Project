import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { vendorAPI, exportAPI } from '../api';

function VendorList() {
  const role = localStorage.getItem('role');
  const isAdmin = role === 'admin';
  const [vendors, setVendors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchVendors(currentPage);
  }, [currentPage]);

  const fetchVendors = async (page) => {
    try {
      const response = await vendorAPI.getAll(page, 10);
      setVendors(response.data.vendors);
      setTotalPages(response.data.pages);
      setCurrentPage(response.data.current_page);
      setLoading(false);
    } catch (err) {
      setError('Failed to load vendors');
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this vendor? This will also delete all associated track items and inspections.')) {
      try {
        const response = await vendorAPI.delete(id);
        console.log('Delete response:', response);
        fetchVendors(currentPage);
      } catch (err) {
        const errorMessage = err.response?.data?.message || err.response?.data?.error || 'Failed to delete vendor';
        const statusCode = err.response?.status;

        if (statusCode === 403) {
          alert('❌ Access Denied: You need admin privileges to delete vendors.');
        } else if (statusCode === 401) {
          alert('❌ Session expired. Please login again.');
          window.location.href = '/login';
        } else if (statusCode === 500) {
          alert(`❌ Server Error: ${errorMessage}\n\nPlease check the backend console for details.`);
        } else {
          alert(`❌ Error: ${errorMessage}`);
        }
        console.error('Delete error:', err);
        console.error('Error response:', err.response);
      }
    }
  };

  const handleExportCSV = async () => {
    try {
      const response = await exportAPI.vendorsCSV();
      const blob = response.data;
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      const timestamp = new Date().toISOString().slice(0, 19).replace(/[:-]/g, '').replace('T', '_');
      link.setAttribute('download', `vendors_export_${timestamp}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      alert('Export successful!');
    } catch (err) {
      console.error('Export failed:', err);
      alert('Failed to export. Please try again.');
    }
  };

  const getRiskClass = (score) => {
    if (score >= 70) return 'risk-high';
    if (score >= 40) return 'risk-medium';
    return 'risk-low';
  };

  const getRiskLabel = (score) => {
    if (score >= 70) return '🚨 High Risk';
    if (score >= 40) return '⚠️ Medium Risk';
    return '✅ Low Risk';
  };

  if (loading) {
    return (
      <div className="text-center" style={{ padding: '4rem 2rem' }}>
        <div className="spinner"></div>
        <p style={{ color: 'var(--slate-600)', marginTop: '1rem' }}>Loading vendors...</p>
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
      {!isAdmin && (
        <div className="alert alert-warning mb-3">
          <span>⚠️</span> <strong>Admin privileges required:</strong> You need to be logged in as an admin to delete vendors. Current role: <strong>{role || 'Not logged in'}</strong>
        </div>
      )}
      <div className="flex flex-between flex-center mb-3">
        <h1 style={{
          fontSize: '2rem',
          fontWeight: '800',
          background: 'var(--gradient-primary)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text'
        }}>
          👥 Vendors
        </h1>
        <div className="flex gap-2">
          <button onClick={handleExportCSV} className="btn btn-secondary">
            <span>📊</span> Export CSV
          </button>
          <Link to="/add" className="btn btn-primary">
            <span>➕</span> Add Vendor
          </Link>
        </div>
      </div>

      {vendors.length === 0 ? (
        <div className="card text-center" style={{ padding: '4rem 2rem' }}>
          <span style={{ fontSize: '4rem', display: 'block', marginBottom: '1rem' }}>📭</span>
          <p style={{ color: 'var(--slate-500)', marginBottom: '1.5rem', fontSize: '1.1rem' }}>No vendors found</p>
          <Link to="/add" className="btn btn-primary">
            <span>➕</span> Add Your First Vendor
          </Link>
        </div>
      ) : (
        <div className="vendor-list">
          {vendors.map((vendor) => (
            <div key={vendor.id} className="vendor-item">
              <div className="vendor-info">
                <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span style={{ fontSize: '1.5rem' }}>🏢</span> {vendor.vendor_name}
                </h3>
                <p style={{ color: 'var(--slate-400)', fontSize: '0.85rem', marginBottom: '0.5rem' }}>ID: {vendor.id}</p>
                {vendor.contact_email && (
                  <p>
                    <span>📧</span> {vendor.contact_email}
                  </p>
                )}
                {vendor.contact_phone && (
                  <p>
                    <span>📱</span> {vendor.contact_phone}
                  </p>
                )}
                {vendor.city && (
                  <p>
                    <span>📍</span> {vendor.city}, {vendor.state}
                  </p>
                )}
              </div>
              <div className="flex gap-2" style={{ alignItems: 'center' }}>
                <span className={`risk-badge ${getRiskClass(vendor.risk_score)}`}>
                  {getRiskLabel(vendor.risk_score)}
                  <span style={{ marginLeft: '0.25rem', opacity: 0.8 }}>({vendor.risk_score})</span>
                </span>
                <Link to={`/vendors/${vendor.id}`} className="btn btn-secondary btn-sm">
                  <span>👁️</span> View
                </Link>
                {isAdmin && (
                  <button
                    onClick={() => handleDelete(vendor.id)}
                    className="btn btn-danger btn-sm"
                  >
                    <span>🗑️</span> Delete
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex flex-center gap-2 mt-3" style={{ justifyContent: 'center' }}>
          <button
            className="btn btn-secondary"
            onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
            disabled={currentPage === 1}
            style={{
              cursor: currentPage === 1 ? 'not-allowed' : 'pointer',
              opacity: currentPage === 1 ? 0.5 : 1
            }}
          >
            <span>←</span> Previous
          </button>
          <span style={{ 
            padding: '0.5rem 1.5rem', 
            background: 'rgba(255, 255, 255, 0.9)',
            borderRadius: 'var(--radius-xl)',
            color: 'var(--slate-600)',
            fontWeight: '600',
            boxShadow: 'var(--shadow-sm)'
          }}>
            Page {currentPage} of {totalPages}
          </span>
          <button
            className="btn btn-secondary"
            onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
            disabled={currentPage === totalPages}
            style={{
              cursor: currentPage === totalPages ? 'not-allowed' : 'pointer',
              opacity: currentPage === totalPages ? 0.5 : 1
            }}
          >
            Next <span>→</span>
          </button>
        </div>
      )}
    </div>
  );
}

export default VendorList;
