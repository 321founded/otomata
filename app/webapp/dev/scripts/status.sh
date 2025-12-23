#!/bin/bash
PORT=8020
if lsof -ti:${PORT} > /dev/null 2>&1; then
  echo "Serveur actif sur port ${PORT}"
else
  echo "Serveur non actif"
fi
