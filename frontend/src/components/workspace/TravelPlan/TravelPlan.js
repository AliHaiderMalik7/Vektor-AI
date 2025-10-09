import { Text, Card, useMantineTheme } from "@mantine/core";

function TravelPlan() {
  const theme = useMantineTheme();

  return (
    <div style={{ color: theme.other.text, lineHeight: 1.8 }}>
      <Text
        size="lg"
        weight={600}
        style={{ color: theme.other.text, marginBottom: "16px" }}>
        Your Personalized Japan Itinerary
      </Text>
      <Text style={{ color: theme.other.textSecondary, marginBottom: "20px" }}>
        Based on your preferences, here's a customized 7-day spring
        itinerary for Japan...
      </Text>

      <div style={{ display: "grid", gap: "16px" }}>
        {[
          "Day 1: Tokyo Arrival",
          "Day 2: Tokyo Exploration",
          "Day 3: Hakone & Mount Fuji",
          "Day 4: Kyoto Travel",
          "Day 5: Kyoto Temples",
          "Day 6: Osaka Day Trip",
          "Day 7: Departure",
        ].map((day, index) => (
          <Card
            key={index}
            style={{
              backgroundColor: theme.other.cardBackground,
              border: `1px solid ${theme.other.border}`,
            }}>
            <Text weight={500} style={{ color: theme.other.text }}>
              {day}
            </Text>
          </Card>
        ))}
      </div>
    </div>
  );
}

export default TravelPlan;