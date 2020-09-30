FROM python:3.8-slim

LABEL \
    Name=alerts \
    Version=0.0.1

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONBREAKPOINT=0 \
    GROUP=alerts \
    APPUSER=alerts \
    WORKDIR=/home/alerts

ENV PATH=${PATH}:${WORKDIR}/.local/bin

# Add user to run application
RUN groupadd -r ${GROUP} -g 1000 && \
    useradd -r -u 1000 -g ${GROUP} -s /sbin/nologin -d ${WORKDIR} ${APPUSER}

# Install python packages
COPY --chown=1000:1000 requirements.txt ${WORKDIR}/requirements.txt

USER $APPUSER

RUN pip install --user -r ${WORKDIR}/requirements.txt

# Copy source code
COPY --chown=1000:1000 ./dev $WORKDIR

WORKDIR $WORKDIR

EXPOSE 7777
