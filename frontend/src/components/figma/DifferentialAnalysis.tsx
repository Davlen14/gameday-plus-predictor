import { ImageWithFallback } from './figma/ImageWithFallback';
import { GlassCard } from './GlassCard';
import { InsightBox } from './InsightBox';

interface DifferentialAnalysisProps {
  predictionData?: any;
}

export function DifferentialAnalysis({ predictionData }: DifferentialAnalysisProps) {
  const awayTeam = predictionData?.team_selector?.away_team || { name: "Away Team", logo: "https://a.espncdn.com/i/teamlogos/ncaa/500/194.png", primary_color: "#ce1141" };
  const homeTeam = predictionData?.team_selector?.home_team || { name: "Home Team", logo: "https://a.espncdn.com/i/teamlogos/ncaa/500/356.png", primary_color: "#ff6b35" };

  // Parse differential analysis data from formatted_analysis
  const parseDifferentialData = (formattedText: string) => {
    if (!formattedText) return null;
    
    // More robust section matching
    const diffSection = formattedText.match(/🎯 \[8\] DIFFERENTIAL ANALYSIS[\s\S]*?(?=🎯 \[9\])/);
    if (!diffSection) {
      return null;
    }
    
    const section = diffSection[0];
    
    // Parse EPA differentials with more flexible regex
    const overallEPAMatch = section.match(/Overall EPA Diff:\s*([+-]?[0-9]+\.?[0-9]*)/);
    const passingEPAMatch = section.match(/Passing EPA Diff:\s*([+-]?[0-9]+\.?[0-9]*)/);
    const rushingEPAMatch = section.match(/Rushing EPA Diff:\s*([+-]?[0-9]+\.?[0-9]*)/);
    
    // Parse performance metrics
    const successRateMatch = section.match(/Success Rate Diff:\s*([+-]?[0-9]+\.?[0-9]*)/);
    const explosivenessMatch = section.match(/Explosiveness Diff:\s*([+-]?[0-9]+\.?[0-9]*)/);
    
    // Parse situational success
    const passingDownsMatch = section.match(/Passing Downs Diff:\s*([+-]?[0-9]+\.?[0-9]*)/);
    const standardDownsMatch = section.match(/Standard Downs Diff:\s*([+-]?[0-9]+\.?[0-9]*)/);
    
    return {
      overallEPA: overallEPAMatch ? parseFloat(overallEPAMatch[1]) : 0,
      passingEPA: passingEPAMatch ? parseFloat(passingEPAMatch[1]) : 0,
      rushingEPA: rushingEPAMatch ? parseFloat(rushingEPAMatch[1]) : 0,
      successRate: successRateMatch ? parseFloat(successRateMatch[1]) : 0,
      explosiveness: explosivenessMatch ? parseFloat(explosivenessMatch[1]) : 0,
      passingDowns: passingDownsMatch ? parseFloat(passingDownsMatch[1]) : 0,
      standardDowns: standardDownsMatch ? parseFloat(standardDownsMatch[1]) : 0,
    };
  };

  const diffData = parseDifferentialData(predictionData?.formatted_analysis) || {
    overallEPA: 0,
    passingEPA: 0,
    rushingEPA: 0,
    successRate: 0,
    explosiveness: 0,
    passingDowns: 0,
    standardDowns: 0,
  };

  // Determine which team has advantage (positive = home team advantage, negative = away team advantage)
  const getAdvantageTeam = (value: number) => value > 0 ? homeTeam : awayTeam;
  const getAdvantageColor = (value: number) => value > 0 ? homeTeam.primary_color : awayTeam.primary_color;
  return (
    <GlassCard className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <svg className="w-5 h-5 text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
          </svg>
          <h3 className="text-white font-semibold">Comprehensive Differential Analysis</h3>
        </div>
        <div className="flex items-center gap-3 px-3 py-1.5 bg-[#2a3140] rounded-lg border border-[#3a4252]">
          <div className="flex items-center gap-1.5">
            <ImageWithFallback src={homeTeam.logo} alt={homeTeam.name} className="w-4 h-4 object-contain" />
            <span className="text-emerald-400 text-[10px] font-semibold">Positive = {homeTeam.name}</span>
          </div>
          <span className="text-[#3a4252]">|</span>
          <div className="flex items-center gap-1.5">
            <span className="text-red-400 text-[10px] font-semibold">Negative = {awayTeam.name}</span>
            <ImageWithFallback src={awayTeam.logo} alt={awayTeam.name} className="w-4 h-4 object-contain" />
          </div>
        </div>
      </div>

      {/* EPA Differentials */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <svg className="w-4 h-4 text-red-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M18 20V10M12 20V4M6 20v-6"/>
            </svg>
            <h4 className="text-red-400 font-semibold text-sm">EPA Differentials</h4>
          </div>
          <div className="flex items-center gap-2 px-3 py-1 rounded-full border" style={{
            backgroundColor: `${getAdvantageColor(diffData.overallEPA)}10`,
            borderColor: `${getAdvantageColor(diffData.overallEPA)}30`
          }}>
            <ImageWithFallback src={getAdvantageTeam(diffData.overallEPA).logo} alt={getAdvantageTeam(diffData.overallEPA).name} className="w-4 h-4 object-contain" />
            <span className="font-bold text-[10px]" style={{ color: getAdvantageColor(diffData.overallEPA) }}>
              {getAdvantageTeam(diffData.overallEPA).name.toUpperCase()} ADVANTAGE
            </span>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <MetricCard 
            title="Overall EPA" 
            value={diffData.overallEPA > 0 ? `+${diffData.overallEPA.toFixed(3)}` : diffData.overallEPA.toFixed(3)} 
            team={getAdvantageTeam(diffData.overallEPA).name} 
            color={getAdvantageColor(diffData.overallEPA)} 
          />
          <MetricCard 
            title="Passing EPA" 
            value={diffData.passingEPA > 0 ? `+${diffData.passingEPA.toFixed(3)}` : diffData.passingEPA.toFixed(3)} 
            team={getAdvantageTeam(diffData.passingEPA).name} 
            color={getAdvantageColor(diffData.passingEPA)} 
          />
          <MetricCard 
            title="Rushing EPA" 
            value={diffData.rushingEPA > 0 ? `+${diffData.rushingEPA.toFixed(3)}` : diffData.rushingEPA.toFixed(3)} 
            team={getAdvantageTeam(diffData.rushingEPA).name} 
            color={getAdvantageColor(diffData.rushingEPA)} 
          />
        </div>
      </div>

      {/* Performance Metrics */}
      <div className="mb-6">
        <div className="flex items-center gap-2 mb-4">
          <svg className="w-4 h-4 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"/>
            <path d="M12 6v6l4 2"/>
          </svg>
          <h4 className="text-cyan-400 font-semibold text-sm">Performance Metrics</h4>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <MetricCard 
            title="Success Rate" 
            value={diffData.successRate > 0 ? `+${diffData.successRate.toFixed(3)}` : diffData.successRate.toFixed(3)} 
            team={getAdvantageTeam(diffData.successRate).name} 
            color={getAdvantageColor(diffData.successRate)} 
          />
          <MetricCard 
            title="Explosiveness" 
            value={diffData.explosiveness > 0 ? `+${diffData.explosiveness.toFixed(3)}` : diffData.explosiveness.toFixed(3)} 
            team={getAdvantageTeam(diffData.explosiveness).name} 
            color={getAdvantageColor(diffData.explosiveness)} 
          />
        </div>
      </div>

      {/* Situational Success */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <svg className="w-4 h-4 text-blue-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
            </svg>
            <h4 className="text-blue-400 font-semibold text-sm">Situational Success</h4>
          </div>
          <div className="flex items-center gap-2 px-3 py-1 rounded-full border" style={{
            backgroundColor: `${getAdvantageColor(Math.abs(diffData.passingDowns) > Math.abs(diffData.standardDowns) ? diffData.passingDowns : diffData.standardDowns)}10`,
            borderColor: `${getAdvantageColor(Math.abs(diffData.passingDowns) > Math.abs(diffData.standardDowns) ? diffData.passingDowns : diffData.standardDowns)}30`
          }}>
            <ImageWithFallback src={getAdvantageTeam(Math.abs(diffData.passingDowns) > Math.abs(diffData.standardDowns) ? diffData.passingDowns : diffData.standardDowns).logo} alt={getAdvantageTeam(Math.abs(diffData.passingDowns) > Math.abs(diffData.standardDowns) ? diffData.passingDowns : diffData.standardDowns).name} className="w-4 h-4 object-contain" />
            <span className="font-bold text-[10px]" style={{ color: getAdvantageColor(Math.abs(diffData.passingDowns) > Math.abs(diffData.standardDowns) ? diffData.passingDowns : diffData.standardDowns) }}>
              {getAdvantageTeam(Math.abs(diffData.passingDowns) > Math.abs(diffData.standardDowns) ? diffData.passingDowns : diffData.standardDowns).name.toUpperCase()} LEADS
            </span>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <MetricCard 
            title="Passing Downs" 
            value={diffData.passingDowns > 0 ? `+${diffData.passingDowns.toFixed(3)}` : diffData.passingDowns.toFixed(3)} 
            team={getAdvantageTeam(diffData.passingDowns).name} 
            color={getAdvantageColor(diffData.passingDowns)} 
          />
          <MetricCard 
            title="Standard Downs" 
            value={diffData.standardDowns > 0 ? `+${diffData.standardDowns.toFixed(3)}` : diffData.standardDowns.toFixed(3)} 
            team={getAdvantageTeam(diffData.standardDowns).name} 
            color={getAdvantageColor(diffData.standardDowns)} 
          />
        </div>
      </div>

      {/* Insight Box */}
      <InsightBox
        whatItMeans="Differentials compare teams head-to-head across all categories. Positive differentials show where one team has statistical advantages. The magnitude of gaps determines whether advantages are noise (<5%) or meaningful (>10%)."
        whyItMatters={`Teams with 3+ major differentials (>0.15 gaps) in their favor win 75%+ of matchups. Offensive + defensive differentials compounding (both >0.10) create overwhelming advantages. Total EPA differential: ${diffData.overallEPA.toFixed(3)} points across all phases.`}
        whoHasEdge={{
          team: diffData.overallEPA > 0 ? homeTeam.name : awayTeam.name,
          reason: `${diffData.overallEPA > 0 ? homeTeam.name : awayTeam.name} holds ${[diffData.overallEPA, diffData.passingEPA, diffData.rushingEPA, diffData.successRate, diffData.explosiveness].filter(v => (diffData.overallEPA > 0 ? v > 0 : v < 0) && Math.abs(v) > 0.15).length} major advantages (>0.15 gaps). Combined differential strength: Overall EPA ${diffData.overallEPA.toFixed(3)}, Passing ${diffData.passingEPA.toFixed(3)}, Rushing ${diffData.rushingEPA.toFixed(3)}. Largest gap: ${Math.max(Math.abs(diffData.overallEPA), Math.abs(diffData.passingEPA), Math.abs(diffData.rushingEPA), Math.abs(diffData.successRate), Math.abs(diffData.explosiveness)).toFixed(3)}.`,
          magnitude: [diffData.overallEPA, diffData.passingEPA, diffData.rushingEPA].filter(v => Math.abs(v) > 0.15).length >= 2 ? 'major' : 
                     [diffData.overallEPA, diffData.passingEPA, diffData.rushingEPA].filter(v => Math.abs(v) > 0.10).length >= 2 ? 'significant' : 
                     [diffData.overallEPA, diffData.passingEPA, diffData.rushingEPA].filter(v => Math.abs(v) > 0.05).length >= 1 ? 'moderate' : 'small'
        }}
        keyDifferences={[
          `Biggest offensive gap: ${Math.abs(diffData.passingEPA) > Math.abs(diffData.rushingEPA) ? 'Passing' : 'Rushing'} EPA ${Math.max(Math.abs(diffData.passingEPA), Math.abs(diffData.rushingEPA)).toFixed(3)} (${(Math.max(Math.abs(diffData.passingEPA), Math.abs(diffData.rushingEPA)) * 7).toFixed(1)} points per game impact)`,
          `Performance metrics: Success Rate ${diffData.successRate.toFixed(3)}, Explosiveness ${diffData.explosiveness.toFixed(3)}`,
          `Net advantage: ${diffData.overallEPA > 0 ? homeTeam.name : awayTeam.name} holds overall ${Math.abs(diffData.overallEPA).toFixed(3)} EPA edge (${(Math.abs(diffData.overallEPA) * 7).toFixed(1)}pt scoring impact)`
        ]}
      />
    </GlassCard>
  );
}

function MetricCard({ title, value, team, color }: { title: string; value: string; team: string; color: string }) {
  return (
    <div className="relative overflow-hidden rounded-lg p-4 border" style={{
      borderColor: `${color}30`,
      background: `linear-gradient(135deg, ${color}10, ${color}05)`
    }}>
      <div className="flex items-center justify-between mb-2">
        <p className="text-gray-300 text-xs font-semibold">{title}</p>
        <div className="flex items-center gap-1">
          <svg className="w-3 h-3" style={{ color }} viewBox="0 0 24 24" fill="currentColor">
            <path d="M5 12h14M12 5l7 7-7 7"/>
          </svg>
          <span className="text-[10px] font-bold" style={{ color }}>{team}</span>
        </div>
      </div>
      <p className="text-2xl md:text-3xl font-bold font-mono mb-2" style={{ color }}>{value}</p>
      <div className="h-1 bg-[#1a1f28] rounded-full overflow-hidden">
        <div className="h-full rounded-full" style={{ width: '100%', backgroundColor: color }}></div>
      </div>
    </div>
  );
}

function SmallMetricCard({ title, value, positive = false }: { title: string; value: string; positive?: boolean }) {
  const textColor = positive ? 'text-cyan-400' : 'text-red-400';
  const barColor = positive ? 'bg-cyan-500' : 'bg-red-500';

  return (
    <div className="relative overflow-hidden rounded-lg p-3 border border-[#3a4252] bg-[#2a3140]">
      <div className="flex items-center justify-between mb-1.5">
        <p className="text-gray-300 text-[10px] font-semibold">{title}</p>
        <div className="flex items-center gap-1">
          <svg className={`w-3 h-3 ${textColor}`} viewBox="0 0 24 24" fill="currentColor">
            <path d="M5 12h14M12 5l7 7-7 7"/>
          </svg>
        </div>
      </div>
      <p className={`text-xl font-bold font-mono mb-1.5 ${textColor}`}>{value}</p>
      <div className="h-0.5 bg-[#1a1f28] rounded-full overflow-hidden">
        <div className={`h-full ${barColor} rounded-full`} style={{ width: '100%' }}></div>
      </div>
    </div>
  );
}
