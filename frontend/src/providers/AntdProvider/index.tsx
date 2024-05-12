import { ConfigProvider, theme } from "antd";
import en_US from "antd/locale/en_US";

import { useIsMobile } from "@/hooks/useIsMobile";

interface IAntdProviderProps {
  children: React.ReactNode;
}

export const AntdProvider: React.FC<IAntdProviderProps> = ({ children }) => {
  const isMobile = useIsMobile();
  // https://ant.design/docs/spec/dark
  return (
    <ConfigProvider
      theme={{
        algorithm: theme.darkAlgorithm,
        token: {
          fontFamily: "Roboto Flex,Graphik, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif",
          colorPrimary: "#5E5EAF",
          colorText: "#FFFFFF",
          colorLink: "#FFFFFF",
          colorBgLayout: "#000000",
          colorPrimaryText: "#FFFFFF",
          borderRadius: 1,
        },
      }}
      componentSize={isMobile ? "large" : "middle"}
      locale={en_US}
    >
      {children}
    </ConfigProvider>
  );
};
