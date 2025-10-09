import { Avatar, Title, Group } from "@mantine/core";
import { IconUser } from "@tabler/icons-react";

function Header() {
  return (
    <Group
      position="apart"
      align="center"
      style={{ padding: "20px", flexShrink: 0 }}>
      <Group style={{ paddingLeft: "20px" }}>
        <Avatar radius="xl" style={{ backgroundColor: "#373a40" }}>
          <IconUser size={20} />
        </Avatar>
        <Title order={3} style={{ color: "#fff", fontWeight: 600 }}>
          Vektor.ai
        </Title>
      </Group>
    </Group>
  );
}

export default Header;