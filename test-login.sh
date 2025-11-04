#!/bin/bash
curl -X POST http://localhost:8432/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestGoldenSaju2025!","rememberMe":false}' \
  -w "\nHTTP Status: %{http_code}\nTotal time: %{time_total}s\n"
