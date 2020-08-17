FROM python:3.6-alpine
WORKDIR /External
COPY requirments.txt requirments.txt
RUN pip install -r requirments.txt
COPY listener.py listener.py
ENV receiver_queue downstream1
ENV sender_queue downstream2
ENV src_system DOWN
ENV mq_host mq
ENV tracer_ip tracer
ENV sleep_time 60
CMD ["python","listener.py"]