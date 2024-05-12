import axios from "axios";

const requestOptions = () => {
  return {
    withCredentials: true,
    headers: {
      "Content-Type": "application/json",
    },
  };
};

const instance = axios.create({
  baseURL: import.meta.env.VITE_SERVER_DOMAIN,
  ...requestOptions(),
});

export const getFetcher = async (url: string, params?: unknown): Promise<unknown> => {
  const response = await instance.get(url, {
    params,
  });
  return response.data;
};

export const postFetcher = async (url: string, payload: unknown): Promise<unknown> => {
  const response = await instance.post(url, payload);
  return response.data;
};

export const patchFetcher = async (url: string, payload: unknown): Promise<unknown> => {
  const response = await instance.patch(url, payload);
  return response.data;
};

export const deleteFetcher = async (url: string): Promise<unknown> => {
  const response = await instance.delete(url);
  return response.data;
};
