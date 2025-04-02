import React from "react";
import { Row, Column } from "@carbon/react";
import KeywordsCloud from "../KeywordsCloud/KeywordsCloud.tsx";
import QnA from "../QnA/QnA.tsx";
import IOCsTable from "../IOCsTable/IOCsTable.tsx";
import styles from "./AnalysisResult.module.scss";
import IOCsTypeChart from "../IOCsTypeChart/IOCsTypeChart.tsx";

interface AnalysisResultProps {
  analysisResult: any;
}

const AnalysisResult: React.FC<AnalysisResultProps> = ({ analysisResult }) => {
  const iocs = analysisResult?.iocs || [];
  const keywords = analysisResult?.keywords || [];
  const qna = analysisResult?.qna || [];

  return (
    <div className={styles.analysis_result_container}>
      <Row>
        <Column>
          <div className={styles.header_title}>🔍 Scan results</div>
        </Column>
      </Row>

      <Row>
        <Column sm={4} md={4}>
          <Row style={{ margin: 0 }}>
            <Column>
              <div className={styles.card_container}>
                <div className={styles.card_content}>
                  <IOCsTypeChart iocs={iocs} />
                </div>
              </div>
            </Column>
          </Row>
          <Row style={{ margin: 0 }}>
            <Column>
              <div className={styles.card_container}>
                <div className={styles.card_content}>
                  <div className={styles.card_title}>
                    🚨 IoCs found ({iocs.length})
                  </div>
                  <IOCsTable iocs={iocs} />
                </div>
              </div>
            </Column>
          </Row>
        </Column>

        <Column sm={4} md={4}>
          <Row style={{ margin: 0 }}>
            <Column>
              <div className={styles.card_container}>
                <div className={styles.card_content}>
                  <div className={styles.card_title}>
                    🔑 Keywords found ({keywords.length})
                  </div>
                  <KeywordsCloud keywords={keywords} />
                </div>
              </div>
            </Column>
          </Row>
          <Row style={{ margin: 0 }}>
            <Column>
              <div className={styles.card_container}>
                <div className={styles.card_content}>
                  <div className={styles.card_title}>
                    🤔 Questions & Answers
                  </div>
                  <QnA qna={qna} />
                </div>
              </div>
            </Column>
          </Row>
        </Column>
      </Row>
    </div>
  );
};

export default AnalysisResult;
