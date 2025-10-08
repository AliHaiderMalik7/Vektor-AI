import { Paper, Title, ScrollArea } from "@mantine/core";
import TravelPlan from "./TravelPlan/TravelPlan";

function WorkspacePanel() {
  return (
    <Paper
      style={{
        flex: 1,
        display: "flex",
        flexDirection: "column",
        backgroundColor: "#25262b",
        borderRadius: "12px",
        overflow: "hidden",
      }}>
      <div
        style={{
          padding: "20px",
          borderBottom: "1px solid #373a40",
          flexShrink: 0,
        }}>
        <Title order={4} style={{ color: "#fff" }}>
          Travel Plan
        </Title>
      </div>

      <ScrollArea style={{ flex: 1, padding: "20px" }}>
        <TravelPlan />
      </ScrollArea>
    </Paper>
  );
}

export default WorkspacePanel;