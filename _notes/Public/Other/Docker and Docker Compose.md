---
title : Docker and Docker Compose
notetype : feed
date : 01-02-2025
last_modified: 2026-09-16
---


## Docker คืออะไร 
![Docker](https://diagrams.mingrammer.com/img/resources/onprem/container/docker.png)
- **Docker** เป็นแพลตฟอร์มสำหรับสร้าง จัดการ และรัน **Container** ซึ่งบรรจุแอปพลิเคชันพร้อมสิ่งที่ต้องใช้ เช่น ไลบรารีและส่วนประกอบของระบบปฏิบัติการ
- Container ช่วยให้ติดตั้งและจัดการแอปพลิเคชันได้สะดวกขึ้น เพราะจัดเตรียมสภาพแวดล้อมไว้ด้วยกัน ลดปัญหา “เครื่องฉันรันได้ แต่เครื่องเธอรันไม่ได้”
- **Docker Engine** ทำหน้าที่รัน Container ส่วน **Dockerfile** ระบุขั้นตอนสร้าง Image

### Docker ต่างอะไรกับ VM
- VM จำลองฮาร์ดแวร์และรันระบบปฏิบัติการเต็มรูปแบบ จึงใช้ทรัพยากรมากกว่าและบูตช้ากว่า แต่แยกสภาพแวดล้อมได้ชัดเจน
- Docker ใช้ containerization และแชร์ kernel กับ host จึงใช้ทรัพยากรน้อยกว่าและเริ่มทำงานได้เร็วกว่า โดยมีขอบเขตการแยกจาก host ต่างจาก VM

[![Container Vs VMs](/assets/img/Other/Docker/vm-docker5.avif)](https://dockerlabs.collabnix.com/beginners/difference-docker-vm.html)

### Note
```
- ถ้า Host OS เป็น Linux: Docker container ใช้ kernel ของ host OS โดยตรง
- ถ้า Host OS เป็น Windows หรือ macOS: สำหรับ Linux containers Docker Desktop จะใช้ Linux kernel ที่อยู่ใน lightweight VM ซึ่งถูกจัดสรรมาให้โดย Docker Desktop แต่สำหรับ Windows containers (บน Windows) ก็จะใช้ kernel ของ Windows โดยตรง
```

### คำศัพท์ที่ควรรู้
1. **Image**: แม่แบบ (Template) สำหรับสร้าง Container
2. **Container**: อินสแตนซ์ที่สร้างจาก Image เพื่อนำไปรัน
3. **Registry**: ที่เก็บ Image ส่วนกลาง เช่น Docker Hub หรือ Registry ภายในองค์กร



<a id="exmaple-command"></a>

### Example Command


<a id="pre-require"></a>

#### Prerequisites

- ติดตั้ง [Docker Engine](https://docs.docker.com/engine/install/) สำหรับ Linux
- ติดตั้ง [Docker Desktop](https://docs.docker.com/desktop/) หรือ [Rancher Desktop](https://rancherdesktop.io/) สำหรับ Windows และ macOS


<a id="simaple-command"></a>

#### Simple Command

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



<a id="exmaple-1"></a>

#### Example 1:

ลองรันคอนเทนเนอร์จาก Docker image
```bash
docker run hello-world

# Docker จะ pull image hello-world จาก docker hub
# หลังจาก pull image มาแล้ว docker จะรัน image ตัวนั้นทันที
```
---


<a id="exmaple-2"></a>

#### Example 2:

ขั้นตอน:
1. สร้างโฟลเดอร์โปรเจกต์สำหรับเก็บไฟล์ทั้งหมด
2. สร้างไฟล์ Python (`example.py`)
    ```python
    print("test python image file")
    ```
3. สร้างไฟล์ชื่อ `Dockerfile` โดยไม่ใส่นามสกุล
    ```
    From python:3.12.8-slim

    WORKDIR /usr/src/app

    COPY requirements.txt ./
    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    CMD [ "python", "./example.py" ]
    ```
    Note ([Python docker hub](https://hub.docker.com/_/python/tags)): 
    - `alpine` = ใช้ Alpine Linux เป็น base image ซึ่งมีขนาดเล็กและติดตั้งเฉพาะแพ็กเกจที่จำเป็น
    - `slim` = ลดส่วนประกอบบางอย่างจาก image ปกติเพื่อให้มีขนาดเล็กลง
    - `bullseye` = ชื่อรหัสของ Debian 11 (Bullseye)
    - `bookworm` = ชื่อรหัสของ Debian รุ่นถัดจาก Bullseye
4. รันคำสั่ง
    ```
    docker build -t example:1.0.0 .
    docker run -it --rm example:1.0.0
    ```

## Docker Compose คืออะไร
- **Docker Compose** ใช้จัดการแอปพลิเคชันที่มีหลายคอนเทนเนอร์ทำงานร่วมกัน เช่น แอป Python ที่เชื่อมต่อกับ MySQL หรือ Redis
- ไฟล์ `docker-compose.yml` กำหนดว่าจะรันคอนเทนเนอร์ใดบ้าง เชื่อมต่อกันอย่างไร และตั้งค่า volume กับ port mapping แบบใด


<a id="exmaple-command-1"></a>

### Example Command


<a id="pre-require-1"></a>

#### Prerequisites

- ติดตั้ง [Docker Engine](https://docs.docker.com/engine/install/) สำหรับ Linux
- ติดตั้ง [Docker Desktop](https://docs.docker.com/desktop/) หรือ [Rancher Desktop](https://rancherdesktop.io/) สำหรับ Windows และ macOS
- ติดตั้ง [Docker Compose](https://docs.docker.com/compose/install/) หรือใช้ [เวอร์ชัน standalone](https://docs.docker.com/compose/install/standalone/) ซึ่งเรียกด้วย `docker-compose`


<a id="simaple-command-1"></a>

#### Simple Command

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
- ถ้า requirements.txt เปลี่ยน → ขั้นตอน pip install -r requirements.txt จะทำงานใหม่
- ถ้า requirements.txt ไม่เปลี่ยน → Docker อาจใช้เลเยอร์จาก cache โดยไม่รัน pip install ซ้ำ
- ถ้าแก้ Dockerfile ในขั้นตอนหลัง pip install → เลเยอร์ของ pip install ยังใช้ cache เดิมได้
- ถ้าต้องการให้ pip install ทำงานใหม่เสมอ → ใช้ rm -rf /root/.cache/pip หรือ BuildKit cache
