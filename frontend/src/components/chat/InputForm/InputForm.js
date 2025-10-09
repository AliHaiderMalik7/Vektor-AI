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
              border: theme.colorScheme === 'light'
                ? '2px solid #e1e5e9'
                : `1px solid ${theme.other.border}`,
              borderRadius: "12px",
              boxShadow: theme.colorScheme === 'light'
                ? '0 4px 12px rgba(0,0,0,0.1), inset 0 1px 2px rgba(255,255,255,0.8)'
                : 'none',
              transition: 'all 0.3s ease',
              '&::-webkit-scrollbar': {
                width: '8px',
              },
              '&::-webkit-scrollbar-track': {
                background: theme.colorScheme === 'dark' ? '#2c2e33' : '#f1f3f4',
                borderRadius: '4px',
              },
              '&::-webkit-scrollbar-thumb': {
                background: theme.colorScheme === 'dark' ? '#5c5f66' : '#c1c2c5',
                borderRadius: '4px',
              },
              '&::-webkit-scrollbar-thumb:hover': {
                background: theme.colorScheme === 'dark' ? '#909296' : '#a6a7ab',
              },
              '&:focus': {
                borderColor: theme.colors.blue[5],
                boxShadow: theme.colorScheme === 'light'
                  ? '0 0 0 3px rgba(59, 130, 246, 0.1), inset 0 1px 2px rgba(255,255,255,0.8)'
                  : '0 0 0 3px rgba(59, 130, 246, 0.2)',
              },
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