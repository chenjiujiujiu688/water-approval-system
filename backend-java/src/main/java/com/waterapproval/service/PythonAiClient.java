package com.waterapproval.service;

import com.waterapproval.dto.ReviewResultResponse;
import com.waterapproval.entity.Application;
import java.time.LocalDateTime;
import org.springframework.stereotype.Service;

@Service
public class PythonAiClient {

    public ReviewResultResponse mockReview(Application application) {
        ReviewResultResponse response = new ReviewResultResponse();
        response.setApplicationId(application.getId());
        response.setApplicationTitle(application.getTitle());
        response.setReviewStatus("MOCK_APPROVED");
        response.setRiskLevel("LOW");
        response.setSummary("节点一阶段返回模拟初审结果，说明申请材料已经进入可扩展审核流程。");
        response.setSuggestions("后续节点可接入真实知识库检索、材料完整性校验和智能审核模型。");
        response.setReviewedAt(LocalDateTime.now());
        return response;
    }
}

