#!/bin/bash

# CHAIN-005テスト用の命式データ準備スクリプト
# test@example.com アカウントに3件の命式データを登録

echo "=== CHAIN-005テスト用命式データ準備スクリプト ==="
echo ""

# 設定
BASE_URL="http://localhost:8432"
EMAIL="test@example.com"
PASSWORD="TestGoldenSaju2025!"

# 1. ログインしてトークン取得
echo "Step 1: ログイン処理..."
LOGIN_RESPONSE=$(curl -s -X POST "${BASE_URL}/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"${EMAIL}\",\"password\":\"${PASSWORD}\"}")

echo "ログインレスポンス: ${LOGIN_RESPONSE}"

# トークン抽出（jqがある場合）
if command -v jq &> /dev/null; then
  TOKEN=$(echo "${LOGIN_RESPONSE}" | jq -r '.accessToken')
  echo "トークン取得成功: ${TOKEN:0:20}..."
else
  echo "警告: jqがインストールされていません。手動でトークンを確認してください。"
  echo "ログインレスポンス: ${LOGIN_RESPONSE}"
  exit 1
fi

if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
  echo "エラー: トークン取得失敗。ログインレスポンスを確認してください。"
  exit 1
fi

echo ""
echo "Step 2: 命式データ登録（3件）..."
echo ""

# 命式データ1: テスト太郎
echo "--- 命式1: テスト太郎 ---"
SAJU1=$(curl -s -X POST "${BASE_URL}/api/saju/calculate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{
    "name": "テスト太郎",
    "birthDatetime": "1990-03-15T14:30:00+09:00",
    "gender": "male"
  }')

echo "計算結果: $(echo ${SAJU1} | jq -c '.')"

SAVE1=$(curl -s -X POST "${BASE_URL}/api/saju/save" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d "${SAJU1}" \
  -w "\nHTTP Status: %{http_code}\n")

echo "保存結果: ${SAVE1}"
echo ""

# 命式データ2: テスト花子
echo "--- 命式2: テスト花子 ---"
SAJU2=$(curl -s -X POST "${BASE_URL}/api/saju/calculate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{
    "name": "テスト花子",
    "birthDatetime": "1995-06-20T10:15:00+09:00",
    "gender": "female"
  }')

echo "計算結果: $(echo ${SAJU2} | jq -c '.')"

SAVE2=$(curl -s -X POST "${BASE_URL}/api/saju/save" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d "${SAJU2}" \
  -w "\nHTTP Status: %{http_code}\n")

echo "保存結果: ${SAVE2}"
echo ""

# 命式データ3: テスト次郎
echo "--- 命式3: テスト次郎 ---"
SAJU3=$(curl -s -X POST "${BASE_URL}/api/saju/calculate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{
    "name": "テスト次郎",
    "birthDatetime": "2000-01-01T00:00:00+09:00",
    "gender": "male"
  }')

echo "計算結果: $(echo ${SAJU3} | jq -c '.')"

SAVE3=$(curl -s -X POST "${BASE_URL}/api/saju/save" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d "${SAJU3}" \
  -w "\nHTTP Status: %{http_code}\n")

echo "保存結果: ${SAVE3}"
echo ""

# 3. 確認: 一覧取得
echo "Step 3: 命式一覧確認..."
LIST=$(curl -s -X GET "${BASE_URL}/api/saju/list" \
  -H "Authorization: Bearer ${TOKEN}")

echo "一覧取得結果: $(echo ${LIST} | jq '.')"
echo ""

TOTAL=$(echo ${LIST} | jq -r '.total')
echo "=== 登録完了: ${TOTAL}件の命式データ ==="
