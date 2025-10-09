import { Paper, Title, ScrollArea, useMantineTheme } from "@mantine/core";
import MessageList from "./MessageList/MessageList";
import InputForm from "./InputForm/InputForm";

function ChatPanel({ messages, currentPrompt, setCurrentPrompt, handleSubmit, loading }) {
  const theme = useMantineTheme();

  return (
    <Paper
      style={{
        flex: "0 0 35%",
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
          Conversation
        </Title>
      </div>

      <ScrollArea style={{ flex: 1, padding: "20px" }}>
        <MessageList messages={messages} />
      </ScrollArea>

      <InputForm
        currentPrompt={currentPrompt}
        setCurrentPrompt={setCurrentPrompt}
        handleSubmit={handleSubmit}
        loading={loading}
      />
    </Paper>
  );
}

export default ChatPanel;