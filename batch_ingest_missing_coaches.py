"""
Batch Ingestion Script for Missing Coaches
===========================================
Ingests game data for 26 coaches who currently have 0 games in the database.

Usage:
    python batch_ingest_missing_coaches.py --api-key YOUR_API_KEY
    
Or set CFBD_API_KEY environment variable:
    export CFBD_API_KEY="your_key_here"
    python batch_ingest_missing_coaches.py
"""

import sys
import os
from pathlib import Path

# Add archived_scripts to path to import the ingestor
sys.path.insert(0, str(Path(__file__).parent / 'archived_scripts'))

from ingest_coach_graphql import GraphQLCoachIngestor
import argparse


# 26 coaches with 0 games (ID: Name - Current School)
MISSING_COACHES = [
    ("Brent Venables", 179, "Oklahoma"),
    ("Mario Cristobal", 180, "Miami"),
    ("Jon Sumrall", 181, "Tulane"),
    ("Eric Morris", 182, "North Texas"),
    ("Dave Doeren", 183, "NC State"),
    ("Jeff Brohm", 184, "Louisville"),
    ("Brent Key", 185, "Georgia Tech"),
    ("Jake Dickert", 186, "Wake Forest"),
    ("Scott Satterfield", 187, "Cincinnati"),
    ("Jimmy Rogers", 188, "Washington State"),
    ("Scott Frost", 189, "Ucf"),
    ("Manny Diaz", 190, "Duke"),
    ("Justin Wilcox", 191, "California"),
    ("Rich Rodriguez", 192, "West Virginia"),
    ("Jeff Lebby", 193, "Mississippi State"),
    ("David Braun", 194, "Northwestern"),
    ("Tony Elliott", 195, "Virginia"),
    ("Deshaun Foster", 196, "Ucla"),
    ("Bill Belichick", 197, "North Carolina"),
    ("Frank Reich", 198, "Stanford"),
    ("Brent Brennan", 199, "Arizona"),
    ("Brent Pry", 200, "Virginia Tech"),
    ("Fran Brown", 201, "Syracuse"),
    ("Bill O'Brien", 202, "Boston College"),
    ("Jim Mora", 203, "Uconn"),
    ("Trent Bray", 204, "Oregon State"),
]


def main():
    parser = argparse.ArgumentParser(
        description="Batch ingest game data for 26 missing coaches",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        default=os.getenv('CFBD_API_KEY'),
        help='CFBD API key (or set CFBD_API_KEY env var)'
    )
    
    parser.add_argument(
        '--start-at',
        type=int,
        default=0,
        help='Start at coach index (0-25) to resume from failure'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Limit number of coaches to process (for testing)'
    )
    
    args = parser.parse_args()
    
    if not args.api_key:
        print("❌ No API key provided!")
        print("Set CFBD_API_KEY environment variable or use --api-key flag")
        print("\nExample:")
        print("  export CFBD_API_KEY='your_key_here'")
        print("  python batch_ingest_missing_coaches.py")
        return 1
    
    # Check database exists
    db_path = Path('instance/coaches_master.db')
    if not db_path.exists():
        print("❌ Database not found at instance/coaches_master.db")
        return 1
    
    # Initialize ingestor
    ingestor = GraphQLCoachIngestor(args.api_key, db_path=str(db_path))
    
    # Determine which coaches to process
    coaches_to_process = MISSING_COACHES[args.start_at:]
    if args.limit:
        coaches_to_process = coaches_to_process[:args.limit]
    
    print("=" * 80)
    print("🚀 BATCH INGESTION: Missing Coaches")
    print("=" * 80)
    print(f"📊 Total coaches to process: {len(coaches_to_process)}")
    print(f"📡 Expected API calls: ~{len(coaches_to_process) * 8} (GraphQL + REST fallbacks)")
    print(f"🎯 Starting at index: {args.start_at}")
    print("=" * 80)
    print()
    
    results = {
        "success": [],
        "failed": [],
        "skipped": []
    }
    
    for i, (coach_name, coach_id, school) in enumerate(coaches_to_process, start=args.start_at + 1):
        print(f"\n{'='*80}")
        print(f"[{i}/{len(MISSING_COACHES)}] {coach_name} (ID: {coach_id}) - {school}")
        print(f"{'='*80}")
        
        try:
            success = ingestor.ingest(coach_name)
            
            if success:
                results["success"].append(coach_name)
                print(f"✅ SUCCESS: {coach_name}")
            else:
                results["failed"].append(coach_name)
                print(f"⚠️  FAILED: {coach_name} (see errors above)")
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user!")
            print(f"Resume with: --start-at {i-1}")
            break
        except Exception as e:
            print(f"❌ EXCEPTION for {coach_name}: {str(e)}")
            results["failed"].append(coach_name)
    
    # Print summary
    print("\n" + "=" * 80)
    print("📊 BATCH INGESTION SUMMARY")
    print("=" * 80)
    print(f"✅ Successful: {len(results['success'])}")
    print(f"❌ Failed: {len(results['failed'])}")
    print(f"📡 Total API Calls: {ingestor.api_calls}")
    print(f"🎯 Quota Used: {ingestor.api_calls} / 75,000 ({ingestor.api_calls/75000*100:.2f}%)")
    
    if results['success']:
        print(f"\n✅ Successfully ingested:")
        for name in results['success']:
            print(f"  - {name}")
    
    if results['failed']:
        print(f"\n❌ Failed to ingest:")
        for name in results['failed']:
            print(f"  - {name}")
    
    print("\n" + "=" * 80)
    
    return 0 if len(results['failed']) == 0 else 1


if __name__ == "__main__":
    exit(main())
