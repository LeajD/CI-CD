ARG version=${version}
FROM jenkins/jenkins:${version}
USER root
RUN apt-get update && apt-get install jq -y && apt-get clean
RUN apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    wget \
    software-properties-common \
    libc-bin libc6 

RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - | apt-key fingerprint 0EBFCD88
RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"

RUN apt update && apt-get install -y docker-ce docker-ce-cli containerd.io

USER jenkins
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"
COPY jenkins-image/files/security.groovy /usr/share/jenkins/ref/init.groovy.d/security.groovy
COPY jenkins-image/files/jenkins-user /run/secrets/jenkins-user
COPY jenkins-image/files/jenkins-pass /run/secrets/jenkins-pass
RUN jenkins-plugin-cli --plugins active-directory git workflow-cps blueocean kubernetes kubernetes-cli flexible-publish workflow-aggregator ansicolor job-dsl
