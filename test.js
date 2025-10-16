let teams = [];

// API endpoints - using absolute URLs to point to Flask server
const FLASK_BASE_URL = 'http://127.0.0.1:5002'; // Flask server address and port
const TEAMS_API_URL = FLASK_BASE_URL + '/teams';
const PREDICT_API_URL = FLASK_BASE_URL + '/predict';

/**
 * Utility function to display error messages.
 * @param {string} message - The error message to show.
 */
function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

/**
 * Fetches the list of all college football teams.
 */
async function loadTeams() {
    try {
        const response = await fetch(TEAMS_API_URL);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        if (data.success && data.teams) {
            teams = data.teams;
            populateTeamSelectors();
        } else {
            showError('Failed to load teams: Invalid data structure from API');
        }
    } catch (error) {
        showError('Error loading teams. Please ensure the backend is running and reachable: ' + error.message);
    }
}

/**
 * Populates the dropdown menus with fetched team names.
 */
function populateTeamSelectors() {
    const homeSelect = document.getElementById('homeTeam');
    const awaySelect = document.getElementById('awayTeam');

    // Sort teams alphabetically by name
    const sortedTeams = teams.sort((a, b) => a.name.localeCompare(b.name));

    sortedTeams.forEach(team => {
        // Use team.id as value for prediction logic, team.name for display
        const homeOption = new Option(team.name, team.id);
        const awayOption = new Option(team.name, team.id);
        homeSelect.add(homeOption);
        awaySelect.add(awayOption);
    });
}

/**
 * Main function to trigger the prediction when the button is clicked.
 */
async function makePrediction() {
    const homeTeamId = document.getElementById('homeTeam').value;
    const awayTeamId = document.getElementById('awayTeam').value;

    // --- Validation ---
    if (!homeTeamId || !awayTeamId) {
        showError('Please select both home and away teams.');
        return;
    }

    if (homeTeamId === awayTeamId) {
        showError('Home and away teams must be different.');
        return;
    }

    const homeTeam = teams.find(t => t.id == homeTeamId);
    const awayTeam = teams.find(t => t.id == awayTeamId);

    // --- UI State Management ---
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    document.getElementById('error').style.display = 'none';
    document.getElementById('predictButton').disabled = true;

    try {
        const response = await fetch(PREDICT_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                home_team: homeTeam.name, // Send names to API
                away_team: awayTeam.name
            })
        });

        const data = await response.json();

        if (response.ok && data.success !== false && !data.error) {
            displayPrediction(data, homeTeam.name, awayTeam.name);
        } else {
            // Check for explicit error message from the API
            showError('Prediction failed: ' + (data.error || 'The backend returned a non-success status.'));
        }
    } catch (error) {
        showError('Error making prediction: ' + error.message);
    } finally {
        // --- Reset UI State ---
        document.getElementById('loading').style.display = 'none';
        document.getElementById('predictButton').disabled = false;
    }
}

/**
 * Fills the dashboard sections with the prediction data from the API.
 * @param {object} data - The JSON response from the prediction API.
 * @param {string} homeTeamName - The name of the home team.
 * @param {string} awayTeamName - The name of the away team.
 */
function displayPrediction(data, homeTeamName, awayTeamName) {
    // --- Utility Functions ---
    const formatProb = (prob) => `${prob.toFixed(1)}%`;
    const formatSpread = (spread) => spread > 0 ? `${homeTeamName} +${spread.toFixed(1)}` : `${awayTeamName} +${Math.abs(spread).toFixed(1)}`;
    const formatTotal = (total) => total.toFixed(1);
    const formatDiff = (value) => value ? (value > 0 ? `+${value.toFixed(1)}` : value.toFixed(1)) : '--';
    const getEdge = (val1, val2) => val1 && val2 ? (val1 > val2 ? `${homeTeamName} Edge` : `${awayTeamName} Edge`) : '--';
    const getAdvantageName = (val1, val2) => val1 && val2 ? (val1 > val2 ? homeTeamName : awayTeamName) : '--';
    const toPercent = (rate) => rate ? (rate * 100).toFixed(1) + '%' : '--';

    // --- Header & Logos ---
    document.getElementById('matchupHeader').textContent = `${awayTeamName} @ ${homeTeamName}`;
    const awayLogo = document.getElementById('awayTeamLogo');
    const homeLogo = document.getElementById('homeTeamLogo');
    awayLogo.src = data.away_logo || '';
    homeLogo.src = data.home_logo || '';
    awayLogo.style.display = data.away_logo ? 'block' : 'none';
    homeLogo.style.display = data.home_logo ? 'block' : 'none';

    // --- Primary Predictions ---
    const awayWinProb = (100 - data.home_win_probability);
    document.getElementById('winProbability').innerHTML =
        `${awayTeamName}: ${formatProb(awayWinProb)}<br>${homeTeamName}: ${formatProb(data.home_win_probability)}`;
    document.getElementById('predictedSpread').textContent = data.spread ? formatSpread(data.spread) : '--';
    document.getElementById('predictedTotal').textContent = data.total ? formatTotal(data.total) : '--';

    // --- Value Picks ---
    const valuePicksSection = document.getElementById('valuePicksSection');
    const bestBets = data.best_bets || {};

    if (bestBets.spread || bestBets.total) {
        valuePicksSection.style.display = 'block';
        document.getElementById('spreadPickLine').textContent = bestBets.spread || 'No Spread Pick';
        document.getElementById('spreadPickEdge').textContent = bestBets.spread_edge ? `${bestBets.spread_edge.toFixed(1)}-point edge` : 'No significant edge detected';
        document.getElementById('totalPickLine').textContent = bestBets.total || 'No Total Pick';
        document.getElementById('totalPickEdge').textContent = bestBets.total_edge ? `${bestBets.total_edge.toFixed(1)}-point edge` : 'No significant edge detected';
    } else {
        valuePicksSection.style.display = 'none';
    }

    // --- EPA Analysis ---
    const awayStats = data.enhanced_team_metrics?.away || {};
    const homeStats = data.enhanced_team_metrics?.home || {};

    document.getElementById('awayTeamHeader').textContent = awayTeamName;
    document.getElementById('homeTeamHeader').textContent = homeTeamName;

    document.getElementById('epaTableBody').innerHTML =
        `<tr><td>Overall EPA</td><td>${awayStats.overall_epa ? awayStats.overall_epa.toFixed(3) : '--'}</td><td>${homeStats.overall_epa ? homeStats.overall_epa.toFixed(3) : '--'}</td><td>${getEdge(homeStats.overall_epa, awayStats.overall_epa)}</td></tr>` +
        `<tr><td>EPA Allowed</td><td>${awayStats.epa_allowed ? awayStats.epa_allowed.toFixed(3) : '--'}</td><td>${homeStats.epa_allowed ? homeStats.epa_allowed.toFixed(3) : '--'}</td><td>${getEdge(awayStats.epa_allowed, homeStats.epa_allowed)}</td></tr>` + // Lower is better
        `<tr><td>Passing EPA</td><td>${awayStats.passing_epa ? awayStats.passing_epa.toFixed(3) : '--'}</td><td>${homeStats.passing_epa ? homeStats.passing_epa.toFixed(3) : '--'}</td><td>${getEdge(homeStats.passing_epa, awayStats.passing_epa)}</td></tr>` +
        `<tr><td>Rushing EPA</td><td>${awayStats.rushing_epa ? awayStats.rushing_epa.toFixed(3) : '--'}</td><td>${homeStats.rushing_epa ? homeStats.rushing_epa.toFixed(3) : '--'}</td><td>${getEdge(homeStats.rushing_epa, awayStats.rushing_epa)}</td></tr>`;


    // --- Model Confidence ---
    const confidenceData = data.confidence_breakdown || {};
    const totalConfidence = data.confidence || 0; // Assuming confidence is a number from 0 to 100

    document.getElementById('confidenceFactorsTable').innerHTML =
        `<tr><td>Consistency Factor</td><td>${(confidenceData.consistency || 0).toFixed(1)}</td></tr>` +
        `<tr><td>Differential Strength</td><td>${(confidenceData.differential || 0).toFixed(1)}</td></tr>` +
        `<tr><td>Trend Factor</td><td>${(confidenceData.trend || 0).toFixed(1)}</td></tr>` +
        `<tr><td>Weather/Calendar</td><td>${(confidenceData.weather || 0).toFixed(1)}</td></tr>` +
        `<tr><td>Data Quality</td><td>${(confidenceData.data_quality || 0).toFixed(1)}</td></tr>`;
    document.getElementById('totalConfidenceScore').textContent = `${totalConfidence.toFixed(1)}%`;


    // --- Market Comparison ---
    const marketData = data.market_comparison || {};
    const consensusSpread = marketData.consensus_spread;
    const consensusTotal = marketData.consensus_total;

    // Spread difference: Model - Market (Positive means model is higher, negative means model is lower)
    const spreadDiff = (data.spread && consensusSpread) ? (data.spread - consensusSpread).toFixed(1) : '--';
    const totalDiff = (data.total && consensusTotal) ? (data.total - consensusTotal).toFixed(1) : '--';

    document.getElementById('modelSpread').textContent = data.spread ? data.spread.toFixed(1) : '--';
    document.getElementById('modelTotal').textContent = data.total ? data.total.toFixed(1) : '--';
    document.getElementById('consensusSpread').textContent = consensusSpread ? consensusSpread.toFixed(1) : '--';
    document.getElementById('consensusTotal').textContent = consensusTotal ? consensusTotal.toFixed(1) : '--';
    document.getElementById('consensusDiff').textContent = spreadDiff;
    
    // Individual sportsbook differences
    document.getElementById('dkSpread').textContent = marketData.draftkings_spread || '--';
    document.getElementById('dkTotal').textContent = marketData.draftkings_total || '--';
    document.getElementById('bovadaSpread').textContent = marketData.bovada_spread || '--';
    document.getElementById('bovadaTotal').textContent = marketData.bovada_total || '--';

    const analysisText = (data.spread && consensusSpread) ? 
        `Model projects ${homeTeamName} ${data.spread > consensusSpread ? 'higher' : 'lower'} spread. Total discrepancy: ${totalDiff}`
        : 'Market data incomplete for detailed analysis.';
    document.getElementById('valueAnalysis').textContent = analysisText;


    // --- Situational Performance ---
    document.getElementById('awaySituationalHeader').textContent = `${awayTeamName} Situational Performance`;
    document.getElementById('homeSituationalHeader').textContent = `${homeTeamName} Situational Performance`;

    document.getElementById('awaySituationalTable').innerHTML =
        `<tr><td>Success Rate</td><td id="awaySuccessRateDetail">${toPercent(awayStats.success_rate)}</td></tr>` +
        `<tr><td>Explosiveness</td><td id="awayExplosivenessDetail">${awayStats.explosiveness ? awayStats.explosiveness.toFixed(3) : '--'}</td></tr>` +
        `<tr><td>Passing Downs Success</td><td id="awayPassingDownsDetail">${toPercent(awayStats.passing_downs_success)}</td></tr>` +
        `<tr><td>Standard Downs Success</td><td id="awayStandardDownsDetail">${toPercent(awayStats.standard_downs_success)}</td></tr>`;

    document.getElementById('homeSituationalTable').innerHTML =
        `<tr><td>Success Rate</td><td id="homeSuccessRateDetail">${toPercent(homeStats.success_rate)}</td></tr>` +
        `<tr><td>Explosiveness</td><td id="homeExplosivenessDetail">${homeStats.explosiveness ? homeStats.explosiveness.toFixed(3) : '--'}</td></tr>` +
        `<tr><td>Passing Downs Success</td><td id="homePassingDownsDetail">${toPercent(homeStats.passing_downs_success)}</td></tr>` +
        `<tr><td>Standard Downs Success</td><td id="homeStandardDownsDetail">${toPercent(homeStats.standard_downs_success)}</td></tr>`;


    // --- Advanced Metrics ---
    const ratings = data.detailed_analysis?.ratings || {};
    const awayElo = ratings.away?.elo || 0;
    const homeElo = ratings.home?.elo || 0;
    const awayFpi = ratings.away?.fpi || 0;
    const homeFpi = ratings.home?.fpi || 0;
    const awayTalent = ratings.away?.talent || 0;
    const homeTalent = ratings.home?.talent || 0;

    document.getElementById('awayElo').textContent = awayElo ? awayElo.toFixed(0) : '--';
    document.getElementById('homeElo').textContent = homeElo ? homeElo.toFixed(0) : '--';
    document.getElementById('eloAdvantage').textContent = getAdvantageName(homeElo, awayElo);

    document.getElementById('awayFpi').textContent = awayFpi ? awayFpi.toFixed(1) : '--';
    document.getElementById('homeFpi').textContent = homeFpi ? homeFpi.toFixed(1) : '--';
    document.getElementById('fpiAdvantage').textContent = getAdvantageName(homeFpi, awayFpi);

    document.getElementById('awayTalent').textContent = awayTalent ? awayTalent.toFixed(0) : '--';
    document.getElementById('homeTalent').textContent = homeTalent ? homeTalent.toFixed(0) : '--';
    document.getElementById('talentAdvantage').textContent = getAdvantageName(homeTalent, awayTalent);


    // --- Final Statement ---
    document.getElementById('winProbabilityStatement').innerHTML = data.home_win_probability ?
        `The model projects a **${homeTeamName}** win with a **${formatProb(data.home_win_probability)}** probability.` : '--';
    document.getElementById('finalSpreadCalc').textContent = data.spread ? formatSpread(data.spread) : '--';


    // Finally, show the results section
    document.getElementById('results').style.display = 'block';
}

// Attach event listener to load teams when the script is loaded
window.addEventListener('load', loadTeams);