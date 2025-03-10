# Guía de despliegue proyecto en GCP 

Se detalla los pasos para desplegar la aplicación en GCP utilizando Kubernetes Engine, Cloud SQL, Cloud Storage y Artifact Registry.

## Tabla de Contenidos

1. [Prerrequisitos](#prerrequisitos)
2. [Configuración Inicial en GCP](#configuración-inicial-en-gcp)
3. [Configuración de Cloud Storage](#configuración-de-cloud-storage)
4. [Configuración de Cloud SQL](#configuración-de-cloud-sql)
5. [Configuración de Kubernetes](#configuración-de-kubernetes)
6. [Configuración de cuentas de servicio y secretos](#configuración-de-cuentas-de-servicio-y-secretos)
7. [Construcción y publicación de imágenes Docker](#construcción-y-publicación-de-imágenes-docker)
8. [Despliegue de microservicios](#despliegue-de-microservicios)
9. [Configuración del Ingress](#configuración-del-ingress)
10. [Monitoreo y alertas](#monitoreo-y-alertas)
11. [Resolución de problemas](#resolución-de-problemas)

## Prerrequisitos

* Cuenta en Google Cloud Platform
* gcloud CLI instalado y configurado
* kubectl instalado
* Docker instalado
* Permisos adecuados en el proyecto GCP

## Configuración inicial en GCP

### 1. Crear un proyecto en GCP
```bash
gcloud projects create appnomonoliticas-452202 --name="Aplicaciones No Monolíticas"
```

### 2. Habilitar las APIs necesarias
```bash
gcloud services enable container.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  sqladmin.googleapis.com \
  storage.googleapis.com \
  compute.googleapis.com \
  --project=appnomonoliticas-452202
```

### 3. Configurar gcloud CLI para usar el proyecto
```bash
gcloud config set project appnomonoliticas-452202
```

## Configuración de Cloud Storage

### 1. Crear los buckets para almacenamiento de imágenes
```bash
# Bucket para imágenes de Latinoamérica
gsutil mb -l us-central1 gs://imagenes-lat

# Bucket para imágenes de USA
gsutil mb -l us-central1 gs://imagenes-usa
```

### 2. Configurar permisos de los buckets
```bash
# Dar acceso de lectura/escritura a la cuenta de servicio que usarán los microservicios
gsutil iam ch serviceAccount:app-no-monoliticas-sa@appnomonoliticas-452202.iam.gserviceaccount.com:objectAdmin gs://imagenes-lat
gsutil iam ch serviceAccount:app-no-monoliticas-sa@appnomonoliticas-452202.iam.gserviceaccount.com:objectAdmin gs://imagenes-usa
```

## Configuración de Cloud SQL

### 1. Crear instancias de Cloud SQL para PostgreSQL
```bash
# Base de datos para el servicio de Usuarios
gcloud sql instances create monoliticas-users-db \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --root-password=monolitic4s-users \
  --storage-size=10GB \
  --storage-type=HDD

# Base de datos para el servicio de Anonimización
gcloud sql instances create monoliticas-anonimizacion-db \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --root-password=monolitic4s-anonimizacion \
  --storage-size=10GB \
  --storage-type=HDD

# Base de datos para el servicio de Verificacion
gcloud sql instances create monoliticas-verificacion-db \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --root-password=monolitic4s-verificacion \
  --storage-size=10GB \
  --storage-type=HDD

# Base de datos para el servicio de Ingesta
gcloud sql instances create monoliticas-ingesta-db \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --root-password=monolitic4s-ingesta \
  --storage-size=10GB \
  --storage-type=HDD

```

# Base de datos para el servicio de Verificacion

### 2. Crear bases de datos en las instancias
```bash
# Crear base de datos en la instancia de usuarios
gcloud sql databases create user_db --instance=monoliticas-users-db

# Crear base de datos en la instancia de anonimización
gcloud sql databases create anonimizacion_db --instance=monoliticas-anonimizacion-db

# Crear base de datos en la instancia de verificacion
gcloud sql databases create verificacion_db --instance=monoliticas-verificacion-db

# Crear base de datos en la instancia de ingesta
gcloud sql databases create ingesta_db --instance=monoliticas-ingesta-db
```

### 3. Inicializar la base de datos de usuarios con el esquema (Opcional)
```bash
# Crear un bucket temporal para el script SQL
gsutil mb -l us-central1 gs://monoliticas-sql-scripts

# Subir el script SQL
gsutil cp init.sql gs://monoliticas-sql-scripts/

# Importar el script a la base de datos
gcloud sql import sql monoliticas-users-db gs://monoliticas-sql-scripts/init.sql \
  --database=user_db
```

## Configuración de Kubernetes

### 1. Crear un cluster de Kubernetes
```bash
gcloud container clusters create app-no-monoliticas-cluster \
  --num-nodes=2 \
  --zone=us-central1-a \
  --machine-type=e2-standard-2 \
  --disk-size=24GB \
  --disk-type=pd-standard
```

### 2. Obtener credenciales para kubectl
```bash
gcloud container clusters get-credentials app-no-monoliticas-cluster \
  --zone=us-central1-a
```

## Configuración de cuentas de servicio y secretos

### 1. Crear una cuenta de servicio para los microservicios
```bash
# Crear la cuenta de servicio
gcloud iam service-accounts create app-no-monoliticas-sa \
  --display-name="Cloud Storage Service Account"

# Asignar roles para acceso a Cloud Storage
gcloud projects add-iam-policy-binding appnomonoliticas-452202 \
  --member="serviceAccount:app-no-monoliticas-sa@appnomonoliticas-452202.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"

# Asignar roles para acceso a Cloud SQL
gcloud projects add-iam-policy-binding appnomonoliticas-452202 \
  --member="serviceAccount:app-no-monoliticas-sa@appnomonoliticas-452202.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"
```

### 2. Crear claves para la cuenta de servicio
```bash
# Generar clave para GCP Storage
gcloud iam service-accounts keys create key.json \
  --iam-account=app-no-monoliticas-sa@appnomonoliticas-452202.iam.gserviceaccount.com
```

### 3. Crear secretos en Kubernetes con las claves
```bash
# Crear secreto para credenciales de GCP
kubectl create secret generic gcp-credentials \
  --from-file=key.json

# Crear secreto para Cloud SQL Proxy
kubectl create secret generic cloudsql-instance-credentials \
  --from-file=credentials.json=key.json
```

## Construcción y publicación de imágenes Docker

### 1. Configurar Artifact Registry
```bash
# Crear repositorio para las imágenes
gcloud artifacts repositories create app-no-monoliticas-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="Repositorio para microservicios de Aplicaciones No Monolíticas"

# Configurar autenticación para Docker
gcloud auth configure-docker us-central1-docker.pkg.dev
```

### 2. Construir y publicar imágenes de los microservicios

#### Servicio de Manejo de Usuarios
```bash
cd manejo_usuarios
docker build -t us-central1-docker.pkg.dev/appnomonoliticas-452202/app-no-monoliticas-repo/manejo-usuarios:1.0 .
docker push us-central1-docker.pkg.dev/appnomonoliticas-452202/app-no-monoliticas-repo/manejo-usuarios:1.0
```

#### Servicio de Anonimización
```bash
cd anonimizacion_imagenes
docker build -t us-central1-docker.pkg.dev/appnomonoliticas-452202/app-no-monoliticas-repo/anonimizacion:1.0 .
docker push us-central1-docker.pkg.dev/appnomonoliticas-452202/app-no-monoliticas-repo/anonimizacion:1.0
```

#### Servicio de Ingesta
```bash
cd ingesta_imagenes
docker build -t us-central1-docker.pkg.dev/appnomonoliticas-452202/app-no-monoliticas-repo/ingesta:1.0 .
docker push us-central1-docker.pkg.dev/appnomonoliticas-452202/app-no-monoliticas-repo/ingesta:1.0
```

#### BFF
```bash
cd ../bff
docker build -t us-central1-docker.pkg.dev/appnomonoliticas-452202/app-no-monoliticas-repo/bff:1.0 .
docker push us-central1-docker.pkg.dev/appnomonoliticas-452202/app-no-monoliticas-repo/bff:1.0
```

#### Servicio de Verificacion
```bash
cd ../verificacion
docker build -t us-central1-docker.pkg.dev/appnomonoliticas-452202/app-no-monoliticas-repo/verificacion:1.0 .
docker push us-central1-docker.pkg.dev/appnomonoliticas-452202/app-no-monoliticas-repo/verificacion:1.0
```

#### Servicio Saga
```bash
cd ../saga_log
docker build -t us-central1-docker.pkg.dev/appnomonoliticas-452202/app-no-monoliticas-repo/saga:2.0 .
docker push us-central1-docker.pkg.dev/appnomonoliticas-452202/app-no-monoliticas-repo/saga:1.0
```

#### Servicio de Pulsar
```bash
cd ..
# Usar imagen oficial de Apache Pulsar
# No es necesario construir
```


## Despliegue de microservicios

### 1. Desplegar Apache Pulsar
```bash
kubectl apply -f deployment/pulsar-deployment.yaml
```

### 2. Desplegar servicio de Manejo de Usuarios
```bash
kubectl apply -f deployment/manejo-usuarios-deployment.yaml
```

### 3. Desplegar servicio de Anonimización
```bash
kubectl apply -f deployment/anonimizacion-deployment.yaml
```

### 4. Desplegar servicio de Ingesta
```bash
kubectl apply -f deployment/ingesta-deployment.yaml
```

### 4. Desplegar servicio de Verificacion
```bash
kubectl apply -f deployment/verificacion-deployment.yaml
```

### 5. Desplegar BFF
```bash
kubectl apply -f deployment/bff-deployment.yaml
```

### 5. Desplegar Saga
```bash
kubectl apply -f deployment/saga-deployment.yaml
```

## Configuración del Ingress

### 1. Crear y aplicar configuración de Ingress
```bash
kubectl apply -f deployment/ingress.yaml
```

### 2. Obtener la IP del Ingress
```bash
kubectl get ingress gateway-ingress
```

## Monitoreo y alertas

### 1. Configurar alertas de presupuesto (Opcional)
```bash
# Crear un topic para alertas de presupuesto
gcloud pubsub topics create budget-alerts

# Configurar alerta de presupuesto
gcloud billing budgets create \
  --billing-account=[ID_CUENTA_FACTURACIÓN] \
  --display-name="AppNoMonoliticas Budget Alert" \
  --budget-amount=100USD \
  --threshold-rule=percent=80,basis=current-spend \
  --threshold-rule=percent=100,basis=current-spend \
  --notifications-rule-pubsub-topic=projects/appnomonoliticas-452202/topics/budget-alerts \
  --email-recipients=[CORREO_ELECTRÓNICO]
```

### 2. Habilitar Cloud Monitoring (Opcional)
```bash
gcloud container clusters update app-no-monoliticas-cluster \
  --enable-stackdriver-kubernetes \
  --zone=us-central1-a
```

## Resolución de problemas

### Verificar estado de los pods
```bash
kubectl get pods
```

### Ver logs de un pod específico
```bash
kubectl logs [nombre-del-pod]
```

### Ver logs de un contenedor específico en un pod
```bash
kubectl logs [nombre-del-pod] -c [nombre-del-contenedor]
```

### Verificar eventos del cluster
```bash
kubectl get events
```

### Ingresar a pod

```bash
kubectl exec -it <pod-name> -- /bin/sh
```

```bash
kubectl exec -it saga-786746666-pmfpf -- /bin/sh
```

```bash
kubectl exec -it pulsar-f76b4f45c-wtmvw -- /bin/sh
```

scp saga_logs.db .   

```bash
kubectl cp <pod-name>:<path-to-file-in-pod> <path-on-local-machine>
```
```bash
kubectl cp saga-786746666-pmfpf:saga_logs.db ./saga_logs.db
```

### Problemas de conexión con Cloud SQL
Si aparecen errores de conexión a la base de datos, verificar:
1. El estado del contenedor cloud-sql-proxy
2. Las credenciales están correctamente montadas
3. El nombre de la instancia de Cloud SQL es correcto

### Problemas con Pulsar
Si Pulsar muestra errores de conexión o no inicia correctamente:
1. Verificar si hay suficientes recursos en el cluster
2. Reiniciar el pod de Pulsar
3. Considerar una configuración más básica con menos componentes habilitados

---

## Autor
Robert Castro

