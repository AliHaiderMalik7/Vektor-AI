import { Card, Text } from "@mantine/core";

function parseText(text) {
  // Replace newlines with <br>
  let html = text.replace(/\n/g, '<br>');
  // Replace **text** with <strong>text</strong>
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  return html;
}

function MessageList({ messages }) {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "12px",
      }}>
      {messages.map((msg) => (
        <Card
          key={msg.id}
          shadow="sm"
          p="md"
          radius="md"
          style={{
            backgroundColor: "#2c2e33",
            border: "1px solid #373a40",
          }}>
          {msg.type === "bot" ? (
            <div
              style={{
                color: "#fff",
                lineHeight: 1.6,
                margin: 0,
                fontFamily: "inherit",
                whiteSpace: "pre-wrap",
                wordWrap: "break-word",
              }}
              dangerouslySetInnerHTML={{ __html: parseText(msg.text) }}
            />
          ) : (
            <Text style={{ color: "#fff", lineHeight: 1.6 }}>
              {msg.text}
            </Text>
          )}
        </Card>
      ))}
    </div>
  );
}

export default MessageList;