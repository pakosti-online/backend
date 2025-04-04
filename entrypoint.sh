#!/bin/bash

if [ ! -d "/app/migrations" ]; then
  echo "Инициализация миграций..."
  aerich init -t your_project.db_config.TORTOISE_ORM
  aerich migrate
fi

echo "Применение миграций..."
aerich upgrade

exec "$@"
