import { Accordion, AccordionItem } from "@carbon/react";
import styles from "./QnA.module.scss";

interface QnAItem {
  question: string;
  answer: string;
}

interface QnAProps {
  qna: QnAItem[];
}

const QnA: React.FC<QnAProps> = ({ qna }) => {
  const hasAnswer = (item: QnAItem) => {
    return !item.answer.includes(
      "The answer cannot be determined from the provided context.",
    );
  };
  const itemTitle = (item: QnAItem) => {
    return (
      <div className={styles.question}>
        {hasAnswer(item) ? <span>✅ </span> : null}
        {item.question}
      </div>
    );
  };

  const itemContent = (item: QnAItem) => {
    return <div className={styles.answer}>{item.answer}</div>;
  };

  return (
    <div className={styles.qna_container}>
      <Accordion>
        {qna.map((item, index) => (
          <AccordionItem key={index} title={itemTitle(item)}>
            {itemContent(item)}
          </AccordionItem>
        ))}
      </Accordion>
    </div>
  );
};

export default QnA;
