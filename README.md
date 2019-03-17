# NotZam
NotZam is a just study project for me to learn how to use Python, Django, Kafka, Docker, and Deep Learning. The training model of detecting a trigger word and sample audio files are from an assignment in [Cousera Deep Learning Specialization](https://www.coursera.org/specializations/deep-learning).


## Note to Readers
If you are Korean, click this [link](README_kor.md).

Because I'm a Java back-end application programmer, almost concepts, I used for this project, are not familiar to me. That's why the code convention of this project is somewhat mess. But I'm gonna fix it in the near future.


## Getting Started
1. Install [Docker](https://www.docker.com/products/docker-desktop).
2. Change the value of "{HOSTNAME}" in ".env" to your \$HOSTNAME result of command "echo $HOSTNAME"
3. Run following commands: 
<pre><code>$docker network create kafka-network
$docker-comspose -f docker-comspose.kafka.yml up
#open another tab and run. It will takes a few minutes:
$docker-compose up --build </code></pre>
4. Open your web browser and connect to "http://localhost:8000/ml/word-trigger"
5. If you can see a simple web page, which contains a file upload form, it's done.
6. Download and upload a [sample](web/uploads/sample.wav) for test.
7. After uploading a file, you can see "Get Result" below the file form and please click it. Then, you can see "[2567.2727272727275]", which indicating trigger words time position in the sample audio.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details