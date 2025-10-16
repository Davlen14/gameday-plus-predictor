import fbsData from '../fbs.json';

interface Team {
  id: number;
  school: string;
  mascot: string;
  abbreviation: string;
  conference: string;
  primary_color: string;
  alt_color: string;
  logos: string[];
}

export const teams: Team[] = fbsData;

export function getTeamBySchool(schoolName: string): Team | undefined {
  return teams.find(team => 
    team.school.toLowerCase().includes(schoolName.toLowerCase()) ||
    schoolName.toLowerCase().includes(team.school.toLowerCase())
  );
}

export function getTeamColors(schoolName: string): { primary: string; alt: string } {
  const team = getTeamBySchool(schoolName);
  return {
    primary: team?.primary_color || '#6b7280',
    alt: team?.alt_color || '#9ca3af'
  };
}

export function getTeamLogo(schoolName: string, dark: boolean = true): string {
  const team = getTeamBySchool(schoolName);
  if (!team?.logos?.length) return '';
  
  // Prefer dark logo if available, fallback to regular logo
  return dark && team.logos[1] ? team.logos[1] : team.logos[0];
}

export function getTeamById(id: number): Team | undefined {
  return teams.find(team => team.id === id);
}

/**
 * Generate team abbreviations with special case handling
 */
export const generateTeamAbbr = (teamName: string): string => {
  // Special cases for common team names
  const specialCases: { [key: string]: string } = {
    'USC': 'USC',
    'UCLA': 'UCLA',
    'TCU': 'TCU',
    'SMU': 'SMU',
    'BYU': 'BYU',
    'LSU': 'LSU',
    'ECU': 'ECU',
    'UCF': 'UCF',
    'Notre Dame': 'ND',
    'Texas A&M': 'A&M',
    'Virginia Tech': 'VT',
    'Georgia Tech': 'GT',
    'Florida State': 'FSU',
    'Arizona State': 'ASU',
    'Michigan State': 'MSU',
    'Ohio State': 'OSU',
    'Penn State': 'PSU',
    'Oklahoma State': 'OKST',
    'Iowa State': 'ISU',
    'Kansas State': 'KSU',
    'Mississippi State': 'MSST',
    'South Carolina': 'SC',
    'North Carolina': 'UNC',
    'NC State': 'NCST',
    'West Virginia': 'WVU',
    'Virginia': 'UVA',
    'Boston College': 'BC',
    'Wake Forest': 'WAKE',
    'Louisville': 'LOU',
    'Pittsburgh': 'PITT',
    'Syracuse': 'SYR',
    'Clemson': 'CLEM',
    'Miami': 'MIA',
    'Duke': 'DUKE',
    'Georgia': 'UGA',
    'Alabama': 'BAMA',
    'Tennessee': 'TENN',
    'Kentucky': 'UK',
    'Vanderbilt': 'VAND',
    'Missouri': 'MIZ',
    'Arkansas': 'ARK',
    'Auburn': 'AUB',
    'Ole Miss': 'MISS',
    'Texas': 'TEX',
    'Oklahoma': 'OU',
    'Kansas': 'KU',
    'Baylor': 'BAY',
    'Texas Tech': 'TTU',
    'Cincinnati': 'CIN',
    'Houston': 'HOU',
    'Iowa': 'IOWA',
    'Wisconsin': 'WISC',
    'Minnesota': 'MINN',
    'Illinois': 'ILL',
    'Northwestern': 'NW',
    'Indiana': 'IND',
    'Purdue': 'PUR',
    'Nebraska': 'NEB',
    'Rutgers': 'RU',
    'Maryland': 'MD',
    'Michigan': 'MICH',
    'Washington': 'WASH',
    'Oregon': 'ORE',
    'Stanford': 'STAN',
    'California': 'CAL',
    'Utah': 'UTAH',
    'Colorado': 'COL',
    'Arizona': 'ARIZ'
  };

  if (specialCases[teamName]) {
    return specialCases[teamName];
  }

  // For other teams, use first letter of each word, max 4 characters
  return teamName.split(' ').map((word: string) => word.charAt(0)).join('').substring(0, 4);
};

/**
 * Extract section from formatted analysis by section number
 */
export const extractSection = (analysis: string, sectionNumber: number): string => {
  const sectionPattern = new RegExp(`\\[${sectionNumber}\\][\\s\\S]*?(?=\\[${sectionNumber + 1}\\]|================================================================================\\s*🎯\\s*COMPREHENSIVE ANALYSIS|$)`, 'i');
  const match = analysis.match(sectionPattern);
  return match ? match[0] : '';
};

/**
 * Parse team-specific numeric data from text
 */
export const parseTeamValue = (text: string, teamName: string, metric?: string): number => {
  const patterns = [
    new RegExp(`${teamName}:\\s*([0-9.-]+)`, 'i'),
    new RegExp(`${teamName}\\s+([0-9.-]+)`, 'i'),
    ...(metric ? [new RegExp(`${metric}.*${teamName}.*?([0-9.-]+)`, 'i')] : []),
  ];

  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      return parseFloat(match[1]);
    }
  }
  return 0;
};