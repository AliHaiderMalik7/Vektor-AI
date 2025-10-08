import { Avatar, Title, Group } from "@mantine/core";

function Header() {
  return (
    <Group
      position="apart"
      align="center"
      style={{ padding: "20px", flexShrink: 0 }}>
      <Group style={{ paddingLeft: "20px" }}>
        <Avatar radius="xl" style={{ backgroundColor: "#4db6ac" }}>
          U
        </Avatar>
        <Title order={3} style={{ color: "#fff", fontWeight: 600 }}>
          Vektor.ai
        </Title>
      </Group>
    </Group>
  );
}

export default Header;