import { Textarea, Button } from "@mantine/core";

function InputForm({ currentPrompt, setCurrentPrompt, handleSubmit, loading }) {
  return (
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
  );
}

export default InputForm;