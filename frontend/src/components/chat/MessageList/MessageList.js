import { Card, Text, Avatar, useMantineTheme } from "@mantine/core";
import { IconUser } from "@tabler/icons-react";

function parseText(text) {
  if (!text) return "";

  // Replace markdown-style bold (**text** or __text__)
  let html = text.replace(/(\*\*|__)(.*?)\1/g, "<strong>$2</strong>");

  // Replace *text* with <em>text</em> (italic)
  html = html.replace(/\*(.*?)\*/g, "<em>$1</em>");

  // Replace newlines with <br>
  html = html.replace(/\n/g, "<br/>");

  return html;
}

function MessageList({ messages }) {
  const theme = useMantineTheme();

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
            backgroundColor: theme.other.cardBackground,
            border: `1px solid ${theme.other.border}`,
          }}>
          {msg.type === "bot" ? (
            <pre
              style={{
                color: theme.other.text,
                lineHeight: 1.6,
                fontFamily: "inherit",
                whiteSpace: "pre-wrap",
                wordWrap: "break-word",
              }}
              dangerouslySetInnerHTML={{ __html: parseText(msg.text) }}
            />
          ) : (
            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <Avatar size="sm" radius="xl" color="blue">
                <IconUser size={16} />
              </Avatar>
              <Text style={{ color: theme.other.text, lineHeight: 1.6 }}>{msg.text}</Text>
            </div>
          )}
        </Card>
      ))}
    </div>
  );
}

export default MessageList;
