# 🔍 ESQL Code Analyzer - SonarQube Style

A comprehensive code quality analyzer for IBM App Connect Enterprise (ACE) and Integration Bus (IIB) ESQL files, implementing SonarQube-style analysis rules.

## 🎯 Overview

This analyzer performs static code analysis on ESQL files to identify:
- **Security vulnerabilities** (hardcoded credentials, SQL injection risks)
- **Bugs** (empty error handling, missing null checks, unused variables)
- **Code smells** (magic numbers, commented code, complex functions)
- **Performance issues** (string concatenation in loops, inefficient algorithms)
- **Style violations** (naming conventions, formatting, typos)

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses Python standard library only)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/jorlin2022/IIBAppRepo.git
cd IIBAppRepo
```

2. Make the analyzer executable:
```bash
chmod +x esql_analyzer.py
```

### Usage

#### Basic Analysis

Analyze all ESQL files in the current directory:
```bash
python esql_analyzer.py .
```

Analyze a specific directory:
```bash
python esql_analyzer.py /path/to/esql/files
```

#### Output

The analyzer generates three report formats in the `analysis_reports/` directory:

1. **JSON Report** - Machine-readable format for CI/CD integration
2. **Markdown Report** - Human-readable format for documentation
3. **HTML Report** - Interactive web-based report with visualizations

Example output:
```
================================================================================
ESQL Code Analyzer - SonarQube Style Analysis
================================================================================

Found 3 ESQL files to analyze...
Analyzing: FileNodeTest/FileTransfer_Compute.esql
Analyzing: FileTransferIndependent/FileTransfer_Compute.esql
Analyzing: SFTPApplication/SFTPSampleMsgFlow_Compute.esql

JSON report saved: analysis_reports/esql_analysis_20260401_170714.json
Markdown report saved: analysis_reports/esql_analysis_20260401_170714.md
HTML report saved: analysis_reports/esql_analysis_20260401_170714.html

================================================================================
Analysis Complete!
================================================================================
Files Analyzed: 3
Lines Analyzed: 72
Total Issues: 33

Issues by Severity:
  CRITICAL: 0
  HIGH: 0
  MEDIUM: 0
  LOW: 33
```

## 📋 Analysis Rules

The analyzer implements 14 comprehensive rules:

| Rule ID | Rule Name | Category | Severity | Description |
|---------|-----------|----------|----------|-------------|
| ESQL001 | Magic Number | Code Smell | MEDIUM | Detects numeric literals that should be constants |
| ESQL002 | Hardcoded Credentials | Security | CRITICAL | Identifies hardcoded passwords, API keys, tokens |
| ESQL003 | SQL Injection Risk | Security | CRITICAL | Detects string concatenation in SQL statements |
| ESQL004 | Empty Block | Bug | HIGH | Finds empty BEGIN/END blocks |
| ESQL005 | Commented Code | Code Smell | LOW | Identifies commented-out code |
| ESQL006 | Poor Naming Convention | Style | LOW | Checks for single-letter variable names |
| ESQL007 | Unused Variable | Code Smell | MEDIUM | Detects declared but unused variables |
| ESQL008 | String Concatenation in Loop | Performance | MEDIUM | Identifies inefficient string operations |
| ESQL009 | Missing Null Check | Bug | HIGH | Detects field access without null checks |
| ESQL010 | Incomplete Error Handling | Bug | MEDIUM | Checks for proper exception handling |
| ESQL011 | High Complexity | Code Smell | MEDIUM | Identifies overly complex code |
| ESQL012 | Redundant Code | Code Smell | HIGH | Detects duplicate or unnecessary code |
| ESQL013 | Inconsistent Spacing | Style | LOW | Checks for formatting consistency |
| ESQL014 | Typo Detection | Style | LOW | Identifies common spelling mistakes |

## 🔧 Configuration

### Customizing Rules

You can modify the analyzer to add custom rules or adjust severity levels:

```python
# In esql_analyzer.py

def _check_custom_rule(self, file: str, line_num: int, line: str) -> List[Issue]:
    """Add your custom rule here"""
    issues = []
    
    # Your custom logic
    if 'YOUR_PATTERN' in line:
        issues.append(Issue(
            file=file,
            line=line_num,
            column=1,
            severity=Severity.HIGH.value,
            category=Category.BUG.value,
            rule_id="ESQL015",
            rule_name="Custom Rule",
            message="Your custom message",
            code_snippet=line.strip(),
            suggestion="Your suggestion"
        ))
    
    return issues
```

### Severity Levels

- **CRITICAL** - Security vulnerabilities requiring immediate attention
- **HIGH** - Bugs that could cause runtime errors or data corruption
- **MEDIUM** - Code smells and performance issues
- **LOW** - Style violations and minor improvements
- **INFO** - Informational messages

## 🔄 CI/CD Integration

### GitHub Actions

Create `.github/workflows/esql-analysis.yml`:

```yaml
name: ESQL Code Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Run Analysis
      run: python esql_analyzer.py .
    - name: Upload Reports
      uses: actions/upload-artifact@v3
      with:
        name: analysis-reports
        path: analysis_reports/
```

### Jenkins

```groovy
stage('ESQL Analysis') {
    steps {
        sh 'python3 esql_analyzer.py .'
        publishHTML([
            reportDir: 'analysis_reports',
            reportFiles: 'esql_analysis_*.html',
            reportName: 'ESQL Analysis'
        ])
    }
}
```

### Pre-commit Hook

```bash
#!/bin/bash
python esql_analyzer.py .
CRITICAL=$(python -c "import json; print(json.load(open('analysis_reports/esql_analysis_*.json'))['issues_by_severity']['CRITICAL'])")
if [ "$CRITICAL" -gt 0 ]; then
    echo "❌ Commit blocked: Critical issues found"
    exit 1
fi
```

## 📊 Report Formats

### JSON Report

Machine-readable format containing:
- Analysis metadata (timestamp, files analyzed, lines analyzed)
- Issue counts by severity and category
- Detailed issue list with file paths, line numbers, and suggestions

### Markdown Report

Human-readable format with:
- Executive summary
- Issues grouped by severity
- Code snippets and suggestions
- Easy to include in documentation

### HTML Report

Interactive web-based report featuring:
- Visual charts and graphs
- Color-coded severity indicators
- Searchable and filterable issue list
- Professional presentation for stakeholders

## 🎯 Best Practices

### Security

✅ **DO:**
- Store credentials in environment variables
- Use parameterized queries
- Validate all input data
- Implement proper error handling

❌ **DON'T:**
- Hardcode passwords or API keys
- Concatenate user input into SQL
- Log sensitive information
- Expose internal errors

### Performance

✅ **DO:**
- Use efficient algorithms
- Minimize database calls
- Cache frequently accessed data
- Profile performance-critical code

❌ **DON'T:**
- Concatenate strings in loops
- Make unnecessary queries
- Load entire datasets into memory
- Use inefficient searches

### Maintainability

✅ **DO:**
- Use descriptive names
- Add meaningful comments
- Keep functions small and focused
- Follow consistent formatting

❌ **DON'T:**
- Use single-letter variables
- Leave commented code
- Create complex functions
- Mix tabs and spaces

## 🛠️ Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError`
```bash
# Solution: Ensure Python 3.7+ is installed
python --version
```

**Issue:** No ESQL files found
```bash
# Solution: Check file extensions and directory path
ls -la *.esql
```

**Issue:** Permission denied
```bash
# Solution: Make analyzer executable
chmod +x esql_analyzer.py
```

## 📈 Metrics and KPIs

Track these metrics to measure code quality:

- **Code Quality Score** - Overall health indicator (0-100)
- **Technical Debt** - Estimated time to fix all issues
- **Issue Density** - Issues per 1000 lines of code
- **Severity Distribution** - Breakdown by severity level
- **Category Distribution** - Breakdown by issue category

## 🤝 Contributing

We welcome contributions! To add new rules:

1. Fork the repository
2. Create a feature branch
3. Add your rule in `esql_analyzer.py`
4. Add tests for your rule
5. Update documentation
6. Submit a pull request

### Adding a New Rule

```python
def _check_your_rule(self, file: str, line_num: int, line: str) -> List[Issue]:
    """
    Check for [your rule description]
    
    Args:
        file: File path
        line_num: Line number
        line: Line content
        
    Returns:
        List of issues found
    """
    issues = []
    
    # Your detection logic here
    if condition:
        issues.append(Issue(
            file=file,
            line=line_num,
            column=1,
            severity=Severity.MEDIUM.value,
            category=Category.CODE_SMELL.value,
            rule_id="ESQL0XX",
            rule_name="Your Rule Name",
            message="Description of the issue",
            code_snippet=line.strip(),
            suggestion="How to fix it"
        ))
    
    return issues
```

## 📚 Resources

- [IBM ACE Documentation](https://www.ibm.com/docs/en/app-connect)
- [ESQL Language Reference](https://www.ibm.com/docs/en/app-connect/12.0?topic=reference-esql)
- [SonarQube Rules](https://rules.sonarsource.com/)
- [Code Quality Best Practices](https://www.sonarsource.com/learn/code-quality/)

## 📞 Support

- **Issues:** Report bugs on GitHub Issues
- **Questions:** Contact the ACE Modernization team
- **Documentation:** See `COMPREHENSIVE_ANALYSIS_REPORT.md`

## 📄 License

This analyzer is part of the IIBAppRepo project.

## 🙏 Acknowledgments

- Based on SonarQube code quality principles
- Inspired by sonar-esql-plugin
- Built for the ACE Modernization initiative

---

**Version:** 1.0.0  
**Last Updated:** April 1, 2026  
**Maintainer:** ACE Modernization Team

---

*For detailed analysis results, see `COMPREHENSIVE_ANALYSIS_REPORT.md`*