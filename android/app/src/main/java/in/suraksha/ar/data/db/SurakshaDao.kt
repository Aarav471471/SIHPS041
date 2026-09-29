package in.suraksha.ar.data.db

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query

@Dao
interface SurakshaDao {
    @Query("SELECT * FROM modules")
    suspend fun getAllModules(): List<ModuleEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertModules(modules: List<ModuleEntity>)

    @Query("SELECT * FROM attempts WHERE synced = 0")
    suspend fun getUnsyncedAttempts(): List<AttemptEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAttempt(attempt: AttemptEntity)
    
    @Query("UPDATE attempts SET synced = 1 WHERE id IN (:ids)")
    suspend fun markAttemptsSynced(ids: List<String>)

    @Query("SELECT * FROM certificates")
    suspend fun getCertificates(): List<CertificateEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertCertificates(certs: List<CertificateEntity>)
}
