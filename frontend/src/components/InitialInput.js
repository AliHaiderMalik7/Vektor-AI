import { Textarea, Button, Title, Text } from "@mantine/core";

function InitialInput({ currentPrompt, setCurrentPrompt, handleSubmit, loading }) {
  return (
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
  );
}

export default InitialInput;