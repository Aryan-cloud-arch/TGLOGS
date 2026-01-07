#!/bin/bash
# Telegram Account Manager Setup
# Created by: @MaiHuAryan | t.me/MaiHuAryan

echo "🚀 Installing Telegram Account Manager..."
echo ""

# Install Python packages
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Setup complete!"
    echo ""
    echo "Next steps:"
    echo "1. Edit config.yaml with your API credentials"
    echo "2. Get API from: https://my.telegram.org/apps"
    echo "3. Run: python tgm.py"
    echo ""
    echo "Created by @MaiHuAryan | t.me/MaiHuAryan"
else
    echo "❌ Setup failed!"
fi
