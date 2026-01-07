# Refactoring Skill - Usage Guide

## Overview

The `refactoring` skill provides systematic, safe code restructuring with comprehensive validation. Handles complex refactorings while preserving behavior, with built-in testing, rollback capabilities, and step-by-step validation.

**Token Efficiency**: ~1.2K tokens vs ~3K manual refactoring (60% reduction)

## Quick Start

### Natural Language Invocation
```
"Refactor this monolithic function into smaller pieces"
"Extract the business logic from this controller"
"Restructure this inheritance hierarchy"
```

### Direct Skill Invocation
```
/refactoring
```

## Refactoring Types

✅ **Code Structure**:
- Extract methods/functions
- Split large files
- Reorganize classes/modules
- Simplify complex logic

✅ **Architecture**:
- Extract service layers
- Separate concerns
- Introduce interfaces
- Restructure dependencies

✅ **Data Structures**:
- Rename variables/classes
- Change method signatures
- Migrate data formats
- Update type definitions

✅ **Design Patterns**:
- Introduce patterns systematically
- Replace anti-patterns
- Standardize implementations
- Improve extensibility

## Refactoring Process

### Phase 1: Analysis & Planning
Understands current structure:
- Code complexity analysis
- Dependency mapping
- Risk assessment
- Refactoring strategy

### Phase 2: Safe Transformation
Performs changes systematically:
- Step-by-step modifications
- Continuous validation
- Automated testing
- Progress tracking

### Phase 3: Comprehensive Validation
Ensures behavior preservation:
- Multi-level testing
- Regression detection
- Performance validation
- Integration verification

### Phase 4: Cleanup & Optimization
Polishes the result:
- Code cleanup
- Documentation updates
- Performance optimization
- Final validation

## Example Usage

### Example 1: Method Extraction
```
User: "Extract the validation logic from this large method"

Claude: 🔧 Analyzing method extraction opportunity...

📊 Extraction Analysis:
- Target method: process_user_registration (147 lines)
- Validation section: lines 45-89 (44 lines)
- Extraction complexity: Medium
- Dependencies: 6 local variables, 3 external calls
- Risk level: Low (pure validation logic)

🔨 Step-by-Step Refactoring:

Step 1: Create extracted method signature
```python
def validate_user_data(username, email, password, age):
    """Validates user registration data."""
    # Extracted validation logic will go here
    pass
```

Step 2: Move validation logic
✅ Extracted validation logic safely
✅ Preserved all validation rules
✅ Maintained error message consistency

Step 3: Update original method
```python
def process_user_registration(user_data):
    # Extract validation call
    validation_result = validate_user_data(**user_data)
    if not validation_result.is_valid:
        return validation_result.errors
    # Continue with registration logic...
```

Step 4: Comprehensive testing
✅ Unit tests for extracted method: PASSED
✅ Integration tests: PASSED
✅ Regression tests: PASSED
✅ Edge case validation: PASSED

📈 Refactoring Results:
- Original method: 147 lines → 89 lines (-40%)
- Extracted method: 44 lines (focused, testable)
- Cyclomatic complexity: Reduced by 35%
- Test coverage: Improved from 65% to 87%
- Performance: Maintained (no degradation)

🎯 Benefits Achieved:
- Better separation of concerns
- Improved testability
- Reduced complexity
- Reusable validation logic
```

### Example 2: Class Extraction
```
User: "Extract business logic from this controller into a service class"

Claude: 🔧 Analyzing service layer extraction...

📊 Extraction Analysis:
- Source: UserController (234 lines)
- Business logic: 167 lines (71%)
- Data access: Embedded
- External dependencies: Database, cache, email
- Complexity: High (mixed concerns)

🏗️ Architecture Transformation:

Step 1: Design service interface
```python
class UserService:
    def create_user(self, user_data: dict) -> User
    def update_user(self, user_id: int, updates: dict) -> User
    def delete_user(self, user_id: int) -> bool
    def get_user_by_email(self, email: str) -> Optional[User]
```

Step 2: Extract business logic systematically
✅ User creation logic extracted
✅ Validation rules preserved
✅ Email notifications maintained
✅ Database transactions handled

Step 3: Update controller to use service
```python
class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
    
    def create_user(self, request):
        # Delegate to service layer
        result = self.user_service.create_user(request.data)
        return self._format_response(result)
```

Step 4: Dependency injection setup
```python
# Configure dependencies
user_service = UserService(database, cache, email_service)
user_controller = UserController(user_service)
```

Step 5: Comprehensive validation
✅ All existing tests pass: CONFIRMED
✅ Service layer tests added: 23 NEW TESTS
✅ Controller tests updated: 15 MODIFIED
✅ Integration tests pass: CONFIRMED
✅ Performance maintained: NO DEGRADATION

🏆 Architecture Results:
- Separation of concerns: ACHIEVED
- Controller size: 234 lines → 67 lines (-71%)
- Service layer: 167 lines (focused, testable)
- Test coverage: 72% → 91% (+19%)
- Dependency management: PROPERLY STRUCTURED
```

### Example 3: Inheritance Refactoring
```
User: "Replace this inheritance hierarchy with composition"

Claude: 🔧 Analyzing inheritance to composition refactoring...

📊 Hierarchy Analysis:
- Base class: PaymentProcessor (abstract)
- Subclasses: CreditCardProcessor, PayPalProcessor, BitcoinProcessor
- Shared behavior: 40% of base class
- Specific behavior: 60% unique per subclass
- Complexity: Medium-High (deep hierarchy)

🔄 Composition Transformation:

Step 1: Identify shared behaviors
```python
# Shared behaviors to extract
class PaymentValidator:
    def validate_amount(self, amount): ...
    def validate_currency(self, currency): ...

class PaymentLogger:
    def log_payment_attempt(self, payment): ...
    def log_payment_success(self, payment): ...

class PaymentSecurity:
    def encrypt_payment_data(self, data): ...
    def validate_security_tokens(self, tokens): ...
```

Step 2: Create strategy pattern for specific behaviors
```python
from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, payment_data):
        pass
    
    @abstractmethod
    def get_payment_method(self):
        pass

class CreditCardStrategy(PaymentStrategy):
    def process_payment(self, payment_data):
        # Credit card specific processing
        pass

class PayPalStrategy(PaymentStrategy):
    def process_payment(self, payment_data):
        # PayPal specific processing
        pass
```

Step 3: Create composed payment processor
```python
class PaymentProcessor:
    def __init__(self, strategy: PaymentStrategy, validator: PaymentValidator,
                 logger: PaymentLogger, security: PaymentSecurity):
        self.strategy = strategy
        self.validator = validator
        self.logger = logger
        self.security = security
    
    def process_payment(self, payment_data):
        # Use composed behaviors
        self.validator.validate_amount(payment_data.amount)
        self.logger.log_payment_attempt(payment_data)
        secured_data = self.security.encrypt_payment_data(payment_data)
        result = self.strategy.process_payment(secured_data)
        self.logger.log_payment_success(payment_data)
        return result
```

Step 4: Systematic migration
✅ Extracted shared behaviors into components
✅ Created strategy hierarchy for specific behaviors
✅ Implemented composition-based processor
✅ Maintained all existing functionality
✅ Preserved public API compatibility

Step 5: Comprehensive validation
✅ All payment methods work: TESTED
✅ Existing client code unchanged: BACKWARD COMPATIBLE
✅ New payment methods easy to add: EXTENSIBLE
✅ Shared behaviors reusable: MODULAR
✅ No performance degradation: OPTIMIZED

🎉 Composition Benefits:
- Flexibility: Easy to add new payment methods
- Maintainability: Shared behaviors centralized
- Testability: Components isolated and testable
- Reusability: Components usable elsewhere
- Extensibility: New behaviors easy to add
```

## Refactoring Patterns

### 🏗️ Structural Patterns
- **Extract Method**: Break large methods into smaller ones
- **Extract Class**: Move related functionality to new class
- **Inline Method/Class**: Combine simple methods/classes
- **Move Method/Field**: Relocate to more appropriate class

### 🔄 Behavioral Patterns
- **Replace Conditional with Polymorphism**: Use inheritance
- **Replace Inheritance with Composition**: Use delegation
- **Strategy Pattern**: Encapsulate algorithms
- **Observer Pattern**: Decouple dependencies

### 🎯 Optimization Patterns
- **Split Temporary Variable**: Separate variable usages
- **Remove Assignments to Parameters**: Improve clarity
- **Replace Method with Method Object**: Complex algorithms
- **Substitute Algorithm**: Better implementation

## Safety Mechanisms

### 🔒 Multi-Level Validation
Ensures correctness at every level:
```
1. Syntax validation: Code compiles/imports
2. Unit tests: Individual components work
3. Integration tests: Components work together
4. Regression tests: Existing behavior preserved
5. Performance tests: No degradation
```

### 🔄 Rollback Capability
Safe failure handling:
```
1. Git checkpoint before refactoring
2. Step-by-step validation
3. Immediate rollback on failure
4. Detailed change tracking
5. Recovery procedures documented
```

### 📊 Continuous Monitoring
Real-time progress tracking:
```
- Test results at each step
- Complexity metrics
- Code coverage changes
- Performance benchmarks
- Quality gate validation
```

## Configuration Options

**Refactoring Scope**:
- `--method-level`: Function/method extraction
- `--class-level`: Class structure changes
- `--architecture-level`: System-wide changes
- `--pattern-level`: Design pattern application

**Safety Level**:
- `--conservative`: Maximum safety checks
- `--balanced`: Standard safety (recommended)
- `--aggressive`: Faster execution, less validation

**Validation Depth**:
- `--syntax-only`: Basic compilation checks
- `--unit-tests`: Component-level testing
- `--full-validation`: Complete test suite
- `--performance-check`: Include performance validation

## Integration with Development

**TDD Integration**:
```
1. Write tests for desired behavior
2. /refactoring --with-tests
3. Ensure all tests pass
4. Refactor with confidence
```

**CI/CD Pipeline**:
```
1. Automated refactoring checks
2. Safety validation gates
3. Performance benchmarks
4. Quality metrics tracking
```

**Code Review Process**:
```
1. Refactoring plan review
2. Safety mechanism validation
3. Results verification
4. Post-refactoring review
```

## Quality Metrics

### Complexity Reduction
Measure improvement:
```
Before: Cyclomatic complexity 25
After: Cyclomatic complexity 12
Improvement: 52% reduction
```

### Maintainability Improvement
Assess long-term benefits:
```
Before: Method length 150 lines
After: Methods average 20 lines
Improvement: Better separation of concerns
```

### Testability Enhancement
Improve testing capability:
```
Before: 65% test coverage
After: 87% test coverage
Improvement: 22% increase
```

## Best Practices

### 1. Plan Thoroughly
- Analyze current structure
- Identify improvement opportunities
- Assess risks and dependencies
- Design target architecture

### 2. Validate Continuously
- Test at every step
- Monitor quality metrics
- Check performance impact
- Ensure behavior preservation

### 3. Document Changes
- Update documentation
- Document rationale
- Record design decisions
- Update comments

### 4. Iterate Gradually
- Small, incremental changes
- Frequent validation
- Easy rollback capability
- Continuous improvement

## Common Challenges

### Challenge 1: Complex Dependencies
**Solution**: Map dependencies thoroughly, refactor incrementally

### Challenge 2: Hidden Behavior
**Solution**: Comprehensive testing, edge case validation

### Challenge 3: Performance Impact
**Solution**: Benchmark before/after, optimize carefully

### Challenge 4: Team Coordination
**Solution**: Clear communication, incremental rollout

## Success Criteria

### Technical Success
- All tests pass
- No performance degradation
- Code quality improved
- Maintainability enhanced

### Business Success
- Development velocity increased
- Bug rate decreased
- Feature delivery faster
- Technical debt reduced

## Token Efficiency

- Simple refactoring: ~800 tokens
- Medium complexity: ~1,200 tokens
- Complex architectural: ~2,000 tokens
- Validation and testing: ~400 tokens

## Related Skills

- `development/lean-plan` - Plan refactoring approach
- `development/quick-test-runner` - Validate changes quickly
- `analysis/code/dead-code-hunter` - Clean up after refactoring
- `git/diff-summariser` - Review refactoring changes

---

**Ready to refactor safely?** Just tell Claude: "Refactor this code" or "Extract this functionality"!