import React from "react";
import {
  TextInput,
  Button,
  Title,
  Stack,
  Paper,
  Text,
  Box,
  Group,
  ActionIcon,
  useMantineTheme,
} from "@mantine/core";
import { IconSun, IconMoon } from "@tabler/icons-react";
import { useTheme } from "./ThemeProvider";
import "./App.css";

function Login() {
  const { theme, toggleTheme } = useTheme();
  const mantineTheme = useMantineTheme();

  return (
    <div className="auth-container">
      <div className="auth-image">
        <div className="image-overlay">
          <img
            src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80"
            alt="Travel destination"
          />
          <div className="image-content">
            <Text size="xl" weight={600} color="white" mb="sm">
              Welcome Back Traveler
            </Text>
            <Text size="sm" color="white" opacity={0.9}>
              Continue your journey to discover amazing destinations
            </Text>
          </div>
        </div>
      </div>

      <div className="auth-form">
        <Paper
          p="xl"
          radius="lg"
          style={{
            width: "100%",
            maxWidth: "480px",
            background: "rgba(255, 255, 255, 0.95)",
            backdropFilter: "blur(10px)",
            border: "1px solid rgba(255, 255, 255, 0.2)",
          }}>
          <Box mb="xl" style={{ textAlign: "center" }}>
            <Title
              order={2}
              mb="xs"
              style={{
                background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
                fontWeight: 700,
              }}>
              Welcome Back
            </Title>
            <Text size="sm" color="dimmed">
              Sign in to your Vektor.ai account
            </Text>
          </Box>

          {/* Social Login Buttons */}
          <Group grow mb="md">
            <Button
              variant="default"
              size="md"
              style={{
                borderColor: "#e0e0e0",
                fontWeight: 500,
                color: "#333",
              }}>
              Continue with Google
            </Button>
            <Button
              variant="default"
              size="md"
              style={{
                borderColor: "#e0e0e0",
                fontWeight: 500,
                color: "#333",
              }}>
              Continue with Facebook
            </Button>
          </Group>

          <Text
            align="center"
            size="sm"
            color="dimmed"
            my="lg"
            style={{ position: "relative" }}>
            <span
              style={{
                background: "white",
                padding: "0 10px",
                position: "relative",
                zIndex: 1,
              }}>
              Or continue with email
            </span>
            <div
              style={{
                position: "absolute",
                top: "50%",
                left: 0,
                right: 0,
                height: "1px",
                background: "#e0e0e0",
                zIndex: 0,
              }}
            />
          </Text>

          <form>
            <Stack spacing="md">
              <TextInput
                label="Email Address"
                placeholder="Enter your email"
                type="email"
                size="md"
                required
                styles={{
                  input: {
                    fontSize: "15px",
                    border: "1px solid #e0e0e0",
                    transition: "all 0.2s ease",
                    "&:focus": {
                      borderColor: "#667eea",
                      boxShadow: "0 0 0 3px rgba(102, 126, 234, 0.1)",
                    },
                  },
                  label: {
                    fontWeight: 600,
                    fontSize: "14px",
                    marginBottom: "6px",
                    color: "#333",
                  },
                }}
              />

              <TextInput
                label="Password"
                placeholder="Enter your password"
                type="password"
                size="md"
                required
                styles={{
                  input: {
                    fontSize: "15px",
                    border: "1px solid #e0e0e0",
                    transition: "all 0.2s ease",
                    "&:focus": {
                      borderColor: "#667eea",
                      boxShadow: "0 0 0 3px rgba(102, 126, 234, 0.1)",
                    },
                  },
                  label: {
                    fontWeight: 600,
                    fontSize: "14px",
                    marginBottom: "6px",
                    color: "#333",
                  },
                }}
              />

              <Box style={{ textAlign: "right", marginBottom: "8px" }}>
                <Text
                  size="sm"
                  color="#667eea"
                  weight={600}
                  style={{ cursor: "pointer" }}>
                  Forgot Password?
                </Text>
              </Box>

              <Button
                type="submit"
                fullWidth
                size="md"
                style={{
                  background:
                    "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                  border: "none",
                  fontWeight: 600,
                  fontSize: "15px",
                  height: "48px",
                  marginTop: "8px",
                }}>
                Sign In
              </Button>
            </Stack>
          </form>

          <Text align="center" size="sm" color="dimmed" mt="lg">
            Don't have an account?{" "}
            <Text
              component="span"
              color="#667eea"
              weight={600}
              style={{ cursor: "pointer" }}>
              Sign up
            </Text>
          </Text>
        </Paper>
      </div>
    </div>
  );
}

export default Login;
