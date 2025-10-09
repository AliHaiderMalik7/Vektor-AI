import { Paper, Title, ScrollArea, useMantineTheme } from "@mantine/core";
import TravelPlan from "./TravelPlan/TravelPlan";

function WorkspacePanel() {
  const theme = useMantineTheme();

  return (
    <Paper
      style={{
        flex: 1,
        display: "flex",
        flexDirection: "column",
        backgroundColor: theme.other.surface,
        borderRadius: "12px",
        overflow: "hidden",
      }}>
      <div
        style={{
          padding: "20px",
          borderBottom: `1px solid ${theme.other.border}`,
          flexShrink: 0,
        }}>
        <Title order={4} style={{ color: theme.other.text }}>
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