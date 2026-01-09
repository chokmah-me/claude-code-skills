#!/usr/bin/env python3
"""
Test Runner for Claude Code Skills

Convenient wrapper for running different test suites.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run command and display results."""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}\n")

    result = subprocess.run(cmd, shell=True)

    if result.returncode == 0:
        print(f"\n✅ {description} - PASSED")
    else:
        print(f"\n❌ {description} - FAILED")

    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="Run Claude Code Skills test suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py --all                 # Run all tests
  python run_tests.py --install             # Run installation tests
  python run_tests.py --meta                # Run meta-skills tests
  python run_tests.py --validation          # Run validation tests
  python run_tests.py --phase2              # Run Phase 2 tests
  python run_tests.py --phase3              # Run Phase 3 tests
  python run_tests.py --coverage            # Run with coverage report
        """
    )

    parser.add_argument('--all', action='store_true',
                       help='Run all test suites')
    parser.add_argument('--install', action='store_true',
                       help='Run installation tests (enhanced)')
    parser.add_argument('--meta', action='store_true',
                       help='Run meta-skills execution tests')
    parser.add_argument('--validation', action='store_true',
                       help='Run skill validation tests')
    parser.add_argument('--phase2', action='store_true',
                       help='Run Phase 2 tests (install enhanced)')
    parser.add_argument('--phase3', action='store_true',
                       help='Run Phase 3 tests (meta-skills)')
    parser.add_argument('--coverage', action='store_true',
                       help='Generate coverage report')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')

    args = parser.parse_args()

    # Check if pytest is installed
    try:
        subprocess.run([sys.executable, '-m', 'pytest', '--version'],
                      capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print("❌ pytest not installed. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install',
                       '-r', 'tests/requirements.txt'])

    results = []
    verbose_flag = '-v' if args.verbose else ''

    # Run specific test suites
    if args.all or args.install or args.phase2:
        code = run_command(
            f"{sys.executable} -m pytest tests/test_install_enhanced.py {verbose_flag}",
            "Phase 2: Enhanced Installation Tests"
        )
        results.append(('Installation Tests', code))

    if args.all or args.meta or args.phase3:
        code = run_command(
            f"{sys.executable} -m pytest tests/test_meta_skills.py {verbose_flag}",
            "Phase 3: Meta-Skills Execution Tests"
        )
        results.append(('Meta-Skills Tests', code))

    if args.all or args.validation:
        code = run_command(
            f"{sys.executable} tests/validate_skills.py",
            "Skill Validation Tests"
        )
        results.append(('Validation Tests', code))

        code = run_command(
            f"{sys.executable} tests/test_skills.py",
            "Basic Functionality Tests"
        )
        results.append(('Functionality Tests', code))

    # Coverage report
    if args.coverage:
        code = run_command(
            f"{sys.executable} -m pytest tests/ --cov=. --cov-report=html --cov-report=term {verbose_flag}",
            "Full Test Suite with Coverage"
        )
        results.append(('Coverage Report', code))

        if code == 0:
            print("\n📊 Coverage report generated: htmlcov/index.html")

    # If no specific test selected, show help
    if not any([args.all, args.install, args.meta, args.validation,
                args.phase2, args.phase3, args.coverage]):
        parser.print_help()
        return 0

    # Print summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}\n")

    total_tests = len(results)
    passed_tests = sum(1 for _, code in results if code == 0)
    failed_tests = total_tests - passed_tests

    for test_name, code in results:
        status = "✅ PASS" if code == 0 else "❌ FAIL"
        print(f"{status} {test_name}")

    print(f"\nTotal: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")

    if failed_tests > 0:
        print(f"\n❌ {failed_tests} test suite(s) failed")
        return 1
    else:
        print("\n✅ All test suites passed!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
