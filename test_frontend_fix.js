// Test script to verify the frontend data flow fix
console.log("🔧 Testing Frontend Data Flow Fix...");

// Test the parsePlayerData logic with actual data structure
function testParsePlayerData(predictionData) {
  console.log("🔍 Testing parsePlayerData function...");
  
  if (!predictionData?.detailed_analysis?.enhanced_player_analysis) {
    console.log("❌ Missing enhanced_player_analysis data");
    return {
      awayTeam: { name: "Away Team", logo: "", primary_color: "#6366f1" },
      homeTeam: { name: "Home Team", logo: "", primary_color: "#10b981" },
      awayPlayers: {},
      homePlayers: {},
      positionalAdvantages: {},
      totalImpact: 0,
      databaseStats: {}
    };
  }

  const playerData = predictionData.detailed_analysis.enhanced_player_analysis;
  
  // Use the team_selector data which exists in the processed data
  const awayTeam = predictionData.team_selector?.away_team || {
    name: "Away Team",
    logo: "",
    primary_color: "#6366f1"
  };
  const homeTeam = predictionData.team_selector?.home_team || {
    name: "Home Team", 
    logo: "",
    primary_color: "#10b981"
  };

  return {
    awayTeam,
    homeTeam,
    awayPlayers: playerData.away_players || {},
    homePlayers: playerData.home_players || {},
    positionalAdvantages: playerData.positional_advantages || {},
    totalImpact: playerData.total_impact || 0,
    databaseStats: playerData.database_stats || {}
  };
}

// Test with API call
async function testWithRealData() {
  console.log("📡 Making API call...");
  
  try {
    const response = await fetch('http://127.0.0.1:5002/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        home_team: "Arizona State",
        away_team: "Texas Tech"
      })
    });

    const data = await response.json();
    
    // Simulate the App.tsx data transformation
    const predictionData = data.ui_components ? { 
      ...data.ui_components, 
      formatted_analysis: data.formatted_analysis 
    } : data;
    
    console.log("✅ API Response received");
    
    // Test the parsing logic
    const parsed = testParsePlayerData(predictionData);
    
    console.log("🎯 Parse Results:");
    console.log("- Away Team:", parsed.awayTeam?.name || "undefined");
    console.log("- Home Team:", parsed.homeTeam?.name || "undefined");
    console.log("- Database Stats QBs:", parsed.databaseStats?.quarterbacks_analyzed || 0);
    console.log("- Database Stats WRs:", parsed.databaseStats?.wide_receivers_analyzed || 0);
    
    // Check if we have the data we need
    const hasTeamData = parsed.awayTeam?.name !== "Away Team" && parsed.homeTeam?.name !== "Home Team";
    const hasDBStats = parsed.databaseStats?.quarterbacks_analyzed > 0;
    
    console.log("\n🔍 Component State Prediction:");
    if (hasTeamData && hasDBStats) {
      console.log("✅ Component should show database stats correctly");
    } else if (!hasTeamData) {
      console.log("⚠️  Component will show loading state (missing team data)");
    } else if (!hasDBStats) {
      console.log("⚠️  Component will show 0 values (missing database stats)");
    }
    
  } catch (error) {
    console.error("❌ API Test failed:", error.message);
  }
}

// Run the test
testWithRealData();