# Contributing Guidelines

## Project Structure

This project follows a highly modular structure. When contributing, please maintain this organization:

- **src/core/**: Core business logic only
- **src/config/**: Configuration management
- **src/utils/**: Generic, reusable utilities
- **src/media_management/**: Media-specific functionality
- **examples/**: Practical usage examples
- **tests/**: Test suites (unit and integration)
- **docs/**: Documentation

## Code Standards

### Modularity
- One class per file (unless tightly coupled)
- Single responsibility principle
- Clear module boundaries
- Reusable components

### Documentation
- Docstrings for all public APIs
- Type hints for parameters and return values
- Usage examples in docstrings
- Update docs/ when adding features

### Error Handling
- Use try-catch for external operations
- Log errors with context
- Return meaningful error messages
- Don't suppress exceptions silently

### Testing
- Add unit tests for new functionality
- Use mocks for AWS services
- Follow existing test patterns
- Maintain >80% code coverage

### Code Quality
- Follow PEP 8 style guide
- Use meaningful variable names
- Keep functions small (<50 lines)
- Add comments for complex logic

## Pull Request Process

1. Create a feature branch
2. Implement changes following code standards
3. Add/update tests
4. Update documentation
5. Ensure all tests pass
6. Submit PR with clear description

## Adding New Modules

When adding new modules:

1. Choose the appropriate directory (core, utils, etc.)
2. Create `__init__.py` with exports
3. Add comprehensive docstrings
4. Include unit tests
5. Update API_REFERENCE.md
6. Add usage example if applicable

## Questions?

Open an issue for:
- Bug reports
- Feature requests
- Documentation improvements
- General questions
