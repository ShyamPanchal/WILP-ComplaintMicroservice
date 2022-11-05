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
docker image build . -t complaint_service
```
or
```bash
docker build . -t complaint_service
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