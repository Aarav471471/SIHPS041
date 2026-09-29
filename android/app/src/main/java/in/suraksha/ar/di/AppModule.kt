package in.suraksha.ar.di

import android.content.Context
import androidx.room.Room
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import in.suraksha.ar.data.db.SurakshaDao
import in.suraksha.ar.data.db.SurakshaDatabase
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): SurakshaDatabase {
        return Room.databaseBuilder(
            context,
            SurakshaDatabase::class.java,
            "suraksha_local.db"
        ).build()
    }

    @Provides
    fun provideDao(database: SurakshaDatabase): SurakshaDao {
        return database.surakshaDao()
    }
    
    // Retrofit and network providers would go here
}
