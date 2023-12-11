curl "http://localhost:5000/upload"  \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Ik1cdTFlYWRwIiwiaXNfYWRtaW4iOnRydWUsImV4cCI6MTcwMjMyMDMxMSwiaWF0IjoxNzAyMzExMzExfQ.92nB88yXmuYGa2espfDBxMGyxu-cjeUpX7HMfcEQVG4" \
-X POST -F "data=@cat-img.jpeg" \
