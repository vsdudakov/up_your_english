import React, { useCallback, useContext, useEffect, useMemo, useState } from "react";
import { Input as ChatInput, MessageList, type MessageType } from "react-chat-elements";
import "react-chat-elements/dist/main.css";
import { useMutation } from "@tanstack/react-query";
import { Button, theme } from "antd";

import { postFetcher } from "@/helpers/fetchers";
import { useTrans } from "@/hooks/useTrans";

import { WsContext } from "@/providers/WsProvider";
import styles from "./index.module.css";

const { useToken } = theme;

interface IMessage {
  msg: string;
  name: string;
  date: string;
}

export const Chat: React.FC = () => {
  const inputRef: React.RefObject<HTMLTextAreaElement> = React.createRef();
  const listRef = React.createRef();
  const [inputValue, setInputValue] = useState<string>("");
  const { token } = useToken();
  const [messages, setMessages] = useState<IMessage[]>([]);
  const [typing, setTyping] = useState<boolean>(false);
  const { lastJsonMessage, isReady } = useContext(WsContext);

  const { t } = useTrans();

  useEffect(() => {
    if (lastJsonMessage) {
      switch (lastJsonMessage.message_type) {
        case "MESSAGE":
          setTyping(false);
          setMessages((prevMessages) => [...prevMessages, lastJsonMessage.payload]);
          break;
        case "TYPING":
          setTyping(true);
          break;
      }
    }
  }, [lastJsonMessage]);

  const { mutate: sendMessageMutate } = useMutation({
    mutationFn: (payload: IMessage) => postFetcher("/api/chat/message", payload) as Promise<IMessage>,
    onSuccess: (message: IMessage) => {
      setMessages((prevMessages) => [...prevMessages, message]);
      if (listRef.current) {
        // biome-ignore lint/suspicious/noExplicitAny: <explanation>
        (listRef.current as any).scrollToBottom(); // eslint-disable-line
      }
    },
  });

  const sendMessage = useCallback(
    (message: string) => {
      sendMessageMutate({
        msg: message,
        name: t("You"),
        date: new Date().getTime().toString(),
      });
    },
    [t, sendMessageMutate],
  );

  const messageData: MessageType[] = useMemo(() => {
    return (
      typing
        ? [
            ...messages,
            {
              msg: t("Typing..."),
              name: t("AI Agent"),
              date: new Date().getTime().toString(),
            },
          ]
        : messages
    ).map((value: IMessage, index: number) => {
      const position = value.name === t("You") ? "right" : "left";
      const date = Number.parseInt(value.date);

      return {
        position: position,
        type: "text",
        title: value.name,
        text: value.msg,
        focus: false,
        id: index,
        date: date,
        titleColor: "#4f81a1",
        forwarded: false,
        replyButton: false,
        removeButton: false,
        status: "read",
        notch: false,
        retracted: false,
      };
    });
  }, [messages, t, typing]);

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
            disabled={!inputValue || typing || !isReady}
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
