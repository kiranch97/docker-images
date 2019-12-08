# Object Detection Kit

The Object Detection Kit is a easy way to start captering frames, detecting objects on them and finally mapping them. Everything works out-of-the-box, so no special setup is needed.

ODK (Object Detection Kit) is a project by the Municipality of Amsterdam CTO tech team. For more information about the project check [odk.ai]().

## Content

This stack contains all the elements of the ODK project: 

- **ODK App**: Vue JS PWA for streaming frames to be analyzed

- **ODK Dashboard**: Vue JS showing incoming frames real-time and analyzed data on an map

- **ODK Frame Analyzer**: Machine Learning Worker analyzing frames

- **ODK API**: Handles streams of ODK App via websockets, utilizes:
	- PostgreSQL database for storing analyzed data
	- RabbitMQ message broker 

## Getting started

To get the whole stack up and running quickly follow these steps. To run/debug each element seperately, see the README file in their respective folders.

### Requirements

- Docker
- Node (tested with v12.2.0)
- NPM
- Python (v3.7)
- CUDA Toolkit (optional)

### Setup

Build ODK App:
```
$ cd odk-app
$ npm install
$ npm run build
``` 

Setup virtual environment for Frame Analyzer:
```
$ cd odk-frame-analyzer
$ python3 -m venv venv
$ source venv/bin/active
(venv) $ pip install -r requirements.txt
```

Download the model for detecting garbage:
```
$ cd odk-frame-analyzer/model/weights
$ cat download_link.txt | xargs -L 1 wget
```

### Run

Start Frame Analyzer:
```
$ cd odk-frame-analyzer
$ source venv/bin/active
(venv) $ python MlWorker.py
```

Run docker-compose (dev file) to starts the App, Dashboard, API, PostgreSQL database and RabbitMQ broker:
```
$ docker-compose -f docker-compose.dev.yml up -d
```

Visit [localhost:8000]() to open the ODK App.

Visit [localhost:8001]() for the ODK Dashboard.
