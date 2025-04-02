import { Content, Theme } from "@carbon/react";
import DashboardPage from "./pages/Dashboard/DashboardPage.tsx";

function App() {
  return (
    <Theme theme={"g100"}>
      <Content>
        <DashboardPage />
      </Content>
    </Theme>
  );
}

export default App;
