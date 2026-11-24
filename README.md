# Kubernetes Learning

## Block 1: Kubernetes microservices demo

The demo in [`msa-demo/`](./msa-demo/) contains three FastAPI services: a GraphQL
gateway, a user service, and an order service.

```text
Client --GraphQL--> gateway Service --> user-service (2 pods)
                                 \----> order-service (2 pods)
```

The gateway exposes one GraphQL endpoint and fetches data from the two
independent REST services. Kubernetes Deployments manage the pods, and Services
provide stable in-cluster names and load-balancing.

| What we did | Concept | Exam point |
| --- | --- | --- |
| Wrote three FastAPI services | Microservices | Each service has its own code, deployment, and scaling |
| Wrote a Dockerfile | Containerization | A Dockerfile specifies a base image, files, dependencies, exposed port, and run command |
| Ran `docker build` | Image creation | An image is a read-only template made of layers |
| Ran `kind create cluster` | Local Kubernetes cluster | Kubernetes has a control plane and worker nodes; kind runs cluster nodes in Docker |
| Ran `kind load docker-image` | Image availability | For a remote cluster, push to a registry and let the cluster pull the image |
| Ran `kubectl apply -f app.yaml` | Declarative deployment | Describe the desired state; Kubernetes works to make it true |
| Set `replicas: 2` in a Deployment | Replication and self-healing | A ReplicaSet keeps the requested number of pods running |
| Created a Service | Stable networking | Pods can get new IPs; a Service provides stable DNS and load-balances to selected pods |
| Added a `readinessProbe` | Health checking | Traffic is sent only to pods that are ready |
| Added Strawberry to the gateway | GraphQL integration | Clients request specific fields; the gateway aggregates service data |
| Scaled a Deployment and deleted a pod | Scaling and self-healing | Kubernetes creates replacement pods to match the desired replica count |
| Added a GitHub Actions workflow | CI/CD | A pipeline can automate image builds and publishing |

### Docker commands

| Command | Purpose |
| --- | --- |
| `docker build -t name:tag .` | Build an image from the current directory |
| `docker images` | List images |
| `docker run -d -p 8000:8000 name:tag` | Run a container in the background and map a host port |
| `docker ps` / `docker ps -a` | List running / all containers |
| `docker logs <id>` | View container logs |
| `docker exec -it <id> sh` | Open a shell inside a container |
| `docker stop <id>` / `docker rm <id>` / `docker rmi <image>` | Stop or remove a container, or remove an image |
| `docker login` / `docker tag` / `docker push` | Log in, tag, and publish an image to a registry |

### Kubernetes commands

| Command | Purpose |
| --- | --- |
| `kubectl apply -f file.yaml` | Create or update resources from a manifest |
| `kubectl get pods` / `svc` / `deploy` / `nodes` | List resources (add `-o wide` to show additional details, such as IPs) |
| `kubectl describe pod <name>` | Inspect a pod and its events; useful for debugging |
| `kubectl logs <pod>` | View pod logs |
| `kubectl exec -it <pod> -- sh` | Open a shell inside a pod |
| `kubectl scale deploy <name> --replicas=4` | Manually scale a Deployment |
| `kubectl set image deploy/<name> <container>=<image>:<tag>` | Change a Deployment's image and start a rolling update |
| `kubectl rollout status deploy/<name>` | Watch a rollout |
| `kubectl rollout undo deploy/<name>` | Roll back a Deployment |
| `kubectl delete -f file.yaml` / `kubectl delete pod <name>` | Delete resources or a pod |
| `kubectl port-forward svc/<name> 8000:8000` | Forward a local port to a Service |
| `kubectl get all` | List common resources in the current namespace |

### Kubernetes architecture

| Component | Role |
| --- | --- |
| API Server | Entry point for `kubectl` and other Kubernetes API clients |
| etcd | Key-value store containing cluster state |
| Scheduler | Chooses a node for each newly scheduled pod |
| Controller Manager | Runs controllers that reconcile actual state with desired state |
| kubelet | Node agent that makes sure the node's pods are running |
| kube-proxy | Maintains networking rules used by Services (depending on cluster configuration) |
| Container runtime | Runs containers, for example containerd |

### Service types

| Type | Reachable from |
| --- | --- |
| `ClusterIP` (default) | Inside the cluster |
| `NodePort` | Through a node IP and a port, typically in the `30000`-`32767` range |
| `LoadBalancer` | Through an external load balancer, when supported by the environment |

### Other Kubernetes objects

| Object | Purpose |
| --- | --- |
| Namespace | Logical isolation and grouping within a cluster |
| ConfigMap | Non-sensitive configuration, such as environment variables |
| Secret | Sensitive values, such as passwords or API keys; use a secure secret-management approach for real workloads |
| Ingress | HTTP routing to Services, such as routing `/users` to the user service; requires an Ingress controller |
| HPA (Horizontal Pod Autoscaler) | Adjusts pod replica counts based on metrics such as CPU or memory |
| Rolling update | Gradually replaces old pods with new ones to help keep an application available during updates |

### GraphQL vs. REST

| | REST | GraphQL |
| --- | --- | --- |
| Endpoints | Often multiple endpoints, such as `/users` and `/orders` | Commonly one endpoint, such as `/graphql` |
| Over-fetching | Clients may receive more data than needed | Clients select the fields they need |
| Multiple resources | May require several requests | Can request related data in one query |
| Microservices | Each service can expose REST endpoints | A gateway can aggregate services behind one schema |

### CI/CD for microservices

A typical flow is: push to Git, test, build an image for each service, push
images to a registry, deploy the new images, and monitor the rollout. Separate
service pipelines can allow one service to be deployed without rebuilding or
releasing the others.

The workflow in this demo builds and pushes service images. Its deploy job
currently prints an example `kubectl set image` command; it does not apply a
deployment itself. A production pipeline should also configure registry
credentials and a secure way for its deployment job to access the cluster.

## Five-minute practice

### Rolling update and rollback

```sh
kubectl rollout restart deploy/order-service
kubectl rollout history deploy/order-service
kubectl rollout undo deploy/order-service
```

### ConfigMap and Secret

```sh
kubectl create configmap app-config --from-literal=ENV=dev
kubectl create secret generic db-secret --from-literal=password=abc123
kubectl get configmap,secret
```

The password above is only a disposable example for a local learning cluster.
Do not use real credentials in command-line arguments, shell history, or
committed manifests.

### Autoscaling

```sh
kubectl autoscale deploy order-service --cpu-percent=50 --min=2 --max=5
```

This creates an HPA, but it will not scale without a working metrics API. A
default kind cluster does not include metrics-server.

