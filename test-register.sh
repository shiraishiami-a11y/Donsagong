#!/bin/bash
curl -X POST http://localhost:8432/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestGoldenSaju2025!","migrateGuestData":false}'
