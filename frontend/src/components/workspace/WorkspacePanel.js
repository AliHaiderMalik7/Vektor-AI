import { Paper, Title, ScrollArea, useMantineTheme, Text } from "@mantine/core";
import TravelPlan from "./TravelPlan/TravelPlan";

function WorkspacePanel({ workspaceContent }) {
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
          Fitness Plan
        </Title>
      </div>

      <ScrollArea style={{ flex: 1, padding: "20px" }}>
        {workspaceContent ? (
          <div>
            <Text style={{ whiteSpace: 'pre-wrap', color: theme.other.text }}>
              {workspaceContent.response}
            </Text>
          </div>
        ) : (
          <Text style={{ color: theme.other.text, opacity: 0.6 }}>
            Your fitness plan will appear here after generation.
          </Text>
        )}
      </ScrollArea>
    </Paper>
  );
}

export default WorkspacePanel;