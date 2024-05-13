import { useContext, useEffect, useState } from "react";

import type { IMessage } from "@/interfaces/chat";
import { WsContext } from "@/providers/WsProvider";

export const useMessage = () => {
  const { lastJsonMessage } = useContext(WsContext);
  const [message, setMessage] = useState<IMessage | null>(null);

  useEffect(() => {
    switch (lastJsonMessage?.message_type) {
      case "WELCOME":
      case "TYPING":
      case "MESSAGE":
        setMessage(lastJsonMessage.message);
        break;
      case "MESSAGE_CHUNK":
        setMessage((prevMessage) => {
          if (prevMessage) {
            const message = prevMessage.message + lastJsonMessage.message.message;
            return {
              ...prevMessage,
              message: message.trim().replace("Typing...", ""),
            };
          }
          return lastJsonMessage.message;
        });
        break;
    }
  }, [lastJsonMessage]);

  return message;
};
