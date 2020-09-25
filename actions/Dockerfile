# Extend the official Rasa SDK image
FROM rasa/rasa-sdk:1.10.2

# Change back to root user to install dependencies
USER root

RUN apt-get update && apt-get install -y libaio1 wget unzip

WORKDIR /opt/oracle
RUN wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip && \
    unzip instantclient-basiclite-linuxx64.zip && rm -f instantclient-basiclite-linuxx64.zip && \
    cd /opt/oracle/instantclient* && rm -f *jdbc* *occi* *mysql* *README *jar uidrvci genezi adrci && \
    echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf && ldconfig

COPY tnsnames.ora /opt/oracle/instantclient_19_8/network/admin

# Use subdirectory as working directory
WORKDIR /app

# Copy any additional custom requirements, if necessary (uncomment next line)
COPY requirements-actions.txt ./

# Change back to root user to install dependencies
USER root

# Install extra requirements for actions code, if necessary (uncomment next line)
RUN python -m pip install --upgrade pip
RUN pip install -r requirements-actions.txt
RUN python -m spacy download en_core_web_sm

# Copy actions folder to working directory
COPY . /app/actions

# By best practices, don't run the code with root user
USER 1001