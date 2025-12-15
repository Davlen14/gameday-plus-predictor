// Coach headshot service
import coachHeadshotsData from '../../../power5_coaches_headshots.json';

interface CoachHeadshot {
  coach: string;
  school: string;
  headshot_url: string;
}

interface CoachHeadshotsData {
  big12: CoachHeadshot[];
  big10: CoachHeadshot[];
  sec: CoachHeadshot[];
  acc: CoachHeadshot[];
}

const coachHeadshots = coachHeadshotsData as CoachHeadshotsData;

/**
 * Get coach headshot URL by school name
 * @param schoolName - The school name to search for
 * @returns The headshot URL or undefined if not found
 */
export const getCoachHeadshot = (schoolName: string): string | undefined => {
  if (!schoolName) return undefined;

  const normalizedSchool = schoolName.toLowerCase().trim();

  // Search all conferences
  const allConferences = [
    ...coachHeadshots.big12,
    ...coachHeadshots.big10,
    ...coachHeadshots.sec,
    ...coachHeadshots.acc
  ];

  // First try exact match
  let coach = allConferences.find(c => {
    const coachSchool = c.school.toLowerCase();
    return coachSchool === normalizedSchool;
  });

  // If no exact match, try partial match (but avoid substring issues like Texas vs Texas Tech)
  if (!coach) {
    coach = allConferences.find(c => {
      const coachSchool = c.school.toLowerCase();
      // Only match if the school name is at word boundaries
      const schoolWords = normalizedSchool.split(/\s+/);
      const coachWords = coachSchool.split(/\s+/);
      
      // Check if all words from search match all words in coach school
      return schoolWords.length === coachWords.length && 
             schoolWords.every((word, i) => coachWords[i].includes(word) || word.includes(coachWords[i]));
    });
  }

  return coach?.headshot_url;
};

/**
 * Get coach data by school name
 * @param schoolName - The school name to search for
 * @returns The coach data object or undefined if not found
 */
export const getCoachData = (schoolName: string): CoachHeadshot | undefined => {
  if (!schoolName) return undefined;

  const normalizedSchool = schoolName.toLowerCase().trim();

  const allConferences = [
    ...coachHeadshots.big12,
    ...coachHeadshots.big10,
    ...coachHeadshots.sec,
    ...coachHeadshots.acc
  ];

  // First try exact match
  let coach = allConferences.find(c => {
    const coachSchool = c.school.toLowerCase();
    return coachSchool === normalizedSchool;
  });

  // If no exact match, try word-by-word match
  if (!coach) {
    coach = allConferences.find(c => {
      const coachSchool = c.school.toLowerCase();
      const schoolWords = normalizedSchool.split(/\s+/);
      const coachWords = coachSchool.split(/\s+/);
      
      return schoolWords.length === coachWords.length && 
             schoolWords.every((word, i) => coachWords[i].includes(word) || word.includes(coachWords[i]));
    });
  }

  return coach;
};

/**
 * Get all coaches for a specific conference
 * @param conference - The conference name (big12, big10, sec, acc)
 * @returns Array of coach data for that conference
 */
export const getCoachesByConference = (conference: string): CoachHeadshot[] => {
  const normalizedConf = conference.toLowerCase().replace(/\s+/g, '');
  
  const conferenceMap: { [key: string]: CoachHeadshot[] } = {
    'big12': coachHeadshots.big12,
    'big10': coachHeadshots.big10,
    'sec': coachHeadshots.sec,
    'acc': coachHeadshots.acc,
    'bigten': coachHeadshots.big10, // Alias
    'bigtwelve': coachHeadshots.big12 // Alias
  };

  return conferenceMap[normalizedConf] || [];
};

export default {
  getCoachHeadshot,
  getCoachData,
  getCoachesByConference
};
