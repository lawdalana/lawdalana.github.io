---
title : Docker and Docker Compose
notetype : feed
date : 01-02-2025
---


## Docker คืออะไร 
![Docker](https://diagrams.mingrammer.com/img/resources/onprem/container/docker.png)
- **Docker** เป็นแพลตฟอร์มสำหรับการสร้าง จัดการ และรัน **Container** ซึ่งเป็นเหมือนกล่องเล็ก ๆ ที่บรรจุแอปพลิเคชันและ dependencies (เช่น ไลบรารี, ระบบปฏิบัติการขั้นต่ำ ฯลฯ) เอาไว้
- ข้อดีหลักของการใช้ Container คือทำให้การติดตั้งและจัดการแอปพลิเคชันสะดวกขึ้น เพราะทุกอย่างรวมอยู่ใน Container เดียว ลดปัญหา “เครื่องฉันรันได้ ทำไมเครื่องเธอรันไม่ได้”
- Docker ใช้ **Docker Engine** ในการรัน Container และใช้ **Dockerfile** สำหรับสร้าง Image

### Docker ต่างอะไรกับ VM
- VM จำลองระบบฮาร์ดแวร์และรัน OS เต็มรูปแบบ ทำให้มีการใช้ทรัพยากรมากขึ้นและมีเวลาบูตช้ากว่า แต่ให้การแยกส่วนและความปลอดภัยที่สูง
- Docker ใช้ containerization โดยแชร์ kernel ของ host ทำให้มีน้ำหนักเบา ใช้ทรัพยากรน้อยกว่าและบูตได้เร็วกว่า แต่มีระดับการแยกส่วนที่ต่ำกว่าในบางแง่มุม

[![Container Vs VMs](/assets/img/Other/Docker/vm-docker5.avif)](https://dockerlabs.collabnix.com/beginners/difference-docker-vm.html)

### Note
```
- ถ้า Host OS เป็น Linux: Docker container ใช้ kernel ของ host OS โดยตรง
- ถ้า Host OS เป็น Windows หรือ macOS: สำหรับ Linux containers Docker Desktop จะใช้ Linux kernel ที่อยู่ใน lightweight VM ซึ่งถูกจัดสรรมาให้โดย Docker Desktop แต่สำหรับ Windows containers (บน Windows) ก็จะใช้ kernel ของ Windows โดยตรง
```

### คำศัพท์ที่ควรรู้
1. **Image**: แม่แบบ (Template) สำหรับสร้าง Container
2. **Container**: อินสแตนซ์ที่เกิดจาก Image เมื่อทำงานจริง
3. **Registry**: ที่เก็บ Image ส่วนกลาง เช่น Docker Hub หรือ Registry ภายในองค์กร


### Exmaple Command
#### Pre-Require
- Install [Docker Engine](https://docs.docker.com/engine/install/) ถ้าใช้ Linux
- Install [Docker Desktop](https://docs.docker.com/desktop/), [Rancher Desktop](https://rancherdesktop.io/) ถ้าใช้ Window, Mac

#### Simaple Command
```bash
docker build -t {image_name}:{tag} .        # Build local image

docker run {image_name}:{tag}               # Run containers
docker run -p 8080:80 {image_name}:{tag}    # Run containers with mapping port to our host

docker stop my_container                    # Stop container but still have status `stopped`
docker rm my_container                      # Remove container but have to stop first
docker rm -f my_container                   # Force remove container

docker ps                                   # List running containers
docker ps -a                                # List running and stopped containers

docker pull {image_name}:{tag}              # Pull from docker hub
docker push {image_name}:{tag}              # Psuh image from local to repository

docker images ls                            # List downloaded images
docker images prune                         # Remove dangling images ซึ่งคือ Docker images ที่ไม่ได้ถูกใช้งานหรือไม่มี tag

docker exec -it {container} {/bin/bash}     # Shell inside container

docker save -o my_image.tar my_image:latest # Save docker image as a file
docker load -i my_image.tar                 # Load docker image
```

[![Container Vs VMs](/assets/img/Other/Docker/dockercheatsheet8.avif)](https://dockerlabs.collabnix.com/docker/cheatsheet/)


#### Exmaple 1:
ลองรัน docker image
```bash
docker run hello-world

# Docker จะ pull image hello-world จาก docker hub
# หลังจาก pull image มาแล้ว docker จะรัน image ตัวนั้นทันที
```
---

#### Exmaple 2:
Step
1. สร้าง project folder และใช้เป็นที่เก็บไฟล์ทั้งหมด
2. สร้าง python file (`example.py`)
    ```python
    print("test python image file")
    ```
3. สร้างไฟล์ ชื่อ `Dockerfile` (ไม่ต้องมีนามสกุล)
    ```
    From python:3.12.8-slim

    WORKDIR /usr/src/app

    COPY requirements.txt ./
    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    CMD [ "python", "./example.py" ]
    ```
    Note ([Python docker hub](https://hub.docker.com/_/python/tags)): 
    - `alpine` = ใช้ Alpine Linux เป็น base image ที่มีขนาดเล็ก เบา และมีเพียงแพ็คเกจที่จำเป็นเท่านั้น
    - `slim` = เป็น variant ที่ตัดส่วนที่ไม่จำเป็นออกจาก image ปกติ มีขนาดเล็กลง
    - `bullseye` = เป็นชื่อรหัสของ Debian 11 (Bullseye) ซึ่งเป็นระบบปฏิบัติการที่เสถียรและมีแพ็คเกจครบครัน
    - `bookworm` =  เป็นชื่อรหัสของ Debian รุ่นใหม่กว่า (ในขณะนี้คือ Debian Bookworm ซึ่งอาจอยู่ในช่วง testing หรือ release ใหม่)
4. รันคำสั่ง
    ```
    docker build -t example:1.0.0 .
    docker run -it --rm example:1.0.0
    ```

## Docker Compose คืออะไร
- **Docker Compose** เป็นเครื่องมือสำหรับจัดการ **Multi-Container** ในการพัฒนาแอปพลิเคชันที่ต้องมีหลาย Service ทำงานร่วมกัน เช่น แอปพลิเคชัน python คุยกับฐานข้อมูล MySQL หรือ Redis
- ใช้ไฟล์ `docker-compose.yml` ในการกำหนดว่าเราต้องการรันคอนเทนเนอร์อะไรบ้าง แต่ละคอนเทนเนอร์เชื่อมต่อกันอย่างไร และมี Volume หรือ Port mapping อย่างไร

### Exmaple Command
#### Pre-Require
- Install [Docker Engine](https://docs.docker.com/engine/install/) ถ้าใช้ Linux
- Install [Docker Desktop](https://docs.docker.com/desktop/), [Rancher Desktop](https://rancherdesktop.io/) ถ้าใช้ Window, Mac
- Install [Docker Compose](https://docs.docker.com/compose/install/) / มี [version stand alone](https://docs.docker.com/compose/install/standalone/) `docker-compose`

#### Simaple Command
```bash
docker-compose up                                       # Build local image
docker-compose up {service_name1} {service_name2} ...   # Start the follow service name container 
docker-compose up --build                               # Build image but use the old conatainer
docker-compose up --build --force-recreate              # Build local image

docker-compose --profile db up                          # Start

docker-compose down                                     # Delete container and network
docker-compose down -v                                  # Delete container, network and volumes
```

#### Note กรณีที่เจอบ่อย
```
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt  # 🔥
COPY . .  # <-- เพิ่มบรรทัดนี้ทีหลัง
CMD ["python", "app.py"]
```
Command: `docker-compose up --build`
- ถ้า requirements.txt เปลี่ยน → pip install -r requirements.txt จะทำงานใหม่
- ถ้า requirements.txt ไม่เปลี่ยน → pip install จะใช้ cache และไม่รันใหม่
- ถ้าคุณแก้ Dockerfile แต่มันอยู่หลังคำสั่ง pip install → pip install จะใช้ cache และไม่รันใหม่
- ถ้าต้องการให้ pip install ทำงานใหม่เสมอ → ใช้ rm -rf /root/.cache/pip หรือ BuildKit cache

