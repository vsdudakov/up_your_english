import { BookOutlined, MenuOutlined } from "@ant-design/icons";
import { Button, Col, Dropdown, Row, Space } from "antd";
import { useNavigate } from "react-router-dom";

import { useIsMobile } from "@/hooks/useIsMobile";
import { useTrans } from "@/hooks/useTrans";

export const HeaderContent: React.FC = () => {
  const isMobile = useIsMobile();
  const { t } = useTrans();
  const navigate = useNavigate();

  return (
    <Row justify="space-between" align="middle">
      {!isMobile && (
        <Col>
          <Space>
            <Button type="link" icon={<BookOutlined />} onClick={() => navigate("/")}>
              {t("English Room")}
            </Button>
          </Space>
        </Col>
      )}
      {isMobile && (
        <Col>
          <Space>
            <Dropdown
              trigger={["click"]}
              menu={{
                onClick: ({ key }) => {
                  switch (key) {
                    case "/":
                      navigate("/");
                      break;
                    default:
                      break;
                  }
                },
                items: [
                  {
                    key: "menu",
                    type: "group",
                    label: t("Menu"),
                    children: [
                      {
                        key: "/",
                        label: t("English Room"),
                        icon: <BookOutlined />,
                      },
                    ],
                  },
                ],
              }}
            >
              <Button icon={<MenuOutlined />} />
            </Dropdown>
          </Space>
        </Col>
      )}
    </Row>
  );
};
