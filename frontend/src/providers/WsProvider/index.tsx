import { getSessionId } from "@/helpers/fetchers";
import { createContext } from "react";
import useWebSocket from "react-use-websocket";

interface IWsContext {
  sendMessage: (message: string) => void;
  // biome-ignore lint/suspicious/noExplicitAny: <explanation>
  lastJsonMessage: any | null; // eslint-disable-line
  isReady: boolean;
}

export const WsContext = createContext<IWsContext>({
  sendMessage: () => {},
  lastJsonMessage: null,
  isReady: false,
});

interface IWsProviderProps {
  children: React.ReactNode;
}

export const WsProvider: React.FC<IWsProviderProps> = ({ children }) => {
  const sessionId = getSessionId();
  const { sendMessage, lastJsonMessage, readyState } = useWebSocket(
    `${import.meta.env.VITE_WS_SERVER_DOMAIN}/api/ws?session_id=${sessionId}`,
    {
      shouldReconnect: () => true,
      retryOnError: true,
      reconnectAttempts: 10,
    },
  );

  return (
    <WsContext.Provider
      value={{
        sendMessage,
        lastJsonMessage,
        isReady: readyState === 1,
      }}
    >
      {children}
    </WsContext.Provider>
  );
};
