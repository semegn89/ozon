#!/bin/bash

echo "🚀 Railway Admin Setup"
echo "====================="

# Проверяем Railway CLI
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI не установлен"
    echo "Установите: npm install -g @railway/cli"
    exit 1
fi

echo "✅ Railway CLI найден"

# Логинимся в Railway
echo "🔐 Проверяем авторизацию..."
if ! railway whoami &> /dev/null; then
    echo "Войдите в Railway:"
    railway login
fi

echo "📋 Текущие переменные:"
railway variables

echo ""
echo "🔧 Для добавления админа выполните:"
echo "railway variables set ADMIN_CHAT_IDS='318073844,новый_chat_id'"
echo ""
echo "📝 Пример:"
echo "railway variables set ADMIN_CHAT_IDS='318073844,123456789'"
echo ""
echo "🔄 После изменения переменных перезапустите бота:"
echo "railway redeploy"
