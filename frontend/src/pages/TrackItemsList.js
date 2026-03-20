import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { trackItemsAPI } from '../api';

function TrackItemsList() {
  const navigate = useNavigate();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [filters, setFilters] = useState({
    item_type: '',
    status: ''
  });

  const itemTypes = {
    elastic_rail_clip: 'Elastic Rail Clip',
    rail_pad: 'Rail Pad',
    liner: 'Liner',
    sleeper: 'Sleeper'
  };

  const statusTypes = {
    in_stock: 'In Stock',
    installed: 'Installed',
    in_service: 'In Service',
    defective: 'Defective',
    replaced: 'Replaced'
  };

  useEffect(() => {
    fetchItems();
  }, [page, filters]);

  const fetchItems = async () => {
    try {
      setLoading(true);
      const response = await trackItemsAPI.getAll(page, 10, filters);
      setItems(response.data.track_items || []);
      setTotalPages(response.data.pages || 1);
      setError(null);
    } catch (err) {
      setError('Failed to load track items');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value
    });
    setPage(1);
  };

  const getStatusBadgeClass = (status) => {
    switch (status) {
      case 'in_service': return 'badge-success';
      case 'in_stock': return 'badge-info';
      case 'installed': return 'badge-primary';
      case 'defective': return 'badge-danger';
      case 'replaced': return 'badge-warning';
      default: return 'badge-secondary';
    }
  };

  if (loading && items.length === 0) {
    return <div>Loading track items...</div>;
  }

  return (
    <div>
      <div className="flex justify-between align-center mb-3">
        <h1>Track Fittings & Components</h1>
        <button
          className="btn btn-primary"
          onClick={() => navigate('/track-items/add')}
        >
          + Add Track Item
        </button>
      </div>

      {/* Filters */}
      <div className="card mb-3">
        <div className="grid grid-3 gap-2">
          <div className="form-group">
            <label className="form-label">Item Type</label>
            <select
              name="item_type"
              className="form-control"
              value={filters.item_type}
              onChange={handleFilterChange}
            >
              <option value="">All Types</option>
              {Object.keys(itemTypes).map(key => (
                <option key={key} value={key}>{itemTypes[key]}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Status</label>
            <select
              name="status"
              className="form-control"
              value={filters.status}
              onChange={handleFilterChange}
            >
              <option value="">All Status</option>
              {Object.keys(statusTypes).map(key => (
                <option key={key} value={key}>{statusTypes[key]}</option>
              ))}
            </select>
          </div>

          <div className="form-group flex align-end">
            <button
              className="btn btn-secondary"
              onClick={() => {
                setFilters({ item_type: '', status: '' });
                setPage(1);
              }}
            >
              Clear Filters
            </button>
          </div>
        </div>
      </div>

      {error && (
        <div className="alert alert-danger mb-3">{error}</div>
      )}

      {/* Track Items Table */}
      <div className="card">
        <div className="table-responsive">
          <table className="table">
            <thead>
              <tr>
                <th>Lot Number</th>
                <th>Item Type</th>
                <th>Vendor</th>
                <th>Quantity</th>
                <th>Manufacture Date</th>
                <th>Status</th>
                <th>Location</th>
                <th>Warranty</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {items.length === 0 ? (
                <tr>
                  <td colSpan="9" style={{ textAlign: 'center', padding: '2rem' }}>
                    No track items found. Add your first track item to get started.
                  </td>
                </tr>
              ) : (
                items.map((item) => (
                  <tr key={item.id}>
                    <td>
                      <strong>{item.lot_number}</strong>
                      <br />
                      <small style={{ color: '#888' }}>{item.id}</small>
                    </td>
                    <td>{itemTypes[item.item_type] || item.item_type}</td>
                    <td>
                      {item.vendor_name || item.vendor_id}
                      <br />
                      <small style={{ color: '#888' }}>{item.vendor_id}</small>
                    </td>
                    <td>{item.quantity?.toLocaleString()}</td>
                    <td>{item.manufacture_date ? new Date(item.manufacture_date).toLocaleDateString() : '-'}</td>
                    <td>
                      <span className={`badge ${getStatusBadgeClass(item.status)}`}>
                        {statusTypes[item.status] || item.status}
                      </span>
                    </td>
                    <td>
                      {item.section_name || '-'}
                      {item.division && <><br /><small>{item.division}</small></>}
                    </td>
                    <td>
                      {item.warranty_expiry_date ? (
                        <>
                          {new Date(item.warranty_expiry_date).toLocaleDateString()}
                          {new Date(item.warranty_expiry_date) < new Date() && (
                            <span className="badge badge-danger ml-1">Expired</span>
                          )}
                        </>
                      ) : '-'}
                    </td>
                    <td>
                      <button
                        className="btn btn-sm btn-primary"
                        onClick={() => navigate(`/track-items/${item.id}`)}
                      >
                        View
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex justify-center gap-2 mt-3">
            <button
              className="btn btn-secondary"
              disabled={page === 1}
              onClick={() => setPage(page - 1)}
            >
              Previous
            </button>
            <span className="flex align-center" style={{ padding: '0 1rem' }}>
              Page {page} of {totalPages}
            </span>
            <button
              className="btn btn-secondary"
              disabled={page === totalPages}
              onClick={() => setPage(page + 1)}
            >
              Next
            </button>
          </div>
        )}
      </div>

      <div className="alert alert-info mt-3">
        <strong>📊 Total Items:</strong> {items.length} track fitting items displayed
      </div>
    </div>
  );
}

export default TrackItemsList;
