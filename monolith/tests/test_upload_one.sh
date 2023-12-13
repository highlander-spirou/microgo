curl "http://localhost:5000/upload"  \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Ik1cdTFlYWRwIiwiZXhwIjoxNzA4NDg2MTk4LCJpYXQiOjE3MDI0ODYxOTh9.-kHILLDStGbXJDkuLoG9Ahr99New8n7GrluP-fWEEHg" \
-X POST -F "data=@imgs/cat-img.jpeg"