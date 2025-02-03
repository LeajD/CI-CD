#------------------------------------------------------------------------------------------------------------------------------
export GITLAB_DEST=/tmp/
/etc/apache-maven-3.8.8/apache-maven-3.8.8/bin/mvn org.apache.maven.plugins:maven-dependency-plugin:3.1.2:get \
-Dartifact=com.company:graylog-plugin-tieto-json-output:4.3.13-4.3.13base-1.0.0 -U \
-DrepoUrl=https://company.git/api/v4/projects/2074/packages/maven/ -Ddest=$GITLAB_DEST/plugin.jar \
--settings ./gitlab/ci_settings.xml --file ./gitlab/pom.xml
#------------------------------------------------------------------------------------------------------------------------------
/etc/apache-maven-3.8.8/apache-maven-3.8.8/bin/mvn org.apache.maven.plugins:maven-dependency-plugin:3.1.2:get \
-Dartifact=com.company:graylog-plugin-groupmapping:4.3.13-4.3.13base-1.0.0 -U \
-DrepoUrl=https://company.git/api/v4/projects/2069/packages/maven/ -Ddest=$GITLAB_DEST/plugin.jar \
--settings ./gitlab/ci_settings.xml --file ./gitlab/pom.xml
#------------------------------------------------------------------------------------------------------------------------------
/etc/apache-maven-3.8.8/apache-maven-3.8.8/bin/mvn org.apache.maven.plugins:maven-dependency-plugin:3.1.2:get \
-Dartifact=com.company:graylog-plugin-audit-logs:4.3.13-4.3.13base-1.0.0 -U \
-DrepoUrl=https://company.git/api/v4/projects/2070/packages/maven/ -Ddest=$GITLAB_DEST/plugin.jar \
--settings ./gitlab/ci_settings.xml --file ./gitlab/pom.xml
#------------------------------------------------------------------------------------------------------------------------------
/etc/apache-maven-3.8.8/apache-maven-3.8.8/bin/mvn org.apache.maven.plugins:maven-dependency-plugin:3.1.2:get \
-Dartifact=com.company:graylog-plugin-snapshot-restore:4.3.13-4.3.13base-1.0.0 -U \
-DrepoUrl=https://company.git/api/v4/projects/2065/packages/maven/ -Ddest=$GITLAB_DEST/plugin.jar \
--settings ./gitlab/ci_settings.xml --file ./gitlab/pom.xml
#------------------------------------------------------------------------------------------------------------------------------
/etc/apache-maven-3.8.8/apache-maven-3.8.8/bin/mvn org.apache.maven.plugins:maven-dependency-plugin:3.1.2:get \
-Dartifact=com.company:graylog-plugin-azure-output:4.3.13-4.3.13base-1.0.0 -U \
-DrepoUrl=https://company.git/api/v4/projects/2068/packages/maven/ -Ddest=$GITLAB_DEST/plugin.jar \
--settings ./gitlab/ci_settings.xml --file ./gitlab/pom.xml
#------------------------------------------------------------------------------------------------------------------------------
/etc/apache-maven-3.8.8/apache-maven-3.8.8/bin/mvn org.apache.maven.plugins:maven-dependency-plugin:3.1.2:get \
-Dartifact=com.company:graylog-plugin-output-overview:4.3.13-4.3.13base-1.0.0 -U \
-DrepoUrl=https://company.git/api/v4/projects/2083/packages/maven/ -Ddest=$GITLAB_DEST/plugin.jar \
--settings ./gitlab/ci_settings.xml --file ./gitlab/pom.xml
#------------------------------------------------------------------------------------------------------------------------------
