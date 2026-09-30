package in.suraksha.ar

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import dagger.hilt.android.AndroidEntryPoint
import in.suraksha.ar.ui.screens.LoginScreen
import in.suraksha.ar.ui.screens.HomeScreen
import in.suraksha.ar.ui.screens.CertificateScreen
import in.suraksha.ar.ar.ui.ArSessionScreen
import in.suraksha.ar.ar.engine.StepDefinition

import in.suraksha.ar.ui.theme.SurakshaARTheme

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            SurakshaARTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    val navController = rememberNavController()

                    NavHost(navController = navController, startDestination = "login") {
                        composable("login") {
                            LoginScreen(
                                onLoginSuccess = { navController.navigate("home") { popUpTo("login") { inclusive = true } } }
                            )
                        }
                        composable("home") {
                            HomeScreen(
                                onNavigateToAr = { moduleId -> navController.navigate("ar/$moduleId") },
                                onNavigateToCertificates = { navController.navigate("certificates") }
                            )
                        }
                        composable("certificates") {
                            CertificateScreen(
                                onBack = { navController.popBackStack() }
                            )
                        }
                        composable("ar/{moduleId}") { backStackEntry ->
                            val moduleId = backStackEntry.arguments?.getString("moduleId") ?: "fire"
                            // Mocking the step for architecture completion
                            val mockStep = StepDefinition(
                                id = "intro",
                                type = "INTRO",
                                titleKey = "${moduleId}_intro_title",
                                instructionKey = "${moduleId}_intro_desc",
                                audioKey = "none",
                                maxPoints = 10
                            )
                            
                            ArSessionScreen(
                                currentStep = mockStep,
                                onStepComplete = { navController.popBackStack() }, // normally goes to next step
                                onAbort = { navController.popBackStack() }
                            )
                        }
                    }
                }
            }
        }
    }
}

