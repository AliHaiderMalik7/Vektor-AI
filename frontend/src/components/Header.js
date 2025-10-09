import { Avatar, Title, Group, Button, ActionIcon, useMantineTheme } from "@mantine/core";
import { IconUser, IconSun, IconMoon } from "@tabler/icons-react";
import { Link } from "react-router-dom";
import { useTheme } from "../ThemeProvider";

function Header() {
  const { theme: currentTheme, toggleTheme } = useTheme();
  const theme = useMantineTheme();

  return (
    <Group
      justify="space-between" 
      align="center"
      style={{
        padding: "20px",
        flexShrink: 0,
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        zIndex: 1000,
        backgroundColor: currentTheme === 'dark' ? '#1a1b1e' : '#ffffff',
        display: "flex",
      }}
    >
      <Group style={{ paddingLeft: "20px" }}>
        <Avatar radius="xl" style={{ backgroundColor: currentTheme === 'dark' ? '#495057' : '#dee2e6' }}>
          <IconUser size={20} color={currentTheme === 'dark' ? '#fff' : '#000'} />
        </Avatar>
        <Title order={3} style={{ color: currentTheme === 'dark' ? '#fff' : '#000', fontWeight: 600 }}>
          Vektor.ai
        </Title>
      </Group>

      <Group
        style={{
          paddingRight: "20px",
          gap: "10px",
          marginLeft: "auto", 
        }}
      >
        <Button
          component={Link}
          to="/login"
          variant="filled"
          style={{
            background: theme.other.gradient,
            color: "#fff",
            fontWeight: 600,
          }}
        >
          Login
        </Button>
        <Button
          component={Link}
          to="/signup"
          variant="filled"
          style={{
            background: theme.other.gradient,
            color: "#fff",
            fontWeight: 600,
          }}
        >
          Signup
        </Button>
        <ActionIcon
          onClick={toggleTheme}
          variant="subtle"
          color="blue"
          size="lg"
          style={{
            boxShadow: '0 4px 8px rgba(0,0,0,0.3)',
          }}
        >
          {currentTheme === 'dark' ? <IconSun size={18} /> : <IconMoon size={18} />}
        </ActionIcon>
      </Group>
    </Group>
  );
}

export default Header;
