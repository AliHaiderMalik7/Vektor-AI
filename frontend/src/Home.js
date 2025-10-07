import { Avatar, Title, Textarea, Button, Group, Text } from '@mantine/core';
import './App.css';

function Home() {
  return (
    <div style={{ width: '100vw', height: '100vh', display: 'flex', flexDirection: 'column', backgroundColor: '#1a1b1e' }}>
      <Group position="apart" align="center" style={{ padding: '20px' }}>
        <Group style={{ paddingLeft: '20px' }}>
          <Avatar src="https://via.placeholder.com/40" alt="User" radius="xl" />
          <Title order={3} style={{ color: '#fff', fontWeight: 600 }}>Vektor.ai</Title>
        </Group>
      </Group>
      <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ width: '100%', maxWidth: '600px', textAlign: 'center' }}>
          <Title order={1} style={{ color: '#fff', marginBottom: '20px', fontWeight: 700 }}>
            Discover Your Next Adventure
          </Title>
          <Text size="lg" color="dimmed" style={{ marginBottom: '30px' }}>
            Enter your travel prompt below to get personalized recommendations
          </Text>
          <Textarea
            placeholder="e.g., Plan a 7-day trip to Japan in spring"
            size="lg"
            minRows={6}
            style={{ marginBottom: '20px' }}
            styles={{
              input: { fontSize: '16px', fontWeight: 500, backgroundColor: '#2c2e33', color: '#fff', minHeight: '150px' },
            }}
          />
          <Button size="lg" style={{ fontWeight: 600, fontSize: '16px' }}>
            Generate Travel Plan
          </Button>
        </div>
      </div>
    </div>
  );
}

export default Home;