package in.suraksha.ar.data.db

import androidx.room.Database
import androidx.room.RoomDatabase

@Database(
    entities = [
        ModuleEntity::class,
        AttemptEntity::class,
        CertificateEntity::class
    ],
    version = 1,
    exportSchema = false
)
abstract class SurakshaDatabase : RoomDatabase() {
    abstract fun surakshaDao(): SurakshaDao
}
