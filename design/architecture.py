from diagrams import Cluster, Diagram
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import SVC
from diagrams.programming.framework import Django
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.database import Postgresql
from diagrams.aws.analytics import Redshift

with Diagram("Django PDF", show=True, filename='architecture', direction='TB'):
    ui = Django('UI')
    redis = Redis('Cache')
    db = Postgresql('DB')
    data_warehouse = Redshift('Data Warehouse')
    with Cluster("Kube") as kube:
        svc = SVC('Django PDF')
        pods = [Pod('Django PDF - 1'),
                Pod('Django PDF - 2')]
        svc >> pods
        ui >> svc
        pods >> db
        pods >> redis
        pods >> data_warehouse
        redis - data_warehouse
