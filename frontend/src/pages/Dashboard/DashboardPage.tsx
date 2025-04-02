import { FlexGrid, Row, Column } from "@carbon/react";
import { useSelector } from "react-redux";
import SearchBanner from "../../components/SearchBanner/SearchBanner.tsx";
import AnalysisResult from "../../components/AnalysisResult/AnalysisResult.tsx";
import AppHeader from "../../components/Header/Header.tsx";

const DashboardPage = () => {
  const analysisResult = useSelector((state: any) => state.analysis);
  return (
    <FlexGrid condensed={true}>
      <Row>
        <Column>
          <AppHeader />
        </Column>
      </Row>
      <Row>
        <Column>
          <SearchBanner />
        </Column>
      </Row>
      {analysisResult.url && <AnalysisResult analysisResult={analysisResult} />}
    </FlexGrid>
  );
};

export default DashboardPage;
