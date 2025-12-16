#!/usr/bin/env python3
"""
Update teams table with wordmark URLs from wordmark.csv
"""

import sqlite3
import csv

def update_wordmarks_from_csv():
    """Update teams table with full GitHub URLs from wordmark.csv"""
    
    conn = sqlite3.connect('instance/coaches_master.db')
    cursor = conn.cursor()
    
    # Read CSV and extract team -> wordmark_url mapping
    wordmark_map = {}
    with open('wordmark.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            team = row['team']
            wordmark_url = row['wordmark_url']
            if wordmark_url and wordmark_url != 'NA':
                wordmark_map[team] = wordmark_url
    
    print(f"📊 Found {len(wordmark_map)} teams with wordmarks in CSV")
    
    # Update database with full URLs
    updated = 0
    for team, url in wordmark_map.items():
        cursor.execute('UPDATE teams SET wordmark_url = ? WHERE school = ?', (url, team))
        if cursor.rowcount > 0:
            updated += 1
            print(f"✅ {team}: {url}")
    
    conn.commit()
    print(f"\n✅ Updated {updated} teams with full GitHub URLs")
    
    # Verify updates
    cursor.execute('SELECT school, wordmark_url FROM teams WHERE wordmark_url LIKE "https://%" LIMIT 3')
    results = cursor.fetchall()
    
    print("\n🔍 Sample updated records:")
    for school, url in results:
        print(f"  {school}: {url[:80]}...")
    
    conn.close()

if __name__ == '__main__':
    update_wordmarks_from_csv()

# Old hardcoded dictionary - keeping for reference
OLD_WORDMARKS = {
    # ACC
    "Boston College": "7381_boston_college-wordmark.png",
    "California": "7066_california_golden_bears-wordmark-2013.png",
    "Clemson": "2397_clemson_tigers-wordmark-2014.png",
    "Duke": "1549_duke_blue_devils-wordmark-1978.png",
    "Florida State": "5954_florida_state_seminoles-wordmark-2014.png",
    "Georgia Tech": "georgia_tech_wordmark_gt_lockup_02.png",
    "Louisville": "8185_louisville_cardinals-wordmark-2013.png",
    "Miami": "2537_miami_wordmark.png",
    "NC State": "north_carolina_state_wolfpack_logo_wordmark_2011_sportslogosnet-5725.png",
    "North Carolina": "north_carolina_tar_heels_logo_wordmark_19965588.png",
    "Pittsburgh": "9267_pittsburgh_panthers-wordmark-1997.png",
    "SMU": "smu_mustangs_logo_wordmark_2021_sportslogosnet-3447.png",
    "Stanford": "stanford_cardinal_logo_wordmark_2015_sportslogosnet-4752.png",
    "Syracuse": "syracuse_orange_logo_wordmark_2015_sportslogosnet-2819.png",
    "Virginia": "8905_virginia_cavaliers-wordmark-2020.png",
    "Virginia Tech": "virginia_tech_hokies_logo_wordmark_2016_sportslogosnet-6021.png",
    "Wake Forest": "2196_wake_forest_demon_deacons-wordmark-2007.png",
    
    # American Athletic
    "Army": "1039_army_black_knights-wordmark-2015.png",
    "Charlotte": "2285_charlotte_49ers-wordmark-2020.png",
    "East Carolina": "east_carolina_pirates_logo_secondary_2009_sportslogosnet-1391.png",
    "Florida Atlantic": "florida_atlantic_owls_logo_wordmark_2014_sportslogosnet-2808.png",
    "Memphis": "memphis_tigers_logo_wordmark_2021_sportslogosnet-8745.png",
    "Navy": "navy_midshipmen_logo_wordmark_20095936.png",
    "North Texas": "north_texas_mean_green_logo_wordmark_20051155.png",
    "Rice": "2538_rice_owls-wordmark-2017.png",
    "South Florida": "south_florida_bulls_logo_secondary_2011_sportslogosnet-7610.png",
    "Temple": "temple_owls_logo_wordmark_2020_sportslogosnet-1905.png",
    "Tulane": "6263_tulane_green_wave-wordmark-2014.png",
    "Tulsa": "tulsa_golden_hurricane_logo_wordmark_2021_sportslogosnet-4838.png",
    "UAB": "uab_blazers_logo_wordmark_2015_sportslogosnet-3373.png",
    # UTSA - NA
    
    # Big 12
    "Arizona": "2804_arizona_wildcats-wordmark-2003.png",
    "Arizona State": "2342_arizona_state_sun_devils-wordmark-2012.png",
    "BYU": "brigham_young_cougars_logo_wordmark_19992374.png",
    "Baylor": "1778_baylor_bears-wordmark-2005.png",
    "Cincinnati": "cincinnati_bearcats_logo_wordmark_20058032.png",
    "Colorado": "8028_colorado_buffaloes-wordmark-2006.png",
    "Houston": "houston_cougars_logo_wordmark_20129226.png",
    "Iowa State": "iowa_state_wordmark.png",
    "Kansas": "1709_kansas_jayhawks-wordmark-2006.png",
    "Kansas State": "kansas_state_wildcats_logo_alternate_2019_sportslogosnet-4205.png",
    "Oklahoma State": "9181_oklahoma_state_cowboys-wordmark-2001.png",
    "TCU": "tcu_horned_frogs_logo_wordmark_2013_sportslogosnet-8595.png",
    "Texas Tech": "6911_texas_tech_red_raiders-wordmark-2000.png",
    "UCF": "central_florida_knights_logo_wordmark_20076509.png",
    "Utah": "4760_utah_utes-wordmark-2015.png",
    "West Virginia": "west_virginia_mountaineers_logo_wordmark_2019_sportslogosnet-4155.png",
    
    # Big Ten
    "Illinois": "3664_illinois_fighting_illini-wordmark-2014.png",
    "Indiana": "5051_indiana_hoosiers-wordmark-0.png",
    "Iowa": "iowa_hawkeyes_logo_wordmark_2012_sportslogosnet-5540.png",
    "Maryland": "maryland_terrapins_logo_wordmark_20115592.png",
    "Michigan": "michigan_wolverines_logo_wordmark_2016_sportslogosnet-8199.png",
    "Michigan State": "michigan_state_spartans_logo_wordmark_2010_sportslogosnet-9157.png",
    "Minnesota": "University_of_Minnesota_wordmark.png",
    "Nebraska": "6089_nebraska_cornhuskers-wordmark-2016.png",
    "Northwestern": "6442_northwestern_wildcats-wordmark-1981.png",
    "Ohio State": "2586_ohio_state_buckeyes-wordmark-2013.png",
    "Oregon": "oregon_ducks_wordmark.png",
    "Penn State": "penn_state_nittany_lions_logo_wordmark_19968994.png",
    "Purdue": "purdue_boilermakers_logo_wordmark_20121876.png",
    "Rutgers": "rutgers_scarlet_knights_logo_wordmark_2016_sportslogosnet-2651.png",
    "UCLA": "ucla_bruins_logo_wordmark_2017_sportslogosnet-6926.png",
    "USC": "southern_california_trojans_logo_wordmark_20162572.png",
    "Washington": "washington_huskies_logo_wordmark_2016_sportslogosnet-3187.png",
    "Wisconsin": "wisconsin-wordmark.png",
    
    # Conference USA
    "Delaware": "delaware_blue_hens_logo_wordmark_2018_sportslogosnet-3269.png",
    "Florida International": "5979_florida_intl_golden_panthers-wordmark-2009.png",
    "FIU": "5979_florida_intl_golden_panthers-wordmark-2009.png",  # Alias
    "Jacksonville State": "jacksonville_state_gamecocks_logo_wordmark_20028913.png",
    "Kennesaw State": "kennesaw_state_owls_logo_wordmark_20128370.png",
    "Liberty": "liberty_flames_logo_wordmark_20131049.png",
    "Louisiana Tech": "la_tech_wordmark.png",
    "Middle Tennessee": "middle_tennessee_blue_raiders_logo_wordmark_2015_sportslogosnet-8290.png",
    "Missouri State": "1731_missouri_state__bears-alternate-2006.png",
    "New Mexico State": "new_mexico_state_aggies_logo_wordmark_20056268.png",
    "Sam Houston": "7125_sam_houston_state_bearkats-wordmark-2020.png",
    "Sam Houston State": "7125_sam_houston_state_bearkats-wordmark-2020.png",  # Alias
    "UTEP": "2713_utep-wordmark.png",
    "Western Kentucky": "western_kentucky_hilltoppers_logo_wordmark_2017_sportslogosnet-6489.png",
    
    # FBS Independents
    "Notre Dame": "notre_dame_fighting_irish_logo_wordmark_2015_sportslogosnet-5359.png",
    "UConn": "uconn_huskies_logo_alternate_20132910.png",
    "Connecticut": "uconn_huskies_logo_alternate_20132910.png",  # Alias
    
    # Mid-American
    "Akron": "akron_zips_logo_wordmark_2022_sportslogosnet-1159.png",
    "Ball State": "ball_state_cardinals_logo_wordmark_2015_sportslogosnet-7204.png",
    "Bowling Green": "bowling_green_falcons_logo_wordmark_20148415.png",
    "Buffalo": "3264_buffalo_bulls-wordmark-2016.png",
    "Central Michigan": "central_michigan-wordmark.png",
    "Eastern Michigan": "9448_eastern_michigan_eagles-alternate-2000.png",
    "Kent State": "kent_state_golden_flashes_logo_wordmark_2017_sportslogosnet-7257.png",
    # Massachusetts - NA
    "Miami (OH)": "miami_(ohio)_redhawks_logo_wordmark_20131371.png",
    "Northern Illinois": "5142_northern_illinois_huskies-wordmark-2001.png",
    "Ohio": "4346_ohio_bobcats-wordmark-1996.png",
    "Toledo": "toledo_rockets_logo_primary_2019_sportslogosnet-7348.png",
    "Western Michigan": "western_michigan_broncos_logo_wordmark_20168247.png",
    
    # Mountain West
    "Air Force": "air_force_falcons_logo_wordmark_20202087.png",
    "Boise State": "boise_state_broncos_logo_wordmark_2013_sportslogosnet-5682.png",
    "Colorado State": "colorado_state_rams_logo_wordmark_20217977.png",
    "Fresno State": "fresno_state_bulldogs_logo_wordmark_2020_sportslogosnet-2559.png",
    "Hawai'i": "hawaii_warriors_logo_wordmark_2000_sportslogosnet-3044.png",
    "Hawaii": "hawaii_warriors_logo_wordmark_2000_sportslogosnet-3044.png",  # Alias
    "Nevada": "5309_nevada_wolf_pack-primary-2008.png",
    "New Mexico": "new_mexico_lobos_logo_secondary_2017_sportslogosnet-2427.png",
    "San Diego State": "san_diego_state_aztecs_logo_wordmark_20135405.png",
    "San José State": "san_jose_state_spartans_logo_secondary_2018_sportslogosnet-7284.png",
    "San Jose State": "san_jose_state_spartans_logo_secondary_2018_sportslogosnet-7284.png",  # Alias
    "UNLV": "unlv_rebels_logo_secondary_2017_sportslogosnet-7738.png",
    "Utah State": "utah_state_aggies_logo_wordmark_20149097.png",
    "Wyoming": "1604_wyoming_cowboys-wordmark-2004.png",
    
    # Pac-12
    "Oregon State": "oregon_state_beavers_logo_wordmark_20133449.png",
    "Washington State": "1054_washington_state_cougars-wordmark-2011.png",
    
    # SEC
    "Alabama": "alabama_crimson_tide_logo_secondary_19987746.png",
    "Arkansas": "2749_arkansas_razorbacks-wordmark-2014.png",
    "Auburn": "auburn_tigers_logo_wordmark_20067195.png",
    "Florida": "9227_florida_gators-wordmark-1992.png",
    "Georgia": "georgia_bulldogs_logo_wordmark_20156350.png",
    "Kentucky": "kentucky_wildcats_logo_wordmark_20162011.png",
    "LSU": "lsu_tigers_logo_wordmark_20029527.png",
    "Mississippi State": "8440_mississippi_state_bulldogs-wordmark-2009.png",
    "Missouri": "missouri_tigers_logo_wordmark_2018_sportslogosnet-1762.png",
    "Oklahoma": "oklahoma_sooners_logo_wordmark_2008_sportslogosnet-1138.png",
    "Ole Miss": "mississippi_rebels_logo_wordmark_20206855.png",
    "Mississippi": "mississippi_rebels_logo_wordmark_20206855.png",  # Alias
    "South Carolina": "south_carolina_gamecocks_logo_alternate_2008_sportslogosnet-4735.png",
    "Tennessee": "tennessee_volunteers_logo_wordmark_20052034.png",
    "Texas": "texas_longhorns_logo_wordmark_2000_sportslogosnet-1899.png",
    "Texas A&M": "2346_texas_a&m_aggies-wordmark-2001.png",
    "Vanderbilt": "vanderbilt_commodores_logo_wordmark_2012_sportslogosnet-9359.png",
    
    # Sun Belt
    "Appalachian State": "appalachian_state_wordmark.png",  # Placeholder - was NA
    "App State": "appalachian_state_wordmark.png",  # Alias - was NA
    "Arkansas State": "arkansas_state_red_wolves_logo_secondary_2017_sportslogosnet-9157.png",
    "Coastal Carolina": "coastal_carolina_chanticleers_logo_wordmark_2016_sportslogosnet-2620.png",
    "Georgia Southern": "georgia_southern_eagles_logo_wordmark_2016_sportslogosnet-9844.png",
    "Georgia State": "georgia_state_panthers_logo_wordmark_20159932.png",
    "James Madison": "3393_james_madison_dukes-wordmark-2017.png",
    "Louisiana": "louisiana_ragin_cajuns_logo_wordmark_2018_sportslogosnet-9665.png",
    "Louisiana-Lafayette": "louisiana_ragin_cajuns_logo_wordmark_2018_sportslogosnet-9665.png",  # Alias
    "Marshall": "4715_marshall_thundering_herd-wordmark-2001.png",
    "Old Dominion": "old_dominion_monarchs_logo_wordmark_20027264.png",
    "South Alabama": "9070_south_alabama_jaguars-wordmark-2008.png",
    "Southern Miss": "3959_southern_miss_golden_eagles-wordmark-2003.png",
    "Southern Mississippi": "3959_southern_miss_golden_eagles-wordmark-2003.png",  # Alias
    "Texas State": "texas_state_bobcats_logo_secondary_20082403.png",
    "Troy": "troy_trojans_logo_wordmark_2016_sportslogosnet-8357.png",
    # UL Monroe - NA
}


def update_wordmarks():
    """Update teams table with wordmark URLs"""
    db_path = Path(__file__).parent / "instance" / "coaches_master.db"
    
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all teams
    cursor.execute("SELECT id, school FROM teams")
    teams = cursor.fetchall()
    
    updated = 0
    not_found = []
    
    for team_id, school in teams:
        if school in WORDMARKS:
            wordmark_file = WORDMARKS[school]
            cursor.execute(
                "UPDATE teams SET wordmark_url = ? WHERE id = ?",
                (wordmark_file, team_id)
            )
            updated += 1
            print(f"✅ {school}: {wordmark_file}")
        else:
            not_found.append(school)
    
    conn.commit()
    conn.close()
    
    print(f"\n📊 Summary:")
    print(f"  ✅ Updated: {updated} teams")
    print(f"  ⚠️  Not found in mapping: {len(not_found)} teams")
    
    if not_found and len(not_found) <= 20:
        print(f"\n  Teams without wordmark mapping:")
        for team in not_found[:20]:
            print(f"    - {team}")


if __name__ == "__main__":
    update_wordmarks()
