# WIP

# How to Run?

All you need is to have Docker installed on your machine. Then, you can build and run the application using the following commands (make sure you are in the root directory of the project):

```bash
docker build -t tasks-app:py3.13 .
```
```bash
docker run --rm -p 8000:8000 --name tasks-app tasks-app:py3.13
```
