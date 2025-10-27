import { Paper, Title, ScrollArea, useMantineTheme, Text, Card, Badge, Group, Stack, Divider, List, ThemeIcon, Progress, RingProgress, Center } from "@mantine/core";
import { IconCheck, IconClock, IconTarget, IconBulb, IconBarbell, IconCalendar, IconTrendingUp } from "@tabler/icons-react";
import TravelPlan from "./TravelPlan/TravelPlan";

function FitnessPlanCard({ planData, theme }) {
  if (!planData || !planData.plans) return null;

  const totalExercises = planData.plans.reduce((acc, plan) => acc + plan.exercises.length, 0);
  const totalSets = planData.plans.reduce((acc, plan) => acc + plan.exercises.reduce((exAcc, ex) => exAcc + ex.sets, 0), 0);

  return (
    <Card shadow="lg" p="xl" radius="lg" style={{
      background: theme.colorScheme === 'dark'
        ? `linear-gradient(135deg, ${theme.colors.dark[6]} 0%, ${theme.colors.dark[7]} 100%)`
        : `linear-gradient(135deg, ${theme.other.cardBackground} 0%, ${theme.other.surface} 100%)`,
      border: `2px solid ${theme.other.border}`,
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Decorative background element */}
      <div style={{
        position: 'absolute',
        top: 0,
        right: 0,
        width: '100px',
        height: '100px',
        background: theme.colorScheme === 'dark'
          ? `linear-gradient(135deg, ${theme.colors.blue[9]} 0%, ${theme.colors.green[9]} 100%)`
          : `linear-gradient(135deg, ${theme.colors.blue[1]} 0%, ${theme.colors.green[1]} 100%)`,
        borderRadius: '50%',
        opacity: theme.colorScheme === 'dark' ? 0.15 : 0.1,
        transform: 'translate(30px, -30px)'
      }} />

      <Group position="apart" mb="lg" style={{ position: 'relative', zIndex: 1 }}>
        <div>
          <Title order={2} style={{ color: theme.other.text, marginBottom: '8px' }}>
            <ThemeIcon color="blue" size="lg" radius="xl" mr="sm" variant="filled">
              <IconBarbell size={20} />
            </ThemeIcon>
            {planData.title}
          </Title>
          <Text size="md" style={{ color: theme.colorScheme === 'dark' ? theme.colors.gray[3] : theme.colors.gray[7] }}>{planData.summary}</Text>
        </div>
        {planData.bmi && (
          <div style={{ textAlign: 'center' }}>
            <RingProgress
              size={80}
              thickness={8}
              sections={[{ value: Math.min(planData.bmi * 2, 100), color: planData.bmi < 25 ? 'green' : planData.bmi < 30 ? 'yellow' : 'red' }]}
              label={
                <Center>
                  <Text size="xs" weight={700}>{planData.bmi}</Text>
                </Center>
              }
            />
            <Text size="xs" style={{ color: theme.colorScheme === 'dark' ? theme.colors.gray[4] : theme.colors.gray[6] }} mt="xs">BMI</Text>
          </div>
        )}
      </Group>

      {/* Stats Cards */}
      <Group grow mb="xl" style={{ position: 'relative', zIndex: 1 }}>
        <Card shadow="sm" p="md" radius="md" style={{ backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[6] : theme.other.surface }}>
          <Group>
            <ThemeIcon color="blue" size="lg" radius="xl" variant="light">
              <IconCalendar size={20} />
            </ThemeIcon>
            <div>
              <Text size="lg" weight={700} style={{ color: theme.other.text }}>{planData.plans.length}</Text>
              <Text size="sm" style={{ color: theme.colorScheme === 'dark' ? theme.colors.gray[4] : theme.colors.gray[6] }}>Days</Text>
            </div>
          </Group>
        </Card>
        <Card shadow="sm" p="md" radius="md" style={{ backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[6] : theme.other.surface }}>
          <Group>
            <ThemeIcon color="green" size="lg" radius="xl" variant="light">
              <IconTarget size={20} />
            </ThemeIcon>
            <div>
              <Text size="lg" weight={700} style={{ color: theme.other.text }}>{totalExercises}</Text>
              <Text size="sm" style={{ color: theme.colorScheme === 'dark' ? theme.colors.gray[4] : theme.colors.gray[6] }}>Exercises</Text>
            </div>
          </Group>
        </Card>
        <Card shadow="sm" p="md" radius="md" style={{ backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[6] : theme.other.surface }}>
          <Group>
            <ThemeIcon color="orange" size="lg" radius="xl" variant="light">
              <IconTrendingUp size={20} />
            </ThemeIcon>
            <div>
              <Text size="lg" weight={700} style={{ color: theme.other.text }}>{totalSets}</Text>
              <Text size="sm" style={{ color: theme.colorScheme === 'dark' ? theme.colors.gray[4] : theme.colors.gray[6] }}>Total Sets</Text>
            </div>
          </Group>
        </Card>
      </Group>

      {planData.plans.map((plan, planIndex) => (
        <Card key={planIndex} shadow="md" p="lg" radius="md" mb="lg" style={{
          backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[6] : theme.other.surface,
          border: `1px solid ${theme.other.border}`,
          position: 'relative'
        }}>
          <Group position="apart" mb="lg">
            <Title order={3} style={{ color: theme.other.text }}>
              <ThemeIcon color="green" size="lg" radius="xl" mr="sm" variant="filled">
                <IconCalendar size={18} />
              </ThemeIcon>
              {plan.day}
            </Title>
            <Badge color="blue" variant="light" size="lg">
              {plan.exercises.length} Exercises
            </Badge>
          </Group>

          <Stack spacing="md">
            {plan.exercises.map((exercise, exIndex) => (
              <Card key={exIndex} shadow="sm" p="md" radius="md" style={{
                background: theme.colorScheme === 'dark'
                  ? `linear-gradient(135deg, ${theme.colors.dark[5]} 0%, ${theme.colors.dark[6]} 100%)`
                  : `linear-gradient(135deg, ${theme.other.background} 0%, ${theme.other.cardBackground} 100%)`,
                border: `1px solid ${theme.other.border}`
              }}>
                <Group position="apart" align="flex-start">
                  <div style={{ flex: 1 }}>
                    <Text weight={600} size="lg" style={{ color: theme.other.text, marginBottom: '8px' }}>
                      {exercise.name}
                    </Text>
                    <Group spacing="xl">
                      <Group spacing="xs">
                        <ThemeIcon color="blue" size="sm" radius="xl" variant="filled">
                          <IconCheck size={14} />
                        </ThemeIcon>
                        <Text size="sm" weight={500} style={{ color: theme.other.text }}>
                          {exercise.sets} sets × {exercise.reps || exercise.duration}
                        </Text>
                      </Group>
                      <Group spacing="xs">
                        <ThemeIcon color="orange" size="sm" radius="xl" variant="filled">
                          <IconClock size={14} />
                        </ThemeIcon>
                        <Text size="sm" weight={500} style={{ color: theme.other.text }}>
                          Rest: {exercise.rest}
                        </Text>
                      </Group>
                    </Group>
                  </div>
                  <Progress
                    value={(exIndex + 1) / plan.exercises.length * 100}
                    size="sm"
                    color="blue"
                    style={{ width: '60px' }}
                  />
                </Group>
              </Card>
            ))}
          </Stack>

          {plan.tips && plan.tips.length > 0 && (
            <>
              <Divider my="lg" />
              <Title order={4} style={{ color: theme.other.text, marginBottom: '12px' }}>
                <ThemeIcon color="yellow" size="lg" radius="xl" mr="sm" variant="filled">
                  <IconBulb size={18} />
                </ThemeIcon>
                Pro Tips
              </Title>
              <List spacing="sm" size="sm">
                {plan.tips.map((tip, tipIndex) => (
                  <List.Item
                    key={tipIndex}
                    icon={
                      <ThemeIcon color="yellow" size="sm" radius="xl" variant="filled">
                        <IconBulb size={12} />
                      </ThemeIcon>
                    }
                    style={{ color: theme.other.text }}
                  >
                    {tip}
                  </List.Item>
                ))}
              </List>
            </>
          )}
        </Card>
      ))}
    </Card>
  );
}

function WorkspacePanel({ workspaceContent }) {
  const theme = useMantineTheme();

  return (
    <Paper
      style={{
        flex: 1,
        display: "flex",
        flexDirection: "column",
        backgroundColor: theme.other.surface,
        borderRadius: "12px",
        overflow: "hidden",
      }}>
      <div
        style={{
          padding: "20px",
          borderBottom: `1px solid ${theme.other.border}`,
          flexShrink: 0,
        }}>
        <Title order={4} style={{ color: theme.other.text }}>
          Fitness Plan Responses
        </Title>
      </div>

      <ScrollArea style={{ flex: 1, padding: "20px" }}>
        {workspaceContent && workspaceContent.length > 0 ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            {workspaceContent.map((content, index) => (
              <div key={index} style={{ borderBottom: index < workspaceContent.length - 1 ? `1px solid ${theme.other.border}` : 'none', paddingBottom: '20px' }}>
                {content.response && typeof content.response === 'object' && !content.response.missing_info ? (
                  <FitnessPlanCard planData={content.response} theme={theme} />
                ) : (
                  <Text style={{ whiteSpace: 'pre-wrap', color: theme.other.text }}>
                    {typeof content.response === 'object' && content.response.missing_info
                      ? content.response.missing_info
                      : typeof content.response === 'string'
                      ? content.response
                      : JSON.stringify(content.response, null, 2)}
                  </Text>
                )}
              </div>
            ))}
          </div>
        ) : (
          <Text style={{ color: theme.other.text, opacity: 0.6 }}>
            Your fitness plan responses will appear here after generation.
          </Text>
        )}
      </ScrollArea>
    </Paper>
  );
}

export default WorkspacePanel;