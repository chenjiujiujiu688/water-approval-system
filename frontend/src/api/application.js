import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8080",
  timeout: 10000
});

export function fetchApplications() {
  return api.get("/api/applications");
}

export function fetchApplicationDetail(id) {
  return api.get(`/api/applications/${id}`);
}

export function fetchReviewResult(id) {
  return api.get(`/api/applications/${id}/review`);
}

export function createApplication(payload) {
  return api.post("/api/applications", payload, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  });
}

