import { useSelector } from "react-redux";
import { Security } from "@carbon/pictograms-react";
import styles from "./Header.module.scss";

const AppHeader = () => {
  const appName = useSelector((state: any) => state.config.appName);

  return (
    <div className={styles.header_container}>
      <div className={styles.title_container}>
        <Security className={styles.logo} />
        <div className={styles.title}>{appName}</div>
      </div>
      <div className={styles.description}>
        <span style={{ fontWeight: "bold" }}>AutoC</span> is an automated tool
        designed to extract and analyze Indicators of Compromise (IoCs) from
        open-source threat intelligence sources.
      </div>
    </div>
  );
};

export default AppHeader;
