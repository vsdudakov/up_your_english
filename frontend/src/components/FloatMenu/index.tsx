import { MenuFoldOutlined } from "@ant-design/icons";
import { Dropdown, FloatButton, Tooltip } from "antd";
import classNames from "classnames";

import { useIsMobile } from "@/hooks/useIsMobile";

import styles from "./index.module.css";

export interface MenuItem {
  key: string;
  tooltip: string;
  icon: React.ReactNode;
  onClick: () => void;
  active?: boolean;
}

interface IFloatMenuProps {
  menu: MenuItem[];
  style?: React.CSSProperties;
}

export const FloatMenu: React.FC<IFloatMenuProps> = ({ menu, style }) => {
  const isMobile = useIsMobile();
  if (isMobile) {
    const menuActive = menu.some((item) => item.active);
    if (menu.length === 1) {
      const item = menu[0];
      return (
        <Tooltip title={item.tooltip} placement="leftTop" key={item.key}>
          <FloatButton
            style={style}
            className={classNames(styles.mobileFloatMenu, {
              [styles.activeBtn]: menuActive,
            })}
            type="primary"
            icon={item.icon}
            onClick={item.onClick}
          />
        </Tooltip>
      );
    }
    return (
      <Dropdown
        overlayStyle={style}
        trigger={["click"]}
        menu={{
          items: menu.map((item) => ({
            key: item.key,
            icon: item.icon,
            label: item.tooltip,
            className: classNames({ [styles.activeBtn]: item.active }),
          })),
          onClick: ({ key }) => {
            const item = menu.find((item) => item.key === key);
            item?.onClick();
          },
        }}
        placement="topLeft"
      >
        <FloatButton
          className={classNames(styles.mobileFloatMenu, {
            [styles.activeBtn]: menuActive,
          })}
          type="primary"
          icon={<MenuFoldOutlined />}
        />
      </Dropdown>
    );
  }
  return (
    <FloatButton.Group className={styles.desktopFloatMenu}>
      {menu.map((item) => (
        <Tooltip title={item.tooltip} placement="left" key={item.key}>
          <FloatButton
            className={classNames({ [styles.activeBtn]: item.active })}
            type="primary"
            icon={item.icon}
            onClick={item.onClick}
          />
        </Tooltip>
      ))}
    </FloatButton.Group>
  );
};
