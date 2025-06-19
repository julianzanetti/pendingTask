#!/bin/sh

echo "========== INICIANDO ENTRYPOINT =========="

echo "Esperando a que la base de datos esté lista..."

RETRIES=20
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q' > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Esperando conexión a la base de datos... ($RETRIES intentos restantes)"
  sleep 3
  RETRIES=$((RETRIES - 1))
done

if [ $RETRIES -eq 0 ]; then
  echo "Error: no se pudo conectar a la base de datos después de múltiples intentos."
  exit 1
fi

echo "Base de datos lista. Ejecutando migraciones..."

python manage.py migrate --noinput || exit 1

echo "Verificando migraciones aplicadas:"
python manage.py showmigrations

echo "Iniciando servidor Django..."
exec python manage.py runserver 0.0.0.0:8000