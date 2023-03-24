#! /usr/bin/env bash

# Run migrations
alembic upgrade head

# Start background scheduler
python -m wf_public_profiles.cron &

# Start service
python -m wf_public_profiles
