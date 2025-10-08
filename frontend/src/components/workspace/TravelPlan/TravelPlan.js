import { Text, Card } from "@mantine/core";

function TravelPlan() {
  return (
    <div style={{ color: "#fff", lineHeight: 1.8 }}>
      <Text
        size="lg"
        weight={600}
        style={{ color: "#fff", marginBottom: "16px" }}>
        Your Personalized Japan Itinerary
      </Text>
      <Text style={{ color: "#c1c2c5", marginBottom: "20px" }}>
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
              backgroundColor: "#2c2e33",
              border: "1px solid #373a40",
            }}>
            <Text weight={500} style={{ color: "#fff" }}>
              {day}
            </Text>
          </Card>
        ))}
      </div>
    </div>
  );
}

export default TravelPlan;