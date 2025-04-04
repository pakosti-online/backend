#!/bin/bash

if [ ! -d "/app/migrations" ]; then
  echo "Инициализация миграций..."
  aerich init -t app.db.TORTOISE_ORM
  aerich migrate
fi

echo "Применение миграций..."
aerich upgrade

exec "$@"
