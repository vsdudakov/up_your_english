import React, { useCallback, useContext, useEffect, useMemo, useState } from "react";
import { Input as ChatInput, MessageList, type MessageType } from "react-chat-elements";
import "react-chat-elements/dist/main.css";
import { useMutation } from "@tanstack/react-query";
import { Button, theme } from "antd";
import { v4 } from "uuid";

import { postFetcher } from "@/helpers/fetchers";
import { useTrans } from "@/hooks/useTrans";

import { useMessage } from "@/hooks/useMessage";
import type { IMessage } from "@/interfaces/chat";
import { SessionContext } from "@/providers/SessionProvider";
import { WsContext } from "@/providers/WsProvider";
import styles from "./index.module.css";

const { useToken } = theme;

export const Chat: React.FC = () => {
  const inputRef: React.RefObject<HTMLTextAreaElement> = React.createRef();
  const listRef = React.createRef();
  const { session } = useContext(SessionContext);

  const [inputValue, setInputValue] = useState<string>("");
  const { token } = useToken();
  const [messages, setMessages] = useState<Record<string, IMessage>>({});
  const { isReady } = useContext(WsContext);
  const message = useMessage();

  const { t } = useTrans();

  // biome-ignore lint/correctness/useExhaustiveDependencies: <explanation>
  useEffect(() => {
    setMessages({});
  }, [session?.session_id]);

  useEffect(() => {
    if (message) {
      setMessages((prevMessages) => {
        prevMessages[message.id] = message;
        return { ...prevMessages };
      });
    }
  }, [message]);

  const { mutate: sendMessageMutate } = useMutation({
    mutationFn: (payload: IMessage) => postFetcher("/api/chat/message", payload) as Promise<IMessage>,
    onSuccess: (message: IMessage) => {
      setMessages((prevMessages) => {
        prevMessages[message.id] = message;
        return { ...prevMessages };
      });
      if (listRef.current) {
        // biome-ignore lint/suspicious/noExplicitAny: <explanation>
        (listRef.current as any).scrollToBottom(); // eslint-disable-line
      }
    },
  });

  const sendMessage = useCallback(
    (message: string) => {
      sendMessageMutate({
        id: v4(),
        message,
        user_name: t("You"),
        timestamp: new Date().getTime(),
      });
    },
    [t, sendMessageMutate],
  );

  const messageData: MessageType[] = useMemo(() => {
    const messagesList = (messages ? Object.values(messages) : []).sort((a, b) => a.timestamp - b.timestamp);

    return messagesList.map((value: IMessage) => {
      const position = value.user_name === t("You") ? "right" : "left";

      return {
        position: position,
        type: "text",
        title: value.user_name,
        text: value.message,
        focus: false,
        id: value.id,
        date: value.timestamp,
        titleColor: "#4f81a1",
        forwarded: false,
        replyButton: false,
        removeButton: false,
        status: "read",
        notch: false,
        retracted: false,
      };
    });
  }, [messages, t]);

  return (
    <div className={styles.chatArea}>
      <MessageList
        className={styles.chatMessagesList}
        lockable={false}
        toBottomHeight={50}
        dataSource={messageData}
        referance={listRef}
      />
      <ChatInput
        className={styles.chatInput}
        referance={inputRef}
        placeholder={t("Type here...")}
        multiline={true}
        minHeight={10}
        maxHeight={100}
        autoHeight
        value={inputValue}
        rightButtons={
          <Button
            disabled={!isReady || !inputValue}
            onClick={() => {
              sendMessage(inputValue);
              setInputValue("");
              if (inputRef.current) {
                inputRef.current.value = "";
              }
            }}
          >
            {t("Send")}
          </Button>
        }
        onChange={(event: React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
          setInputValue(event.target.value);
        }}
        inputStyle={{
          height: token.controlHeight,
          backgroundColor: token.colorBgContainer,
          borderRadius: token.borderRadius,
          color: token.colorText,
          borderColor: token.colorBorder,
          borderWidth: 1,
          borderStyle: "solid",
        }}
      />
    </div>
  );
};
