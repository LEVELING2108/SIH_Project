import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { trackItemsAPI, vendorAPI } from '../api';

function AddTrackItem() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [vendors, setVendors] = useState([]);
  const [formData, setFormData] = useState({
    id: '',
    item_type: 'elastic_rail_clip',
    lot_number: '',
    vendor_id: '',
    quantity: '',
    manufacture_date: '',
    supply_date: '',
    installation_date: '',
    warranty_period_years: '5',
    installation_location: '',
    kilometer_from: '',
    kilometer_to: '',
    section_name: '',
    division: '',
    zone: '',
    status: 'in_stock',
    performance_status: 'good',
    specifications: '',
    details: '',
    notes: ''
  });

  useEffect(() => {
    // Fetch vendors for dropdown
    fetchVendors();
  }, []);

  const fetchVendors = async () => {
    try {
      const response = await vendorAPI.getAll(1, 100);
      setVendors(response.data.vendors || []);
    } catch (err) {
      console.error('Failed to fetch vendors', err);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Convert string numbers to actual numbers
      const submitData = {
        ...formData,
        quantity: parseInt(formData.quantity),
        warranty_period_years: parseInt(formData.warranty_period_years),
        kilometer_from: formData.kilometer_from ? parseFloat(formData.kilometer_from) : null,
        kilometer_to: formData.kilometer_to ? parseFloat(formData.kilometer_to) : null,
      };

      await trackItemsAPI.create(submitData);
      alert('Track item created successfully!');
      navigate('/track-items');
    } catch (err) {
      alert(err.response?.data?.message || 'Failed to create track item');
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="mb-3">Add New Track Fitting Item</h1>

      <div className="card">
        <form onSubmit={handleSubmit}>
          {/* Basic Information */}
          <h3 style={{ marginTop: 0 }}>Basic Information</h3>
          <div className="grid grid-2">
            <div className="form-group">
              <label className="form-label">Item ID *</label>
              <input
                type="text"
                name="id"
                className="form-control"
                value={formData.id}
                onChange={handleChange}
                placeholder="e.g., CLIP-001, PAD-001"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Item Type *</label>
              <select
                name="item_type"
                className="form-control"
                value={formData.item_type}
                onChange={handleChange}
                required
              >
                <option value="elastic_rail_clip">Elastic Rail Clip</option>
                <option value="rail_pad">Rail Pad</option>
                <option value="liner">Liner</option>
                <option value="sleeper">Sleeper</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Lot Number *</label>
              <input
                type="text"
                name="lot_number"
                className="form-control"
                value={formData.lot_number}
                onChange={handleChange}
                placeholder="e.g., LOT-2024-00001"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Vendor *</label>
              <select
                name="vendor_id"
                className="form-control"
                value={formData.vendor_id}
                onChange={handleChange}
                required
              >
                <option value="">Select Vendor</option>
                {vendors.map((vendor) => (
                  <option key={vendor.id} value={vendor.id}>
                    {vendor.vendor_name} ({vendor.id})
                  </option>
                ))}
              </select>
              <small style={{ color: '#888' }}>
                Don't see your vendor? <a href="/vendors/add">Add new vendor</a>
              </small>
            </div>

            <div className="form-group">
              <label className="form-label">Quantity *</label>
              <input
                type="number"
                name="quantity"
                className="form-control"
                value={formData.quantity}
                onChange={handleChange}
                placeholder="Number of items in lot"
                required
                min="1"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Status</label>
              <select
                name="status"
                className="form-control"
                value={formData.status}
                onChange={handleChange}
              >
                <option value="in_stock">In Stock</option>
                <option value="installed">Installed</option>
                <option value="in_service">In Service</option>
                <option value="defective">Defective</option>
                <option value="replaced">Replaced</option>
              </select>
            </div>
          </div>

          {/* Dates */}
          <h3>Dates</h3>
          <div className="grid grid-3">
            <div className="form-group">
              <label className="form-label">Manufacture Date *</label>
              <input
                type="date"
                name="manufacture_date"
                className="form-control"
                value={formData.manufacture_date}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Supply Date</label>
              <input
                type="date"
                name="supply_date"
                className="form-control"
                value={formData.supply_date}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Installation Date</label>
              <input
                type="date"
                name="installation_date"
                className="form-control"
                value={formData.installation_date}
                onChange={handleChange}
              />
            </div>
          </div>

          {/* Warranty */}
          <h3>Warranty Information</h3>
          <div className="grid grid-2">
            <div className="form-group">
              <label className="form-label">Warranty Period (Years)</label>
              <input
                type="number"
                name="warranty_period_years"
                className="form-control"
                value={formData.warranty_period_years}
                onChange={handleChange}
                min="1"
                max="20"
              />
              <small style={{ color: '#888' }}>
                Warranty will be calculated from supply date
              </small>
            </div>
          </div>

          {/* Location Information */}
          <h3>Location Information</h3>
          <div className="grid grid-2">
            <div className="form-group" style={{ gridColumn: 'span 2' }}>
              <label className="form-label">Installation Location</label>
              <input
                type="text"
                name="installation_location"
                className="form-control"
                value={formData.installation_location}
                onChange={handleChange}
                placeholder="e.g., Delhi-Mumbai Track Section A"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Section Name</label>
              <input
                type="text"
                name="section_name"
                className="form-control"
                value={formData.section_name}
                onChange={handleChange}
                placeholder="e.g., Delhi-Jaipur Section"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Division</label>
              <input
                type="text"
                name="division"
                className="form-control"
                value={formData.division}
                onChange={handleChange}
                placeholder="e.g., Central Railway"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Zone</label>
              <input
                type="text"
                name="zone"
                className="form-control"
                value={formData.zone}
                onChange={handleChange}
                placeholder="e.g., CR, WR, NR"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Kilometer From</label>
              <input
                type="number"
                step="0.001"
                name="kilometer_from"
                className="form-control"
                value={formData.kilometer_from}
                onChange={handleChange}
                placeholder="Start km"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Kilometer To</label>
              <input
                type="number"
                step="0.001"
                name="kilometer_to"
                className="form-control"
                value={formData.kilometer_to}
                onChange={handleChange}
                placeholder="End km"
              />
            </div>
          </div>

          {/* Additional Information */}
          <h3>Additional Information</h3>
          <div className="grid grid-2">
            <div className="form-group">
              <label className="form-label">Performance Status</label>
              <select
                name="performance_status"
                className="form-control"
                value={formData.performance_status}
                onChange={handleChange}
              >
                <option value="good">Good</option>
                <option value="average">Average</option>
                <option value="poor">Poor</option>
                <option value="failed">Failed</option>
              </select>
            </div>

            <div className="form-group" style={{ gridColumn: 'span 2' }}>
              <label className="form-label">Technical Specifications (JSON)</label>
              <textarea
                name="specifications"
                className="form-control"
                value={formData.specifications}
                onChange={handleChange}
                rows="3"
                placeholder='{"material": "Steel", "grade": "E-Type", "standard": "IRS-T-12"}'
              />
              <small style={{ color: '#888' }}>
                Enter technical specs as JSON (optional)
              </small>
            </div>

            <div className="form-group" style={{ gridColumn: 'span 2' }}>
              <label className="form-label">Details</label>
              <textarea
                name="details"
                className="form-control"
                value={formData.details}
                onChange={handleChange}
                rows="4"
                placeholder="Additional details about the track item..."
              />
            </div>

            <div className="form-group" style={{ gridColumn: 'span 2' }}>
              <label className="form-label">Notes</label>
              <textarea
                name="notes"
                className="form-control"
                value={formData.notes}
                onChange={handleChange}
                rows="3"
                placeholder="Internal notes, special instructions, etc."
              />
            </div>
          </div>

          <div className="flex gap-2 mt-3">
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Creating...' : 'Create Track Item'}
            </button>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => navigate('/track-items')}
            >
              Cancel
            </button>
          </div>
        </form>
      </div>

      <div className="alert alert-info mt-3">
        <strong>💡 Tip:</strong> Fill in all available information for better AI-powered quality monitoring and exception detection.
      </div>
    </div>
  );
}

export default AddTrackItem;
