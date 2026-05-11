package com.waterapproval.repository;

import com.waterapproval.entity.ReviewResult;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ReviewResultRepository extends JpaRepository<ReviewResult, Long> {

    Optional<ReviewResult> findByApplication_Id(Long applicationId);
}
