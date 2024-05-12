import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import { AntdProvider } from "./AntdProvider";
import { SessionProvider } from "./SessionProvider";

const queryClient = new QueryClient();

interface IProvidersProps {
  children: React.ReactNode;
}

export const Providers: React.FC<IProvidersProps> = ({ children }) => {
  return (
    <AntdProvider>
      <QueryClientProvider client={queryClient}>
        <SessionProvider>{children}</SessionProvider>
      </QueryClientProvider>
    </AntdProvider>
  );
};
