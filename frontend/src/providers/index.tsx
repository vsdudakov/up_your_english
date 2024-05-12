import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import { AntdProvider } from "./AntdProvider";
import { WsProvider } from "./WsProvider";

const queryClient = new QueryClient();

interface IProvidersProps {
  children: React.ReactNode;
}

export const Providers: React.FC<IProvidersProps> = ({ children }) => {
  return (
    <AntdProvider>
      <QueryClientProvider client={queryClient}>
        <WsProvider>{children}</WsProvider>
      </QueryClientProvider>
    </AntdProvider>
  );
};
