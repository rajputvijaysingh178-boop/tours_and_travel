import { FormEvent, useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { api, ApiRecord } from './api/client';
import './admin.css';

type Field = {
  key: string;
  label: string;
  type?: 'text' | 'number' | 'date' | 'email' | 'textarea' | 'select' | 'list';
  required?: boolean;
  options?: { value: string; label: string }[];
};

type Summary = {
  destinations: number;
  packages: number;
  hotels: number;
  customers: number;
  bookings: number;
  revenue: number;
};

const sections = [
  { id: 'destinations', label: 'Destinations', group: 'Inventory' },
  { id: 'packages', label: 'Packages', group: 'Inventory' },
  { id: 'hotels', label: 'Hotels', group: 'Inventory' },
  { id: 'rooms', label: 'Rooms', group: 'Inventory' },
  { id: 'activities', label: 'Activities', group: 'Inventory' },
  { id: 'guides', label: 'Guides', group: 'Inventory' },
  { id: 'vehicles', label: 'Vehicles', group: 'Inventory' },
  { id: 'departures', label: 'Departures', group: 'Operations' },
  { id: 'bookings', label: 'Bookings', group: 'Operations' },
  { id: 'customers', label: 'Customers', group: 'People & finance' },
  { id: 'payments', label: 'Payments', group: 'People & finance' },
  { id: 'invoices', label: 'Invoices', group: 'People & finance' },
  { id: 'refunds', label: 'Refunds', group: 'People & finance' },
];

const editable = new Set(['destinations', 'packages', 'hotels', 'rooms', 'activities', 'guides', 'vehicles']);
const listOptions = (items: ApiRecord[], key: string, label: (item: ApiRecord) => string) => items.map(item => ({ value: String(item[key]), label: label(item) }));
const destinationsFor = (items: ApiRecord[]) => listOptions(items, 'destination_id', item => `${item.name} · ${item.state || item.country}`);
const hotelsFor = (items: ApiRecord[]) => listOptions(items, 'hotel_id', item => item.name);
const statusOptions = (active = 'Active', inactive = 'Inactive') => [{ value: 'active', label: active }, { value: 'inactive', label: inactive }];

function fieldsFor(resource: string, destinations: ApiRecord[], hotels: ApiRecord[]): Field[] {
  const destination = { key: 'destination_id', label: 'Destination', type: 'select' as const, required: true, options: destinationsFor(destinations) };
  const status = { key: 'status', label: 'Status', type: 'select' as const, required: true, options: statusOptions() };
  switch (resource) {
    case 'destinations': return [
      { key: 'name', label: 'Destination name', required: true }, { key: 'country', label: 'Country', required: true },
      { key: 'state', label: 'State or region', required: true }, { key: 'description', label: 'Description', type: 'textarea', required: true }, status,
    ];
    case 'packages': return [
      { key: 'name', label: 'Package name', required: true }, destination, { key: 'description', label: 'Description', type: 'textarea', required: true },
      { key: 'duration', label: 'Duration in days', type: 'number', required: true }, { key: 'base_price', label: 'Price per passenger', type: 'number', required: true },
      { key: 'max_passengers', label: 'Maximum passengers', type: 'number', required: true }, { key: 'available_from', label: 'Available from', type: 'date', required: true },
      { key: 'available_until', label: 'Available until', type: 'date', required: true }, { key: 'cancellation_policy', label: 'Cancellation policy', type: 'textarea', required: true },
      { key: 'status', label: 'Availability', type: 'select', required: true, options: [{ value: 'draft', label: 'Inactive' }, { value: 'published', label: 'Active' }] },
    ];
    case 'hotels': return [
      { key: 'name', label: 'Hotel name', required: true }, destination, { key: 'description', label: 'Description', type: 'textarea', required: true },
      { key: 'location', label: 'Location', required: true }, { key: 'contact_details', label: 'Contact details', required: true },
      { key: 'star_rating', label: 'Star rating', type: 'number', required: true }, { key: 'amenities', label: 'Amenities', type: 'list' }, status,
    ];
    case 'rooms': return [
      { key: 'hotel_id', label: 'Hotel', type: 'select', required: true, options: hotelsFor(hotels) },
      { key: 'room_type', label: 'Room type', required: true }, { key: 'description', label: 'Description', type: 'textarea', required: true },
      { key: 'capacity', label: 'Guest capacity', type: 'number', required: true }, { key: 'nightly_rate', label: 'Nightly rate', type: 'number', required: true },
      { key: 'total_units', label: 'Total units', type: 'number', required: true }, status,
    ];
    case 'activities': return [
      { key: 'name', label: 'Activity name', required: true }, destination, { key: 'description', label: 'Description', type: 'textarea', required: true },
      { key: 'duration_minutes', label: 'Duration in minutes', type: 'number', required: true }, { key: 'price', label: 'Price', type: 'number', required: true },
      { key: 'price_unit', label: 'Price unit', type: 'select', required: true, options: [{ value: 'per_person', label: 'Per person' }, { value: 'per_group', label: 'Per group' }] }, status,
    ];
    case 'guides': return [
      { key: 'name', label: 'Guide name', required: true }, destination, { key: 'bio', label: 'Bio', type: 'textarea', required: true },
      { key: 'languages', label: 'Languages', type: 'list' }, { key: 'experience_years', label: 'Years of experience', type: 'number', required: true },
      { key: 'fee', label: 'Fee', type: 'number', required: true }, status,
    ];
    case 'vehicles': return [
      { key: 'name', label: 'Vehicle name', required: true }, { key: 'vehicle_type', label: 'Vehicle type', required: true },
      { ...destination, required: false }, { key: 'capacity', label: 'Passenger capacity', type: 'number', required: true },
      { key: 'daily_fee', label: 'Daily fee', type: 'number', required: true }, status,
    ];
    default: return [];
  }
}

const columns: Record<string, { key: string; label: string }[]> = {
  destinations: [{ key: 'name', label: 'Destination' }, { key: 'state', label: 'Region' }, { key: 'country', label: 'Country' }, { key: 'status', label: 'Status' }],
  packages: [{ key: 'name', label: 'Package' }, { key: 'destination_name', label: 'Destination' }, { key: 'available_from', label: 'Available from' }, { key: 'available_until', label: 'Available until' }, { key: 'duration', label: 'Days' }, { key: 'base_price', label: 'Price' }, { key: 'status', label: 'Availability' }],
  hotels: [{ key: 'name', label: 'Hotel' }, { key: 'location', label: 'Location' }, { key: 'destination_name', label: 'Destination' }, { key: 'star_rating', label: 'Stars' }, { key: 'status', label: 'Status' }],
  rooms: [{ key: 'room_type', label: 'Room' }, { key: 'hotel_name', label: 'Hotel' }, { key: 'capacity', label: 'Capacity' }, { key: 'nightly_rate', label: 'Nightly rate' }, { key: 'total_units', label: 'Units' }, { key: 'status', label: 'Status' }],
  activities: [{ key: 'name', label: 'Activity' }, { key: 'destination_name', label: 'Destination' }, { key: 'duration_minutes', label: 'Minutes' }, { key: 'price', label: 'Price' }, { key: 'status', label: 'Status' }],
  guides: [{ key: 'name', label: 'Guide' }, { key: 'destination_name', label: 'Destination' }, { key: 'languages', label: 'Languages' }, { key: 'experience_years', label: 'Experience' }, { key: 'fee', label: 'Fee' }, { key: 'status', label: 'Status' }],
  vehicles: [{ key: 'name', label: 'Vehicle' }, { key: 'vehicle_type', label: 'Type' }, { key: 'capacity', label: 'Capacity' }, { key: 'daily_fee', label: 'Daily fee' }, { key: 'status', label: 'Status' }],
  departures: [{ key: 'departure_id', label: 'Departure' }, { key: 'package_id', label: 'Package ID' }, { key: 'travel_date', label: 'Travel date' }, { key: 'capacity', label: 'Capacity' }, { key: 'status', label: 'Status' }],
  bookings: [
    { key: 'booking_id', label: 'Booking ID' }, { key: 'customer_name', label: 'Customer' }, { key: 'customer_email', label: 'Email' },
    { key: 'package_name', label: 'Package' }, { key: 'destination_name', label: 'Destination' }, { key: 'travel_date', label: 'Travel date' },
    { key: 'passenger_count', label: 'Passengers' }, { key: 'hotel_name', label: 'Hotel' }, { key: 'room_type', label: 'Room' },
    { key: 'activities', label: 'Activities' }, { key: 'guide_name', label: 'Guide' }, { key: 'vehicle_name', label: 'Vehicle' },
    { key: 'amount', label: 'Amount' }, { key: 'payment_status', label: 'Payment' }, { key: 'booking_status', label: 'Booking' },
  ],
  customers: [{ key: 'name', label: 'Customer' }, { key: 'email', label: 'Email' }, { key: 'phone', label: 'Phone' }, { key: 'address', label: 'Address' }, { key: 'created_at', label: 'Joined' }],
  payments: [{ key: 'payment_record_id', label: 'Payment' }, { key: 'booking_id', label: 'Booking ID' }, { key: 'amount', label: 'Amount' }, { key: 'currency', label: 'Currency' }, { key: 'status', label: 'Status' }, { key: 'created_at', label: 'Date' }],
  invoices: [{ key: 'invoice_number', label: 'Invoice' }, { key: 'booking_id', label: 'Booking ID' }, { key: 'customer_id', label: 'Customer ID' }, { key: 'amount', label: 'Amount' }, { key: 'status', label: 'Status' }, { key: 'created_at', label: 'Created' }],
  refunds: [{ key: 'refund_record_id', label: 'Refund' }, { key: 'booking_id', label: 'Booking ID' }, { key: 'refund_amount', label: 'Amount' }, { key: 'reason', label: 'Reason' }, { key: 'status', label: 'Status' }, { key: 'refund_date', label: 'Date' }],
};

const recordId = (resource: string, item: ApiRecord) => {
  const fields: Record<string, string> = { destinations: 'destination_id', packages: 'package_id', hotels: 'hotel_id', rooms: 'room_id', activities: 'activity_id', guides: 'guide_id', vehicles: 'vehicle_id', departures: 'departure_id', bookings: 'booking_id', customers: 'customer_id', payments: 'payment_record_id', invoices: 'invoice_record_id', refunds: 'refund_record_id' };
  return String(item[fields[resource]] || item.id || item._id || '');
};
const display = (value: unknown, key = '') => {
  if (Array.isArray(value)) return value.map(entry => typeof entry === 'object' && entry ? (entry as ApiRecord).url || '' : String(entry)).filter(Boolean).join(', ');
  if (value && typeof value === 'object') return JSON.stringify(value);
  if (value === undefined || value === null || value === '') return '—';
  if (typeof value === 'number' && ['amount', 'base_price', 'nightly_rate', 'daily_fee', 'refund_amount', 'fee', 'price'].includes(key)) return `₹${value.toLocaleString('en-IN')}`;
  return String(value);
};

function Login() {
  const location = useLocation();
  const navigate = useNavigate();
  const [credentials, setCredentials] = useState({ email: '', password: '' });
  const [error, setError] = useState(new URLSearchParams(location.search).has('session_expired') ? 'Your admin session expired. Sign in again.' : '');
  const [submitting, setSubmitting] = useState(false);
  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setSubmitting(true);
    setError('');
    try {
      const result = await api.admin.login(credentials);
      localStorage.setItem('admin_access_token', result.access_token);
      navigate('/admin', { replace: true });
    } catch (exception) {
      setError((exception as Error).message);
    } finally {
      setSubmitting(false);
    }
  };
  return <main className="admin-login">
    <div className="admin-login-art"><span className="admin-kicker">TRAVELEASE / OPERATIONS</span><h1>Good journeys,<br /><em>well run.</em></h1><p>Platform administration</p></div>
    <form className="admin-login-form" onSubmit={submit}>
      <span className="admin-kicker">ADMIN ACCESS</span><h2>Sign in</h2><p>Use your administrator account to continue.</p>
      <label>Email address<input type="email" autoComplete="username" required value={credentials.email} onChange={event => setCredentials({ ...credentials, email: event.target.value })} /></label>
      <label>Password<input type="password" autoComplete="current-password" required value={credentials.password} onChange={event => setCredentials({ ...credentials, password: event.target.value })} /></label>
      {error && <div className="admin-alert" role="alert">{error}</div>}
      <button className="admin-primary" disabled={submitting}>{submitting ? 'Signing in…' : 'Sign in to dashboard'} <span aria-hidden="true">→</span></button>
      <a className="admin-back-link" href="/">← Return to TravelEase</a>
    </form>
  </main>;
}

function AdminApp() {
  const location = useLocation();
  const navigate = useNavigate();
  const isLogin = location.pathname === '/admin/login' || location.pathname === '/admin/login/';
  const routeSection = location.pathname.replace(/^\/admin\/?/, '').split('/')[0];
  const section = sections.some(item => item.id === routeSection) ? routeSection : 'dashboard';
  const [session, setSession] = useState<ApiRecord | null>(null);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [records, setRecords] = useState<ApiRecord[]>([]);
  const [destinations, setDestinations] = useState<ApiRecord[]>([]);
  const [hotels, setHotels] = useState<ApiRecord[]>([]);
  const [search, setSearch] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [editor, setEditor] = useState<ApiRecord | null>(null);
  const [values, setValues] = useState<ApiRecord>({});
  const [images, setImages] = useState<string[]>([]);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    if (isLogin) return;
    if (!localStorage.getItem('admin_access_token')) {
      navigate('/admin/login', { replace: true });
      return;
    }
    api.admin.session().then(setSession).catch(() => {
      localStorage.removeItem('admin_access_token');
      navigate('/admin/login', { replace: true });
    });
  }, [isLogin, navigate]);

  useEffect(() => {
    if (!session || isLogin) return;
    setError('');
    setBusy(true);
    const load = section === 'dashboard'
      ? Promise.all([api.admin.overview(), api.admin.records('bookings')]).then(([overview, bookings]) => {
        setSummary(overview as Summary);
        setRecords(bookings);
      })
      : api.admin.records(section, search).then(setRecords);
    const references = Promise.all([api.admin.records('destinations'), api.admin.records('hotels')]).then(([destinationItems, hotelItems]) => {
      setDestinations(destinationItems);
      setHotels(hotelItems);
    });
    Promise.all([load, references]).catch(exception => setError((exception as Error).message)).finally(() => setBusy(false));
  }, [section, search, session, isLogin]);

  if (isLogin) return <Login />;
  if (!session) return <main className="admin-loading"><span /> Verifying administrator access</main>;

  const logout = () => {
    localStorage.removeItem('admin_access_token');
    setSession(null);
    navigate('/admin/login', { replace: true });
  };
  const openEditor = (item: ApiRecord | null = null) => {
    setEditor(item || {});
    const nextValues: ApiRecord = {};
    for (const field of fieldsFor(section, destinations, hotels)) {
      const value = item?.[field.key];
      nextValues[field.key] = field.type === 'list' ? (Array.isArray(value) ? value.join(', ') : '') : (value ?? '');
    }
    if (item?.images) setImages(item.images.map((image: ApiRecord | string) => typeof image === 'string' ? image : image.url).filter(Boolean));
    else setImages([]);
    if (section === 'hotels' && !item) nextValues.status = 'active';
    if (section === 'packages' && !item) nextValues.status = 'draft';
    setValues(nextValues);
  };
  const closeEditor = () => setEditor(null);
  const save = async (event: FormEvent) => {
    event.preventDefault();
    setBusy(true);
    setError('');
    const payload: ApiRecord = { ...values };
    for (const field of fieldsFor(section, destinations, hotels)) {
      if (field.type === 'list') payload[field.key] = String(payload[field.key] || '').split(',').map(value => value.trim()).filter(Boolean);
      if (field.type === 'number') payload[field.key] = Number(payload[field.key]);
    }
    if (['destinations', 'packages', 'hotels', 'rooms', 'activities', 'guides', 'vehicles'].includes(section)) payload.images = images;
    const hotelId = payload.hotel_id;
    delete payload.hotel_id;
    try {
      if (editor && Object.keys(editor).length) await api.admin.update(section, recordId(section, editor), payload);
      else await api.admin.create(section, payload, hotelId);
      closeEditor();
      const [updatedRecords, updatedOverview] = await Promise.all([
        section === 'dashboard' ? api.admin.records('bookings') : api.admin.records(section, search),
        api.admin.overview(),
      ]);
      setRecords(updatedRecords);
      setSummary(updatedOverview as Summary);
    } catch (exception) {
      setError((exception as Error).message);
    } finally {
      setBusy(false);
    }
  };
  const upload = async (file?: File) => {
    if (!file) return;
    setUploading(true);
    setError('');
    try {
      const image = await api.admin.uploadImage(file);
      setImages(current => [...current, image.url]);
    } catch (exception) {
      setError((exception as Error).message);
    } finally {
      setUploading(false);
    }
  };
  const activeMeta = sections.find(item => item.id === section);
  const pageTitle = activeMeta?.label || 'Dashboard';
  const visibleFields = fieldsFor(section, destinations, hotels);

  return <div className="admin-app">
    <aside className="admin-sidebar">
      <a href="/admin" className="admin-brand"><span className="brand-mark">T</span><span>TravelEase<small>CONTROL ROOM</small></span></a>
      <div className="admin-nav-scroll">
        {['Inventory', 'Operations', 'People & finance'].map(group => <div className="admin-nav-group" key={group}>
          <span className="admin-nav-label">{group}</span>
          {(group === 'Inventory' ? sections.filter(item => item.group === group) : sections.filter(item => item.group === group)).map(item => <button key={item.id} className={`admin-nav-item ${section === item.id ? 'selected' : ''}`} onClick={() => navigate(`/admin/${item.id}`)}><span className="admin-nav-dot" />{item.label}</button>)}
        </div>)}
      </div>
      <button className="admin-logout" onClick={logout}><span>↗</span> Sign out</button>
    </aside>
    <main className="admin-main">
      <header className="admin-topbar"><div><span className="admin-breadcrumb">ADMIN / {section.toUpperCase()}</span><h1>{pageTitle}</h1></div><div className="admin-user"><span className="admin-avatar">{String(session.name || 'A').slice(0, 1).toUpperCase()}</span><span>{session.name || 'Administrator'}<small>{session.email}</small></span></div></header>
      {error && <div className="admin-alert page-alert" role="alert">{error}<button onClick={() => setError('')} aria-label="Dismiss error">×</button></div>}
      {section === 'dashboard' ? <section className="admin-content">
        <div className="admin-welcome"><div><span className="admin-kicker">LIVE PLATFORM DATA</span><h2>Good day, {String(session.name || 'Administrator').split(' ')[0]}.</h2><p>Here is the current shape of your travel business.</p></div><div className="welcome-date">TravelEase · Administration</div></div>
        <div className="stat-grid">{[
          ['Destinations', summary?.destinations, 'Places in the catalog'], ['Packages', summary?.packages, 'Curated journeys'],
          ['Hotels', summary?.hotels, 'Properties listed'], ['Customers', summary?.customers, 'Registered profiles'],
          ['Bookings', summary?.bookings, 'All-time reservations'], ['Gross collected', summary ? `₹${summary.revenue.toLocaleString('en-IN')}` : undefined, 'Paid and completed payments'],
        ].map(([label, value, hint]) => <article className="stat-card" key={String(label)}><span>{label}</span><strong>{value ?? '—'}</strong><small>{hint}</small></article>)}</div>
        <section className="admin-panel"><div className="panel-heading"><div><span className="admin-kicker">LATEST ACTIVITY</span><h2>Recent bookings</h2></div><button className="admin-text-action" onClick={() => navigate('/admin/bookings')}>All bookings <span>→</span></button></div><RecordTable resource="bookings" records={records.slice(0, 6)} busy={busy} onEdit={undefined} /></section>
      </section> : <section className="admin-content">
        <div className="list-toolbar"><div><span className="admin-kicker">PLATFORM RECORDS</span><p>{editable.has(section) ? 'Create, update, and publish catalog records.' : 'Current records from the TravelEase database.'}</p></div><div className="list-actions"><label className="search-box"><span aria-hidden="true">⌕</span><input value={search} onChange={event => setSearch(event.target.value)} placeholder={`Search ${pageTitle.toLowerCase()}`} aria-label={`Search ${pageTitle}`} /></label>{editable.has(section) && <button className="admin-primary compact" onClick={() => openEditor()}>＋ Add {section === 'rooms' ? 'room' : section.slice(0, -1)}</button>}</div></div>
        <section className="admin-panel record-panel"><div className="record-count">{busy ? 'Loading records…' : `${records.length} ${pageTitle.toLowerCase()} record${records.length === 1 ? '' : 's'}`}</div><RecordTable resource={section} records={records} busy={busy} onEdit={editable.has(section) ? openEditor : undefined} /></section>
      </section>}
    </main>
    {editor && <div className="admin-modal-backdrop" role="presentation" onMouseDown={event => { if (event.target === event.currentTarget) closeEditor(); }}><form className="admin-modal" onSubmit={save}>
      <header><div><span className="admin-kicker">{Object.keys(editor).length ? 'EDIT RECORD' : 'NEW RECORD'}</span><h2>{Object.keys(editor).length ? 'Update' : 'Add'} {section === 'rooms' ? 'room' : section.slice(0, -1)}</h2></div><button type="button" className="modal-close" onClick={closeEditor} aria-label="Close">×</button></header>
      <div className="admin-form-grid">{visibleFields.map(field => <label className={field.type === 'textarea' ? 'wide-field' : ''} key={field.key}>{field.label}{field.type === 'textarea' ? <textarea required={field.required} rows={3} value={values[field.key] ?? ''} onChange={event => setValues({ ...values, [field.key]: event.target.value })} /> : field.type === 'select' ? <select required={field.required} value={values[field.key] ?? ''} onChange={event => setValues({ ...values, [field.key]: event.target.value })}><option value="">Choose…</option>{field.options?.map(option => <option value={option.value} key={option.value}>{option.label}</option>)}</select> : <input type={field.type === 'list' ? 'text' : field.type || 'text'} min={field.type === 'number' ? 0 : undefined} step={field.key === 'star_rating' ? 0.5 : 'any'} required={field.required} value={values[field.key] ?? ''} onChange={event => setValues({ ...values, [field.key]: event.target.value })} placeholder={field.type === 'list' ? 'Separate values with commas' : ''} />}</label>)}</div>
      <div className="image-upload"><div><strong>Images</strong><small>Files are uploaded to Cloudinary; only their secure URLs are saved.</small></div><label className="upload-button">{uploading ? 'Uploading…' : '＋ Upload image'}<input type="file" accept="image/*" disabled={uploading} onChange={event => { void upload(event.target.files?.[0]); event.target.value = ''; }} /></label>{images.length > 0 && <div className="image-previews">{images.map((image, index) => <div key={`${image}-${index}`}><img src={image} alt="Uploaded travel listing" /><button type="button" onClick={() => setImages(current => current.filter((_, imageIndex) => imageIndex !== index))} aria-label="Remove image">×</button></div>)}</div>}</div>
      <footer><button type="button" className="admin-secondary" onClick={closeEditor}>Cancel</button><button className="admin-primary" disabled={busy || uploading}>{busy ? 'Saving…' : 'Save record'}</button></footer>
    </form></div>}
  </div>;
}

function RecordTable({ resource, records, busy, onEdit }: { resource: string; records: ApiRecord[]; busy: boolean; onEdit?: (item: ApiRecord) => void }) {
  const fields = columns[resource] || [];
  if (busy && !records.length) return <div className="table-empty">Loading records…</div>;
  if (!records.length) return <div className="table-empty"><strong>No records found</strong><span>Data will appear here when it exists in the platform.</span></div>;
  return <div className="table-scroll"><table><thead><tr>{fields.map(field => <th key={field.key}>{field.label}</th>)}{onEdit && <th>Action</th>}</tr></thead><tbody>{records.map((item, index) => <tr key={recordId(resource, item) || index}>{fields.map(field => <td key={field.key}>{field.key === 'status' || field.key.endsWith('_status') ? <span className={`status-pill ${String(item[field.key] || '').toLowerCase()}`}>{display(item[field.key], field.key)}</span> : display(item[field.key], field.key)}</td>)}{onEdit && <td><button className="edit-action" onClick={() => onEdit(item)}>Edit</button></td>}</tr>)}</tbody></table></div>;
}

export default AdminApp;
