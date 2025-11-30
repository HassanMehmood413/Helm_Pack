# 🚀 Helm Chart

This Helm chart deploys your FastAPI application with PostgreSQL database.

## 📦 What's Included

### Application (FastAPI)
- **Deployment**: Your Python FastAPI app
- **Service**: ClusterIP/NodePort/LoadBalancer
- **ConfigMap**: Environment configuration
- **Autoscaling**: (Optional) HPA for production

### PostgreSQL Database
- **Deployment**: PostgreSQL 16 Alpine
- **Service**: Internal ClusterIP
- **ConfigMap**: Database credentials
- **PVC**: Persistent storage

---

## 🎯 Quick Start

### 1. Install for Development

```bash
cd d:/Anaconda/kubernets/side_project_03_Helm/proj_01

# Install to dev namespace
helm install dev-proj01 ./proj_01_helm \
  -f ./proj_01_helm/values-dev.yaml \
  -n dev-proj01 \
  --create-namespace

# Check status
kubectl get all -n dev-proj01
```

### 2. Install for Production

```bash
# Install to prod namespace
helm install prod-proj01 ./proj_01_helm \
  -f ./proj_01_helm/values-prod.yaml \
  -n prod-proj01 \
  --create-namespace

# Check status
kubectl get all -n prod-proj01
```

---

## 📋 Chart Structure

```
proj_01_helm/
├── Chart.yaml                      # Chart metadata
├── values.yaml                     # Default values
├── values-dev.yaml                 # Development overrides
├── values-prod.yaml                # Production overrides
└── templates/
    ├── deployment.yaml             # App deployment
    ├── service.yaml                # App service
    ├── postgres-configmap.yaml     # PostgreSQL config
    ├── postgres-deployment.yaml    # PostgreSQL deployment
    ├── postgres-service.yaml       # PostgreSQL service
    ├── postgres-pvc.yaml           # PostgreSQL storage
    ├── serviceaccount.yaml         # Service account
    ├── hpa.yaml                    # Autoscaling (optional)
    └── ingress.yaml                # Ingress (optional)
```

---

## ⚙️ Configuration

### Application Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of app pods | `2` |
| `image.repository` | App image repository | `hm413/helm-proj01` |
| `image.tag` | App image tag | `0.1.1` |
| `service.type` | Service type | `ClusterIP` |
| `service.port` | Service port | `8080` |
| `service.targetPort` | Container port | `8000` |
| `env.databaseUrl` | Database connection string | `postgresql://...` |

### PostgreSQL Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `postgresql.enabled` | Enable PostgreSQL | `true` |
| `postgresql.image.tag` | PostgreSQL version | `16-alpine` |
| `postgresql.auth.database` | Database name | `proj2_db` |
| `postgresql.auth.username` | Database user | `postgres` |
| `postgresql.auth.password` | Database password | `postgres123` |
| `postgresql.persistence.size` | PVC size | `1Gi` |

---

## 🛠️ Common Commands

### Install/Upgrade

```bash
# Install new release
helm install <release-name> ./proj_01_helm -f values-dev.yaml -n <namespace>

# Upgrade existing release
helm upgrade <release-name> ./proj_01_helm -f values-dev.yaml -n <namespace>

# Install or upgrade (idempotent)
helm upgrade --install <release-name> ./proj_01_helm -f values-dev.yaml -n <namespace>
```

### Testing & Debugging

```bash
# Validate chart syntax
helm lint ./proj_01_helm

# Render templates (dry run)
helm template proj01 ./proj_01_helm -f values-dev.yaml

# Install with dry-run
helm install proj01 ./proj_01_helm -f values-dev.yaml --dry-run --debug
```

### Managing Releases

```bash
# List all releases
helm list --all-namespaces

# Get release status
helm status <release-name> -n <namespace>

# Get release values
helm get values <release-name> -n <namespace>

# Rollback to previous version
helm rollback <release-name> -n <namespace>

# Uninstall release
helm uninstall <release-name> -n <namespace>
```

### Accessing Your Application

```bash
# Development (NodePort)
kubectl get svc -n dev-proj01
# Access via: http://<node-ip>:<nodeport>

# Production (LoadBalancer)
kubectl get svc -n prod-proj01
# Access via: http://<external-ip>:8080

# Port-forward (any environment)
kubectl port-forward svc/proj-2 8080:8080 -n <namespace>
# Access via: http://localhost:8080
```

---

## 🔧 Customization Examples

### Override Image Tag

```bash
helm install dev ./proj_01_helm \
  --set image.tag=0.2.0 \
  -n dev
```

### Disable PostgreSQL (use external DB)

```bash
helm install prod ./proj_01_helm \
  --set postgresql.enabled=false \
  --set env.databaseUrl="postgresql://external-db:5432/mydb" \
  -n prod
```

### Change Replicas

```bash
helm upgrade prod ./proj_01_helm \
  --set replicaCount=5 \
  -n prod
```

---

## 📊 Comparison with Raw Manifests

### Before (Raw Manifests)

```bash
kubectl apply -f manifest/namespace.yml
kubectl apply -f manifest/postgres/ConfigMap.yml
kubectl apply -f manifest/postgres/pvc.yml
kubectl apply -f manifest/postgres/Deployment.yml
kubectl apply -f manifest/postgres/Service.yml
kubectl apply -f manifest/deployment.yml
kubectl apply -f manifest/service.yml
```

**Problem**: Same configuration for dev and prod!

### After (Helm)

```bash
# Deploy to dev
helm install dev ./proj_01_helm -f values-dev.yaml -n dev

# Deploy to prod (different config!)
helm install prod ./proj_01_helm -f values-prod.yaml -n prod
```

**Benefits**:
- ✅ Different configurations per environment
- ✅ Easy version management
- ✅ Simple rollback
- ✅ Parameterized deployments

---

## 🎯 Environment Differences

| Feature | Development | Production |
|---------|-------------|------------|
| **Replicas** | 1 | 3 |
| **Image Tag** | `dev-latest` | `0.1.1` (fixed) |
| **Service Type** | NodePort | LoadBalancer |
| **CPU Limit** | 200m | 1000m |
| **Memory Limit** | 256Mi | 1Gi |
| **Autoscaling** | Disabled | Enabled (3-10 pods) |
| **PG Storage** | 500Mi | 5Gi |

---

## 🚨 Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods -n <namespace>

# View pod logs
kubectl logs <pod-name> -n <namespace>

# Describe pod for events
kubectl describe pod <pod-name> -n <namespace>
```

### Database Connection Issues

```bash
# Check PostgreSQL pod
kubectl logs postgres-<pod-id> -n <namespace>

# Test connection from app pod
kubectl exec -it <app-pod> -n <namespace> -- env | grep DATABASE_URL
```

### Service Not Accessible

```bash
# Check service
kubectl get svc -n <namespace>

# Check endpoints
kubectl get endpoints -n <namespace>
```

---

## 📚 Next Steps

1. **Add Ingress**: Configure ingress for external access
2. **Add Secrets**: Move database credentials to Kubernetes secrets
3. **Add Monitoring**: Integrate Prometheus/Grafana
4. **CI/CD**: Automate deployments with GitHub Actions
5. **Backup**: Set up database backup strategy

---

## 🎓 Learning Resources

- [Helm Documentation](https://helm.sh/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Best Practices Guide](../helm/HELM_GUIDE.md)

---

## 📝 Notes

- **Never use `latest` tag in production!** Always pin to specific versions
- **Store secrets securely**: Don't hardcode passwords in values.yaml
- **Test in dev first**: Always test changes in dev before deploying to prod
- **Monitor resources**: Keep an eye on CPU/memory usage

---

Made with ❤️ for learning Kubernetes and Helm!
