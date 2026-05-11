package com.waterapproval.repository;

import com.waterapproval.entity.ApplicationFile;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ApplicationFileRepository extends JpaRepository<ApplicationFile, Long> {

    List<ApplicationFile> findByApplication_Id(Long applicationId);
}
