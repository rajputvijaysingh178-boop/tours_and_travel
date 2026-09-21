from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_checkup():
	return {"checkup": "completed"}