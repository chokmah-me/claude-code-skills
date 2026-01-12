# Repository Briefing Skill - Usage Guide

## Overview

The `repo-briefing` skill provides comprehensive yet concise analysis of git repositories. Perfect for understanding project structure, technology stack, development activity, and code quality metrics when joining new projects or assessing existing ones.

**Token Efficiency**: ~600 tokens vs ~2K manual exploration (70% reduction)

## Quick Start

### Natural Language Invocation
```
"Give me a briefing on this repository"
"What's the state of this codebase?"
"Analyze this project's structure and health"
```

### Direct Skill Invocation
```
/repo-briefing
```

## What It Analyzes

✅ **Project Structure**:
- Directory organization and purpose
- Technology stack identification
- Configuration and setup files
- Documentation completeness

✅ **Development Activity**:
- Commit frequency and patterns
- Contributor analysis
- Recent development trends
- Branch management practices

✅ **Code Quality**:
- Code complexity metrics
- Test coverage indicators
- Security vulnerability assessment
- Maintainability evaluation

✅ **Operational Health**:
- Build system status
- Dependency health
- Configuration quality
- Deployment readiness

## Analysis Process

### Phase 1: Repository Scanning
Maps repository structure:
- File system exploration
- Technology detection
- Configuration analysis
- Documentation assessment

### Phase 2: Git History Analysis
Examines development patterns:
- Commit log analysis
- Author contribution tracking
- Branch structure evaluation
- Release pattern identification

### Phase 3: Code Quality Assessment
Evaluates codebase health:
- Complexity analysis
- Test presence evaluation
- Security scan results
- Dependency analysis

### Phase 4: Health Report Generation
Synthesizes comprehensive briefing:
- Executive summary
- Detailed findings
- Risk assessment
- Recommendations

## Example Usage

### Example 1: New Project Onboarding
```
User: "Give me a briefing on this codebase I'm joining"

Claude: 📊 Generating comprehensive repository briefing...

📋 Repository Briefing: Machine Learning Platform

🏗️ Project Structure:
- Type: Python-based ML web application
- Size: 8,247 files, 234,567 lines of code
- Languages: Python (78%), JavaScript (15%), SQL (7%)
- Architecture: Flask backend, React frontend

🔧 Technology Stack:
Backend: Flask 2.0, SQLAlchemy, Redis, Celery
Frontend: React 18, TypeScript, Material-UI
ML/AI: scikit-learn, TensorFlow, PyTorch
Database: PostgreSQL, Redis (caching)
Infrastructure: Docker, Kubernetes, AWS

📈 Development Activity:
- Active development: High (15 commits/week)
- Contributors: 8 active developers
- Recent focus: ML model optimization, UI improvements
- Last release: 2 weeks ago (v2.1.4)

📝 Code Quality Assessment:
Overall Quality: 7.5/10 (Good)
- Test coverage: 82% (excellent)
- Documentation: Comprehensive (API docs, READMEs)
- Code complexity: Moderate (some areas need attention)
- Security: Good (regular dependency updates)

⚠️ Areas for Improvement:
1. ML model tests: Limited coverage (45%)
2. Frontend error handling: Could be more robust
3. Database migrations: Some lack rollback procedures
4. Performance monitoring: Basic implementation

🚀 Getting Started:
1. Setup: `docker-compose up` (well documented)
2. Tests: `pytest` (comprehensive test suite)
3. Frontend: `npm start` (standard React setup)
4. Database: PostgreSQL required (setup script provided)

📊 Development Practices:
- Git workflow: Feature branches with PR reviews
- Code style: Black (Python), ESLint (JavaScript)
- Testing: pytest, Jest, comprehensive CI/CD
- Deployment: Automated via GitHub Actions

💡 Key Insights:
- Well-maintained, actively developed project
- Strong testing culture (82% coverage)
- Good documentation for onboarding
- Modern technology stack
- Room for improvement in ML testing
```

### Example 2: Project Health Assessment
```
User: "Assess the health of this legacy project"

Claude: 📊 Analyzing legacy project health...

🏥 Project Health Report: Legacy E-commerce System

📊 Overall Health Score: 5.2/10 (Needs Attention)

🏗️ Project Structure:
- Type: Java-based e-commerce platform
- Size: 12,543 files, 456,789 lines of code
- Age: 8 years (last major update: 2 years ago)
- Languages: Java (85%), XML (10%), SQL (5%)

🔧 Technology Stack:
Backend: Java 8, Spring Boot 1.5, Hibernate
Frontend: JSP, jQuery, Bootstrap 3
Database: MySQL 5.7
Build: Maven 3.x
Server: Tomcat 8

📈 Development Activity:
- Active development: Low (2 commits/week)
- Contributors: 3 active developers
- Recent focus: Bug fixes, minor feature additions
- Last major release: 6 months ago

🚨 Critical Issues Identified:

1. SECURITY: High-risk vulnerabilities
   - Java 8 (end-of-life, security issues)
   - Dependencies: 23 high-severity CVEs
   - Framework: Spring Boot 1.5 (unsupported)

2. TECHNICAL DEBT: High complexity
   - Cyclomatic complexity: Average 28 (high)
   - File length: Some files >2000 lines
   - Duplicate code: ~15% estimated

3. INFRASTRUCTURE: Outdated stack
   - Java version: 8 (should be 17+)
   - Framework: Boot 1.5 (should be 2.7+)
   - Frontend: jQuery (should be modern framework)

📊 Quality Metrics:
- Test coverage: 34% (poor)
- Documentation: Minimal (outdated)
- Code complexity: High (needs refactoring)
- Security: Poor (multiple vulnerabilities)

💡 Modernization Roadmap:

Phase 1 (Immediate - Security):
- Update Java to 17
- Upgrade Spring Boot to 2.7
- Address high-severity CVEs
- Implement security scanning

Phase 2 (Short-term - Quality):
- Increase test coverage to 70%
- Refactor high-complexity methods
- Extract duplicate code
- Update documentation

Phase 3 (Long-term - Architecture):
- Migrate to microservices
- Modernize frontend (React/Vue)
- Implement CI/CD pipeline
- Containerize application

📈 Business Impact Assessment:
- Maintenance cost: High (technical debt)
- Security risk: Critical (vulnerabilities)
- Development velocity: Low (complexity)
- Innovation capability: Limited (old stack)

🎯 Recommended Actions:
1. Immediate: Address security vulnerabilities
2. Short-term: Improve test coverage
3. Medium-term: Plan modernization roadmap
4. Long-term: Allocate budget for migration

💰 Cost-Benefit Analysis:
- Modernization cost: High
- Maintenance savings: Significant
- Security risk reduction: Critical
- Development velocity gain: Substantial
```

### Example 3: Technology Stack Analysis
```
User: "Analyze the technology choices in this repository"

Claude: 📊 Analyzing technology stack and choices...

🔧 Technology Stack Analysis: Modern Web Application

📊 Stack Modernity Score: 8.5/10 (Very Good)

🏗️ Architecture Overview:
- Pattern: Microservices architecture
- Communication: REST APIs + Message queue
- Deployment: Containerized (Docker + Kubernetes)
- Cloud: AWS-native services

💻 Backend Technologies:
Languages: Go 1.21 (services), Python 3.11 (ML/data)
Frameworks: Gin (Go), FastAPI (Python)
Databases: PostgreSQL 15, Redis 7, Elasticsearch 8
Message Queue: Apache Kafka
Caching: Redis Cluster

🎨 Frontend Technologies:
Framework: React 18 with TypeScript 5
State Management: Redux Toolkit
UI Library: Tailwind CSS + Headless UI
Build Tool: Vite 5
Testing: Jest + React Testing Library

🔧 Infrastructure & DevOps:
Container: Docker with multi-stage builds
Orchestration: Kubernetes (EKS)
CI/CD: GitHub Actions
Monitoring: Prometheus + Grafana
Logging: ELK Stack (Elasticsearch, Logstash, Kibana)

📊 Technology Assessment:

✅ Excellent Choices:
- Go for high-performance services
- FastAPI for Python APIs (modern, fast)
- React 18 with TypeScript (current, type-safe)
- PostgreSQL 15 (latest features)
- Kubernetes (industry standard)
- Tailwind CSS (utility-first, efficient)

⚠️ Areas for Consideration:
- Message queue: Kafka (complex, consider RabbitMQ for simplicity)
- Frontend build: Vite (good, but Webpack more standard)
- Monitoring: Basic setup, could use APM tools

🔍 Dependencies Analysis:
- Backend: 127 dependencies (reasonable)
- Frontend: 892 dependencies (typical for React)
- Security: 2 medium-severity issues (manageable)
- Licenses: All compatible (MIT, Apache, BSD)

⚡ Performance Characteristics:
- Go services: Excellent (low latency, high throughput)
- Python APIs: Good (FastAPI efficient)
- Frontend: Optimized (code splitting, lazy loading)
- Database: Well-indexed (good query performance)

🔒 Security Posture:
- Framework versions: Current (no known vulnerabilities)
- Dependencies: Regularly updated (automated)
- Authentication: JWT with refresh tokens
- Authorization: RBAC implementation
- Input validation: Comprehensive

📈 Scalability Assessment:
- Horizontal scaling: Supported (stateless services)
- Database scaling: Read replicas configured
- Caching strategy: Multi-level (Redis + CDN)
- Load balancing: Application Load Balancer
- Auto-scaling: Configured for key services

💡 Technology Recommendations:

Short-term (3 months):
1. Implement distributed tracing (Jaeger)
2. Add APM monitoring (New Relic/DataDog)
3. Set up chaos engineering testing

Medium-term (6-12 months):
1. Evaluate GraphQL for API efficiency
2. Consider WebAssembly for performance-critical features
3. Implement advanced caching strategies

Long-term (1+ years):
1. Evaluate edge computing for global performance
2. Consider serverless for specific use cases
3. Plan for emerging technologies (WebGPU, etc.)

🎯 Overall Assessment:
- Technology choices: Modern and appropriate
- Architecture: Well-designed for scale
- Performance: Optimized for current needs
- Security: Strong foundation implemented
- Future-proofing: Good foundation for evolution
```

## Analysis Categories

### 🏗️ Architecture Analysis
Structural assessment:
- Design pattern identification
- Component relationships
- Scalability indicators
- Maintainability factors

### 💻 Technology Evaluation
Stack assessment:
- Framework appropriateness
- Language choice justification
- Version currency
- Ecosystem health

### 📈 Development Practices
Process evaluation:
- Git workflow analysis
- Testing practices
- Code quality indicators
- Documentation completeness

### 🔒 Security Assessment
Risk evaluation:
- Vulnerability identification
- Dependency security
- Configuration safety
- Best practice adherence

### ⚡ Performance Analysis
Efficiency evaluation:
- Bottleneck identification
- Optimization opportunities
- Scalability assessment
- Resource utilization

## Configuration Options

**Analysis Focus**:
- `--comprehensive`: Full analysis (default)
- `--security-focus`: Emphasize security aspects
- `--performance-focus`: Highlight performance issues
- `--technology-focus`: Deep technology analysis

**Scope Control**:
- `--recent=N`: Focus on last N weeks
- `--directory=path`: Analyze specific directory
- `--technology=tech`: Focus on specific technology

**Output Control**:
- `--format=detailed`: Comprehensive report
- `--format=executive`: Summary for management
- `--format=technical`: Technical details only

## Integration with Workflows

### Onboarding Process
Help new team members:
```
1. New developer joins team
2. /repo-briefing provides overview
3. Focus areas identified
4. Learning path created
5. Productivity accelerated
```

### Regular Health Checks
Monitor project evolution:
```
1. Weekly health assessments
2. Trend analysis over time
3. Issue identification
4. Improvement planning
5. Progress tracking
```

### Technology Decisions
Support decision-making:
```
1. Evaluate current stack
2. Identify improvement areas
3. Assess alternatives
4. Plan migrations
5. Measure results
```

## Advanced Analysis

### Historical Trend Analysis
Track changes over time:
```
- Technology adoption patterns
- Code quality evolution
- Development velocity trends
- Security posture changes
```

### Comparative Analysis
Benchmark against standards:
```
- Industry best practices
- Similar project comparison
- Maturity model assessment
- Performance benchmarking
```

### Predictive Insights
Forecast future needs:
```
- Scalability predictions
- Technology roadmap suggestions
- Risk anticipation
- Resource planning
```

## Best Practices

### 1. Regular Assessment
Monitor continuously:
- Monthly health checks
- Quarterly deep dives
- Annual comprehensive reviews
- Continuous monitoring

### 2. Context-Aware Analysis
Consider project context:
- Project maturity stage
- Team size and experience
- Business requirements
- Technical constraints

### 3. Actionable Insights
Drive improvement:
- Specific recommendations
- Prioritized action items
- Measurable outcomes
- Clear next steps

### 4. Collaborative Usage
Share insights:
- Team presentations
- Stakeholder reports
- Decision documentation
- Knowledge sharing

## Success Metrics

### Quantitative Measures
Objective assessments:
- Health score improvement
- Issue reduction count
- Performance metrics
- Security vulnerability fixes

### Qualitative Measures
Subjective evaluations:
- Developer satisfaction
- Stakeholder confidence
- Decision quality
- Team productivity

## Common Use Cases

### Due Diligence
Assess acquisition targets:
```
Technology stack evaluation
Code quality assessment
Security posture review
Technical debt quantification
```

### Project Evaluation
Assess project status:
```
Health assessment
Risk identification
Improvement planning
Resource allocation
```

### Technology Planning
Plan modernizations:
```
Stack evaluation
Migration planning
Roadmap development
Success measurement
```

## Token Efficiency

- Small project (<50 files): ~400 tokens
- Medium project (50-500 files): ~600 tokens
- Large project (500+ files): ~800 tokens
- Historical analysis: +200 tokens per time period

## Related Skills

- `git/diff-summariser` - Understand recent changes
- `analysis/code/api-contract-sniffer` - Check API health
- `analysis/code/dependency-audit` - Assess dependencies
- `analysis/code/dead-code-hunter` - Identify cleanup opportunities

---

**Ready to understand your repository?** Just tell Claude: "Give me a briefing on this repo" or "Analyze this project"!