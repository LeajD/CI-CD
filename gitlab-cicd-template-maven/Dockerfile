ARG version=${version}
FROM graylog/graylog:${version} AS main
ARG ver_alert_main=${ver_alert_main}
ARG ver_alert_minor=${ver_alert_minor}
ARG ver_alert_main
ARG ver_alert_minor
USER root
RUN export DEBIAN_FRONTEND=noninteractive && apt update -y && apt install gpg xz-utils -y
COPY plugin.jar /usr/share/graylog/plugin/graylog-${CI_PROJECT_NAME}-${CI_COMMIT_BRANCH}.jar
RUN chown -R graylog:graylog /usr/share/graylog/
USER graylog
EXPOSE 9000/tcp
