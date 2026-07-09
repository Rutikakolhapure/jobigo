Auth Service module details and developer notes:

- JWT tokens: SimpleJWT used. Access tokens lifetime, refresh lifetime configurable via environment.
- Email verification and password reset use signed short-lived tokens (itsdangerous). For production use TLS-protected links and secure email.
- RBAC: role stored in user.role (ADMIN, RECRUITER, SEEKER). Use permission classes in endpoints for Authorization checks.
- Integration: other services should validate JWTs using the same signing key and algorithm (SIMPLE_JWT SIGNING_KEY & ALGORITHM). Alternatively, use asymmetric keys for stronger separation.
- In a production multi-service environment, secrets should be stored in a secrets manager and rotated regularly.
