import { Card, Text, Title, List, Group, Image, Badge } from "@mantine/core";

const baseUrl = process.env.REACT_APP_APP_URL;

function WorkoutPlan({ data }) {
  console.log("in workput");
  
  const { title, summary, bmi, plans, error, missing_info } = data;

  if (error) {
    return <Text color="red">Error: {error}</Text>;
  }

  if (missing_info) {
    return <Text color="orange">Missing Info: {missing_info}</Text>;
  }

  // Collect all days from plans, handling nested structure
  const allDays = [];
  if (plans && Array.isArray(plans)) {
    plans.forEach(plan => {
      if (plan.days && Array.isArray(plan.days)) {
        // Nested structure: plan has days array
        plan.days.forEach(day => {
          allDays.push({ ...day, week: plan.week });
        });
      } else if (plan.day) {
        // Flat structure: plan is directly a day
        allDays.push(plan);
      }
    });
  }

  const getFullGifUrl = (gifPath) => {
    if (!gifPath) return null;

    // If already an absolute URL, return it directly
    if (gifPath.startsWith("http")) return gifPath;

    // Ensure there's exactly one slash between baseUrl and path
    const normalizedPath = gifPath.startsWith("/") ? gifPath : `/${gifPath}`;
    return `${baseUrl}${normalizedPath}`;
  };

  return (
    <div>
   
      {bmi && <Badge>BMI: {bmi}</Badge>}
      {allDays?.map((day, index) => (
        <Card key={index} shadow="sm" p="md" radius="md" mt="md">
          <Title order={4}>
            {day.week ? `Week ${day.week} - ${day.day}` : day.day}
          </Title>
          <List>
            {day.exercises &&
              Array.isArray(day.exercises) &&
              day.exercises.map((exercise, idx) => (
                <List.Item key={idx}>
                  <Group>
                    <Text>
                      <strong>{exercise.name}</strong>: {exercise.sets} sets x{" "}
                      {exercise.reps || exercise.duration}{" "}
                      {exercise.reps ? "reps" : ""},{" "}
                      {exercise?.rest ? "Rest:":""} {exercise.rest}
                    </Text>
                    {exercise.media &&
                      exercise.media.gif &&
                      (() => {
                        const fullUrl = getFullGifUrl(exercise.media.gif);
                        return (
                          <Image
                            src={fullUrl}
                            alt={`${exercise.name} gif`}
                            width={100}
                            height={100}
                            fit="contain"
                          />
                        );
                      })()}
                  </Group>
                </List.Item>
              ))}
          </List>
          {day.tips && Array.isArray(day.tips) && (
            <div style={{ marginTop: "10px" }}>
              <Text fw={500}>Tips:</Text>
              <List>
                {day.tips.map((tip, idx) => (
                  <List.Item key={idx}>{tip}</List.Item>
                ))}
              </List>
            </div>
          )}
        </Card>
      ))}
    </div>
  );
}

export default WorkoutPlan;