import {
  Avatar,
  Title,
  Group,
  Button,
  ActionIcon,
  useMantineTheme,
  Menu,
  Text,
} from "@mantine/core";
import {
  IconUser,
  IconSun,
  IconMoon,
  IconLogout,
  IconUserCircle,
  IconPlus,
} from "@tabler/icons-react";
import { Link, useNavigate } from "react-router-dom";
import { useTheme } from "../ThemeProvider";
import { useState, useEffect } from "react";

function Header() {
  const { theme: currentTheme, toggleTheme } = useTheme();
  const theme = useMantineTheme();
  const navigate = useNavigate();
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    setIsAuthenticated(!!token);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsAuthenticated(false);
    navigate("/login");
  };

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
        backgroundColor: currentTheme === "dark" ? "#1a1b1e" : "#ffffff",
        display: "flex",
      }}>
      <Group style={{ paddingLeft: "20px" }}>
        <Avatar
          radius="xl"
          style={{
            backgroundColor: currentTheme === "dark" ? "#495057" : "#dee2e6",
          }}>
          <IconUser
            size={20}
            color={currentTheme === "dark" ? "#fff" : "#000"}
          />
        </Avatar>
        <Title
          order={3}
          style={{
            color: currentTheme === "dark" ? "#fff" : "#000",
            fontWeight: 600,
          }}>
          Vektor.ai
        </Title>
      </Group>

      {/* New Chat Button in Center */}
      <Group justify="center" style={{ flex: 1 }}>
        <Group align="center" spacing="xs">
          <Text
            size="sm"
            style={{
              color: currentTheme === "dark" ? "#fff" : "#000",
              fontWeight: 500,
            }}>
            New Chat
          </Text>
          <ActionIcon
            variant="filled"
            color="blue"
            size="lg"
            style={{
              background: theme.other.gradient,
              boxShadow: "0 4px 8px rgba(0,0,0,0.3)",
              borderRadius: "50%",
            }}
            onClick={() => navigate('/')} // Navigate to home or new chat
          >
            <IconPlus size={20} />
          </ActionIcon>
          <Menu
            shadow="md"
            width={200}
            styles={(t) => ({
              dropdown: {
                backgroundColor: currentTheme === "dark" ? "#1a1b1e" : "#ffffff",
                border: currentTheme === "dark" ? "1px solid #333" : "1px solid #e0e0e0",
              },
              item: {
                color: currentTheme === "dark" ? "#ffffff" : "#000",
                "&[data-hovered], &:hover": {
                  backgroundColor: currentTheme === "dark" ? "#2c2e33" : t.colors.gray[0],
                },
              },
            })}
          >
            <Menu.Target>
              <Button
                variant="subtle"
                size="sm"
                style={{
                  color: currentTheme === "dark" ? "#fff" : "#000",
                  fontWeight: 500,
                }}
              >
                GPT-4.0 ▼
              </Button>
            </Menu.Target>
            <Menu.Dropdown>
              <Menu.Item>GPT-4.0</Menu.Item>
              <Menu.Item>DeepSeek</Menu.Item>
            </Menu.Dropdown>
          </Menu>
        </Group>
      </Group>

      <Group
        style={{
          paddingRight: "20px",
          gap: "10px",
          marginLeft: "auto",
        }}>
        {isAuthenticated ? (
          <Menu
            shadow="md"
            width={200}
            styles={(t) => ({
              dropdown: {
                backgroundColor:
                  currentTheme === "dark" ? "#1a1b1e" : "#ffffff",
                border:
                  currentTheme === "dark"
                    ? "1px solid #333"
                    : "1px solid #e0e0e0",
              },
              // Override item hover for dark mode and set a subtle hover for light theme
              item: {
                color: currentTheme === "dark" ? "#ffffff" : undefined,
                // Neutralize hover background in dark mode; keep gentle hover in light mode
                "&[data-hovered], &:hover": {
                  backgroundColor:
                    currentTheme === "dark"
                      ? "transparent !important" // remove hover highlight in dark mode
                      : t.colors.gray[0], // gentle hover in light mode
                },
              },
            })}>
            <Menu.Target>
              <ActionIcon
                variant="subtle"
                color="blue"
                size="lg"
                style={{
                  boxShadow: "0 4px 8px rgba(0,0,0,0.3)",
                }}>
                <IconUserCircle size={20} />
              </ActionIcon>
            </Menu.Target>

            <Menu.Dropdown>
              <Menu.Item
                leftSection={<IconLogout size={16} />}
                onClick={handleLogout}
                // color is controlled here (text color), hover/bg handled by Menu.styles above
                style={{
                  color: currentTheme === "dark" ? "#ffffff" : "#dc3545",
                  backgroundColor: "transparent",
                }}>
                Logout
              </Menu.Item>
            </Menu.Dropdown>
          </Menu>
        ) : (
          <>
            <Button
              component={Link}
              to="/login"
              variant="filled"
              style={{
                background: theme.other.gradient,
                color: "#fff",
                fontWeight: 600,
              }}>
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
              }}>
              Signup
            </Button>
          </>
        )}
        <ActionIcon
          onClick={toggleTheme}
          variant="subtle"
          color="blue"
          size="lg"
          style={{
            boxShadow: "0 4px 8px rgba(0,0,0,0.3)",
          }}>
          {currentTheme === "dark" ? (
            <IconSun size={18} />
          ) : (
            <IconMoon size={18} />
          )}
        </ActionIcon>
      </Group>
    </Group>
  );
}

export default Header;
