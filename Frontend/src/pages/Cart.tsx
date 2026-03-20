import { useEffect, useState } from 'react';
import { Trash2, ShoppingBag } from 'lucide-react';
import { api } from '../services/api';
import type { CartItem } from '../services/api';

import { useAuth } from '../context/AuthContext';

export function Cart() {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    if (user) {
      loadCart();
    }
  }, [user]);

  const loadCart = async () => {
    if (!user) return;
    try {
      const data = await api.getCart(user.id);
      setCartItems(data);
    } catch (error) {
      console.error('Failed to load cart:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveItem = async (cartItemId: number) => {
    try {
      await api.removeFromCart(cartItemId);
      setCartItems(cartItems.filter((item) => item.id !== cartItemId));
    } catch (error) {
      console.error('Failed to remove item:', error);
      alert('Failed to remove item from cart');
    }
  };

  const total = cartItems.reduce((sum, item) => sum + item.product.price * item.quantity, 0);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-12">
      <div className="max-w-4xl mx-auto px-4">
        <h1 className="text-4xl font-bold text-gray-900 mb-8 flex items-center space-x-3">
          <ShoppingBag className="w-10 h-10 text-blue-600" />
          <span>Shopping Cart</span>
        </h1>

        {cartItems.length === 0 ? (
          <div className="bg-white rounded-xl shadow-lg p-12 text-center">
            <ShoppingBag className="w-20 h-20 text-gray-300 mx-auto mb-4" />
            <p className="text-xl text-gray-600 mb-4">Your cart is empty</p>
            <a
              href="/"
              className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Start Shopping
            </a>
          </div>
        ) : (
          <div className="space-y-6">
            {cartItems.map((item) => (
              <div key={item.id} className="bg-white rounded-xl shadow-lg p-6 flex items-center space-x-6">
                <div className="w-24 h-24 bg-gradient-to-br from-blue-100 to-blue-200 rounded-lg flex items-center justify-center flex-shrink-0">
                  <img
                    src={item.product.image}
                    alt={item.product.name}
                    className="w-full h-full object-cover rounded-lg"
                  />
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-bold text-gray-900 mb-1">{item.product.name}</h3>
                  <p className="text-gray-600 text-sm mb-2">{item.product.description}</p>
                  <div className="flex items-center space-x-4">
                    <span className="text-blue-600 font-semibold">Quantity: {item.quantity}</span>
                    <span className="text-gray-400">|</span>
                    <span className="text-lg font-bold text-gray-900">
                      ${(item.product.price * item.quantity).toFixed(2)}
                    </span>
                  </div>
                </div>
                <button
                  onClick={() => handleRemoveItem(item.id)}
                  className="text-red-600 hover:text-red-700 transition-colors p-2"
                  title="Remove from cart"
                >
                  <Trash2 className="w-6 h-6" />
                </button>
              </div>
            ))}

            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex justify-between items-center mb-4">
                <span className="text-xl font-semibold text-gray-700">Total:</span>
                <span className="text-3xl font-bold text-blue-600">${total.toFixed(2)}</span>
              </div>
              <button className="w-full bg-blue-600 text-white py-4 rounded-lg hover:bg-blue-700 transition-colors text-lg font-semibold">
                Proceed to Checkout
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
