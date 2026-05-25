package com.waterapproval.service;

import com.waterapproval.dto.ReviewResultResponse;
import com.waterapproval.entity.Application;
import com.waterapproval.entity.ApplicationFile;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

@Service
public class PythonAiClient {

    private final RestTemplate restTemplate;

    @Value("${python.ai.base-url}")
    private String pythonAiBaseUrl;

    public PythonAiClient(RestTemplateBuilder restTemplateBuilder) {
        this.restTemplate = restTemplateBuilder.build();
    }

    public ReviewResultResponse review(Application application, List<ApplicationFile> files) {
        AgentReviewRequest request = AgentReviewRequest.from(application, files);
        try {
            AgentReviewResponse agentResponse = restTemplate.postForObject(
                    pythonAiBaseUrl + "/agent/review",
                    request,
                    AgentReviewResponse.class);
            return toReviewResult(application, agentResponse);
        } catch (RestClientException ex) {
            return fallbackReview(application, ex.getMessage());
        }
    }

    public ReviewResultResponse mockReview(Application application) {
        return fallbackReview(application, "Python AI service is not available.");
    }

    private ReviewResultResponse toReviewResult(Application application, AgentReviewResponse agentResponse) {
        ReviewResultResponse response = new ReviewResultResponse();
        response.setApplicationId(application.getId());
        response.setApplicationTitle(application.getTitle());
        response.setReviewStatus(agentResponse.reviewStatus());
        response.setRiskLevel(agentResponse.riskLevel());
        response.setSummary(agentResponse.summary());
        response.setSuggestions(agentResponse.suggestions());
        response.setIssues(agentResponse.issues().stream().map(AgentIssue::toDisplayText).toList());
        response.setKnowledgeSources(agentResponse.knowledgeSources());
        response.setCompletenessRate(agentResponse.completenessRate());
        response.setReviewedAt(LocalDateTime.parse(agentResponse.reviewedAt()));
        return response;
    }

    private ReviewResultResponse fallbackReview(Application application, String reason) {
        ReviewResultResponse response = new ReviewResultResponse();
        response.setApplicationId(application.getId());
        response.setApplicationTitle(application.getTitle());
        response.setReviewStatus("AI_SERVICE_UNAVAILABLE");
        response.setRiskLevel("MEDIUM");
        response.setSummary("Python Agent 初审服务暂不可用，已生成降级结果。");
        response.setSuggestions("请确认 Python AI 服务已启动并可访问 /agent/review。错误信息：" + reason);
        response.setIssues(List.of("Python Agent 服务调用失败，需要人工复核。"));
        response.setKnowledgeSources(List.of());
        response.setCompletenessRate(0.0);
        response.setReviewedAt(LocalDateTime.now());
        return response;
    }

    public record AgentReviewRequest(
            Long applicationId,
            String title,
            String applicantName,
            String organizationName,
            String contactPhone,
            String email,
            String waterUsage,
            String waterLocation,
            String applicationPeriod,
            String description,
            List<AgentFileItem> files) {

        static AgentReviewRequest from(Application application, List<ApplicationFile> files) {
            List<AgentFileItem> fileItems = new ArrayList<>();
            for (ApplicationFile file : files) {
                fileItems.add(new AgentFileItem(
                        file.getOriginalName(),
                        file.getStoragePath(),
                        file.getContentType()));
            }
            return new AgentReviewRequest(
                    application.getId(),
                    application.getTitle(),
                    application.getUser().getApplicantName(),
                    application.getUser().getOrganizationName(),
                    application.getUser().getContactPhone(),
                    application.getUser().getEmail(),
                    application.getWaterUsage(),
                    application.getWaterLocation(),
                    application.getApplicationPeriod(),
                    application.getDescription(),
                    fileItems);
        }
    }

    public record AgentFileItem(String originalName, String storagePath, String contentType) {
    }

    public record AgentReviewResponse(
            Long applicationId,
            String reviewStatus,
            String riskLevel,
            String summary,
            String suggestions,
            List<AgentIssue> issues,
            List<String> knowledgeSources,
            Double completenessRate,
            String reviewedAt) {
    }

    public record AgentIssue(
            String category,
            String severity,
            String message,
            String suggestion,
            String evidence) {

        String toDisplayText() {
            return "[" + category + "/" + severity + "] " + message + " 建议：" + suggestion;
        }
    }
}
