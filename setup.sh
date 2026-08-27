#!/bin/bash
# Quick setup script untuk BugBountyAI v2

echo "═════════════════════════════════════════════════════════"
echo "   BugBountyAI v2 - Quick Setup Script"
echo "═════════════════════════════════════════════════════════"
echo ""

# Check Python version
echo "🐍 Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python version: $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "   ✅ Virtual environment created"
else
    echo "   ⚠️  Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate
echo "   ✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip -q
echo "   ✅ pip upgraded"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
echo "   Note: Using minimal requirements for Python 3.14 compatibility"
pip install -r requirements-minimal.txt -q
echo "   ✅ Dependencies installed"
echo ""

# Create .env file
echo "⚙️  Setting up configuration..."
if [ ! -f ".env.gemini" ]; then
    cp .env.gemini.example .env.gemini
    echo "   ✅ .env.gemini created"
    echo "   ⚠️  Please edit .env.gemini and add your Gemini API Key"
else
    echo "   ⚠️  .env.gemini already exists"
fi
echo ""

# Verify installation
echo "✅ Verifying installation..."
python -c "from bugbountyai import BugBountyAnalyzer; print('   ✅ BugBountyAI imported successfully')" 2>/dev/null || echo "   ⚠️  Import check failed"
python -c "import google.generativeai; print('   ✅ Gemini AI library available')" 2>/dev/null || echo "   ⚠️  Gemini AI not available"
echo ""

# Display next steps
echo "═════════════════════════════════════════════════════════"
echo "   ✅ Setup Complete!"
echo "═════════════════════════════════════════════════════════"
echo ""
echo "📋 Next Steps:"
echo "   1. Edit .env.gemini and add your Gemini API Key:"
echo "      nano .env.gemini"
echo ""
echo "   2. Test basic scan:"
echo "      python -m bugbountyai.cli.main scan https://example.com"
echo ""
echo "   3. Test with Gemini AI:"
echo "      python -m bugbountyai.cli.gemini_cli scan-gemini https://example.com --gemini-key YOUR_KEY"
echo ""
echo "   4. Start API server:"
echo "      uvicorn bugbountyai.api.v2_api:app --reload"
echo ""
echo "💡 For more help, see INSTALLATION.md"
echo ""
