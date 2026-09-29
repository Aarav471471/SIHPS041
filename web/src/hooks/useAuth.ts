import { create } from "zustand";

interface User {
  id: number;
  name: string;
  phone: string;
  role: string;
  site_id?: number;
}

interface AuthState {
  user: User | null;
  token: string | null;
  setAuth: (user: User, token: string) => void;
  logout: () => void;
}

const getStoredToken = () => localStorage.getItem("token");
const getStoredUser = () => {
  const u = localStorage.getItem("user");
  return u ? JSON.parse(u) : null;
};

export const useAuth = create<AuthState>((set) => ({
  user: getStoredUser(),
  token: getStoredToken(),
  setAuth: (user, token) => {
    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(user));
    set({ user, token });
  },
  logout: () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    set({ user: null, token: null });
  },
}));
