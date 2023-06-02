## Simple python application in minikube
<sub>Only for local running purposes</sub>

Tested on `macOS Monterey, verion: 12.6.5 (21G531), Intel`

Requirements:
- [homebrew](https://brew.sh/)
- [Docker Desktop](https://docs.docker.com/desktop/install/mac-install/) - v4.19.0 (106363)
- [minikube](https://minikube.sigs.k8s.io/docs/start/) - v1.30.1
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/) - client version: v1.25.9
- [helm](https://helm.sh/docs/intro/install/) - v3.12.0


### 1. Build and deploy application
```
# Start minikube
minikube start

# Check minikube up and running
kubectl get nodes

# Set docker env
eval $(minikube docker-env) 

# Build image
cd app/
docker build -t demo-app:0.0.1 .

# Run in minikube
kubectl run demo-app --image=demo-app:0.0.1 --image-pull-policy=Never

# Check pod up and running
kubectl get pods

# Cleaning test pod
kubectl delete pods/demo-app

# Apply application manifests
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

Add ingress addon to expose network traffic outside of the minikube. This is the main difference between running minikube on linux and on the mac: on linux the ingress controller gets expose under its own IP `minikube ip`. Since the docker bridge behaves differently on the mac the ingress controller listens on localhost and needs to be tunneled to, by running `minikube tunnel` in a separate terminal.

```
# Enable ingress addon
minikube addons enable ingress

# Verify
kubectl get pods -n ingress-nginx

# Apply ingress manifest
kubectl apply -f ingress.yaml
```

### 2. Add monitoring stack.

```
# Install prometheus and grafana
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts

helm install prometheus prometheus-community/prometheus
helm install demo grafana/grafana
```

### 3. Expose traffic outside of minikube

```
minikube tunnel

# Add this line to /etc/hosts
127.0.0.1 app.minikube.dev grafana.minikube.dev
```

### 4. Check application
```
# From browser it needs 'https:// ' or from curl
curl https://app.minikube.dev/ --insecure
```

Output should looks like this:
```
Timestamp: 2023-06-02 14:11:29
Hostname: demo-app-deployment-6bcb968b9f-sgdnw
```
Try curl several time and you can see different Hostnames, which is name of the Pod

### 5. Check monitoring stack
```
# To use grafana it needs to use preconfigured password
kubectl get secret --namespace default demo-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

# Open browser - user: admin password:'output_from_terminal'
https://grafana.minikube.dev/
```