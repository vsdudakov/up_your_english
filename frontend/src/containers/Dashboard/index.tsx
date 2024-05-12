import { QuestionCircleOutlined, ReloadOutlined } from "@ant-design/icons";
import { Card, Col, Row } from "antd";

import { Chat } from "@/components/Chat";
import { FloatMenu } from "@/components/FloatMenu";
import { useTrans } from "@/hooks/useTrans";

import styles from "./index.module.css";

export const Dashboard = () => {
  const { t } = useTrans();
  return (
    <Row gutter={[16, 16]} justify="center">
      <Col xs={24} md={12}>
        <Card className={styles.card} title={t("Up Your English with Chat Bot")}>
          <Chat />
        </Card>
      </Col>
      <FloatMenu
        menu={[
          {
            key: "reset-session",
            icon: <ReloadOutlined />,
            tooltip: t("Reset session"),
            onClick: () => {
              localStorage.removeItem("sessionId");
              window.location.reload();
            },
          },
          {
            key: "ask-support",
            icon: <QuestionCircleOutlined />,
            tooltip: t("Ask support"),
            onClick: () => {
              window.open("https://t.me/ukwahlula");
            },
          },
        ]}
      />
    </Row>
  );
};
