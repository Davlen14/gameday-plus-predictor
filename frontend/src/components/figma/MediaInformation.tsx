import { GlassCard } from './GlassCard';
import { Tv, Radio, Users, Globe } from 'lucide-react';

interface MediaInformationProps {
  predictionData?: any;
}

export function MediaInformation({ predictionData }: MediaInformationProps) {
  // Extract media data from API
  const parseMediaFromFormattedAnalysis = (formattedText: string) => {
    if (!formattedText) return null;
    
    // Try to find TV network in header section first (more flexible regex)
    const headerMatch = formattedText.match(/Network:\s*([A-Z0-9&\s]+)/i);
    if (headerMatch) return headerMatch[1].trim();
    
    // Fallback to media information section
    const mediaMatch = formattedText.match(/TV:\s*([A-Z0-9&\s]+)/i);
    if (mediaMatch) return mediaMatch[1].trim();
    
    return null;
  };

  // Parse game time and date from formatted analysis
  const parseGameInfo = (formattedText: string) => {
    if (!formattedText) return { date: "TBD", time: "TBD" };
    
    const dateMatch = formattedText.match(/Date:\s*([^\\n]+)/);
    const timeMatch = formattedText.match(/Time:\s*([^\\n]+)/);
    
    return {
      date: dateMatch ? dateMatch[1].trim() : "TBD",
      time: timeMatch ? timeMatch[1].trim() : "TBD"
    };
  };

  const networkInfo = parseMediaFromFormattedAnalysis(predictionData?.formatted_analysis);
  const gameInfo = parseGameInfo(predictionData?.formatted_analysis);
  const gameDate = gameInfo.date;
  const gameTime = gameInfo.time;

  return (
    <GlassCard glowColor="from-purple-500/20 to-pink-500/20" className="p-6 border-purple-500/40">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-purple-500/20 border border-purple-500/40">
          <Tv className="w-5 h-5 text-purple-400" />
        </div>
        <h2 className="text-xl font-bold text-white">Media Information</h2>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* TV Coverage */}
        <div className="bg-gray-800/40 border border-gray-600/40 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <Tv className="w-4 h-4 text-violet-400" />
            <span className="text-sm text-gray-300">Television</span>
          </div>
          <div className="text-2xl font-bold text-violet-400 mb-1">{networkInfo || "TBD"}</div>
          <div className="text-xs text-gray-400">{networkInfo ? `${gameTime} ${gameDate}` : "Network TBD"}</div>
        </div>

        {/* Radio Coverage */}
        <div className="bg-gray-800/40 border border-gray-600/40 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <Radio className="w-4 h-4 text-violet-400" />
            <span className="text-sm text-gray-300">Radio</span>
          </div>
          <div className="text-lg font-bold text-violet-400 mb-1">Local Stations</div>
          <div className="text-xs text-gray-400">Team & Regional Networks</div>
        </div>

        {/* Streaming */}
        <div className="bg-gray-800/40 border border-gray-600/40 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <Globe className="w-4 h-4 text-violet-400" />
            <span className="text-sm text-gray-300">Streaming</span>
          </div>
          <div className="text-lg font-bold text-violet-400 mb-1">
            {networkInfo === 'FOX' ? 'FOX Sports' : 
             networkInfo === 'ESPN' ? 'ESPN+' :
             networkInfo === 'CBS' ? 'Paramount+' :
             networkInfo === 'NBC' ? 'Peacock' :
             networkInfo ? `${networkInfo} App` : 'TBD'}
          </div>
          <div className="text-xs text-gray-400">
            {networkInfo ? 'Available on streaming app' : 'Streaming TBD'}
          </div>
        </div>
      </div>

      {/* Coverage Details */}
      <div className="mt-4 p-3 bg-violet-500/10 border border-violet-500/30 rounded-lg">
        <div className="text-sm text-violet-200">
          <span className="font-semibold">Coverage Notes:</span> {
            networkInfo ? 
            `Game will be broadcast on ${networkInfo} with streaming available on the ${networkInfo} app.` :
            'Media coverage information will be updated as game approaches.'
          }
        </div>
      </div>
    </GlassCard>
  );
}