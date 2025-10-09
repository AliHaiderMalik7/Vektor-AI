import { Textarea, Button, useMantineTheme } from "@mantine/core";

function InputForm({ currentPrompt, setCurrentPrompt, handleSubmit, loading }) {
  const theme = useMantineTheme();

  return (
    <div
      style={{
        padding: "20px",
        borderTop: `1px solid ${theme.other.border}`,
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
              backgroundColor: theme.other.inputBackground,
              color: theme.other.text,
              border: `1px solid ${theme.other.border}`,
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
            background: theme.other.gradient,
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