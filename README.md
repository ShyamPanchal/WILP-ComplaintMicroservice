# WILP-ComplaintMicroservice
Complaint Microservice for Scalable Service for WILP M.Tech. Course

---

## To run the application

```bash
uvicorn main:app --reload
```

This will run the application on [http://localhost:8000/](http://localhost:8000/)

---

## Docs
For swagger docs visit [http://localhost:8000/docs](http://localhost:8000/docs)  
For redoc visit [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## To build docker image
```bash
docker image build . -t shyam/complaint_service
```
or
```bash
docker build . -t shyam/complaint_service
```
---

## To run image with docker on port 8001
```bash
docker container run -p 8001:80 --name complaint_service complaint_service
```
or
```bash
docker run -p 8001:80 --name complaint_service complaint_service
```
---

## Docker application
After running docker container run command, the application will be running on [http://localhost:8001/](http://localhost:8001/)

---

## To deploy on Kubernetes

```bash
minikube start --nodes 2
minikube dashboard

eval $(minikube docker-env)

kubectl apply -f complaint-service.yaml
kubectl create deployment complaint-service --image=registry.k8s.io/echoserver:1.4

kubectl expose deployment complaint-service --type=LoadBalancer --port=8001

minikube service complaint-service     
```