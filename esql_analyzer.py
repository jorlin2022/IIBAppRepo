#!/usr/bin/env python3
"""
ESQL Code Analyzer - SonarQube Style Analysis
Implements comprehensive code quality checks for IBM ACE/IIB ESQL files
Based on sonar-esql-plugin rules and best practices
"""

import re
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from enum import Enum


class Severity(Enum):
    """Issue severity levels"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class Category(Enum):
    """Issue categories"""
    SECURITY = "Security"
    BUG = "Bug"
    CODE_SMELL = "Code Smell"
    PERFORMANCE = "Performance"
    STYLE = "Style"


@dataclass
class Issue:
    """Represents a code quality issue"""
    file: str
    line: int
    column: int
    severity: str
    category: str
    rule_id: str
    rule_name: str
    message: str
    code_snippet: str
    suggestion: str = ""
    
    def to_dict(self):
        return asdict(self)


class ESQLAnalyzer:
    """Comprehensive ESQL code analyzer"""
    
    def __init__(self):
        self.issues: List[Issue] = []
        self.files_analyzed = 0
        self.lines_analyzed = 0
        
    def analyze_file(self, file_path: str) -> List[Issue]:
        """Analyze a single ESQL file"""
        file_issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                self.files_analyzed += 1
                self.lines_analyzed += len(lines)
                
                for line_num, line in enumerate(lines, 1):
                    # Run all analysis rules
                    file_issues.extend(self._check_magic_numbers(file_path, line_num, line))
                    file_issues.extend(self._check_hardcoded_credentials(file_path, line_num, line))
                    file_issues.extend(self._check_sql_injection(file_path, line_num, line))
                    file_issues.extend(self._check_empty_blocks(file_path, line_num, line))
                    file_issues.extend(self._check_commented_code(file_path, line_num, line))
                    file_issues.extend(self._check_naming_conventions(file_path, line_num, line))
                    file_issues.extend(self._check_unused_variables(file_path, line_num, line, lines))
                    file_issues.extend(self._check_string_concatenation(file_path, line_num, line))
                    file_issues.extend(self._check_null_checks(file_path, line_num, line))
                    file_issues.extend(self._check_error_handling(file_path, line_num, line))
                    file_issues.extend(self._check_complexity(file_path, line_num, line))
                    file_issues.extend(self._check_duplicate_code(file_path, line_num, line))
                    file_issues.extend(self._check_formatting(file_path, line_num, line))
                    file_issues.extend(self._check_typos(file_path, line_num, line))
                    
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            
        self.issues.extend(file_issues)
        return file_issues
    
    def _check_magic_numbers(self, file: str, line_num: int, line: str) -> List[Issue]:
        """Check for magic numbers that should be constants"""
        issues = []
        # Look for numeric literals (excluding 0, 1, -1 which are common)
        pattern = r'\b(?<![\w.])((?:[2-9]|\d{2,})(?:\.\d+)?)\b(?![\w.])'
        matches = re.finditer(pattern, line)
        
        for match in matches:
            # Skip if it's part of a declaration or in comments
            if 'DECLARE' in line or '--' in line[:match.start()]:
                continue
                
            issues.append(Issue(
                file=file,
                line=line_num,
                column=match.start() + 1,
                severity=Severity.MEDIUM.value,
                category=Category.CODE_SMELL.value,
                rule_id="ESQL001",
                rule_name="Magic Number",
                message=f"Magic number '{match.group(1)}' should be replaced with a named constant",
                code_snippet=line.strip(),
                suggestion="Declare a constant: DECLARE MY_CONSTANT CONSTANT INTEGER {value};"
            ))
        
        return issues
    
    def _check_hardcoded_credentials(self, file: str, line_num: int, line: str) -> List[Issue]:
        """Check for hardcoded credentials"""
        issues = []
        patterns = [
            (r'password\s*=\s*["\']([^"\']+)["\']', 'password'),
            (r'pwd\s*=\s*["\']([^"\']+)["\']', 'password'),
            (r'apikey\s*=\s*["\']([^"\']+)["\']', 'API key'),
            (r'api_key\s*=\s*["\']([^"\']+)["\']', 'API key'),
            (r'secret\s*=\s*["\']([^"\']+)["\']', 'secret'),
            (r'token\s*=\s*["\']([^"\']+)["\']', 'token'),
        ]
        
        for pattern, cred_type in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                issues.append(Issue(
                    file=file,
                    line=line_num,
                    column=1,
                    severity=Severity.CRITICAL.value,
                    category=Category.SECURITY.value,
                    rule_id="ESQL002",
                    rule_name="Hardcoded Credentials",
                    message=f"Hardcoded {cred_type} detected - security vulnerability",
                    code_snippet=line.strip(),
                    suggestion="Use environment variables or secure vault: SET password = Environment.Variables.PASSWORD;"
                ))
        
        return issues
    
    def _check_sql_injection(self, file: str, line_num: int, line: str) -> List[Issue]:
        """Check for potential SQL injection vulnerabilities"""
        issues = []
        
        # Check for string concatenation in SQL statements
        if re.search(r'(PASSTHRU|DATABASE)\s*\(', line, re.IGNORECASE):
            if '||' in line or '+' in line:
                issues.append(Issue(
                    file=file,
                    line=line_num,
                    column=1,
                    severity=Severity.CRITICAL.value,
                    category=Category.SECURITY.value,
                    rule_id="ESQL003",
                    rule_name="SQL Injection Risk",
                    message="Potential SQL injection - string concatenation in SQL statement",
                    code_snippet=line.strip(),
                    suggestion="Use parameterized queries with ? placeholders"
                ))
        
        return issues
    
    def _check_empty_blocks(self, file: str, line_num: int, line: str) -> List[Issue]:
        """Check for empty BEGIN/END blocks"""
        issues = []
        
        if re.search(r'BEGIN\s*END', line, re.IGNORECASE):
            issues.append(Issue(
                file=file,
                line=line_num,
                column=1,
                severity=Severity.HIGH.value,
                category=Category.BUG.value,
                rule_id="ESQL004",
                rule_name="Empty Block",
                message="Empty BEGIN/END block - likely unfinished error handling",
                code_snippet=line.strip(),
                suggestion="Add proper error handling or remove empty block"
            ))
        
        return issues
    
    def _check_commented_code(self, file: str, line_num: int, line: str) -> List[Issue]:
        """Check for commented out code"""
        issues = []
        
        if line.strip().startswith('--'):
            # Check if it looks like code (has keywords)
            code_keywords = ['SET', 'DECLARE', 'CALL', 'CREATE', 'IF', 'WHILE', 'FOR']
            if any(keyword in line.upper() for keyword in code_keywords):
                issues.append(Issue(
                    file=file,
                    line=line_num,
                    column=1,
                    severity=Severity.LOW.value,
                    category=Category.CODE_SMELL.value,
                    rule_id="ESQL005",
                    rule_name="Commented Code",
                    message="Commented out code should be removed",
                    code_snippet=line.strip(),
                    suggestion="Remove commented code or use version control"
                ))
        
        return issues
    
    def _check_naming_conventions(self, file: str, line_num: int, line: str) -> List[Issue]:
        """Check naming conventions"""
        issues = []
        
        # Check for single letter variable names (except I, J in loops)
        if 'DECLARE' in line:
            match = re.search(r'DECLARE\s+([A-Z])\s+', line)
            if match and match.group(1) not in ['I', 'J', 'K']:
                issues.append(Issue(
                    file=file,
                    line=line_num,
                    column=match.start() + 1,
                    severity=Severity.LOW.value,
                    category=Category.STYLE.value,
                    rule_id="ESQL006",
                    rule_name="Poor Naming Convention",
                    message=f"Single letter variable '{match.group(1)}' should have descriptive name",
                    code_snippet=line.strip(),
                    suggestion="Use descriptive names: DECLARE messageCount INTEGER;"
                ))
        
        return issues
    
    def _check_unused_variables(self, file: str, line_num: int, line: str, all_lines: List[str]) -> List[Issue]:
        """Check for unused variables"""
        issues = []
        
        # Simple check: if variable is declared but never used after declaration
        if 'DECLARE' in line:
            match = re.search(r'DECLARE\s+(\w+)\s+', line)
            if match:
                var_name = match.group(1)
                # Check if variable is used in subsequent lines
                used = False
                for future_line in all_lines[line_num:]:
                    if var_name in future_line and 'DECLARE' not in future_line:
                        used = True
                        break
                
                if not used:
                    issues.append(Issue(
                        file=file,
                        line=line_num,
                        column=match.start() + 1,
                        severity=Severity.MEDIUM.value,
                        category=Category.CODE_SMELL.value,
                        rule_id="ESQL007",
                        rule_name="Unused Variable",
                        message=f"Variable '{var_name}' is declared but never used",
                        code_snippet=line.strip(),
                        suggestion="Remove unused variable declaration"
                    ))
        
        return issues
    
    def _check_string_concatenation(self, file: str, line_num: int, line: str) -> List[Issue]:
        """Check for inefficient string concatenation in loops"""
        issues = []
        
        # Check if we're in a loop and doing string concatenation
        if ('WHILE' in line or 'FOR' in line) and '||' in line:
            issues.append(Issue(
                file=file,
                line=line_num,
                column=1,
                severity=Severity.MEDIUM.value,
                category=Category.PERFORMANCE.value,
                rule_id="ESQL008",
                rule_name="String Concatenation in Loop",
                message="String concatenation in loop can cause performance issues",
                code_snippet=line.strip(),
                suggestion="Consider using ESQL string functions or building array first"
            ))
        
        return issues
    
    def _check_null_checks(self, file: str, line_num: int, line: str) -> List[Issue]:
        """Check for missing null checks"""
        issues = []
        
        # Check for direct field access without null check
        if re.search(r'InputRoot\.\w+\.\w+', line) and 'IS NULL' not in line and 'IF' not in line:
            issues.append(Issue(
                file=file,
                line=line_num,
                column=1,
                severity=Severity.HIGH.value,
                category=Category.BUG.value,
                rule_id="ESQL009",
                rule_name="Missing Null Check",
                message="Direct field access without null check can cause runtime errors",
                code_snippet=line.strip(),
                suggestion="Add null check: IF InputRoot.Field IS NOT NULL THEN"
            ))
        
        return issues
    
    def _check_error_handling(self, file: str, line_num: int, line: str) -> List[Issue]:
        """Check for proper error handling"""
        issues = []
        
        # Check for THROW without proper error information
        if 'THROW' in line and 'USER EXCEPTION' not in line:
            issues.append(Issue(
                file=file,
                line=line_num,
                column=1,
                severity=Severity.MEDIUM.value,
                category=Category.BUG.value,
                rule_id="ESQL010",
                rule_name="Incomplete Error Handling",
                message="THROW statement should include USER EXCEPTION with details",
                code_snippet=line.strip(),
                suggestion="Use: THROW USER EXCEPTION MESSAGE 2951 VALUES('Error details');"
            ))
        
        return issues
    
    def _check_complexity(self, file: str, line_num: int, line: str) -> List[Issue]:
        """Check for high cyclomatic complexity"""
        issues = []
        
        # Count decision points in a line (simplified)
        decision_keywords = ['IF', 'WHILE', 'FOR', 'CASE', 'WHEN']
        complexity = sum(1 for keyword in decision_keywords if keyword in line.upper())
        
        if complexity > 3:
            issues.append(Issue(
                file=file,
                line=line_num,
                column=1,
                severity=Severity.MEDIUM.value,
                category=Category.CODE_SMELL.value,
                rule_id="ESQL011",
                rule_name="High Complexity",
                message=f"Line has high complexity ({complexity} decision points)",
                code_snippet=line.strip(),
                suggestion="Consider breaking into smaller functions"
            ))
        
        return issues
    
    def _check_duplicate_code(self, file: str, line_num: int, line: str) -> List[Issue]:
        """Check for duplicate code patterns"""
        issues = []
        
        # Check for redundant operations
        if 'CopyMessageHeaders' in line and 'CopyEntireMessage' in line:
            issues.append(Issue(
                file=file,
                line=line_num,
                column=1,
                severity=Severity.HIGH.value,
                category=Category.CODE_SMELL.value,
                rule_id="ESQL012",
                rule_name="Redundant Code",
                message="CopyMessageHeaders is redundant when CopyEntireMessage is called",
                code_snippet=line.strip(),
                suggestion="Remove CopyMessageHeaders() call - CopyEntireMessage() copies everything"
            ))
        
        return issues
    
    def _check_formatting(self, file: str, line_num: int, line: str) -> List[Issue]:
        """Check code formatting"""
        issues = []
        
        # Check for inconsistent spacing
        if re.search(r'\s{2,}', line) and not line.strip().startswith('--'):
            issues.append(Issue(
                file=file,
                line=line_num,
                column=1,
                severity=Severity.LOW.value,
                category=Category.STYLE.value,
                rule_id="ESQL013",
                rule_name="Inconsistent Spacing",
                message="Multiple consecutive spaces - use consistent formatting",
                code_snippet=line.strip(),
                suggestion="Use single space or proper indentation"
            ))
        
        return issues
    
    def _check_typos(self, file: str, line_num: int, line: str) -> List[Issue]:
        """Check for common typos"""
        issues = []
        
        # Common typos in comments or strings
        typos = {
            'recieve': 'receive',
            'occured': 'occurred',
            'seperator': 'separator',
            'sucessful': 'successful'
        }
        
        for typo, correction in typos.items():
            if typo in line.lower():
                issues.append(Issue(
                    file=file,
                    line=line_num,
                    column=line.lower().find(typo) + 1,
                    severity=Severity.LOW.value,
                    category=Category.STYLE.value,
                    rule_id="ESQL014",
                    rule_name="Typo",
                    message=f"Typo: '{typo}' should be '{correction}'",
                    code_snippet=line.strip(),
                    suggestion=f"Correct spelling: {correction}"
                ))
        
        return issues
    
    def analyze_directory(self, directory: str) -> Dict[str, Any]:
        """Analyze all ESQL files in directory"""
        esql_files = list(Path(directory).rglob('*.esql'))
        
        print(f"Found {len(esql_files)} ESQL files to analyze...")
        
        for esql_file in esql_files:
            print(f"Analyzing: {esql_file}")
            self.analyze_file(str(esql_file))
        
        return self.generate_summary()
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate analysis summary"""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'files_analyzed': self.files_analyzed,
            'lines_analyzed': self.lines_analyzed,
            'total_issues': len(self.issues),
            'issues_by_severity': {},
            'issues_by_category': {},
            'issues': [issue.to_dict() for issue in self.issues]
        }
        
        # Count by severity
        for severity in Severity:
            count = sum(1 for issue in self.issues if issue.severity == severity.value)
            summary['issues_by_severity'][severity.value] = count
        
        # Count by category
        for category in Category:
            count = sum(1 for issue in self.issues if issue.category == category.value)
            summary['issues_by_category'][category.value] = count
        
        return summary
    
    def save_json_report(self, output_file: str):
        """Save analysis results as JSON"""
        summary = self.generate_summary()
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        print(f"JSON report saved: {output_file}")
    
    def save_markdown_report(self, output_file: str):
        """Save analysis results as Markdown"""
        summary = self.generate_summary()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# ESQL Code Analysis Report\n\n")
            f.write(f"**Generated:** {summary['timestamp']}\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"- **Files Analyzed:** {summary['files_analyzed']}\n")
            f.write(f"- **Lines Analyzed:** {summary['lines_analyzed']}\n")
            f.write(f"- **Total Issues:** {summary['total_issues']}\n\n")
            
            f.write("## Issues by Severity\n\n")
            f.write("| Severity | Count |\n")
            f.write("|----------|-------|\n")
            for severity, count in summary['issues_by_severity'].items():
                f.write(f"| {severity} | {count} |\n")
            f.write("\n")
            
            f.write("## Issues by Category\n\n")
            f.write("| Category | Count |\n")
            f.write("|----------|-------|\n")
            for category, count in summary['issues_by_category'].items():
                f.write(f"| {category} | {count} |\n")
            f.write("\n")
            
            f.write("## Detailed Issues\n\n")
            
            # Group by severity
            for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']:
                severity_issues = [i for i in self.issues if i.severity == severity]
                if severity_issues:
                    f.write(f"### {severity} Severity Issues\n\n")
                    for issue in severity_issues:
                        f.write(f"#### {issue.rule_name} ({issue.rule_id})\n\n")
                        f.write(f"- **File:** `{issue.file}`\n")
                        f.write(f"- **Line:** {issue.line}\n")
                        f.write(f"- **Category:** {issue.category}\n")
                        f.write(f"- **Message:** {issue.message}\n")
                        f.write(f"- **Code:**\n```esql\n{issue.code_snippet}\n```\n")
                        if issue.suggestion:
                            f.write(f"- **Suggestion:** {issue.suggestion}\n")
                        f.write("\n")
        
        print(f"Markdown report saved: {output_file}")
    
    def save_html_report(self, output_file: str):
        """Save analysis results as HTML"""
        summary = self.generate_summary()
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESQL Code Analysis Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .summary-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .summary-card h3 {{
            margin: 0;
            font-size: 2em;
        }}
        .summary-card p {{
            margin: 5px 0 0 0;
            opacity: 0.9;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #3498db;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .issue {{
            margin: 20px 0;
            padding: 15px;
            border-left: 4px solid #3498db;
            background-color: #f8f9fa;
            border-radius: 4px;
        }}
        .issue.CRITICAL {{
            border-left-color: #e74c3c;
            background-color: #fee;
        }}
        .issue.HIGH {{
            border-left-color: #e67e22;
            background-color: #fef5e7;
        }}
        .issue.MEDIUM {{
            border-left-color: #f39c12;
            background-color: #fef9e7;
        }}
        .issue.LOW {{
            border-left-color: #3498db;
            background-color: #ebf5fb;
        }}
        .severity-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: bold;
            color: white;
        }}
        .severity-badge.CRITICAL {{
            background-color: #e74c3c;
        }}
        .severity-badge.HIGH {{
            background-color: #e67e22;
        }}
        .severity-badge.MEDIUM {{
            background-color: #f39c12;
        }}
        .severity-badge.LOW {{
            background-color: #3498db;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        .suggestion {{
            background-color: #d5f4e6;
            padding: 10px;
            border-radius: 4px;
            margin-top: 10px;
            border-left: 3px solid #27ae60;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 ESQL Code Analysis Report</h1>
        <p><strong>Generated:</strong> {summary['timestamp']}</p>
        
        <div class="summary">
            <div class="summary-card">
                <h3>{summary['files_analyzed']}</h3>
                <p>Files Analyzed</p>
            </div>
            <div class="summary-card">
                <h3>{summary['lines_analyzed']}</h3>
                <p>Lines Analyzed</p>
            </div>
            <div class="summary-card">
                <h3>{summary['total_issues']}</h3>
                <p>Total Issues</p>
            </div>
        </div>
        
        <h2>📊 Issues by Severity</h2>
        <table>
            <tr>
                <th>Severity</th>
                <th>Count</th>
            </tr>
"""
        
        for severity, count in summary['issues_by_severity'].items():
            html += f"""            <tr>
                <td><span class="severity-badge {severity}">{severity}</span></td>
                <td>{count}</td>
            </tr>
"""
        
        html += """        </table>
        
        <h2>📋 Issues by Category</h2>
        <table>
            <tr>
                <th>Category</th>
                <th>Count</th>
            </tr>
"""
        
        for category, count in summary['issues_by_category'].items():
            html += f"""            <tr>
                <td>{category}</td>
                <td>{count}</td>
            </tr>
"""
        
        html += """        </table>
        
        <h2>🔎 Detailed Issues</h2>
"""
        
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']:
            severity_issues = [i for i in self.issues if i.severity == severity]
            if severity_issues:
                html += f"""        <h3>{severity} Severity Issues</h3>
"""
                for issue in severity_issues:
                    html += f"""        <div class="issue {issue.severity}">
            <h4>{issue.rule_name} ({issue.rule_id})</h4>
            <p><strong>File:</strong> <code>{issue.file}</code></p>
            <p><strong>Line:</strong> {issue.line} | <strong>Category:</strong> {issue.category}</p>
            <p><strong>Message:</strong> {issue.message}</p>
            <p><strong>Code:</strong></p>
            <pre>{issue.code_snippet}</pre>
"""
                    if issue.suggestion:
                        html += f"""            <div class="suggestion">
                <strong>💡 Suggestion:</strong> {issue.suggestion}
            </div>
"""
                    html += """        </div>
"""
        
        html += """    </div>
</body>
</html>
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"HTML report saved: {output_file}")


def main():
    """Main execution function"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python esql_analyzer.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' not found")
        sys.exit(1)
    
    print("=" * 80)
    print("ESQL Code Analyzer - SonarQube Style Analysis")
    print("=" * 80)
    print()
    
    analyzer = ESQLAnalyzer()
    summary = analyzer.analyze_directory(directory)
    
    # Generate reports
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "analysis_reports"
    os.makedirs(output_dir, exist_ok=True)
    
    json_file = f"{output_dir}/esql_analysis_{timestamp}.json"
    md_file = f"{output_dir}/esql_analysis_{timestamp}.md"
    html_file = f"{output_dir}/esql_analysis_{timestamp}.html"
    
    analyzer.save_json_report(json_file)
    analyzer.save_markdown_report(md_file)
    analyzer.save_html_report(html_file)
    
    print()
    print("=" * 80)
    print("Analysis Complete!")
    print("=" * 80)
    print(f"Files Analyzed: {summary['files_analyzed']}")
    print(f"Lines Analyzed: {summary['lines_analyzed']}")
    print(f"Total Issues: {summary['total_issues']}")
    print()
    print("Issues by Severity:")
    for severity, count in summary['issues_by_severity'].items():
        print(f"  {severity}: {count}")
    print()
    print("Reports generated:")
    print(f"  - JSON: {json_file}")
    print(f"  - Markdown: {md_file}")
    print(f"  - HTML: {html_file}")
    print("=" * 80)


if __name__ == "__main__":
    main()

# Made with Bob
