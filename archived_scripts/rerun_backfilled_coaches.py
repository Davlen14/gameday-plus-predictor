"""
Re-run GraphQL ingestion for coaches that were backfilled to populate all tables.
This preserves the backfilled game data while adding rankings, recruiting, talent, etc.
"""

from ingest_coach_graphql import GraphQLCoachIngestor
import time

API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
DB_PATH = "instance/coaches_master.db"

# Coaches that were backfilled and need complete data
backfilled_coaches = [
    "Chris Klieman",
    "Clark Lea", 
    "Dan Lanning",
    "Dave Aranda",
    "David Braun",
    "Deion Sanders",
    "Deshaun Foster",
    "Joey McGuire",
    "Kenny Dillingham",
    "Rhett Lashlee",
    "Sam Pittman",
    "Shane Beamer",
    "Sherrone Moore"
]

def main():
    """Re-run GraphQL ingestion for backfilled coaches."""
    print("=" * 80)
    print("🔄 RE-RUNNING GRAPHQL INGESTION FOR BACKFILLED COACHES")
    print("=" * 80)
    print("\nThis will add:")
    print("  ✓ Rankings (AP/Coaches polls)")
    print("  ✓ Recruiting classes")
    print("  ✓ Talent composites")
    print("  ✓ Draft picks")
    print("  ✓ Transfer portal data")
    print("  ✓ vs Coaches records")
    print("  ✓ Situational stats")
    print("\nExisting backfilled game data will be preserved (INSERT OR IGNORE).")
    
    proceed = input(f"\n🔄 Proceed with re-ingestion of {len(backfilled_coaches)} coaches? (y/n): ")
    if proceed.lower() != 'y':
        print("❌ Cancelled")
        return
    
    ingestor = GraphQLCoachIngestor(api_key=API_KEY, db_path=DB_PATH)
    
    successful = 0
    failed = []
    
    for i, coach_name in enumerate(backfilled_coaches, 1):
        print(f"\n[{i}/{len(backfilled_coaches)}] {coach_name}...", end=" ", flush=True)
        
        try:
            if ingestor.ingest(coach_name):
                successful += 1
                print("✅")
            else:
                failed.append(coach_name)
                print("❌")
            
            if i < len(backfilled_coaches):
                time.sleep(1)  # Rate limiting
        except Exception as e:
            failed.append(coach_name)
            print(f"❌ ({str(e)[:50]})")
    
    print(f"\n{'=' * 80}")
    print(f"✅ RE-INGESTION COMPLETE")
    print(f"   Successful: {successful}/{len(backfilled_coaches)}")
    print(f"   Total API Calls: {ingestor.api_calls}")
    if failed:
        print(f"\n❌ Failed coaches ({len(failed)}):")
        for coach in failed:
            print(f"   • {coach}")
    print("=" * 80)

if __name__ == "__main__":
    main()
