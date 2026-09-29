package in.suraksha.ar.data.db

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "modules")
data class ModuleEntity(
    @PrimaryKey val id: String,
    val title: String,
    val isLite: Boolean,
    val stepsJson: String
)

@Entity(tableName = "attempts")
data class AttemptEntity(
    @PrimaryKey val id: String,
    val moduleId: String,
    val userId: Int,
    val startTime: Long,
    val endTime: Long,
    val score: Int,
    val passed: Boolean,
    val synced: Boolean = false
)

@Entity(tableName = "certificates")
data class CertificateEntity(
    @PrimaryKey val id: String,
    val payloadJson: String,
    val signature: String,
    val issuedAt: Long,
    val expiresAt: Long
)
