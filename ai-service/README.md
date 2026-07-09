# AI Service for JobiGo

This service provides AI capabilities such as:

- Cover letter generation
- Resume summary
- Skill suggestions
- Embedding generation
- Semantic job matching

It is a stateless microservice that does NOT own users, jobs, or companies. Instead it consumes other services' APIs for data and performs AI processing.

See .env.example for configuration.
