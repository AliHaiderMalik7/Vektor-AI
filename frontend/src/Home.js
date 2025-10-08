import {
  Avatar,
  Title,
  Textarea,
  Button,
  Group,
  Text,
  Grid,
  Card,
  ScrollArea,
  Paper,
} from "@mantine/core";
import "./App.css";
import { useState } from "react";

function Home() {
  const [messages, setMessages] = useState([]);
  const [currentPrompt, setCurrentPrompt] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (currentPrompt.trim() && !loading) {
      const userMessage = { text: currentPrompt, type: "user", id: Date.now() };
      setMessages(prev => [...prev, userMessage]);
      const promptToSend = currentPrompt;
      setCurrentPrompt("");
      setLoading(true);

      const botMessageId = Date.now() + 1;
      setMessages(prev => [...prev, { text: "", type: "bot", id: botMessageId }]);

      try {
       const response = await fetch(
         "https://mellifluous-noncalculative-gwenn.ngrok-free.dev/model/generate",
         {
           method: "POST",
           headers: {
             "Content-Type": "application/json",
           },
           body: JSON.stringify({
            stream:true,
             prompt: promptToSend,
             model: "gpt-4.1-mini",
             system_message: "You are a helpful travel assistant.",
             enable_web_search: true,
           }),
         }
       );

       console.log("response", response);
       

       if (!response.ok) throw new Error(`HTTP ${response.status}`);

       const reader = response.body?.getReader();
       console.log("reeader result", reader);
       
       if (!reader)
         throw new Error("Streaming not supported or no body returned.");

       const decoder = new TextDecoder();
       console.log("decoder", decoder);
       
       let buffer = "";
       let hasStreamed = false;
       let appendPromise = Promise.resolve();
       let lastChar = '';

       while (true) {
         const { done, value } = await reader.read();
         console.log("done and val", done,value);
         console.log("Decoded chunk:", decoder.decode(value));

         if (done) break;

         hasStreamed = true;
         buffer += decoder.decode(value, { stream: true });

         const lines = buffer.split("\n");
         buffer = lines.pop();
        console.log("lines", lines);
        


         for (const line of lines) {
           if (line.startsWith("data: ")) {
             const jsonStr = line.slice(6).trim();
             if (jsonStr && jsonStr !== "[DONE]") {
               // Treat jsonStr as plain text result
               const result = jsonStr;
               // Chain the appending to ensure sequential display
               appendPromise = appendPromise.then(async () => {
                 // Add space if needed between words (if last char is letter and first is letter)
                 if (lastChar && /[a-zA-Z]/.test(lastChar) && result.length > 0 && /[a-zA-Z]/.test(result[0])) {
                   setMessages((prev) =>
                     prev.map((msg) =>
                       msg.id === botMessageId
                         ? { ...msg, text: msg.text + ' ' }
                         : msg
                     )
                   );
                   await new Promise(resolve => setTimeout(resolve, 50)); // delay for space
                 }
                 for (let i = 0; i < result.length; i++) {
                   await new Promise(resolve => setTimeout(resolve, 50)); // 50ms delay per character
                   setMessages((prev) =>
                     prev.map((msg) =>
                       msg.id === botMessageId
                         ? { ...msg, text: msg.text + result[i] }
                         : msg
                     )
                   );
                 }
                 if (result.length > 0) {
                   lastChar = result[result.length - 1];
                 }
               });
             }
           }
         }
       }

       // fallback if nothing streamed
       if (!hasStreamed) {
         setMessages((prev) =>
           prev.map((msg) =>
             msg.id === botMessageId
               ? { ...msg, text: "No streamed data received from server." }
               : msg
           )
         );
       }

      } catch (error) {
        const errorMessage = { text: 'Error: Network issue - please try again', type: "bot", id: Date.now() + 1 };
        setMessages(prev => [...prev, errorMessage]);
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        backgroundColor: "#1a1b1e",
        overflow: "hidden",
      }}>
      {/* Header */}
      <Group
        position="apart"
        align="center"
        style={{ padding: "20px", flexShrink: 0 }}>
        <Group style={{ paddingLeft: "20px" }}>
          <Avatar radius="xl" style={{ backgroundColor: "#4db6ac" }}>
            U
          </Avatar>
          <Title order={3} style={{ color: "#fff", fontWeight: 600 }}>
            Vektor.ai
          </Title>
        </Group>
      </Group>

      {messages.length === 0 ? (
        // Initial State - Centered Input
        <div
          style={{
            flex: 1,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            padding: "20px",
          }}>
          <div
            style={{ width: "100%", maxWidth: "600px", textAlign: "center" }}>
            <Title
              order={1}
              style={{ color: "#fff", marginBottom: "20px", fontWeight: 700 }}>
              Discover Your Next Adventure
            </Title>
            <Text size="lg" color="dimmed" style={{ marginBottom: "30px" }}>
              Enter your travel prompt below to get personalized recommendations
            </Text>
            <form onSubmit={handleSubmit}>
              <Textarea
                value={currentPrompt}
                onChange={(e) => setCurrentPrompt(e.target.value)}
                placeholder="e.g., Plan a 7-day trip to Japan in spring"
                size="lg"
                minRows={6}
                style={{ marginBottom: "20px" }}
                styles={{
                  input: {
                    fontSize: "16px",
                    fontWeight: 500,
                    backgroundColor: "#2c2e33",
                    color: "#fff",
                    minHeight: "150px",
                    border: "1px solid #373a40",
                  },
                }}
              />
              <Button
                type="submit"
                size="lg"
                loading={loading}
                disabled={loading}
                style={{
                  fontWeight: 600,
                  fontSize: "16px",
                  background:
                    "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                }}>
                {loading ? "Generating..." : "Generate Travel Plan"}
              </Button>
            </form>
          </div>
        </div>
      ) : (
        // Chat Interface - Full Screen Layout
        <div
          style={{
            flex: 1,
            display: "flex",
            padding: "0 20px 20px 20px",
            gap: "20px",
            minHeight: 0, // Important for flex children
          }}>
          {/* Left Panel - Conversation */}
          <Paper
            style={{
              flex: "0 0 500px",
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
                    <Text style={{ color: "#fff", lineHeight: 1.6 }}>
                      {msg.text}
                    </Text>
                  </Card>
                ))}
              </div>
            </ScrollArea>

            {/* Input at bottom of left panel */}
            <div
              style={{
                padding: "20px",
                borderTop: "1px solid #373a40",
                flexShrink: 0,
              }}>
              <form
                onSubmit={handleSubmit}
                style={{
                  display: "flex",
                  gap: "12px",
                  alignItems: "flex-end",
                }}>
                <Textarea
                  value={currentPrompt}
                  onChange={(e) => setCurrentPrompt(e.target.value)}
                  placeholder="Continue conversation..."
                  size="md"
                  minRows={2}
                  style={{ flex: 1 }}
                  styles={{
                    input: {
                      fontSize: "14px",
                      fontWeight: 500,
                      backgroundColor: "#2c2e33",
                      color: "#fff",
                      border: "1px solid #373a40",
                    },
                  }}
                />
                <Button
                  type="submit"
                  size="md"
                  loading={loading}
                  disabled={loading}
                  style={{
                    fontWeight: 600,
                    background:
                      "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    height: "fit-content",
                    minHeight: "42px",
                  }}>
                  {loading ? "Generating..." : "Send"}
                </Button>
              </form>
            </div>
          </Paper>

          {/* Right Panel - Workspace */}
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
              <div style={{ color: "#fff", lineHeight: 1.8 }}>
                {/* Sample travel plan content - replace with actual AI response */}
                <Text
                  size="lg"
                  weight={600}
                  style={{ color: "#fff", marginBottom: "16px" }}>
                  Your Personalized Japan Itinerary
                </Text>
                <Text style={{ color: "#c1c2c5", marginBottom: "20px" }}>
                  Based on your preferences, here's a customized 7-day spring
                  itinerary for Japan...
                </Text>

                {/* Add more detailed travel plan content here */}
                <div style={{ display: "grid", gap: "16px" }}>
                  {[
                    "Day 1: Tokyo Arrival",
                    "Day 2: Tokyo Exploration",
                    "Day 3: Hakone & Mount Fuji",
                    "Day 4: Kyoto Travel",
                    "Day 5: Kyoto Temples",
                    "Day 6: Osaka Day Trip",
                    "Day 7: Departure",
                  ].map((day, index) => (
                    <Card
                      key={index}
                      style={{
                        backgroundColor: "#2c2e33",
                        border: "1px solid #373a40",
                      }}>
                      <Text weight={500} style={{ color: "#fff" }}>
                        {day}
                      </Text>
                    </Card>
                  ))}
                </div>
              </div>
            </ScrollArea>
          </Paper>
        </div>
      )}
    </div>
  );
}

export default Home;
