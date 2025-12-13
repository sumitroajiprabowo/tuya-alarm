# Kubernetes Manifests for Tuya Alarm Control API

This directory contains Kubernetes manifests for deploying the Tuya Alarm Control API to a k3s cluster using ArgoCD.

## Directory Structure

```
k8s/
├── argocd/                          # ArgoCD Application manifests
│   ├── application-development.yaml
│   ├── application-staging.yaml
│   └── application-production.yaml
├── base/                            # Base Kubernetes resources
│   ├── deployment.yaml              # Main application deployment
│   ├── service.yaml                 # ClusterIP service
│   ├── secret-template.yaml         # Secret template (DO NOT use as-is)
│   └── kustomization.yaml           # Base kustomization configuration
├── overlays/                        # Environment-specific customizations
│   ├── development/
│   │   └── kustomization.yaml
│   ├── staging/
│   │   └── kustomization.yaml
│   └── production/
│       └── kustomization.yaml
└── README.md                        # This file
```

## Prerequisites

1. **k3s cluster** - A running k3s cluster
2. **ArgoCD** - Installed and configured in your cluster
3. **Secrets** - Tuya API credentials stored in Kubernetes secrets

## Setting Up Secrets

Before deploying, you need to create secrets for each environment. You can use the `secret-template.yaml` as a reference.

### Option 1: Using kubectl (Not Recommended for Production)

```bash
# For development
kubectl create secret generic tuya-alarm-secrets \
  --namespace=development \
  --from-literal=tuya-access-id='YOUR_ACCESS_ID' \
  --from-literal=tuya-access-secret='YOUR_ACCESS_SECRET' \
  --from-literal=tuya-endpoint='https://openapi-sg.iotbing.com'

# For staging
kubectl create secret generic tuya-alarm-secrets \
  --namespace=staging \
  --from-literal=tuya-access-id='YOUR_ACCESS_ID' \
  --from-literal=tuya-access-secret='YOUR_ACCESS_SECRET' \
  --from-literal=tuya-endpoint='https://openapi-sg.iotbing.com'

# For production
kubectl create secret generic tuya-alarm-secrets \
  --namespace=production \
  --from-literal=tuya-access-id='YOUR_ACCESS_ID' \
  --from-literal=tuya-access-secret='YOUR_ACCESS_SECRET' \
  --from-literal=tuya-endpoint='https://openapi-sg.iotbing.com'
```

### Option 2: Using Sealed Secrets (Recommended)

```bash
# Install sealed-secrets controller
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/controller.yaml

# Create sealed secret
echo -n 'YOUR_ACCESS_ID' | kubectl create secret generic tuya-alarm-secrets \
  --dry-run=client \
  --from-file=tuya-access-id=/dev/stdin \
  -o yaml | \
  kubeseal -o yaml > sealed-secret.yaml

# Apply sealed secret
kubectl apply -f sealed-secret.yaml -n production
```

### Option 3: Using External Secrets Operator

For production environments, consider using External Secrets Operator to sync secrets from external secret stores like:
- AWS Secrets Manager
- Azure Key Vault
- HashiCorp Vault
- Google Secret Manager

## Deploying with ArgoCD

### 1. Apply ArgoCD Applications

```bash
# Deploy to development
kubectl apply -f k8s/argocd/application-development.yaml

# Deploy to staging
kubectl apply -f k8s/argocd/application-staging.yaml

# Deploy to production
kubectl apply -f k8s/argocd/application-production.yaml
```

### 2. Access ArgoCD UI

```bash
# Port forward to ArgoCD server
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

Navigate to `https://localhost:8080` and login with:
- Username: `admin`
- Password: (from command above)

### 3. Sync Applications

**Development & Staging:**
These environments are configured for automatic sync with self-healing enabled.

**Production:**
Production requires manual sync for safety. You can sync via:

```bash
# Using ArgoCD CLI
argocd app sync tuya-alarm-production

# Or using kubectl
kubectl patch application tuya-alarm-production \
  -n argocd \
  --type merge \
  -p '{"operation":{"initiatedBy":{"username":"admin"},"sync":{"revision":"main"}}}'
```

## Environment Configuration

### Development
- **Branch:** `develop`
- **Namespace:** `development`
- **Replicas:** 1
- **Auto-sync:** Enabled
- **Self-heal:** Enabled
- **Resources:**
  - Limits: 256Mi memory, 500m CPU
  - Requests: 128Mi memory, 100m CPU

### Staging
- **Branch:** `staging`
- **Namespace:** `staging`
- **Replicas:** 1
- **Auto-sync:** Enabled
- **Self-heal:** Enabled
- **Resources:**
  - Limits: 384Mi memory, 500m CPU
  - Requests: 192Mi memory, 150m CPU

### Production
- **Branch:** `main`
- **Namespace:** `production`
- **Replicas:** 1
- **Auto-sync:** Disabled (Manual sync required)
- **Self-heal:** Disabled
- **Resources:**
  - Limits: 512Mi memory, 500m CPU
  - Requests: 256Mi memory, 200m CPU

## Testing Deployment

After deployment, verify the application is running:

```bash
# Check pods
kubectl get pods -n production

# Check service
kubectl get svc -n production

# Test the health endpoint
kubectl port-forward svc/tuya-alarm-service -n production 5000:5000

# In another terminal
curl http://localhost:5000/health
```

## CI/CD Integration

The GitHub Actions workflow (`.github/workflows/tests.yml`) automatically:
1. Builds and pushes Docker images on push to main
2. Tags images with short SHA (e.g., `sha-abc1234`)
3. Updates `k8s/overlays/production/kustomization.yaml` with the new image tag
4. Commits and pushes the update to trigger ArgoCD sync

## Troubleshooting

### Application not syncing
```bash
# Check ArgoCD application status
argocd app get tuya-alarm-production

# View sync status
kubectl get application tuya-alarm-production -n argocd -o yaml
```

### Pod not starting
```bash
# Check pod logs
kubectl logs -n production -l app=tuya-alarm

# Describe pod
kubectl describe pod -n production -l app=tuya-alarm
```

### Secret issues
```bash
# Verify secret exists
kubectl get secret tuya-alarm-secrets -n production

# Check secret content (be careful!)
kubectl get secret tuya-alarm-secrets -n production -o yaml
```

## Cleaning Up

To remove the deployment:

```bash
# Delete ArgoCD application (this will also delete all resources)
kubectl delete application tuya-alarm-production -n argocd

# Or delete resources directly
kubectl delete -k k8s/overlays/production
```

## Additional Resources

- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [Kustomize Documentation](https://kustomize.io/)
- [k3s Documentation](https://docs.k3s.io/)
- [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets)