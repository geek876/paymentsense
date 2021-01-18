### Application
- See **application** directory
- Using Python's Flask framework and `requests` library.
- The code requests the first page and then iterates over the `total_pages` variable to get `all products`
- The code uses simple `html template` to render the `products` as a table
- Working example is here http://paymentsense.designlinks.net 

### Infrastructure
- A 3 Node GKE cluster.
- Infrastructure code is in `terraform` under **terraform** directory. Currently ran manually but could be part of **CI/CD**
- Ingress is achieved via `gce` ingress controller enabled within the cluster.
- The external IP of the LoadBalancer (Ingress) is mapped to **A** record **paymentsense.designlinks.net**

### Deployment
- Deployment via HELM
- HELM chart under **helm** directory

### CI/CD
- `cloudbuild` workflow is automatically trigged on `push` to `master`
- `push to master -> cloudbuild -> pull latest image for docker caching -> build docker container -> push docker container -> deploy`
- For all other branches `i.e. non master`, `push to branch -> cloudbuild -> tests` 
- Once deployed to **an environment (ex: dev)**, the same docker image can be pushed to higher environments `dev -> qa -> canary -> prod`
- Use something like `mergeable` to control which branches can be merged to `master` (ex: minium reviewers, tests passed etc)

### AutoScaling
- Can be achieved via:
- **Enabling Cluster Autoscaler**: Enabling `autoscaling` on the **node-pool**. This will add/remove nodes depending on the workload/requests.
```
gcloud container clusters update <my-cluster> \
    --enable-autoscaling \
    --min-nodes 1 \ 
    --max-nodes 10 \ 
    --zone <zone> \
    --node-pool <node-pool>
```
- **Enabling Vertical Pod Autoscaler**: This will automatically adjust `cpu/memory limits/requests`. To start with, may be start with `updateMode: off` to simply get recommendations
```
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: my-rec-vpa
spec:
  targetRef:
    apiVersion: "apps/v1"
    kind:       Deployment
    name:       test-vertical-autoscaler
  updatePolicy:
    updateMode: "Off"
```