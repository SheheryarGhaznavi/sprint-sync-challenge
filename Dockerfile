# SprintSync Multi-Service Dockerfile (Meta)
# This file is a placeholder for platforms that require a Dockerfile in the project root.
# It does not build any service directly, but points users to Dockerfile.backend and Dockerfile.frontend.

# For backend, use Dockerfile.backend
# For frontend, use Dockerfile.frontend

# If your platform requires a Dockerfile in the root, you can copy the backend or frontend Dockerfile here, or use docker-compose.yml for multi-service orchestration.

# Example usage:
docker compose up --build

# If you want to build the backend only:
# docker build -t sprintsync-backend -f Dockerfile.backend .

# If you want to build the frontend only:
# docker build -t sprintsync-frontend -f Dockerfile.frontend .
