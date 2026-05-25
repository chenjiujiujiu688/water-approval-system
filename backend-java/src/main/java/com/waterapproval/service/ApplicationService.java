package com.waterapproval.service;

import com.waterapproval.dto.ApplicationResponse;
import com.waterapproval.dto.ReviewResultResponse;
import com.waterapproval.entity.Application;
import com.waterapproval.entity.ApplicationFile;
import com.waterapproval.entity.ReviewResult;
import com.waterapproval.entity.User;
import com.waterapproval.repository.ApplicationFileRepository;
import com.waterapproval.repository.ApplicationRepository;
import com.waterapproval.repository.ReviewResultRepository;
import com.waterapproval.repository.UserRepository;
import jakarta.persistence.EntityNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

@Service
public class ApplicationService {

    private final UserRepository userRepository;
    private final ApplicationRepository applicationRepository;
    private final ApplicationFileRepository applicationFileRepository;
    private final ReviewResultRepository reviewResultRepository;
    private final PythonAiClient pythonAiClient;

    @Value("${app.upload-dir}")
    private String uploadDir;

    public ApplicationService(
            UserRepository userRepository,
            ApplicationRepository applicationRepository,
            ApplicationFileRepository applicationFileRepository,
            ReviewResultRepository reviewResultRepository,
            PythonAiClient pythonAiClient) {
        this.userRepository = userRepository;
        this.applicationRepository = applicationRepository;
        this.applicationFileRepository = applicationFileRepository;
        this.reviewResultRepository = reviewResultRepository;
        this.pythonAiClient = pythonAiClient;
    }

    @Transactional
    public ApplicationResponse createApplication(
            String title,
            String applicantName,
            String organizationName,
            String contactPhone,
            String email,
            String waterUsage,
            String waterLocation,
            String applicationPeriod,
            String description,
            MultipartFile[] files) throws IOException {

        User user = new User();
        user.setApplicantName(applicantName);
        user.setOrganizationName(organizationName);
        user.setContactPhone(contactPhone);
        user.setEmail(email);
        user.setCreatedAt(LocalDateTime.now());
        userRepository.save(user);

        Application application = new Application();
        application.setUser(user);
        application.setTitle(title);
        application.setWaterUsage(waterUsage);
        application.setWaterLocation(waterLocation);
        application.setApplicationPeriod(applicationPeriod);
        application.setStatus("PENDING");
        application.setDescription(description);
        application.setCreatedAt(LocalDateTime.now());
        application.setUpdatedAt(LocalDateTime.now());
        applicationRepository.save(application);

        saveFiles(application, files);
        List<ApplicationFile> savedFiles = applicationFileRepository.findByApplication_Id(application.getId());

        ReviewResultResponse agentReview = pythonAiClient.review(application, savedFiles);
        saveReviewResult(application, agentReview);

        return getApplicationById(application.getId());
    }

    @Transactional(readOnly = true)
    public List<ApplicationResponse> getApplications() {
        return applicationRepository.findAll()
                .stream()
                .map(this::toResponse)
                .collect(Collectors.toList());
    }

    @Transactional(readOnly = true)
    public ApplicationResponse getApplicationById(Long id) {
        Application application = applicationRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("申请不存在，ID=" + id));
        return toResponse(application);
    }

    @Transactional
    public ReviewResultResponse getReviewResult(Long applicationId) {
        Application application = applicationRepository.findById(applicationId)
                .orElseThrow(() -> new EntityNotFoundException("申请不存在，ID=" + applicationId));

        List<ApplicationFile> files = applicationFileRepository.findByApplication_Id(applicationId);
        ReviewResultResponse agentReview = pythonAiClient.review(application, files);
        ReviewResult reviewResult = saveReviewResult(application, agentReview);

        ReviewResultResponse response = new ReviewResultResponse();
        response.setApplicationId(application.getId());
        response.setApplicationTitle(application.getTitle());
        response.setReviewStatus(reviewResult.getReviewStatus());
        response.setRiskLevel(reviewResult.getRiskLevel());
        response.setSummary(reviewResult.getSummary());
        response.setSuggestions(reviewResult.getSuggestions());
        response.setIssues(splitLines(reviewResult.getIssues()));
        response.setKnowledgeSources(splitLines(reviewResult.getKnowledgeSources()));
        response.setCompletenessRate(reviewResult.getCompletenessRate());
        response.setReviewedAt(reviewResult.getReviewedAt());
        return response;
    }

    private void saveFiles(Application application, MultipartFile[] files) throws IOException {
        if (files == null || files.length == 0) {
            return;
        }

        Path uploadPath = Paths.get(uploadDir);
        Files.createDirectories(uploadPath);

        for (MultipartFile file : files) {
            if (file == null || file.isEmpty()) {
                continue;
            }

            String generatedName = UUID.randomUUID() + "_" + file.getOriginalFilename();
            Path target = uploadPath.resolve(generatedName).toAbsolutePath().normalize();
            Files.copy(file.getInputStream(), target, StandardCopyOption.REPLACE_EXISTING);

            ApplicationFile applicationFile = new ApplicationFile();
            applicationFile.setApplication(application);
            applicationFile.setOriginalName(file.getOriginalFilename());
            applicationFile.setStoragePath(target.toString());
            applicationFile.setFileSize(file.getSize());
            applicationFile.setContentType(file.getContentType());
            applicationFile.setUploadedAt(LocalDateTime.now());
            applicationFileRepository.save(applicationFile);
        }
    }

    private ReviewResult saveReviewResult(Application application, ReviewResultResponse response) {
        ReviewResult reviewResult = reviewResultRepository.findByApplication_Id(application.getId())
                .orElseGet(() -> {
                    ReviewResult entity = new ReviewResult();
                    entity.setApplication(application);
                    return entity;
                });
        reviewResult.setReviewStatus(response.getReviewStatus());
        reviewResult.setRiskLevel(response.getRiskLevel());
        reviewResult.setSummary(response.getSummary());
        reviewResult.setSuggestions(response.getSuggestions());
        reviewResult.setIssues(joinLines(response.getIssues()));
        reviewResult.setKnowledgeSources(joinLines(response.getKnowledgeSources()));
        reviewResult.setCompletenessRate(response.getCompletenessRate());
        reviewResult.setReviewedAt(response.getReviewedAt());
        return reviewResultRepository.save(reviewResult);
    }

    private String joinLines(List<String> values) {
        if (values == null || values.isEmpty()) {
            return "";
        }
        return String.join("\n", values);
    }

    private List<String> splitLines(String value) {
        if (value == null || value.isBlank()) {
            return new ArrayList<>();
        }
        return Arrays.stream(value.split("\\R"))
                .filter(line -> !line.isBlank())
                .collect(Collectors.toList());
    }

    private ApplicationResponse toResponse(Application application) {
        ApplicationResponse response = new ApplicationResponse();
        response.setId(application.getId());
        response.setTitle(application.getTitle());
        response.setApplicantName(application.getUser().getApplicantName());
        response.setOrganizationName(application.getUser().getOrganizationName());
        response.setContactPhone(application.getUser().getContactPhone());
        response.setEmail(application.getUser().getEmail());
        response.setWaterUsage(application.getWaterUsage());
        response.setWaterLocation(application.getWaterLocation());
        response.setApplicationPeriod(application.getApplicationPeriod());
        response.setStatus(application.getStatus());
        response.setDescription(application.getDescription());
        response.setCreatedAt(application.getCreatedAt());

        List<ApplicationResponse.FileItem> fileItems = applicationFileRepository.findByApplication_Id(application.getId())
                .stream()
                .map(file -> {
                    ApplicationResponse.FileItem item = new ApplicationResponse.FileItem();
                    item.setId(file.getId());
                    item.setOriginalName(file.getOriginalName());
                    item.setStoragePath(file.getStoragePath());
                    return item;
                })
                .collect(Collectors.toList());
        response.setFiles(fileItems);
        return response;
    }
}
