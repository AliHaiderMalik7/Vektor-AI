import {
  Textarea,
  Button,
  ActionIcon,
  useMantineTheme,
  Modal,
  Text,
  Image,
  Center,
  Stack,
  Loader,
} from "@mantine/core";
import { IconMicrophone, IconMicrophoneOff } from "@tabler/icons-react";
import { useState, useEffect, useRef } from "react";

function InputForm({ currentPrompt, setCurrentPrompt, handleSubmit, loading }) {
  const theme = useMantineTheme();
  const [isRecording, setIsRecording] = useState(false);
  const [interimTranscript, setInterimTranscript] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const recognitionRef = useRef(null);

  // --- Speech Recognition setup ---
  useEffect(() => {
    if (typeof window !== "undefined" && "webkitSpeechRecognition" in window) {
      const recognition = new window.webkitSpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = "en-GB";

      recognition.onresult = (event) => {
        let finalTranscript = "";
        let interim = "";

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          } else {
            interim += transcript;
          }
        }

        if (finalTranscript) {
          setCurrentPrompt((prev) => prev + " " + finalTranscript);
          setInterimTranscript("");
          setTimeout(() => {
            handleSubmit({ preventDefault: () => {} });
          }, 500);
          setIsRecording(false);
          setIsModalOpen(false);
        } else {
          setInterimTranscript(interim);
        }
      };

      recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        setIsRecording(false);
        setInterimTranscript("");
        setIsModalOpen(false);
      };

      recognition.onend = () => {
        setIsRecording(false);
        setInterimTranscript("");
        setIsModalOpen(false);
      };

      recognitionRef.current = recognition;
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      setInterimTranscript("");
    };
  }, []);

  // --- Start/stop speech recognition ---
  useEffect(() => {
    if (recognitionRef.current) {
      if (isRecording) recognitionRef.current.start();
      else recognitionRef.current.stop();
    }
  }, [isRecording]);

  const gradient =
    theme.other?.gradient || "linear-gradient(135deg, #007bff, #00b4d8)";

  return (
    <>
      {/* 🎤 Modal shown during recording */}
      <Modal
        opened={isModalOpen}
        onClose={() => {
          setIsRecording(false);
          setIsModalOpen(false);
        }}
        centered
        size="sm"
        radius="lg"
        overlayProps={{
          blur: 3,
          backgroundOpacity: 0.55,
        }}
        title={
          <Text
            size="lg"
            fw={600}
            style={{
              color: theme.colorScheme === "light" ? "#2c3e50" : "#ffffff",
            }}>
            Listening...
          </Text>
        }>
        <Center>
          <Stack align="center" spacing="xs">
            <Image
              src="https://cdn-icons-png.flaticon.com/512/3845/3845823.png"
              alt="Speak"
              width={100}
              height={100}
              style={{ opacity: 0.9 }}
            />
            <Text size="sm" c="dimmed">
              Speak now — your words will appear below
            </Text>
            <Loader color="blue" size="sm" />
            <Text
              mt="md"
              size="md"
              ta="center"
              style={{
                minHeight: "40px",
                color: theme.colorScheme === "light" ? "#2c3e50" : "#e9ecef",
                fontStyle: "italic",
              }}>
              {interimTranscript
                ? `"${interimTranscript}"`
                : "Waiting for speech..."}
            </Text>
          </Stack>
        </Center>
      </Modal>

      {/* --- Main input area --- */}
      <div
        style={{
          padding: "16px 20px",
          borderTop: `1px solid ${theme.other?.border || "#e1e1e1"}`,
          flexShrink: 0,
          background:
            theme.colorScheme === "light"
              ? "rgba(255,255,255,0.9)"
              : "rgba(25,25,25,0.6)",
          backdropFilter: "blur(8px)",
        }}>
        <form
          onSubmit={handleSubmit}
          style={{
            display: "flex",
            alignItems: "flex-end",
            gap: "10px",
          }}>
          {/* Textarea wrapper */}
          <div style={{ position: "relative", flexGrow: 1 }}>
            <Textarea
              value={currentPrompt + interimTranscript}
              onChange={(e) => setCurrentPrompt(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
              placeholder={
                isRecording ? "Listening..." : "Type or speak your message..."
              }
              size="md"
              minRows={2}
              autosize
              disabled={isRecording}
              styles={{
                input: {
                  fontSize: "15px",
                  fontWeight: 500,
                  backgroundColor:
                    theme.other?.inputBackground ||
                    (theme.colorScheme === "light" ? "#fff" : "#1a1b1e"),
                  color:
                    theme.other?.text ||
                    (theme.colorScheme === "light" ? "#000" : "#fff"),
                  border:
                    theme.colorScheme === "light"
                      ? "2px solid #e1e5e9"
                      : `1px solid ${theme.other?.border || "#333"}`,
                  borderRadius: "14px",
                  paddingRight: "48px",
                  boxShadow:
                    theme.colorScheme === "light"
                      ? "0 4px 10px rgba(0,0,0,0.08)"
                      : "none",
                  transition: "all 0.3s ease",
                  resize: "none",
                },
              }}
            />

            {/* 🎤 Mic button inside textarea */}
            <ActionIcon
              variant="filled"
              size="lg"
              onClick={() => {
                if (recognitionRef.current) {
                  setIsRecording((prev) => !prev);
                  setIsModalOpen((prev) => !prev);
                } else {
                  alert("Speech recognition is not supported in this browser.");
                }
              }}
              style={{
                position: "absolute",
                right: "12px",
                bottom: "10px",
                background: isRecording
                  ? "linear-gradient(135deg, #ff4444, #ff6b6b)"
                  : gradient,
                boxShadow: isRecording
                  ? "0 0 12px rgba(255, 68, 68, 0.6)"
                  : "0 3px 10px rgba(0,0,0,0.15)",
                transition: "all 0.3s ease",
                borderRadius: "12px",
                width: "38px",
                height: "38px",
                zIndex: 2,
              }}>
              {isRecording ? (
                <IconMicrophoneOff size={20} />
              ) : (
                <IconMicrophone size={20} />
              )}
            </ActionIcon>
          </div>

          {/* Send button on right side */}
          <Button
            type="submit"
            size="md"
            loading={loading}
            disabled={loading}
            style={{
              fontWeight: 600,
              background: gradient,
              borderRadius: "12px",
              minHeight: "48px",
              padding: "0 22px",
              boxShadow: "0 3px 10px rgba(59,130,246,0.3)",
              transition: "transform 0.2s ease, box-shadow 0.3s ease",
            }}
            onMouseEnter={(e) =>
              (e.currentTarget.style.transform = "translateY(-2px)")
            }
            onMouseLeave={(e) =>
              (e.currentTarget.style.transform = "translateY(0)")
            }>
            {loading ? "Generating..." : "Send"}
          </Button>
        </form>
      </div>
    </>
  );
}

export default InputForm;
