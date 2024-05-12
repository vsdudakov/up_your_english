import { Layout as AntdLayout, theme } from "antd";

import { useIsMobile } from "@/hooks/useIsMobile";

import { HeaderContent } from "./HeaderContent";
import styles from "./index.module.css";

const { Header, Content } = AntdLayout;

interface ILayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<ILayoutProps> = ({ children }) => {
  const isMobile = useIsMobile();
  const {
    token: { colorBgContainer },
  } = theme.useToken();

  return (
    <AntdLayout className={styles.layout}>
      <AntdLayout>
        <Header style={{ background: colorBgContainer }} className={styles.header}>
          <HeaderContent />
        </Header>
        <Content className={isMobile ? styles.mobileContent : styles.desktopContent}>{children}</Content>
      </AntdLayout>
    </AntdLayout>
  );
};
