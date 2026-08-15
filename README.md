# shopping-listapp
Simple Flask shopping list web app backed by Supabase (Postgres)

## 실행 방법

```bash
pip install -r requirements.txt
cp .env.example .env   # SUPABASE_URL / SUPABASE_KEY 값 채우기
python3 app.py
```

브라우저에서 http://127.0.0.1:5000/ 접속

## 환경 변수

- `SUPABASE_URL`: Supabase 프로젝트 URL
- `SUPABASE_KEY`: Supabase anon/publishable API 키

Vercel에 배포할 때는 프로젝트 설정의 Environment Variables에 위 두 값을 등록해야 한다.

## 데이터베이스

`shopping_items` 테이블 (Supabase):

| 컬럼 | 타입 |
| --- | --- |
| id | bigint, identity, PK |
| text | text |
| checked | boolean, default false |
| created_at | timestamptz, default now() |
