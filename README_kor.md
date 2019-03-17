# NotZam
NotZam은 Python, Django, Kafka, Docker, 및 딥러닝을 어떻게 쓰는지 공부하기 위한 프로젝트 입니다. 시동어를 찾는 훈련 모델 및 오디오 샘플 파일들은  [Cousera Deep Learning Specialization](https://www.coursera.org/specializations/deep-learning)에서 가져온 겁니다.

## 이 글을 읽는 분에게
저는 자바 백엔드 앱 개발자라서 거의 모든 개념들에 익숙하지 않습니다. 그래서 이 프로젝트의 코드 컨벤션은 좀 난잡합니다만, 나중에는 고칠 예정 입니다.


## 시작하기
1. [Docker](https://www.docker.com/products/docker-desktop)를 설치합니다.
2. ".env" 파일의 "{HOSTNAME}" 값을 "echo $HOSTNAME"결과인 \$HOSTNAME으로 바꿉니다.
3. 아래 명령들을 실행 합니다.: 
<pre><code>$docker network create kafka-network
$docker-comspose -f docker-comspose.kafka.yml up
#다른 탭을 열어서 실행합니다. 좀 오래 걸립니다:
$docker-compose up --build </code></pre>
4. 웹 브라우저를 열어서 다음의 주소로 접속합니다. "http://localhost:8000/ml/word-trigger"
5. 파일 업로드 폼이 있는 단순한 웹 페이즈가 보인다면, 잘 된 겁니다.
6. [샘플](web/uploads/sample.wav)파일을 다운로드하고 업로드해서 테스트 해보세요.
7. 업로드가 완료되면, "Get Result"가 보일 것이고, 이를 클릭하면  "[2567.2727272727275]"가 보일 겁니다. 이는 업로드 된 오디오 파일의 시동어 위치를 표시하는 겁니다.

## 라이센스
본 프로젝트는 MIT 라이센스를 따릅니다. 자세한 사항은 [링크](LICENSE)를 클릭해서 확인해 주세요.