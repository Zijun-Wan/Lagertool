import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './itemTable.css';

const exampleItems = [
  {
    id: 1,
    name: "Hammer",
    remaining_quantity: 12,
    location: "Aisle 3"
  },
  {
    id: 2,
    name: "Screwdriver Set",
    remaining_quantity: 5,
    location: "Aisle 1"
  }
];

export default function ItemTable() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    let ignore = false;
    setItems(exampleItems);
    setLoading(false);
    return () => { ignore = true; };
  }, []);

  if (loading) return <div className="item-table-center">Loading...</div>;

  return (
    <div className="item-table-center">
      <table className="item-table">
        <thead>
          <tr>
            <th>Item Name</th>
            <th>Remaining Quantity</th>
            <th>Location</th>
          </tr>
        </thead>
        <tbody>
          {items.length === 0 ? (
            <tr>
              <td colSpan={3}>No items found.</td>
            </tr>
          ) : (
            items.map(item => (
              <tr
                key={item.id}
                style={{ cursor: 'pointer' }}
                onClick={() => navigate(`/items/${item.id}`)}
              >
                <td>{item.name}</td>
                <td>{item.remaining_quantity}</td>
                <td>{item.location}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
