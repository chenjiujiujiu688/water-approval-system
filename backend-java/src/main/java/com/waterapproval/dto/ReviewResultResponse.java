package com.waterapproval.dto;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

public class ReviewResultResponse {

    private Long applicationId;
    private String applicationTitle;
    private String reviewStatus;
    private String summary;
    private String riskLevel;
    private String suggestions;
    private List<String> issues = new ArrayList<>();
    private List<String> knowledgeSources = new ArrayList<>();
    private Double completenessRate;
    private LocalDateTime reviewedAt;

    public Long getApplicationId() {
        return applicationId;
    }

    public void setApplicationId(Long applicationId) {
        this.applicationId = applicationId;
    }

    public String getApplicationTitle() {
        return applicationTitle;
    }

    public void setApplicationTitle(String applicationTitle) {
        this.applicationTitle = applicationTitle;
    }

    public String getReviewStatus() {
        return reviewStatus;
    }

    public void setReviewStatus(String reviewStatus) {
        this.reviewStatus = reviewStatus;
    }

    public String getSummary() {
        return summary;
    }

    public void setSummary(String summary) {
        this.summary = summary;
    }

    public String getRiskLevel() {
        return riskLevel;
    }

    public void setRiskLevel(String riskLevel) {
        this.riskLevel = riskLevel;
    }

    public String getSuggestions() {
        return suggestions;
    }

    public void setSuggestions(String suggestions) {
        this.suggestions = suggestions;
    }

    public List<String> getIssues() {
        return issues;
    }

    public void setIssues(List<String> issues) {
        this.issues = issues;
    }

    public List<String> getKnowledgeSources() {
        return knowledgeSources;
    }

    public void setKnowledgeSources(List<String> knowledgeSources) {
        this.knowledgeSources = knowledgeSources;
    }

    public Double getCompletenessRate() {
        return completenessRate;
    }

    public void setCompletenessRate(Double completenessRate) {
        this.completenessRate = completenessRate;
    }

    public LocalDateTime getReviewedAt() {
        return reviewedAt;
    }

    public void setReviewedAt(LocalDateTime reviewedAt) {
        this.reviewedAt = reviewedAt;
    }
}
