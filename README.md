# avoidance_driving

### 라이다를 사용한 회피주행 알고리즘 구현

  - os : Ubuntu 22.04

  - ros : humble

  - Language : python3.0


```/scan``` 토픽을 사용한 라이다 데이터를 받아서 회피주행 알고리즘을 구현한다.
publish하는 토픽은 ```/cmd_vel```, ```/move_base_simple/goal```, ```/LiDAR_target_num```이다.

LiDAR_callback 에서 전방라이다의 대한 파티션(구역)을 나누고 각 파티션에 대한 거리를 계산한다. 그리고 각 파티션에 대한 거리를 통해 회피주행 알고리즘을 구현한다.

회피주행 알고리즘은 다음과 같다.

1. 전방라이다의 파티션(구역)을 나눈다.
2. 각 파티션에 대한 거리를 계산한다.
3. 각 파티션에 대한 거리를 통해 회피주행 알고리즘을 구현한다.
4. 회피주행 알고리즘을 통해 나온 결과를 ```/cmd_vel``` 토픽에 publish한다.
5. 회피주행 알고리즘을 통해 나온 결과를 ```/move_base_simple/goal``` 토픽에 publish한다.
6. 회피주행 알고리즘을 통해 나온 결과를 ```/LiDAR_target_num``` 토픽에 publish한다.

파티션은 8개로 나누었다. y축으로 150도 축으로 구현되어 있고 
global_x_LiDAR 와 global_y_LiDAR 를 통해 파티션을 나누었다.

