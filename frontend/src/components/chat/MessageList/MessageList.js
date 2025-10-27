import { Card, Text, Avatar, useMantineTheme } from "@mantine/core";
import { IconUser } from "@tabler/icons-react";

function parseText(text) {
  if (!text) return "";

  // Handle case where text is an object (e.g., { missing_info: "..." })
  let textString = "";
  if (typeof text === "object") {
    if (text.missing_info) {
      textString = text.missing_info;
    } else if (text.response) {
      textString = text.response;
    } else {
      textString = JSON.stringify(text);
    }
  } else {
    textString = String(text);
  }

  try {
    // Replace markdown-style bold (**text**)
    let html = textString.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

    // Replace markdown-style bold (__text__)
    html = html.replace(/__(.*?)__/g, "<strong>$1</strong>");

    // Replace *text* with <em>text</em> (italic), but avoid matching ** or __
    html = html.replace(/(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)/g, "<em>$1</em>");

    // Replace newlines with <br>
    html = html.replace(/\n/g, "<br/>");

    return html;
  } catch (error) {
    console.error("Error parsing text:", error);
    // Fallback: just replace newlines
    return textString.replace(/\n/g, "<br/>");
  }
}

function MessageList({ messages }) {
  const theme = useMantineTheme();

  console.log("messages", messages);
  

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "12px",
      }}>
      {messages?.map((msg) => (
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
