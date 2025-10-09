import { Avatar, Title, Group, Button } from "@mantine/core";
import { IconUser } from "@tabler/icons-react";
import { Link } from "react-router-dom";

function Header() {
  return (
    <Group
      justify="space-between" // Mantine v7+ (use "position"="apart" in v6)
      align="center"
      style={{
        padding: "20px",
        flexShrink: 0,
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        zIndex: 1000,
        backgroundColor: "#1a1b1e",
        display: "flex",
      }}
    >
      {/* Left side: logo + title */}
      <Group style={{ paddingLeft: "20px" }}>
        <Avatar radius="xl" style={{ backgroundColor: "#373a40" }}>
          <IconUser size={20} />
        </Avatar>
        <Title order={3} style={{ color: "#fff", fontWeight: 600 }}>
          Vektor.ai
        </Title>
      </Group>

      {/* Right side: buttons */}
      <Group
        style={{
          paddingRight: "20px",
          gap: "10px",
          marginLeft: "auto", // 👈 pushes the buttons fully to the right
        }}
      >
        <Button
          component={Link}
          to="/login"
          variant="outline"
          style={{
            color: "#667eea",
            borderColor: "#667eea",
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
            background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            color: "#fff",
            fontWeight: 600,
          }}
        >
          Signup
        </Button>
      </Group>
    </Group>
  );
}

export default Header;
