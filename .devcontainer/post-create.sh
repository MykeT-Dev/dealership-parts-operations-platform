#!/usr/bin/env bash
set -e

if [ -d "frontend" ]; then
  cd frontend
  npm install
  cd ..
fi

if [ -d "backend" ]; then
  cd backend

  if [ -f "requirements.txt" ]; then
    python -m pip install --upgrade pip
    pip install -r requirements.txt
  fi

  cd ..
fi