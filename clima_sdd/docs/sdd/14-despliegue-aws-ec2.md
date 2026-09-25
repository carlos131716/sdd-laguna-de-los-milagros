# SDD-014 — Despliegue en AWS EC2

## Metadata

| Campo | Valor |
|---|---|
| Version | 1.0 |
| Estado | Implementado |
| Ambiente | AWS EC2 |
| Region | US East (Ohio), `us-east-2` |
| Sistema operativo | Amazon Linux 2023 |
| Tipo de instancia | `t3.micro` |
| Runtime | Docker 25 |
| Exposicion web | HTTP 80 → contenedor 5000 |
| Persistencia | Volumen montado para SQLite |

## Objetivo

Publicar la aplicación de clima y turismo en una instancia EC2 accesible desde Internet mediante la IP pública, manteniendo el código dentro de un contenedor Docker.

## Arquitectura desplegada

```text
Usuario
  │ HTTP :80
  ▼
Security Group EC2
  │
  ▼
EC2 Amazon Linux 2023
  │ Docker :5000
  ▼
Contenedor clima-sdd
  ├── Flask
  ├── frontend
  ├── backend
  └── SQLite en /app/data
```

## Recursos AWS

- Una instancia EC2 `t3.micro`.
- AMI Amazon Linux 2023.
- Una VPC y subred predeterminadas.
- IP pública habilitada.
- Volumen raíz EBS de 8 GiB `gp3`.
- Security Group asociado a la instancia.
- Key pair `clima-sdd-key`.

## Reglas de red

| Regla | Puerto | Origen | Uso |
|---|---:|---|---|
| SSH | 22 | IP del administrador | Administración |
| HTTP | 80 | `0.0.0.0/0` | Aplicación web |
| HTTPS | 443 | Futuro | TLS |

No se expone el puerto 5000 públicamente. Docker publica el puerto 5000 internamente mediante `-p 80:5000`.

## Configuración de aplicación

El archivo `.env` debe existir solo en el servidor y contener:

```env
SECRET_KEY=<secreto-aleatorio>
DATABASE_PATH=/app/data/clima.sqlite3
SESSION_COOKIE_SECURE=0
```

En producción con HTTPS se debe usar `SESSION_COOKIE_SECURE=1`.

## Procedimiento de despliegue

```bash
cd /home/ec2-user/clima-sdd
mkdir -p data
docker build -t clima-sdd .
docker run -d --name clima-sdd \
  --restart unless-stopped \
  --env-file .env \
  -p 80:5000 \
  -v /home/ec2-user/clima-sdd/data:/app/data \
  clima-sdd
```

## Verificación

- `docker ps` muestra el contenedor en estado `Up`.
- `docker logs clima-sdd` no muestra errores de arranque.
- `http://IP_PUBLICA/registro` permite crear cuenta.
- `http://IP_PUBLICA/` permite consultar clima.
- `http://IP_PUBLICA/turismo` muestra la Laguna de los Milagros.
- La base permanece después de reiniciar el contenedor.

## Operación

```bash
docker ps
docker logs --tail 100 clima-sdd
docker restart clima-sdd
```

Para actualizar:

```bash
docker stop clima-sdd
docker rm clima-sdd
docker build -t clima-sdd .
docker run -d --name clima-sdd --restart unless-stopped --env-file .env -p 80:5000 -v /home/ec2-user/clima-sdd/data:/app/data clima-sdd
```

## Seguridad

- No compartir el archivo `.pem`.
- No subir `.env` al repositorio.
- Restringir SSH a la IP del administrador.
- Activar HTTPS antes de usar credenciales reales en producción.
- Crear alertas de facturación y revisar consumo de EC2/EBS.

## Rollback

Conservar la etiqueta anterior de Docker antes de actualizar. Si la nueva versión falla, detenerla y ejecutar el contenedor con la imagen anterior. No eliminar el volumen `/home/ec2-user/clima-sdd/data` durante un rollback.

## Pendientes de producción

- Elastic IP o dominio DNS.
- Nginx y certificado HTTPS.
- PostgreSQL gestionado para crecer.
- Backups automáticos.
- CloudWatch, healthcheck y alertas.
- Pipeline CI/CD.

## Definición de terminado

El despliegue se considera terminado cuando la instancia está en ejecución, el contenedor permanece activo, el puerto 80 responde, el registro/login funciona, clima y turismo cargan, y los datos de usuarios sobreviven a un reinicio del contenedor.
