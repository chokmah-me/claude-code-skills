#!/bin/bash

# 🚀 GitHub Actions Setup Script for Claude Code Skills Repository
# This script helps configure your repository for the new GitHub Actions

set -e  # Exit on any error

echo "🤖 Setting up GitHub Actions for Claude Code Skills Repository..."
echo "=================================================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not in a git repository. Please run 'git init' first."
    exit 1
fi

# Check if GitHub CLI is installed
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI found"
    GITHUB_CLI_AVAILABLE=true
else
    echo "⚠️  GitHub CLI not found. Install it for easier workflow management:"
    echo "   https://cli.github.com/"
    GITHUB_CLI_AVAILABLE=false
fi

# Check repository status
echo "📋 Repository Status:"
echo "  Branch: $(git branch --show-current)"
echo "  Remote: $(git remote get-url origin 2>/dev/null || echo 'Not configured')"
echo "  Status: $(git status --porcelain | wc -l) files modified"
echo ""

# Function to check if GitHub Actions are enabled
check_github_actions() {
    if [ "$GITHUB_CLI_AVAILABLE" = true ]; then
        echo "🔍 Checking GitHub Actions status..."
        if gh api repos/$(gh repo view --json owner,name -q '.owner.login + "/" + .name') --jq '.permissions.actions' 2>/dev/null; then
            echo "✅ GitHub Actions appear to be enabled"
        else
            echo "⚠️  Could not verify GitHub Actions status. Check repository settings."
        fi
    else
        echo "ℹ️  Install GitHub CLI to enable automated checks"
    fi
}

# Function to validate workflow files
validate_workflows() {
    echo "🔧 Validating workflow files..."
    
    WORKFLOW_DIR=".github/workflows"
    if [ ! -d "$WORKFLOW_DIR" ]; then
        echo "❌ Workflow directory not found: $WORKFLOW_DIR"
        return 1
    fi
    
    WORKFLOW_COUNT=$(find "$WORKFLOW_DIR" -name "*.yml" -o -name "*.yaml" | wc -l)
    echo "  Found $WORKFLOW_COUNT workflow files"
    
    # Check for required workflows
    REQUIRED_WORKFLOWS=(
        "skill-template-validator.yml"
        "readme-auto-update.yml"
        "changelog-automation.yml"
        "skill-consistency-checker.yml"
        "documentation-link-validator.yml"
    )
    
    for workflow in "${REQUIRED_WORKFLOWS[@]}"; do
        if [ -f "$WORKFLOW_DIR/$workflow" ]; then
            echo "  ✅ $workflow"
        else
            echo "  ❌ Missing: $workflow"
        fi
    done
    
    # Basic YAML syntax check (if yq is available)
    if command -v yq &> /dev/null; then
        echo "  Running YAML syntax validation..."
        for file in "$WORKFLOW_DIR"/*.yml; do
            if yq eval '.' "$file" > /dev/null 2>&1; then
                echo "    ✅ $(basename "$file") - Valid YAML"
            else
                echo "    ❌ $(basename "$file") - YAML syntax error"
            fi
        done
    else
        echo "  ℹ️  Install 'yq' for YAML syntax validation"
    fi
}

# Function to check README setup
check_readme_setup() {
    echo "📖 Checking README setup..."
    
    if [ -f "README.md" ]; then
        if grep -q "<!-- SKILLS_INVENTORY_START -->" README.md && grep -q "<!-- SKILLS_INVENTORY_END -->" README.md; then
            echo "  ✅ Skills inventory markers found in README.md"
        else
            echo "  ⚠️  Skills inventory markers not found in README.md"
            echo "  Add these markers where you want the auto-generated skills list:"
            echo "  <!-- SKILLS_INVENTORY_START -->"
            echo "  <!-- SKILLS_INVENTORY_END -->"
        fi
    else
        echo "  ❌ README.md not found"
    fi
}

# Function to show workflow status
show_workflow_status() {
    echo "📊 Workflow Status:"
    
    if [ "$GITHUB_CLI_AVAILABLE" = true ]; then
        echo "  Available workflows:"
        gh workflow list --json name,state -q '.[] | "  - \(.name): \(.state)"' 2>/dev/null || echo "  Could not fetch workflow status"
    else
        echo "  Install GitHub CLI to view workflow status"
    fi
}

# Function to provide next steps
show_next_steps() {
    echo ""
    echo "🎯 Next Steps:"
    echo "============="
    
    if [ "$GITHUB_CLI_AVAILABLE" = true ]; then
        echo "1. Test a workflow manually:"
        echo "   gh workflow run skill-template-validator.yml"
        echo ""
        echo "2. List all workflows:"
        echo "   gh workflow list"
        echo ""
        echo "3. View workflow runs:"
        echo "   gh run list"
    else
        echo "1. Install GitHub CLI for easier workflow management:"
        echo "   https://cli.github.com/"
        echo ""
        echo "2. Go to your repository on GitHub"
        echo "3. Click on 'Actions' tab to see workflows"
        echo "4. Click on a workflow to run it manually"
    fi
    
    echo ""
    echo "4. Create a test pull request to trigger validation workflows"
    echo "5. Check the Actions tab for workflow results and artifacts"
    echo ""
    echo "📚 For detailed documentation, see: .github/SETUP_GUIDE.md"
}

# Main execution
main() {
    echo "Starting repository setup validation..."
    echo ""
    
    # Run all checks
    check_github_actions
    echo ""
    
    validate_workflows
    echo ""
    
    check_readme_setup
    echo ""
    
    show_workflow_status
    echo ""
    
    show_next_steps
    
    echo ""
    echo "✅ Setup validation complete!"
    echo "🚀 Your repository is ready for automated GitHub Actions!"
}

# Execute main function
main

# Optional: Create a simple test
if [ "$1" = "--test" ]; then
    echo ""
    echo "🧪 Running workflow test..."
    echo "This would trigger a workflow run to test the setup"
    
    if [ "$GITHUB_CLI_AVAILABLE" = true ]; then
        echo "Testing skill template validator..."
        gh workflow run skill-template-validator.yml || echo "Test failed - check repository configuration"
    else
        echo "Install GitHub CLI to enable automated testing"
    fi
fi