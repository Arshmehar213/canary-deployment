# Canary Demo Application

A lightweight, production-conscious Python/Flask microservice equipped with bounded Prometheus metrics and configurable fault injection (`http_500` and `latency`). Built to test Automated Canary Deployments and Progressive Delivery pipelines using **Argo Rollouts**, **Istio**, **ArgoCD**, **Prometheus**, and **Grafana**.

---

## 1. Local Setup

```bash
cd canary-demo-app
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements-dev.txt