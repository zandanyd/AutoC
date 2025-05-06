import React from "react";
import { Tag } from "@carbon/react";
import styles from "./MitreTTPs.module.scss";

interface MitreTTPsProps {
  mitreTTPs: {
    id: string;
    name: string;
    confidence: number;
    url: string;
  }[];
}

const MitreTTPs: React.FC<MitreTTPsProps> = ({ mitreTTPs }) => {
  return (
    <div className={styles.mitre_ttps_container}>
      {mitreTTPs.map((ttp) => (
        <div key={ttp.id} className={styles.tooltip_wrapper}>
          <a
            href={ttp.url}
            target="_blank"
          >
            <Tag className={styles.ttp_tag}>
              {ttp.name} ({Math.round(ttp.confidence * 100)}%)
            </Tag>
          </a>
          <div className={styles.tooltip}>
            {ttp.name} ({Math.round(ttp.confidence * 100)}%)
          </div>
        </div>
      ))}
    </div>
  );
};

export default MitreTTPs;
