import { getFetcher, postFetcher } from "@/helpers/fetchers";
import { useMutation, useQuery } from "@tanstack/react-query";
import { createContext } from "react";

interface ISession {
  session_id: string;
  model: string;
  functionality: string;
  style?: string;
}

interface ISessionContext {
  session?: ISession;
  // biome-ignore lint/suspicious/noExplicitAny: <explanation>
  newSession: (payload: any) => void; // eslint-disable-line
}

export const SessionContext = createContext<ISessionContext>({
  session: undefined,
  newSession: () => {},
});

interface ISessionProviderProps {
  children: React.ReactNode;
}

export const SessionProvider: React.FC<ISessionProviderProps> = ({ children }) => {
  const { data, refetch } = useQuery<ISession>({
    queryKey: ["/api/session"],
    queryFn: () => getFetcher("/api/session") as Promise<ISession>,
    retry: false,
    refetchOnWindowFocus: false,
  });

  const { mutate } = useMutation({
    mutationFn: (values) => postFetcher("/api/session", values),
    onSuccess: () => {
      refetch();
    },
  });

  return (
    <SessionContext.Provider
      value={{
        session: data,
        newSession: mutate,
      }}
    >
      {children}
    </SessionContext.Provider>
  );
};
