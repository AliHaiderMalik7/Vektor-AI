import { Paper, Title, ScrollArea } from "@mantine/core";
import MessageList from "./MessageList/MessageList";
import InputForm from "./InputForm/InputForm";

function ChatPanel({ messages, currentPrompt, setCurrentPrompt, handleSubmit, loading }) {
  return (
    <Paper
      style={{
        flex: "0 0 400px",
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