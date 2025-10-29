import {
  Textarea,
  Button,
  Title,
  Text,
  ActionIcon,
  useMantineTheme,
  Modal,
  Image,
  Center,
  Stack,
  Loader,
} from "@mantine/core";
import { IconMicrophone, IconMicrophoneOff } from "@tabler/icons-react";
import { useState, useEffect, useRef } from "react";

function InitialInput({
  currentPrompt,
  setCurrentPrompt,
  handleSubmit,
  loading,
}) {
  const theme = useMantineTheme();
  const [isRecording, setIsRecording] = useState(false);
  const [interimTranscript, setInterimTranscript] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const recognitionRef = useRef(null);

  // 🎤 Initialize speech recognition
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

  // 🎧 Handle recording state changes
  useEffect(() => {
    if (recognitionRef.current) {
      if (isRecording) {
        recognitionRef.current.start();
      } else {
        recognitionRef.current.stop();
      }
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
              {currentPrompt + interimTranscript
                ? `"${currentPrompt + interimTranscript}"`
                : "Waiting for speech..."}
            </Text>
          </Stack>
        </Center>
      </Modal>

      <div
        style={{
          flex: 1,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: "40px 20px",
        }}>
        <div
          style={{
            width: "100%",
            maxWidth: "600px",
            textAlign: "center",
          }}>
          {/* 🏔️ Title & Description */}
          <div
            style={{
              marginBottom: "28px",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              gap: "12px",
            }}>
            <Title
              order={2}
              style={{
                color: theme.colorScheme === "light" ? "#2c3e50" : "#ffffff",
                fontWeight: 700,
                fontSize: "2rem",
                lineHeight: 1.2,
                margin: 0,
              }}>
              Push Beyond Your Limits{" "}
            </Title>
            <Text
              size="md"
              style={{
                color: theme.colorScheme === "light" ? "#6c757d" : "#adb5bd",
                fontWeight: 400,
                fontSize: "1rem",
                lineHeight: 1.5,
                maxWidth: "480px",
              }}>
              Enter your fitness goal below to get personalized AI workouts.{" "}
            </Text>
          </div>

          {/* 📝 Input Form */}
          <form onSubmit={handleSubmit}>
            {/* Textarea with embedded mic icon */}
            <div style={{ position: "relative", marginBottom: "20px" }}>
              <Textarea
                value={currentPrompt + interimTranscript}
                onChange={(e) => setCurrentPrompt(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleSubmit(e);
                  }
                }}
                placeholder={
                  isRecording
                    ? "Listening..."
                    : "Generate a personalized full-body workout routine using AI"
                }
                size="md"
                minRows={4}
                disabled={isRecording}
                styles={{
                  input: {
                    fontSize: "15px",
                    fontWeight: 500,
                    backgroundColor: theme.other.inputBackground,
                    color: theme.other.text,
                    minHeight: "120px",
                    border:
                      theme.colorScheme === "light"
                        ? "2px solid #e1e5e9"
                        : `1px solid ${theme.other.border}`,
                    borderRadius: "12px",
                    boxShadow:
                      theme.colorScheme === "light"
                        ? "0 4px 12px rgba(0,0,0,0.1), inset 0 1px 2px rgba(255,255,255,0.8)"
                        : "none",
                    transition: "all 0.3s ease",
                    paddingRight: "50px", // space for mic icon
                    "&::-webkit-scrollbar": {
                      width: "8px",
                    },
                    "&::-webkit-scrollbar-thumb": {
                      backgroundColor:
                        theme.colorScheme === "dark"
                          ? theme.colors.dark[4]
                          : "#c0c0c0",
                      borderRadius: "10px",
                    },
                    "&:focus": {
                      borderColor: theme.colors.blue[5],
                      boxShadow:
                        theme.colorScheme === "light"
                          ? "0 0 0 3px rgba(59, 130, 246, 0.1)"
                          : "0 0 0 3px rgba(59, 130, 246, 0.2)",
                    },
                  },
                }}
              />

              {/* 🎤 Mic icon inside textarea */}
              <ActionIcon
                onClick={() => {
                  if (recognitionRef.current) {
                    setIsRecording((prev) => !prev);
                    setIsModalOpen((prev) => !prev);
                  } else {
                    alert(
                      "Speech recognition is not supported in this browser."
                    );
                  }
                }}
                variant="filled"
                size="lg"
                style={{
                  position: "absolute",
                  bottom: "12px",
                  right: "12px",
                  background: isRecording
                    ? "linear-gradient(135deg, #ff4444, #ff6b6b)"
                    : gradient,
                  boxShadow: isRecording
                    ? "0 0 12px rgba(255, 68, 68, 0.6)"
                    : "0 3px 10px rgba(0,0,0,0.15)",
                  transition: "all 0.3s ease",
                  borderRadius: "12px",
                  width: "40px",
                  height: "40px",
                }}>
                {isRecording ? (
                  <IconMicrophoneOff size={20} />
                ) : (
                  <IconMicrophone size={20} />
                )}
              </ActionIcon>
            </div>

            {/* Submit Button */}
            <Button
              type="submit"
              size="md"
              loading={loading}
              disabled={loading}
              style={{
                fontWeight: 600,
                fontSize: "15px",
                background: theme.other.gradient,
                padding: "12px 24px",
                borderRadius: "10px",
                width: "100%",
              }}>
              {loading ? "Generating..." : "Generate Fitness Plan"}
            </Button>
          </form>
        </div>
      </div>
    </>
  );
}

export default InitialInput;
