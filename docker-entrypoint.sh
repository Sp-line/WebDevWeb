#!/bin/sh

set -e

echo "🚀 Starting deployment..."

echo "🔄 Applying database migrations..."
alembic -c app/alembic.ini upgrade head

echo "✅ Starting application..."
exec "$@"