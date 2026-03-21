const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  image: string;
  stock: number;
  category?: string;
}

export interface CartItem {
  id: number;
  product: Product;
  quantity: number;
  user_id: number;
}

export interface User {
  id: number;
  username: string;
  email: string;
  is_admin?: boolean;
}

export interface LoginResponse {
  access_token: string;
  user: User;
}

class ApiService {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('token');
    return {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    };
  }

  async register(username: string, email: string, password: string) {
    const response = await fetch(`${API_BASE_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, email, password }),
    });
    if (!response.ok) throw new Error('Registration failed');
    return response.json();
  }

  async login(email: string, password: string): Promise<LoginResponse> {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    if (!response.ok) throw new Error('Login failed');
    return response.json();
  }

  async getProducts(): Promise<Product[]> {
    const response = await fetch(`${API_BASE_URL}/`, {
      headers: this.getAuthHeaders(),
    });
    if (!response.ok) throw new Error('Failed to fetch products');
    return response.json();
  }

  async addProduct(product: Omit<Product, 'id'>) {
    const response = await fetch(`${API_BASE_URL}/admin/add-product`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(product),
    });
    if (!response.ok) throw new Error('Failed to add product');
    return response.json();
  }

  async updateProduct(id: number, product: Partial<Product>) {
    const response = await fetch(`${API_BASE_URL}/admin/update-product/${id}`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(product),
    });
    if (!response.ok) throw new Error('Failed to update product');
    return response.json();
  }

  async deleteProduct(id: number) {
    const response = await fetch(`${API_BASE_URL}/admin/delete-product/${id}`, {
      method: 'DELETE',
      headers: this.getAuthHeaders(),
    });
    if (!response.ok) throw new Error('Failed to delete product');
    return response.json();
  }

  async getCart(userId: number): Promise<CartItem[]> {
    const response = await fetch(`${API_BASE_URL}/cart/${userId}`, {
      headers: this.getAuthHeaders(),
    });
    if (!response.ok) throw new Error('Failed to fetch cart');
    return response.json();
  }

 async addToCart(productId: number, quantity: number = 1, userId: number) {
  const response = await fetch(`${API_BASE_URL}/cart/add`, {
    method: 'POST',
    headers: this.getAuthHeaders(),
    body: JSON.stringify({
      user_id: userId,          
      product_id: productId,
      quantity
    }),
  });

  if (!response.ok) throw new Error('Failed to add to cart');
  return response.json();
}

  async removeFromCart(cartItemId: number) {
    const response = await fetch(`${API_BASE_URL}/cart/remove/${cartItemId}`, {
      method: 'DELETE',
      headers: this.getAuthHeaders(),
    });
    if (!response.ok) throw new Error('Failed to remove from cart');
    return response.json();
  }

 async chatWithAgent(message: string) {
  const response = await fetch(`${API_BASE_URL}/agent`, {
    method: 'POST',
    headers: this.getAuthHeaders(),
    body: JSON.stringify({ message: message })
  });

  if (!response.ok) throw new Error('Failed to get agent response');
  return response.json();
}
}

export const api = new ApiService();
