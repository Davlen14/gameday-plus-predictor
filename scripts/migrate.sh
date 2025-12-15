#!/bin/bash
# Quick Migration Script
# Run this to execute the full migration

echo "🏈 GAMEDAY+ DATABASE MIGRATION 🏈"
echo "=================================="
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Virtual environment not activated"
    echo "Activating .venv..."
    source .venv/bin/activate
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python version: $PYTHON_VERSION"

# Check if database_migration directory exists
if [ ! -d "database_migration" ]; then
    echo "❌ database_migration directory not found"
    exit 1
fi

# Make scripts executable
chmod +x database_migration/*.py

# Run master migration
echo ""
echo "🚀 Starting master migration script..."
echo ""

python3 database_migration/run_migration.py

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "🎉 Migration completed successfully!"
    echo ""
    echo "Next steps:"
    echo "  1. Test predictions: python run.py 'Ohio State' 'Michigan'"
    echo "  2. Archive JSONs:    ./archive_jsons.sh"
    echo "  3. Update predictor: Edit graphqlpredictor.py"
else
    echo ""
    echo "❌ Migration failed with exit code $EXIT_CODE"
    echo "Check the output above for errors"
fi

exit $EXIT_CODE
