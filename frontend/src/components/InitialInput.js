import { Textarea, Button, Title, Text, useMantineTheme } from "@mantine/core";

function InitialInput({
  currentPrompt,
  setCurrentPrompt,
  handleSubmit,
  loading,
}) {
  const theme = useMantineTheme();

  return (
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
              fontSize: "2rem", // smaller, better balance
              lineHeight: 1.2,
              margin: 0,
            }}>
            Discover Your Next Adventure
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
            Enter your travel prompt below to get personalized recommendations.
          </Text>
        </div>

        <form onSubmit={handleSubmit}>
          <Textarea
            value={currentPrompt}
            onChange={(e) => setCurrentPrompt(e.target.value)}
            placeholder="e.g., Plan a 7-day trip to Japan in spring"
            size="md"
            minRows={4}
            style={{ marginBottom: "20px" }}
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

          <Button
            type="submit"
            size="md"
            loading={loading}
            disabled={loading}
            fullWidth
            style={{
              fontWeight: 600,
              fontSize: "15px",
              background: theme.other.gradient,
              padding: "12px 0",
              borderRadius: "10px",
            }}>
            {loading ? "Generating..." : "Generate Travel Plan"}
          </Button>
        </form>
      </div>
    </div>
  );
}

export default InitialInput;
