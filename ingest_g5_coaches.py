#!/usr/bin/env python3
"""
Ingest comprehensive data for all G5 coaches using the same logic as Power 5
Uses the proven GraphQL ingestor from archived_scripts/ingest_coach_graphql.py
"""

import sys
from pathlib import Path

# Add archived_scripts to path
sys.path.insert(0, str(Path(__file__).parent / 'archived_scripts'))

from ingest_coach_graphql import GraphQLCoachIngestor

# API Key
API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"

# All G5 coaches that need comprehensive data
G5_COACHES = [
    # MAC
    "Joe Moorhead", "Mike Uremovich", "Eddie George", "Pete Lembo",
    "Matt Drinkall", "Chris Creighton", "Mark Carney", "Chuck Martin",
    "Thomas Hammock", "Brian Smith", "Jason Candle", "Joe Harasymiak",
    "Lance Taylor",
    
    # AAC
    "Jeff Monken", "Tim Albin", "Blake Harrell", "Zach Kittley",
    "Ryan Silverfield", "Brian Newberry", "Scott Abell", "Alex Golesh",
    "K.C. Keeler", "Tre Lamb", "Trent Dilfer", "Jeff Traylor",
    
    # CUSA
    "Ryan Carty", "Willie Simmons", "Charles Kelly", "Jerry Mack",
    "Jamey Chadwell", "Sonny Cumbie", "Derek Mason", "Ryan Beard",
    "Tony Sanchez", "Phil Longo", "Scotty Walden", "Tyson Helton",
    
    # Sun Belt
    "Dowell Loggains", "Butch Jones", "Tim Beck", "Clay Helton",
    "Dell McGee", "Bob Chesney", "Michael Desormeaux", "Bryant Vincent",
    "Tony Gibson", "Ricky Rahne", "Major Applewhite", "Charles Huff",
    "G.J. Kinne", "Gerad Parker",
    
    # Mountain West
    "Troy Calhoun", "Spencer Danielson", "Jay Norvell", "Matt Entz",
    "Timmy Chang", "Jeff Choate", "Jason Eck", "Sean Lewis",
    "Ken Niumatalolo", "Dan Mullen", "Bronco Mendenhall", "Jay Sawvel",
]


def main():
    print("="*80)
    print("🏈 G5 COACHES COMPREHENSIVE DATA INGESTION")
    print("="*80)
    print(f"Total coaches to process: {len(G5_COACHES)}")
    print(f"Using same logic as Power 5 coaches")
    print("="*80)
    print()
    
    # Create ingestor
    ingestor = GraphQLCoachIngestor(api_key=API_KEY, db_path="instance/coaches_master.db")
    
    # Track results
    successful = []
    failed = []
    
    # Process each coach
    for i, coach_name in enumerate(G5_COACHES, 1):
        print(f"\n[{i}/{len(G5_COACHES)}] Processing {coach_name}...")
        
        try:
            success = ingestor.ingest(coach_name)
            if success:
                successful.append(coach_name)
                print(f"✅ {coach_name} - COMPLETE")
            else:
                failed.append(coach_name)
                print(f"⚠️  {coach_name} - No data found")
        except Exception as e:
            failed.append(coach_name)
            print(f"❌ {coach_name} - ERROR: {e}")
    
    # Final summary
    print("\n" + "="*80)
    print("📊 INGESTION SUMMARY")
    print("="*80)
    print(f"✅ Successful: {len(successful)}/{len(G5_COACHES)}")
    print(f"❌ Failed: {len(failed)}/{len(G5_COACHES)}")
    print(f"📡 Total API calls: {ingestor.api_calls}")
    print(f"🎯 Quota used: {ingestor.api_calls}/75,000 ({ingestor.api_calls/75000*100:.2f}%)")
    print("="*80)
    
    if failed:
        print("\n⚠️  Coaches with issues:")
        for coach in failed:
            print(f"  - {coach}")
    
    print("\n✅ G5 coaches now have comprehensive data like Power 5!")


if __name__ == "__main__":
    main()
