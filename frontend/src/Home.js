import "./App.css";
import { useState } from "react";
import Header from "./components/Header";
import InitialInput from "./components/InitialInput";
import ChatPanel from "./components/chat/ChatPanel";
import WorkspacePanel from "./components/workspace/WorkspacePanel";

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
       let currentBotText = '';

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
                 // Add newline if result starts with bullet or number
                 if (result.trim().match(/^[-*]\s|^[0-9]+\./) && currentBotText && !currentBotText.endsWith('\n')) {
                   currentBotText += '\n';
                   setMessages((prev) =>
                     prev.map((msg) =>
                       msg.id === botMessageId
                         ? { ...msg, text: msg.text + '\n' }
                         : msg
                     )
                   );
                   await new Promise(resolve => setTimeout(resolve, 50)); // delay for newline
                 }
                 // Add space if needed before appending (if current text doesn't end with space and result starts with letter)
                 if (currentBotText && !currentBotText.endsWith(' ') && !currentBotText.endsWith('\n') && result.length > 0 && /[a-zA-Z]/.test(result[0])) {
                   currentBotText += ' ';
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
                   currentBotText += result[i];
                   setMessages((prev) =>
                     prev.map((msg) =>
                       msg.id === botMessageId
                         ? { ...msg, text: msg.text + result[i] }
                         : msg
                     )
                   );
                   await new Promise(resolve => setTimeout(resolve, 50)); // 50ms delay per character
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
          <WorkspacePanel />
        </div>
      )}
    </div>
  );
}

export default Home;
