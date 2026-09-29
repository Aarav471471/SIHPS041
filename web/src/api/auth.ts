import { apiClient } from "./client";

export const login = async (phone: string, pin: string) => {
  const { data } = await apiClient.post("/auth/login", { phone, pin });
  return data;
};

export const getMe = async () => {
  const { data } = await apiClient.get("/auth/me");
  return data;
};
