import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import fetchJson from './lib/fetchJson';
import './itemDetail.css';

const exampleItems = [
  {
    id: 1,
    name: "Hammer",
    category: "Tools",
    location: "Aisle 3",
    storage_box_number: "B12",
    remaining_quantity: 12,
    booked_by: [
      { name: "Alice", quantity: 2 },
      { name: "Bob", quantity: 1 }
    ]
  },
  {
    id: 2,
    name: "Screwdriver Set",
    category: "Tools",
    location: "Aisle 1",
    storage_box_number: "A7",
    remaining_quantity: 5,
    booked_by: [
      { name: "Charlie", quantity: 2 }
    ]
  }
];

export default function ItemDetail() {
  const { itemId } = useParams();
  const [item, setItem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [modalType, setModalType] = useState(null); // 'borrow' or 'return'
  const [modalOpen, setModalOpen] = useState(false);
  const [borrowName, setBorrowName] = useState('');
  const [borrowQty, setBorrowQty] = useState(1);
  const [returnName, setReturnName] = useState('');
  const [returnQty, setReturnQty] = useState(1);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;
    // Add this part after you are done with the login part in backend, do the same with itemtable
//     async function load() {
//       try {
//         const data = await fetchJson('/api/me', { credentials: 'include' });
//         if (!ignore) setUser(data);
//       } catch (err) {
//         if (ignore) return;
//         if (err.status === 401) {
//           alert(err.message || 'Please log in first');
//           navigate('/login');
//         } else {
//           setError(err.message || 'Failed to load user');
//         }
//       }
//     }

//     load();
//     const found = exampleItems.find(i => String(i.id) === String(itemId));
//     setItem(found ? { ...found } : null);
//     setLoading(false);

//     return () => { ignore = true; };
//   }, [itemId, navigate]);

//   if (loading || !user) return <div className="item-detail-center">Loading...</div>;




// Add this part after you are done with the backend API
    // async function fetchItemDetail() {
    //   try {
    //     const data = await fetchJson(`/api/items/${itemId}`, { credentials: 'include' });
    //     if (!ignore) setItem(data);
    //   } catch (err) {
    //     if (!ignore) setItem(null);
    //   } finally {
    //     if (!ignore) setLoading(false);
    //   }
    // }
    // fetchItemDetail();
    const found = exampleItems.find(i => String(i.id) === String(itemId));
    setItem(found ? { ...found } : null);
    setLoading(false);
    return () => { ignore = true; };
  }, [itemId]);

  if (loading) return <div className="item-detail-center">Loading...</div>;
  if (!item) return <div className="item-detail-center">Item not found.</div>;

  // Modal logic
  function openModal(type) {
    setModalType(type);
    setModalOpen(true);
    setError('');
    setBorrowName('');
    setBorrowQty(1);
    setReturnName('');
    setReturnQty(1);
  }
  function closeModal() {
    setModalOpen(false);
    setError('');
  }

  // Borrow handler
  async function handleBorrow(e) {
    e.preventDefault();
    if (!borrowName.trim() || borrowQty < 1 || borrowQty > item.remaining_quantity) {
      setError('Invalid name or quantity');
      return;
    }
    // --- Backend call here ---
    // await fetchJson(`/api/items/${item.id}/borrow`, { method: 'POST', body: JSON.stringify({ name: borrowName, quantity: borrowQty }) });
    // --- Update frontend state for demo ---
    setItem(prev => {
      const booked_by = [...prev.booked_by];
      const idx = booked_by.findIndex(b => b.name === borrowName.trim());
      if (idx >= 0) {
        booked_by[idx] = { ...booked_by[idx], quantity: booked_by[idx].quantity + Number(borrowQty) };
      } else {
        booked_by.push({ name: borrowName.trim(), quantity: Number(borrowQty) });
      }
      return {
        ...prev,
        remaining_quantity: prev.remaining_quantity - Number(borrowQty),
        booked_by
      };
    });
    closeModal();
  }

  // Return handler
  async function handleReturn(e) {
    e.preventDefault();
    if (!returnName || returnQty < 1) {
      setError('Select a borrower and quantity');
      return;
    }
    const borrower = item.booked_by.find(b => b.name === returnName);
    if (!borrower || returnQty > borrower.quantity) {
      setError('Invalid return quantity');
      return;
    }
    // --- Backend call here ---
    // await fetchJson(`/api/items/${item.id}/return`, { method: 'POST', body: JSON.stringify({ name: returnName, quantity: returnQty }) });
    // --- Update frontend state for demo ---
    setItem(prev => {
      let booked_by = prev.booked_by.map(b =>
        b.name === returnName ? { ...b, quantity: b.quantity - Number(returnQty) } : b
      ).filter(b => b.quantity > 0);
      return {
        ...prev,
        remaining_quantity: prev.remaining_quantity + Number(returnQty),
        booked_by
      };
    });
    closeModal();
  }

  return (
    <div className="item-detail-center">
      <div className="item-detail-card">
        <h2>{item.name}</h2>
        <div><strong>Category:</strong> {item.category}</div>
        <div><strong>Location:</strong> {item.location}</div>
        <div><strong>Storage Box Number:</strong> {item.storage_box_number}</div>
        <div><strong>Remaining Quantity:</strong> {item.remaining_quantity}</div>
        <div style={{ margin: '16px 0' }}>
          <button className="item-detail-action" onClick={() => openModal('borrow')}>Borrow</button>
          <button className="item-detail-action" onClick={() => openModal('return')}>Return</button>
        </div>
        <div><strong>Booked By:</strong></div>
        <table className="item-detail-booked-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Quantity Taken</th>
            </tr>
          </thead>
          <tbody>
            {item.booked_by && item.booked_by.length > 0 ? (
              item.booked_by.map((person, idx) => (
                <tr key={idx}>
                  <td>{person.name}</td>
                  <td>{person.quantity}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={2}>No bookings</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      {modalOpen && (
        <div className="item-detail-modal-backdrop" onClick={closeModal}>
          <div className="item-detail-modal" onClick={e => e.stopPropagation()}>
            {modalType === 'borrow' ? (
              <form onSubmit={handleBorrow}>
                <h3>Borrow Item</h3>
                <div>
                  <label>
                    Name:
                    <input
                      type="text"
                      value={borrowName}
                      onChange={e => setBorrowName(e.target.value)}
                      required
                    />
                  </label>
                </div>
                <div>
                  <label>
                    Quantity:
                    <input
                      type="number"
                      min="1"
                      max={item.remaining_quantity}
                      value={borrowQty}
                      onChange={e => setBorrowQty(Number(e.target.value))}
                      required
                    />
                  </label>
                </div>
                {error && <div className="item-detail-error">{error}</div>}
                <div className="item-detail-modal-actions">
                  <button type="submit">Confirm</button>
                  <button type="button" onClick={closeModal}>Cancel</button>
                </div>
              </form>
            ) : (
              <form onSubmit={handleReturn}>
                <h3>Return Item</h3>
                <div>
                  <label>
                    Borrower:
                    <select
                      value={returnName}
                      onChange={e => setReturnName(e.target.value)}
                      required
                    >
                      <option value="">Select</option>
                      {item.booked_by.map((b, idx) => (
                        <option key={idx} value={b.name}>{b.name} ({b.quantity})</option>
                      ))}
                    </select>
                  </label>
                </div>
                <div>
                  <label>
                    Quantity:
                    <input
                      type="number"
                      min="1"
                      max={item.booked_by.find(b => b.name === returnName)?.quantity || 1}
                      value={returnQty}
                      onChange={e => setReturnQty(Number(e.target.value))}
                      required
                      disabled={!returnName}
                    />
                  </label>
                </div>
                {error && <div className="item-detail-error">{error}</div>}
                <div className="item-detail-modal-actions">
                  <button type="submit">Confirm</button>
                  <button type="button" onClick={closeModal}>Cancel</button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
