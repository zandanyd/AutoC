import React from "react";
import { Tag } from "@carbon/react";
import styles from "./KeywordsCloud.module.scss";

interface KeywordsCloudProps {
  keywords: string[];
}

const KeywordsCloud: React.FC<KeywordsCloudProps> = ({ keywords }) => {
  return (
    <div className={styles.keywords_cloud_container}>
      {keywords.map((keyword) => (
        <Tag key={keyword} type="warm-gray" className={styles.keyword_tag}>
          {keyword}
        </Tag>
      ))}
    </div>
  );
};

export default KeywordsCloud;
