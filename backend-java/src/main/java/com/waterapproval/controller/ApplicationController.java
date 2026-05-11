package com.waterapproval.controller;

import com.waterapproval.dto.ApplicationResponse;
import com.waterapproval.dto.ReviewResultResponse;
import com.waterapproval.service.ApplicationService;
import java.io.IOException;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/applications")
public class ApplicationController {

    private final ApplicationService applicationService;

    public ApplicationController(ApplicationService applicationService) {
        this.applicationService = applicationService;
    }

    @PostMapping
    public ResponseEntity<ApplicationResponse> createApplication(
            @RequestParam String title,
            @RequestParam String applicantName,
            @RequestParam String organizationName,
            @RequestParam(required = false) String contactPhone,
            @RequestParam(required = false) String email,
            @RequestParam String waterUsage,
            @RequestParam String waterLocation,
            @RequestParam String applicationPeriod,
            @RequestParam(required = false) String description,
            @RequestParam(required = false) MultipartFile[] files) throws IOException {
        ApplicationResponse response = applicationService.createApplication(
                title,
                applicantName,
                organizationName,
                contactPhone,
                email,
                waterUsage,
                waterLocation,
                applicationPeriod,
                description,
                files);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping
    public List<ApplicationResponse> getApplications() {
        return applicationService.getApplications();
    }

    @GetMapping("/{id}")
    public ApplicationResponse getApplication(@PathVariable Long id) {
        return applicationService.getApplicationById(id);
    }

    @GetMapping("/{id}/review")
    public ReviewResultResponse getReview(@PathVariable Long id) {
        return applicationService.getReviewResult(id);
    }
}

