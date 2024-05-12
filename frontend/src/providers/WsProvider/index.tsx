import { createContext, useContext } from "react";
import useWebSocket from "react-use-websocket";
import { SessionContext } from "../SessionProvider";

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
  const { session } = useContext(SessionContext);
  const { sendMessage, lastJsonMessage, readyState } = useWebSocket(
    `${import.meta.env.VITE_WS_SERVER_DOMAIN}/api/ws?sesssion_id=${session?.session_id}`,
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
