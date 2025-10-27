import "./App.css";
import { useState } from "react";
import { useMantineTheme } from "@mantine/core";
import Header from "./components/Header";
import InitialInput from "./components/InitialInput";
import ChatPanel from "./components/chat/ChatPanel";
import WorkspacePanel from "./components/workspace/WorkspacePanel";

function Home() {
  const theme = useMantineTheme();
  const [messages, setMessages] = useState([]);
  const [currentPrompt, setCurrentPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [workspaceContent, setWorkspaceContent] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (currentPrompt.trim() && !loading) {
      const userMessage = { text: currentPrompt, type: "user", id: Date.now() };
      setMessages((prev) => [...prev, userMessage]);
      const promptToSend = currentPrompt;
      setCurrentPrompt("");
      setLoading(true);

      try {
        const token = localStorage.getItem("token");
        const headers = {
          "Content-Type": "application/json",
        };
        if (token) {
          headers["Authorization"] = `Bearer ${token}`;
        }

        const response = await fetch(
          `${process.env.REACT_APP_APP_URL}/model/generate`,
          {
            method: "POST",
            headers,
            body: JSON.stringify({
              prompt: promptToSend,
              model: "gpt-4o",
              conversation_id: 11,
            }),
          }
        );

        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const data = await response.json();

        setWorkspaceContent(prev => [...prev, data]);
      } catch (error) {
        const errorMessage = {
          text: "Error: Network issue - please try again",
          type: "bot",
          id: Date.now() + 1,
        };
        setMessages((prev) => [...prev, errorMessage]);
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
        backgroundColor: theme.other.background,
        overflow: "hidden",
        paddingTop: "80px", // Account for fixed header
      }}>
      <Header />

      {messages.length === 0 ? (
        <InitialInput
          currentPrompt={currentPrompt}
          setCurrentPrompt={setCurrentPrompt}
          handleSubmit={handleSubmit}
          loading={loading}
        />
      ) : (
        <div
          style={{
            flex: 1,
            display: "flex",
            padding: "0 20px 20px 20px",
            gap: "20px",
            minHeight: 0,
          }}>
          <ChatPanel
            messages={messages}
            currentPrompt={currentPrompt}
            setCurrentPrompt={setCurrentPrompt}
            handleSubmit={handleSubmit}
            loading={loading}
          />
          <WorkspacePanel workspaceContent={workspaceContent} />
        </div>
      )}
    </div>
  );
}

export default Home;
