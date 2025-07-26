import React from 'react';
import { useParams } from 'react-router-dom';

const mockProducts = [
  { id: 1, name: 'T-Shirt', category: 'men' },
  { id: 2, name: 'Jeans', category: 'men' },
  { id: 3, name: 'Dress', category: 'women' },
  { id: 4, name: 'Skirt', category: 'women' },
  { id: 5, name: 'Jacket', category: 'kids' },
];

const ProductList = () => {
  const { category } = useParams();
  const filtered = category ? mockProducts.filter(p => p.category === category) : mockProducts;

  return (
    <div className="product-list">
      <h2>{category ? category.toUpperCase() : 'All'} Products</h2>
      <ul>
        {filtered.map(product => (
          <li key={product.id}>
            🛍 {product.name}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ProductList;
