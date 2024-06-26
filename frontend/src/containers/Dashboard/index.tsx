import { QuestionCircleOutlined } from "@ant-design/icons";
import { Button, Card, Col, Empty, Form, Input, Row, Select } from "antd";

import { Chat } from "@/components/Chat";
import { FloatMenu } from "@/components/FloatMenu";
import { useTrans } from "@/hooks/useTrans";

import { SessionContext } from "@/providers/SessionProvider";
import { WsProvider } from "@/providers/WsProvider";
import { useForm } from "antd/es/form/Form";
import { useContext, useEffect, useState } from "react";
import styles from "./index.module.css";

export const Dashboard = () => {
  const [form] = useForm();
  const { t } = useTrans();
  const { session, newSession } = useContext(SessionContext);
  const [showStyle, setShowStyle] = useState<boolean>(false);

  useEffect(() => {
    form.setFieldsValue(session);
    if (session?.functionality === "write-properly") {
      setShowStyle(true);
    }
  }, [session, form]);

  return (
    <Row gutter={[16, 16]}>
      <Col xs={24} md={16}>
        <Card className={styles.card} title={t("English Room Chat")}>
          {session?.session_id ? (
            <WsProvider>
              <Chat />
            </WsProvider>
          ) : (
            <Empty description={t("No session found. Please create a new session.")} />
          )}
        </Card>
      </Col>
      <Col xs={24} md={8}>
        <Card className={styles.card} title={t("Your Session")}>
          <Form
            form={form}
            layout="vertical"
            onFinish={(values) => {
              newSession({
                ...values,
                style: values.functionality === "write-properly" ? values.style : null,
              });
            }}
          >
            <Form.Item name="model" label={t("Model")} rules={[{ required: true }]}>
              <Select placeholder={t("Select Model")} options={[{ value: "gpt-3.5-turbo-instruct", label: "GPT-3" }]} />
            </Form.Item>
            <Form.Item name="functionality" label={t("Functionality")} rules={[{ required: true }]}>
              <Select
                placeholder={t("Select Functionality")}
                options={[
                  { value: "write-the-same-grammar-fixed", label: "Write The Same Grammar Fixed" },
                  { value: "write-properly", label: "Write Properly" },
                  { value: "summarize", label: "Summarize" },
                ]}
                onSelect={(value) => {
                  setShowStyle(value === "write-properly");
                }}
              />
            </Form.Item>
            {showStyle && (
              <Form.Item name="style" label={t("Style Context")}>
                <Input placeholder={t("Provide Style Context")} />
              </Form.Item>
            )}
            <Form.Item>
              <Button type="primary" htmlType="submit">
                {t("Reset Session")}
              </Button>
            </Form.Item>
          </Form>
        </Card>
      </Col>
      <FloatMenu
        menu={[
          {
            key: "ask-support",
            icon: <QuestionCircleOutlined />,
            tooltip: t("Ask Support"),
            onClick: () => {
              window.open("https://t.me/ukwahlula");
            },
          },
        ]}
      />
    </Row>
  );
};
