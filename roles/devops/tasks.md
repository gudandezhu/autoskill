# DevOps Tasks

### devops-001: Docker Compose for Web Application

**Context**: A startup has a Node.js API (Express), a PostgreSQL database, and a Redis cache.
They need a Docker Compose setup for local development and a production-ready Dockerfile.
The API handles 500 req/s at peak. Developers need hot reload during development.

**Requirements**:
- Multi-stage Dockerfile for the Node.js app (dev and production targets)
- docker-compose.yml with api, postgres, redis services
- Health checks for all services (postgres: pg_isready, redis: redis-cli ping, api: HTTP endpoint)
- Volume mounts for development (source code hot reload)
- Environment variable management via .env file (no secrets in compose file)
- Network isolation: api can reach db/redis, but db/redis not exposed to host
- Restart policies for production (unless-stopped for api, always for db/redis)
- Database initialization with seed data script
- Resource limits: api capped at 512MB RAM, redis at 256MB

**Output**: Dockerfile and docker-compose.yml with inline comments explaining choices.

### devops-002: CI/CD Pipeline Debugging

**Context**: A GitHub Actions workflow is failing intermittently (3 out of 10 runs). The pipeline:
1. Runs tests (npm test) — always passes
2. Builds Docker image — passes
3. Pushes to ECR — **fails intermittently** with "no basic auth credentials"
4. Deploys to ECS — never reached when push fails

The workflow uses `aws-actions/configure-aws-credentials@v2` with secrets.AWS_ACCESS_KEY_ID
and secrets.AWS_SECRET_ACCESS_KEY. The AWS IAM user has full ECR and ECS permissions.
Deployments happen 8-10 times per day. The team is using main-branch pushes as the trigger.

**Requirements**:
- Diagnose the root cause of the intermittent ECR auth failure
- Propose a fix with specific code changes to the workflow YAML
- Add retry logic for known transient failures (ECR login, ECS deployment)
- Add a Slack notification step for both success and failure
- Ensure the pipeline can handle concurrent pushes (two devs merging at the same time)
- Add a rollback step: if ECS deployment fails, roll back to the previous task definition

**Output**: Fixed and improved GitHub Actions workflow YAML with comments explaining each change.

### devops-003: Kubernetes Manifests for Microservices Migration

**Context**: A team is migrating 3 microservices from EC2 to Kubernetes:
- **auth-service** (Node.js): handles login/JWT, 200 req/s, needs HPA
- **order-service** (Go): processes orders, 1K req/s, must survive node failure
- **notification-service** (Python): sends emails/push, bursty traffic (0-500 req/s)

Requirements from the team:
- Zero-downtime deployments for all services
- auth-service secrets (JWT signing key, DB password) must use Kubernetes Secrets, not env vars in plain text
- order-service must have a pod disruption budget (min 2 replicas always available)
- notification-service needs a priority class (can be preempted if cluster is under pressure)
- All services must expose /health and /ready endpoints
- Resource requests and limits defined for every container
- Network policy: only auth-service can reach the user database; order-service can reach auth-service but not notification-service

**Requirements**:
- Kubernetes manifests (Deployment, Service, HPA, PDB, NetworkPolicy, Secret) for all 3 services
- A namespace definition with resource quotas (max 8 CPU cores, 16GB RAM total)
- Rolling update strategy: maxSurge=1, maxUnavailable=0 for order-service
- Horizontal Pod Autoscaler for auth-service (target 70% CPU, min 2, max 10)
- Address: what happens if the cluster runs out of resources during a deployment?

**Output**: Kubernetes YAML manifests organized by service, with a README explaining the deployment strategy.
