#!/bin/bash
# Test script for Agentic AI Security System
# Creates safe test files to demonstrate detection

echo "=================================="
echo "Security System Test Script"
echo "=================================="
echo ""
echo "This script will create safe test files to demonstrate"
echo "the security system's detection capabilities."
echo ""
echo "Press Ctrl+C to stop the main system after seeing detections."
echo ""
echo "Starting in 3 seconds..."
sleep 3

# Create test directory
TEST_DIR=~/Downloads/security_test_$$
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

echo ""
echo "Test 1: Creating EICAR test file (industry standard test virus)"
echo "This is a completely safe file that all antivirus software detects."
echo ""
echo 'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*' > eicar.com
echo "✓ Created: eicar.com"
sleep 5

echo ""
echo "Test 2: Creating file with suspicious extension"
echo ""
echo "test content" > document.pdf.exe
echo "✓ Created: document.pdf.exe (double extension trick)"
sleep 5

echo ""
echo "Test 3: Creating file with suspicious keywords"
echo ""
echo "benign content" > password_stealer.txt
echo "✓ Created: password_stealer.txt"
sleep 5

echo ""
echo "Test 4: Creating suspicious executable"
echo ""
echo "test" > virus.exe
echo "✓ Created: virus.exe"
sleep 5

echo ""
echo "Test 5: Creating safe file (should show low threat)"
echo ""
echo "This is a normal document" > report.txt
echo "✓ Created: report.txt"
sleep 5

echo ""
echo "=================================="
echo "All test files created!"
echo "Check the security system output."
echo "=================================="
echo ""
echo "Test files location: $TEST_DIR"
echo ""
echo "To clean up test files:"
echo "  rm -rf $TEST_DIR"
